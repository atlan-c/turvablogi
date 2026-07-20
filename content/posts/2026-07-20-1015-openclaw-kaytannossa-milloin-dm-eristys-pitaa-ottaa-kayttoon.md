---
title: "OpenClaw käytännössä: milloin DM-eristys pitää ottaa käyttöön?"
date: "2026-07-20T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Sessions"
  - "Privacy"
  - "Configuration"
---
OpenClawin oletus on yllättävän mukava niin kauan kuin agenttia käyttää vain yksi ihminen: kaikki suorat viestit voivat jakaa saman pääsession, jolloin keskustelu jatkuu luontevasti kanavasta toiseen. Mutta sama oletus muuttuu nopeasti riskiksi heti, kun useampi ihminen voi laittaa agentille DM:n. Silloin kysymys ei ole enää pelkästä käyttömukavuudesta vaan yksityisyydestä: **jaettu DM-sessio tarkoittaa jaettua keskustelukontekstia**, ja pahimmillaan yhden lähettäjän viesti vuotaa toisen keskustelun taustaksi.

OpenClawin dokumentaatio sanoo tämän nykyään poikkeuksellisen suoraan. `main`-oletuksella kaikki DM:t jakavat saman session. Jos agentille voi kirjoittaa useampi ihminen, DM-eristys kannattaa ottaa käyttöön. Tämä on sellainen asetus, jonka moni jättää myöhemmäksi siksi, että kaikki näyttää ensin toimivan. Käytännössä se kannattaa päättää heti, koska väärä oletus näkyy vasta silloin kun vahinko on jo mahdollinen.

## Milloin oletusasetus on vielä ihan hyvä

Jaettu DM-sessio on järkevä silloin, kun nämä kaikki pitävät paikkansa:

- agentti on oikeasti henkilökohtainen ja vain sinun käytössäsi
- haluat jatkuvuutta eri kanavien välillä
- et tarvitse erillisiä konteksteja esimerkiksi Telegramille ja Signalille
- sinulle on ok, että kaikki omat DM:t kasaantuvat samaan muistivirtaan

Tällaisessa setupissa `session.dmScope: "main"` on usein juuri oikea ratkaisu. OpenClaw osaa silloin reitittää vastaukset takaisin oikeaan kanavaan, vaikka keskusteluhistoria elää saman pääsession alla. Jos siis tavoite on yksi oma "aivovirta", oletus ei ole virhe vaan tarkoituksellinen valinta.

## Missä kohtaa asetuksesta tulee riski

Raja menee siinä, voiko agentille kirjoittaa joku muukin kuin sinä itse. Sessionhallinnan dokumentaatiossa varoitus on selvä: ilman DM-eristystä eri lähettäjien yksityisviestit jakavat saman keskustelukontekstin. Tämä ei tarkoita vain sitä, että lokit ovat samassa paikassa, vaan sitä että malli voi nähdä väärän henkilön aiempaa sisältöä taustakontekstina.

Käytännössä ottaisin eristyksen käyttöön heti, jos jokin näistä toteutuu:

- agentilla on useampi käyttäjä tai testikäyttäjä
- annat ystävien, perheen tai tiimin laittaa sille DM-viestejä
- sama agentti elää sekä henkilökohtaisessa että puolijulkisessa käytössä
- käytät useita kanavia ja haluat pitää niiden keskustelut siisteinä erillään

Tämä on myös hyvä muistaa ryhmien rinnalla. OpenClaw eristää ryhmäkeskustelut jo valmiiksi omiin session-avaimiinsa, mutta DM:t eivät oletuksena saa samaa kohtelua. Siksi moni kuvittelee olevansa turvallisessa mallissa, koska "ryhmät ovat erillään", vaikka todellinen vuotoriski syntyy juuri suorissa viesteissä.

## Mikä `dmScope` kannattaa valita

Useimmille harrastajille ja pienille self-hostatuille agenteille paras kompromissi on `per-channel-peer`. Dokumentaatio suosittelee sitä käytännössä suoraan: sessio erotellaan kanavan ja lähettäjän perusteella. Se on turvallisempi kuin yksi yhteinen pääsessio, mutta ei vielä niin hienojakoinen, että konfiguraatio muuttuisi hankalaksi ylläpitää.

Nopea tulkinta vaihtoehdoista menee näin:

- `main`: kaikki DM:t samaan sessioon
- `per-peer`: yksi sessio per lähettäjä, kanavasta riippumatta
- `per-channel-peer`: yksi sessio per lähettäjä per kanava
- `per-account-channel-peer`: erottelu myös tili-instanssin tasolla

Jos sama ihminen viestii sinulle useasta kanavasta ja haluat silti yhden yhteisen keskustelun, OpenClaw tukee myös `session.identityLinks`-mäppäystä. Tämä on hyödyllinen poikkeus: eristys kannattaa pitää oletuksena päällä, ja vasta sen jälkeen yhdistää vain ne identiteetit, jotka oikeasti kuuluvat samalle ihmiselle.

## Yksi käytännön malli, joka toimii hyvin

Jos haluat yhden henkilökohtaisen agentin mutta myös turvallisen ryhmä- tai yhteisökäytön, hyvä perusmalli on tämä:

1. pidä DM:t eristettyinä asetuksella `per-channel-peer`
2. anna ryhmien pysyä omissa sessioissaan kuten OpenClaw tekee muutenkin
3. sandboxaa non-main-sessiot, jos ryhmissä tai kanavissa on laajempi yleisö
4. käytä toista agenttia vasta silloin, kun tarvitset aidosti erillisen persoonan tai työtilan

Tämä on minusta tärkeä käytännön ero. Kaikkea ei tarvitse ratkaista heti monella agentilla. Usein jo oikein valittu `dmScope` poistaa suurimman yksityisyysriskin ja pitää setupin paljon yksinkertaisempana.

## Tarkistuslista ennen kuin jätät oletuksen voimaan

Kysy nämä neljä kysymystä:

- Kuka kaikki voi lähettää agentille DM:n tänään?
- Haluanko varmasti, että heidän viestinsä elävät samassa keskustelukontekstissa?
- Tarvitsenko kanavakohtaista erottelua vai yhden jatkumon?
- Pitäisikö minun ajaa `openclaw security audit` ennen kuin avaan agentin muille?

Jos toiseen kysymykseen ei tule välitöntä ja varmaa kyllä-vastausta, vaihda pois `main`-oletuksesta. Tämä on halpa korjaus tehdä etukäteen ja kallis oppia vasta jälkikäteen.

## Yhteenveto

DM-eristys ei ole hienosäätöä vaan perushygieniaa heti, kun agentti ei ole enää täysin yksityinen. Yhden ihmisen henkilökohtaisessa käytössä OpenClawin oletus toimii hyvin. Heti kun mukaan tulee toinen lähettäjä, turvallinen oletus muuttuu: `per-channel-peer` on yleensä käytännöllisin valinta, ja vasta sen jälkeen kannattaa miettiä identiteettien yhdistämistä tai monen agentin rakennetta.

## Lähteet

- https://docs.openclaw.ai/concepts/session
- https://docs.openclaw.ai/channels/channel-routing
- https://docs.openclaw.ai/channels/groups
