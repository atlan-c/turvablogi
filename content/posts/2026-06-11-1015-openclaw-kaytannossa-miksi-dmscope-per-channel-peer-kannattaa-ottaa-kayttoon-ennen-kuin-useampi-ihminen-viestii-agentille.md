---
title: "OpenClaw käytännössä: miksi `dmScope: \"per-channel-peer\"` kannattaa ottaa käyttöön ennen kuin useampi ihminen viestii agentille?"
date: "2026-06-11T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Security"
  - "Sessions"
  - "Automation"
---
Yksi OpenClawin helpoimmin ohitettavista asetuksista on myös yksi käytännön vaarallisimmista heti, kun botti ei ole enää vain sinun oma yksityinen leikkikalusi. Oletus on nimittäin tämä: **suoraviestit jakavat saman pääsession**, ellei `session.dmScope`-asetusta muuteta. Se on täysin järkevä oletus yhden ihmisen omassa käytössä, mutta muuttuu nopeasti huonoksi ideaksi, jos bottia saa viestiä useampi ihminen, useampi tili tai useampi kanava.

Minun nyrkkisääntöni on yksinkertainen: **jos enemmän kuin yksi ihminen voi lähettää agentille DM:n, vaihda `dmScope` vähintään arvoon `per-channel-peer` ennen kuin avaat käyttöä enempää**. Tämän voi tehdä vasta ongelman jälkeenkin, mutta silloin siivoat jo syntynyttä sessionsekoilua etkä vain estä sitä.

## Mitä oletus oikeasti tekee

OpenClawin sessionhallinta sanoo tämän aika suoraan: direct message -liikenne menee oletuksena jaettuun sessioon. Dokumentaatiossa tätä kutsutaan `main`-tilaksi. Se on hyvä silloin, kun yksi ihminen käyttää yhtä agenttia jatkuvana henkilökohtaisena keskusteluna ja haluaa, että sama konteksti jatkuu kanavasta riippumatta.

Ongelma alkaa siinä hetkessä, kun samaan bottiin pääsee kiinni toinenkin lähettäjä. Silloin kyse ei enää ole vain "mukavasta jatkuvuudesta", vaan siitä, että **eri lähettäjät voivat päätyä samaan kontekstiin**. OpenClawin oma session docs varoittaa tästä ilman kiertelyä: jos useampi ihminen voi viestiä agentille, ilman DM-eristystä A:n yksityisviestikonteksti voi näkyä B:lle.

Tämä ei tarkoita vain sitä, että malli "muistaa väärän asian". Se voi käytännössä näkyä näin:

- agentti vastaa toisen ihmisen aiempaan kysymykseen
- viestissä näkyy väärän henkilön prioriteetteja tai tehtävälistaa
- työkaluja käyttävä agentti tekee päätelmiä väärän keskusteluhistorian perusteella

Jos agentilla on oikeita työkaluja, tämä ei ole enää esteettinen bugi vaan käyttörajojen bugi.

## Miksi juuri `per-channel-peer` on yleensä paras oletus

OpenClawin dokumentaatio listaa neljä päävaihtoehtoa:

- `main`: kaikki DM:t samaan sessioon
- `per-peer`: yksi sessio per lähettäjä yli kanavien
- `per-channel-peer`: yksi sessio per kanava ja lähettäjä
- `per-account-channel-peer`: yksi sessio per tili, kanava ja lähettäjä

Näistä `per-channel-peer` on useimmille harrastajille paras kompromissi. Syitä on kolme.

Ensimmäinen syy on turvallinen oletus. Eri lähettäjät eivät valu samaan keskusteluun vain siksi, että botti on saman agentin takana.

Toinen syy on käytännön jäljitettävyys. Jos sama henkilö viestii sinulle esimerkiksi eri kanavissa, eri pinnat eivät automaattisesti sekoitu yhdeksi suureksi DM-massaksi. Se helpottaa ymmärtämään, miksi agentti tietää juuri tietyssä paikassa juuri tietyn asian.

Kolmas syy on se, että OpenClawin omat konfiguraatioesimerkit ja security audit suosittelevat nimenomaan tätä arvoa ja nostavat sen esiin "secure DM mode" -asetuksena. Eli kyse ei ole vain yhdestä mahdollisesta tavasta tehdä asiat, vaan käytännössä virallisesti suositellusta monikäyttäjä-DM:n perustasosta.

## Milloin `main` on vielä ihan ok

Kaikkea ei tarvitse ylisuojata. Jos agentti on oikeasti vain sinun oma henkilökohtainen bottisi, eikä kukaan muu voi lähettää sille DM:ää, `main` voi olla edelleen järkevä. Silloin jatkuvuus voi olla hyödyllisempi kuin erilliset sessiot.

Tärkeä kysymys ei siis ole "onko `main` koskaan sallittu", vaan tämä:

**onko varmasti totta, että vain yksi ihminen käyttää agentin DM-pintaa?**

Jos vastaus muuttuu epämääräiseksi, asetuksen pitäisi muuttua samalla. Tyypillisiä kohtia, joissa tämä unohtuu:

- Discord-botti avataan myös yhdelle kaverille testausta varten
- WhatsApp- tai Telegram-DM sallitaan useammalle henkilölle
- käytössä on pairing tai allowlist, johon lisätään toinen henkilö "vain hetkeksi"
- sama agentti alkaa hoitaa sekä omia että puolijulkisia DM-keskusteluja

Juuri näissä tilanteissa `main` jää helposti päälle vahingossa, koska mikään ei mene heti näkyvästi rikki.

