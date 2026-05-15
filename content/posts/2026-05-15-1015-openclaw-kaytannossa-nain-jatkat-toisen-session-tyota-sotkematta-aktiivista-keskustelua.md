---
title: "OpenClaw käytännössä: näin jatkat toisen session työtä sotkematta aktiivista keskustelua"
date: 2026-05-15T10:15:00+03:00
draft: false
topic_family: "openclaw"
---

OpenClawissa tulee nopeasti vastaan käytännön tilanne: yksi työ jäi kesken toisessa sessiossa, subagentti teki taustalla jotain hyödyllistä tai vanhassa cron-ajossa on jälki, johon pitäisi tarttua. Silloin kiusaus on suuri vain jatkaa samasta ihmisthreadista vähän sinne päin. Se toimii joskus, mutta usein samalla sotkee näkyvän keskustelun, rikkoo eristyksen tai hukkaa sen, mistä työ oikeasti piti jatkua.

Lyhyt sääntö on tämä: **katso ensin missä sessiossa työ oikeasti elää, lue siitä vain tarpeellinen konteksti ja viesti takaisin oikeaa reittiä pitkin**. Älä käytä aktiivista ihmisthreadia yleisenä ohjauspaneelina kaikkeen.

## Miksi tämä menee helposti sotkuun

OpenClawin sessiomalli on tarkoituksella eriytetty. Dokumentaation mukaan direct message, group, room, cron, webhook ja subagent-ajot eivät ole vain eri viestejä vaan eri session elinkaaria ja reitityksiä. Tämä on hyvä asia: samaan pottiin ei valu kaikkea. Samalla se tarkoittaa, että "missä tämä työ nyt oikeasti on" on tärkeä kysymys eikä pelkkä detalji.

Käytännössä sotku syntyy yleensä kolmella tavalla:

- yritetään ohjata vanhaa työtä väärästä sessiosta käsin
- luetaan liikaa raakaa historiaa vaikka tarvittaisiin vain rajattu tilannekuva
- lähetetään koordinaatioviesti paikkaan, jossa ihminenkin on aktiivisesti mukana

Jos nämä sekoittuvat, lopputulos on helposti sellainen, että agentti kyllä tekee jotain, mutta audit trail ja keskustelun selkeys kärsivät.

## Aloita tästä: selvitä ensin oikea kohdesessio

Käytännössä oikea ensimmäinen kysymys ei ole "mitä komentoja ajan" vaan "minkä session työtä olen jatkamassa".

OpenClawin session tools -dokumentaatio kuvaa tähän selkeän työjaon:

- `sessions_list` on löytämiseen
- `sessions_history` on rajattuun takaisinlukuun
- `sessions_send` on viestin toimittamiseen toiseen sessioon
- `session_status` on kevyt tilannekortti

Tämä jako on hyödyllinen juuri siksi, että kaikkea ei tarvitse ratkaista yhdellä väkivaltaisella promptilla. Ensin etsit, sitten luet, sitten toimit.

Hyvä käytännön malli on tällainen:

1. listaa näkyvät relevantit sessiot
2. tunnista oikea kohde nimen, tyypin, recency-tiedon tai viimeisen viestin perusteella
3. lue vain rajattu historia tai status
4. lähetä jatko-ohje oikeaan sessioon, jos jatkotyö pitää tehdä siellä

Tämä kuulostaa hitaammalta kuin improvisointi, mutta oikeasti se vähentää virheitä.

## `sessions_history` ei ole sama asia kuin koko raakatranskripti

Tämä on tärkeä käytännön nyanssi. Dokumentaation mukaan `sessions_history` palauttaa tarkoituksella rajatun ja safety-filteröidyn näkymän. Tool payloadit voidaan siivota pois, isoja rivejä voidaan typistää ja tokenimainen tai muuten herkkä sisältö voidaan redaktoida.

Se tarkoittaa kahta asiaa:

- useimmissa jatkotöissä tämä on juuri oikea työkalu, koska saat olennaisen ilman täyttä lokitulvaa
- jos tarvitset tavu tavulta täydellisen transcriptin, `sessions_history` ei ole siihen tarkoitettu

Moni aloittelijan virhe syntyy siitä, että rajattua recall-näkymää tulkitaan täydelliseksi totuudeksi. Käytännössä se on hyvä ohjausnäkymä, ei forensiikan raakakuva.

## Älä työnnä agenttien välistä koordinointia aktiiviseen ihmisthreadiin

