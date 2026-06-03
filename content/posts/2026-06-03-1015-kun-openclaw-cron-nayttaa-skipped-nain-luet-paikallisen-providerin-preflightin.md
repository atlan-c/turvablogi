---
title: "Kun OpenClaw-cron näyttää `skipped`: näin luet paikallisen providerin preflightin"
date: "2026-06-03T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Automation"
  - "Ollama"
  - "Troubleshooting"
---
Kun OpenClawin isolated cron -ajo päättyy tilaan `skipped`, moni tulkitsee sen liian nopeasti yleiseksi epäonnistumiseksi. Käytännössä se tarkoittaa usein jotain tarkempaa ja helpommin rajattavaa: **ajo ei edes ehtinyt varsinaiseen agenttivuoroon asti, koska paikallisen mallipalvelimen reachability-preflight pysäytti sen jo ennen mallikutsua**. Tämä on hyvä asia, jos käytät Ollamaa, LM Studiota, vLLM:ää tai muuta paikallista provideria, koska järjestelmä säästää turhalta tokeni- ja retry-myllyltä silloin kun endpoint on selvästi alhaalla.

Minun käytännön sääntöni on tämä: **`skipped` ei yleensä tarkoita "prompti oli huono", vaan "ensin kannattaa tarkistaa paikallinen provider ja vasta sitten itse työn logiikka".** Kun tämän erottaa tavallisesta `failed`-ajosta, vianrajaus nopeutuu paljon.

## Mitä OpenClaw tekee ennen agentin käynnistystä

OpenClawin cron-dokumentaatio sanoo tämän melko suoraan: isolated jobeille, jotka käyttävät paikallista malliprovideria, ajetaan kevyt preflight ennen kuin agentin varsinainen ajo alkaa. Jos provider on `api: "ollama"` ja osoite on loopback-, private-network- tai `.local`-osoite, OpenClaw koettaa `\`/api/tags\``-pistettä. Jos taas provider on paikallinen OpenAI-yhteensopiva serveri kuten LM Studio, vLLM tai SGLang, probe tehdään `\`/models\``-päähän.

Tällä on iso käytännön merkitys: jos paikallinen malli ei vastaa lainkaan, OpenClaw ei teeskentele että agentti "epäonnistui ajattelemaan". Se kirjaa runin `skipped`-tilaan ja jättää varsinaisen agenttivuoron kokonaan käynnistämättä.

Siksi `skipped` on usein enemmän infrastruktuurisignaali kuin sisältösignaali.

## Miksi `skipped` on parempi kuin turha `failed`

Dokumentaation mukaan `skipped`-ajot pidetään erillään varsinaisista execution erroreista. Niitä ei lasketa mukaan retry backoffiin samalla tavalla kuin oikeita ajovirheitä. Tämä on minusta fiksu ratkaisu erityisesti kotilabrassa, jossa paikallinen provider voi olla hetkellisesti poissa esimerkiksi siksi että:

- Ollama ei ole käynnissä käynnistyksen jälkeen
- LM Studio on auki, mutta local server ei ole aktivoitu
- vLLM tai SGLang käynnistyy hitaasti bootin jälkeen
- VPN, Tailscale tai muu sisäverkkoreitti ei ole vielä valmis

Jos tällaisessa tilanteessa jokainen due-run merkittäisiin tavalliseksi virheeksi, virheloki paisuisi väärästä syystä. `skipped` kertoo käytännössä: **ajastus toimi, mutta providerin esiehto ei täyttynyt**.

## Yksi helposti ohitettu detalji: viiden minuutin kuolleen endpointin välimuisti

Cron-dokumentaatiossa on pieni mutta hyödyllinen nyanssi: jos sama kuollut local endpoint havaitaan, tulos välimuistitetaan viideksi minuutiksi, jotta moni samaa provideria käyttävä jobi ei hakkaa samaa kuollutta palvelinta yhtä aikaa.

Tämä selittää kaksi käytännön ilmiötä, jotka muuten näyttävät oudoilta:

- useampi samaan aikaan erääntyvä jobi voi kaikki päätyä nopeasti `skipped`-tilaan ilman pitkää odotusta
- providerin juuri korjattu käynnistyminen ei välttämättä näy heti aivan seuraavassa sekunnissa, jos sama dead-endpoint-cache on yhä voimassa

Minusta tämä kannattaa muistaa erityisesti silloin, kun "korjasin Ollaman juuri äsken, miksi seuraava ajo silti skipattiin?" tuntuu ristiriitaiselta. Se ei välttämättä ole ristiriita vaan normaali suojausmekanismi.