## Käytännön asetus, jonka laittaisin ensin

Jos tiedät, että useampi ihminen voi DM:ätä agentille, minimimuutos näyttää tältä:

```json5
{
  session: { dmScope: "per-channel-peer" }
}
```

Jos käytät useita tilejä samalla kanavatyypillä, seuraava askel voi olla `per-account-channel-peer`. Se on järkevä silloin, kun haluat pitää esimerkiksi eri Discord- tai Telegram-tilit täysin erillään myös saman lähettäjän tapauksessa.

Jos taas tarkoitus on, että **sama ihminen jakaa tarkoituksella saman session kanavien yli**, silloin `per-peer` voi olla harkinnan arvoinen. Mutta se on minusta erikoistapaus, ei oletus. En ottaisi sitä käyttöön vain mukavuuden vuoksi ennen kuin tiedän, että identiteettien linkitys ja kanavien ero on mietitty kunnolla.

## Älä vaihda asetusta ilman tarkistusta

Tässä kohtaa hyödyllinen työkalu on `openclaw security audit`. OpenClawin CLI-dokumentaatio sanoo, että audit varoittaa nimenomaan tilanteesta, jossa useat DM-lähettäjät jakavat main-session ja suosittelee silloin `per-channel-peer`- tai monen tilin tapauksessa `per-account-channel-peer` -asetusta.

Tämä on hyvä siksi, että audit ei nojaa pelkkään mutuun. Se huomioi myös vihjeitä siitä, että konfiguraatiossa voi olla monikäyttäjäinen ingressi, kuten avoimemmat DM-policyt, useat allowlist-merkinnät tai wildcard-säännöt.

Käytännössä tekisin näin:

1. aja `openclaw security audit`
2. vaihda `session.dmScope`
3. aja audit uudelleen
4. vasta sen jälkeen laajenna DM-käyttöä useammalle ihmiselle

Tämä järjestys on halpa ja paljon siistimpi kuin se, että huomaat session sekoittumisen vasta tuotannossa.

## Yksi helppo unohtuva jälkitoimi

Jos DM-scopea on aiemmin kokeiltu ja sitten palautettu takaisin `main`-tilaan, OpenClawin sessions-komento tuntee myös tämän siivousluokan. Dokumentaation mukaan `openclaw sessions cleanup --fix-dm-scope --dry-run` näyttää, onko vanhoja peer-pohjaisia DM-rivejä jäänyt sessiokauppaan jäljelle, ja varsinainen ajo voi sitten eläköidä ne säilyttäen transcriptit arkistoina.

Tämä ei ole jokapäiväinen komento, mutta se on hyvä tietää kahdesta syystä:

- scope-muutokset eivät ole vain "vaihda yksi rivi configista ja unohda"
- sessionvaraston siisteys vaikuttaa siihen, kuinka helposti myöhempiä reititysongelmia voi lukea ja diagnosoida

Eli vaikka uusi asetus estää tulevan sotkun, vanha sotku ei aina katoa itsestään.

## Tämä ei tee jaetusta gatewaysta monikäyttäjäjärjestelmää

Yksi tärkeä raja kannattaa sanoa ääneen. OpenClawin security docs painottaa, että koko tuote nojaa henkilökohtaisen assistentin luottamusmalliin, ei vihamielisen monikäyttäjäympäristön eristykseen. Toisin sanoen `per-channel-peer` koventaa DM-käyttöä paljon, mutta se **ei** tee yhdestä gatewaysta turvallista yhteiskäyttöpalvelua toisilleen epäluotettaville ihmisille.

Jos tarvitset aidosti eri luottamusrajoja, oikea ratkaisu on eri gateway, eri tunnukset ja mielellään eri hosti tai ainakin eri OS-käyttäjä. `dmScope` korjaa session reitityksen, ei koko luottamusmallia.

## Oma käytännön sääntöni

Minun mielestäni paras tapa ajatella tätä on näin:

- `main` on yksittäisen omistajan mukavuusolettama
- `per-channel-peer` on käytännön minimitaso heti, kun DM-pinta ei ole enää vain yhdelle ihmiselle
- `per-account-channel-peer` kannattaa valita, jos samoja kanavia on usean tilin kautta tai haluat erityisen selvän erottelun
- jos järjestely alkaa muistuttaa "pientä monikäyttäjäpalvelua", ongelma ei enää ratkea yhdellä DM-scope-rivillä

Tämä on juuri sellainen pieni asetus, joka ei tee demossa mitään näyttävää mutta estää myöhemmin todella typerän ja kalliin luokan virheitä.

## Oma johtopäätökseni

Jos OpenClaw-agentti elää vain omassa yksityisessä käytössäsi, jaettu DM-main-session voi olla aivan hyvä. Mutta heti kun toinen ihminen pääsee DM-kanavaan mukaan, oletus kannattaa vaihtaa. Minun suositukseni on selvä: **ota `session.dmScope: "per-channel-peer"` käyttöön ennen laajennusta, tarkista tila `openclaw security audit` -ajolla ja pidä mielessä, että tämä koventaa session reititystä, ei koko järjestelmän luottamusmallia.**

Lyhyt muistilappu on tämä: **yksi käyttäjä voi elää `main`-oletuksella, useampi käyttäjä ei enää pitäisi.**

## Lähteet

- https://docs.openclaw.ai/concepts/session
- https://docs.openclaw.ai/gateway/configuration-examples
- https://docs.openclaw.ai/cli/security
- https://docs.openclaw.ai/cli/sessions
- https://docs.openclaw.ai/gateway/security
