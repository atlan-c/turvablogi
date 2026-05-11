---
title: "OpenClaw käytännössä: miksi cron-ajo näyttää vihreältä vaikka varsinainen työ ei käynnistynyt?"
date: 2026-05-11T20:56:00+03:00
draft: false
topic_family: "openclaw"
---

OpenClaw-cron voi hämätä juuri silloin, kun automaation pitäisi tuntua luotettavalta. Jos daily-job näkyy onnistuneena, on helppo olettaa että koko workflow todella ajettiin loppuun. Käytännössä näin ei aina ole. Erityisesti `main`-sessioon kohdistettu cron voi onnistua vain siinä mielessä, että Gateway sai järjestelmäeventin jonoon. Se ei vielä yksin todista, että varsinainen pitkä työ oikeasti ehti käynnistyä, käyttää työkaluja ja tuottaa lopputuloksen.

Lyhyt käytännön sääntö on tämä: jos cronin tehtävä on vain muistuttaa tai herättää olemassa oleva sessio, `main` on hyvä valinta. Jos taas haluat yhden rajatun työn varmasti käyntiin omana ajonaan, pelkkä vihreä cron-rivi ei riitä todistukseksi — silloin kannattaa ajatella ajotapaa ja tarkistuspolkua tarkemmin.

## Missä väärinymmärrys yleensä syntyy

OpenClawin cron-dokumentaatio sanoo suoraan, että **main session** -tyylinen jobi "enqueue a system event" ja ajaa sen seuraavassa heartbeat-turnissa. Toisin sanoen cronin vastuu on tällöin ennen kaikkea toimittaa heräte oikeaan sessioon, ei pyörittää koko työvaihetta erillisenä ajona.

Samaan aikaan taustatehtävien dokumentaatio muistuttaa, että taskit ovat **aktiivisuusloki**, eivät scheduler itse. Task kertoo mitä taustatyöstä kirjattiin, mutta sitä pitää tulkita yhdessä ajotavan kanssa. Tämä on tärkeä ero: vihreä `succeeded` task ei aina tarkoita "pitkä workflow suoritettiin loppuun", vaan joskus vain "cronin vastuulla ollut toimitusvaihe onnistui".

## Käytännön oire: run näyttää onnistuneelta, mutta tulosta ei synny

Tämä näkyy arjessa näin:

- cron-run on historiassa vihreä
- `openclaw tasks list --json` näyttää `runtime: "cron"` ja `status: "succeeded"`
- mutta odotettua tiedostoa, commitia tai muuta lopputulosta ei ilmesty

Jos jobi oli rakennettu system eventinä pääsessioon, tämä ei ole ristiriita. Cron voi olla tehnyt oman osuutensa oikein, vaikka live-sessiota ei juuri sillä hetkellä olisi käytännössä ollut vastaanottamassa tai jatkamassa työtä loppuun asti samalla tavalla kuin erillisessä ajossa.

## Mistä tämän erottaa nopeasti

Nopein hyödyllinen tarkistus on katsoa tehtäviä eikä jäädä tuijottamaan vain cron-run-historiaa.

Käytännössä tarkistan kolme asiaa:

1. **Mikä oli ajotapa?**
   - `main` = heräte pääsessiolle
   - `isolated` = oma rajattu cron-ajo
   - `session:custom-id` = samaan pysyvään sessioon kertyvä workflow

2. **Näkyykö oikea jatko task-ledgerissä?**
   - jos kyse on aidosta erillisestä taustatyöstä, siitä pitäisi näkyä uskottava eteneminen eikä vain nopea vihreä kuittaus

3. **Näkyykö oikea lopputulos repossa tai muussa kohteessa?**
   - tuliko uusi tiedosto
   - päivittyikö state
   - syntyikö commit
   - muuttuiko jokin muu odotettu artefakti

Tämä viimeinen kohta kuulostaa itsestään selvältä, mutta juuri se estää väärän turvallisuudentunteen. Automaation onnistuminen pitää sitoa havaittavaan lopputulokseen, ei pelkkään yhteen vihreään statukseen.

## Milloin `main` on silti oikea valinta

`main` ei ole huono. Se on oikea työkalu silloin, kun haluat nimenomaan herättää olemassa olevan keskustelusession ja jatkaa sen kontekstissa. Hyviä esimerkkejä ovat:

- muistutukset
- kevyet heartbeat-tyyppiset tarkistukset
- tilanteet, joissa työn kuuluu elää juuri siinä samassa sessiossa

Tällöin kannattaa hyväksyä myös se, että onnistumisen määritelmä on eri. Cronin näkökulmasta "onnistui" voi tarkoittaa herätteen toimitusta, ei sitä että koko työn tulos on jo valmis levyllä.

## Milloin kannattaa vaihtaa `isolated`- tai custom-session-ajoon

Jos työ on rajattu, toistuva ja tuotannollinen — esimerkiksi raportin generointi, blogipostin kirjoitus, tarkistusskriptien ajo tai muu konkreettinen artefakti — valitsisin usein mieluummin `isolated`-ajon tai tarkoituksella nimetyn `session:...`-session.

Syy on yksinkertainen: silloin cron ei vain koputa pääsession oveen, vaan käynnistää työn omana suorituksenaan. Se tekee diagnostiikasta selkeämmän, virheistä näkyvämpiä ja onnistumisesta helpommin todennettavan.

Hyvä nyrkkisääntö:

- **heräte ihmiselle tai pääsessiolle** → `main`
- **rajattu automaatiotyö, jonka pitää oikeasti juosta** → `isolated`
- **toistuva workflow, jonka pitää säilyttää oma historia** → `session:custom-id`

## Käytännön opetus harrastajalle ja ylläpitäjälle

Jos OpenClaw-automaatio näyttää välillä "liian vihreältä", ongelma ei välttämättä ole bugi vaan väärä odotus siitä, mitä status todistaa. Cron, taskit ja sessiot kertovat eri asioita:

- cron kertoo, laukeaako ajastus
- task-ledger kertoo, mitä taustatyöstä kirjattiin
- repo, viesti tai muu artefakti kertoo, syntyikö oikea lopputulos

Luotettava operointi alkaa siitä, ettei sekoita näitä kolmea toisiinsa.

Siksi oma käytännön sääntöni on nykyään tämä: jos työn onnistumista ei voi todeta yhdestä näkyvästä artefaktista, tarkistan aina myös ajotavan. Se säästää paljon aikaa verrattuna siihen, että yrittää etsiä virhettä väärästä paikasta vain siksi, että cron-run oli vihreä.

## Lähteet

- https://docs.openclaw.ai/automation/cron-jobs
- https://docs.openclaw.ai/automation/tasks
- https://docs.openclaw.ai/cli/tasks