Yksi hyödyllinen mutta helposti ohitettu yksityiskohta session tools -dokumentaatiossa on tämä: thread-scoped chat session ei ole oikea `sessions_send`-kohde agenttien väliseen koordinointiin. Ajatus on järkevä. Jos työkalureititetty agenttiviesti alkaa ilmestyä suoraan aktiiviseen ihmiskeskusteluun, keskustelun semantiikka menee rikki nopeasti.

Käytännön seuraus on selvä:

- jos koordinoit sessioiden välillä, kohdista viesti parent channel -sessioon
- pidä ihmisen näkyvä threadi ihmiskeskusteluna, ei agenttien sisäisenä väylänä

Tämä on pieni sääntö, mutta sillä on iso vaikutus siihen tuntuuko automaatio hallitulta vai kaoottiselta.

## Milloin pelkkä `session_status` riittää

Kaikkeen ei tarvitse avata historiaa. Jos kysymys on lähinnä tällainen:

- onko sessio yhä olemassa
- mikä malli sillä on käytössä
- paljonko kontekstia tai käyttöä on kertynyt
- liittyykö siihen taustatehtävä

silloin `session_status` on usein parempi ensimmäinen askel kuin historian selaus. Session management -dokumentaatio kuvaa `/status`-näkymän juuri kevyenä tilannekuvana, ja session tools -dokumentaatio sanoo saman ohjelmallisesta `session_status`-työkalusta.

Hyvä nyrkkisääntö on tämä: **status ensin, historia vasta jos status ei riitä päätöksen tekemiseen**.

## Subagentit muuttavat jatkotyön mallia

Kun työ on delegoitu subagentille, jatkaminen ei yleensä tarkoita sitä, että pääsessio alkaa väkisin pollata lapsen tilaa. Subagent-dokumentaatio painottaa push-pohjaista completion-mallia: spawnin jälkeen odotetaan tuloksen palaavan announce-virtana takaisin, ja jos välissä pitää oikeasti odottaa, oikea malli on `sessions_yield`, ei jatkuva kyselysilmukka.

Tämä on tärkeä käytännön ero. Jos jokaista taustatyötä seurataan manuaalisella pollauksella, pääsessio muuttuu helposti levottomaksi valvomoksi. Jos taas luotetaan oikeaan announce- ja yield-malliin, koordinaatio pysyy siistimpänä.

## Käytännön päätöspuu

Kun sinun pitää jatkaa toisen session työtä, käytä tätä järjestystä:

- **Tarvitsen vain nopean tilannekuvan** → aloita `session_status`
- **En tiedä missä työ on** → aloita `sessions_list`
- **Tiedän kohdesession, mutta tarvitsen kontekstin** → käytä `sessions_history`
- **Työtä pitää jatkaa juuri siinä sessiossa** → käytä `sessions_send`
- **Työ on oma uusi rajattu kokonaisuutensa** → harkitse uutta subagenttia sen sijaan, että tunget kaiken vanhaan keskusteluun

Tämän päätöspuun arvo ei ole siinä, että se on teoreettisesti kaunis. Sen arvo on siinä, että audit trail, näkyvä keskustelu ja työn omistajuus pysyvät erillään.

## Mitä aloittelija usein ymmärtää väärin

Yleinen harha on ajatella, että yksi pitkä main-sessio on aina paras paikka kaikelle jatkuvuudelle. OpenClawin dokumentaatio näyttää käytännössä päinvastaista: jatkuvuus on hyödyllistä, mutta se on rajattava oikeaan session elinkaareen ja oikeaan näkyvyystasoon.

Jos kaikki jatkotyö yritetään tehdä samasta näkyvästä keskustelusta käsin, seurauksena on yleensä ainakin yksi näistä:

- väärä konteksti vuotaa mukaan
- vanhan työn omistajuus hämärtyy
- ihmisen ja agentin välinen keskustelu alkaa täyttyä sisäisellä orkestroinnilla
- myöhempi vianjäljitys vaikeutuu

Siksi parempi ajattelutapa on tämä: **sessio ei ole vain muisti, vaan myös rajaus**.

## Yhteenveto

Kun OpenClaw-työtä pitää jatkaa toisesta sessiosta, tärkeintä ei ole nopein mahdollinen ohjaus vaan siistein mahdollinen reititys. Etsi oikea sessio, lue vain tarvittava konteksti, käytä statusia kun se riittää ja pidä ihmisthreadit erossa agenttien sisäisestä koordinoinnista.

Se tekee automaatiosta vähemmän näyttävää, mutta paljon luotettavampaa. Ja käytännössä juuri se on yleensä se oikea optimointi.

## Lähteet

- https://docs.openclaw.ai/concepts/session
- https://docs.openclaw.ai/concepts/session-tool
- https://docs.openclaw.ai/tools/subagents