## Mistä tarkistaisin asian ensin

Jos oma cron-ajo näyttää `skipped`-tilaa, etenisin tässä järjestyksessä:

1. katson `openclaw cron runs --id <job-id>` ja varmistan, että run todella kirjattiin `skipped`-tilaan eikä `failed`-tilaan
2. tarkistan providerin suoraan ilman OpenClawia
3. vasta sen jälkeen tutkin promptia, mallivalintaa tai workflow-logiikkaa

Käytännön esimerkit:

```bash
# Ollama
curl http://127.0.0.1:11434/api/tags

# OpenAI-yhteensopiva paikallinen provider
curl http://127.0.0.1:1234/v1/models
```

Jos nämä eivät vastaa, ongelma ei ole ensisijaisesti cron-promptissa.

## Missä `tasks` auttaa, vaikka ajo ei koskaan ehtinyt malliin asti

OpenClawin tasks-dokumentaatio muistuttaa, että kaikki cron-ajot luovat task recordin ja että taskit ovat detached workin ledger, eivät scheduler. Tämä on hyödyllinen ero juuri `skipped`-tapauksessa. `openclaw tasks` ei kerro miksi ajastus oli due, mutta se kertoo mitä taustatyölle kirjattiin ja miten run elinkaari päättyi.

Minun mielestäni hyvä käytännön jako on tämä:

- `openclaw cron runs` kertoo mitä juuri tälle jobille tapahtui schedulerin näkökulmasta
- `openclaw tasks show <lookup>` kertoo miten detached run kirjautui task-ledgeriin

Tasks-dokumentaatio sanoo myös, että cron-taskit pysyvät elävinä niin kauan kuin runtime omistaa ne, ja että maintenance tarkistaa durable run historian ennen kuin vanha aktiivinen task merkitään `lost`. Tämä on hyvä uutinen: lyhyt provider-preflight-skip ei ole sama asia kuin katoava tai haamuileva taustatyö.

## Milloin `skipped` kannattaa nostaa hälytykseksi

Koska `skipped` ei kasvata execution-error backoffia, se voi jäädä helposti huomaamatta jos sitä ei seuraa. OpenClawin cron-dokumentaatio tarjoaa tähän oman kytkimen: `--failure-alert-include-skipped`.

Ottaisin tämän käyttöön ainakin silloin, kun:

- cron-jobin pitäisi osua liiketoiminnallisesti tärkeään aikaan
- paikallinen provider on tunnetusti epävakaa bootin jälkeen
- sama jobi toimii "varhaisena varoituksena" siitä, että kotilabran AI-pino ei ole oikeasti ylhäällä

En taas nostaisi jokaista yksittäistä skipiä hälytykseksi, jos kyse on harrastekoneesta joka nukkuu tarkoituksella öisin.

## Tavallinen väärä johtopäätös

Yleisin virhe on minusta tämä: nähdään `skipped`, avataan heti prompti ja aletaan virittää agentin ohjeita. Se on usein väärä taso. Jos preflight ei saanut paikallista endpointia kiinni, prompti ei ollut vielä edes pelissä mukana.

Parempi nyrkkisääntö on tämä:

- `skipped` = tarkista providerin saatavuus, portti ja käynnistystila
- `failed` = tarkista varsinainen ajo, auth, prompti ja mallipolku
- `lost` = tarkista runtime, task maintenance ja katkennut taustasuoritus

Kun nämä kolme erottaa toisistaan, OpenClawin cron-automaatioita on paljon helpompi pitää järkevinä.

## Oma johtopäätökseni

Paikallisia malleja käyttävässä OpenClaw-kotilabrassa `skipped` ei ole nolo sivutapaus vaan hyödyllinen diagnostiikkasignaali. Se kertoo, että scheduler toimi mutta OpenClaw suojasi sinua turhalta agenttiajolta, koska local provider ei ollut oikeasti tavoitettavissa.

Siksi ensimmäinen korjaus ei yleensä ole "kirjoita prompti uusiksi", vaan:

- varmista että provider oikeasti kuuntelee
- testaa oikea endpoint käsin
- muista viiden minuutin dead-endpoint-cache
- tarkista vasta sitten cron-jobin muu logiikka

Tämä pieni tulkintaero säästää yllättävän paljon aikaa, kun oma automaatio alkaa nojata paikalliseen Ollamaan, LM Studioon tai muuhun kotona pyörivään mallipalvelimeen.

## Lähteet

- https://docs.openclaw.ai/cli/cron
- https://docs.openclaw.ai/automation/tasks
- https://docs.openclaw.ai/cron
- https://docs.ollama.com/api/tags
