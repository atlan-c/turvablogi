---
title: "OpenClaw käytännössä: milloin asia kuuluu `HEARTBEAT.md`:hen ja milloin omaksi cron-jobiksi?"
date: "2026-06-05T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Automation"
  - "Heartbeat"
  - "Cron"
---
OpenClawissa moni automaatio-ongelma ei johdu siitä, että ominaisuuksia olisi liian vähän, vaan siitä, että **sama asia yritetään laittaa väärään paikkaan**. Käytännössä yleisin sekaannus on tämä: inboxin, kalenterin ja muiden toistuvien tarkistusten annetaan valua erillisiksi cron-jobeiksi, vaikka ne kuuluisivat yhteiseen heartbeat-rutiiniin. Samaan aikaan tarkasti ajoitettu raportti tai raskas taustaanalyysi jätetään pääsession sykkeeseen, vaikka se kuuluisi omaan eristettyyn ajoonsa.

Minun nyrkkisääntöni on yksinkertainen: **jos työn pitää ymmärtää tämänhetkistä keskustelukontekstia ja sen ajoitus saa vähän elää, se kuuluu heartbeatille. Jos työn pitää osua täsmälliseen aikaan tai pysyä irti pääsession historiasta, se kuuluu cronille.** Kun tämän eron tekee kerran oikein, OpenClawin automaatio muuttuu heti rauhallisemmaksi ylläpitää.

## Aloita tästä päätöksestä: onko työ "jatkuvaa tietoisuutta" vai "täsmäajo"?

OpenClawin virallinen `Cron vs heartbeat` -ohje sanoo asian hyvin suoraan: heartbeat on tarkoitettu periodiseen tietoisuuteen, cron taas tarkkaan ajastukseen. Heartbeat toimii pääsession sisällä ja saa mukaansa saman keskustelukontekstin kuin muukin agentin arki. Cron taas voidaan ajaa eristetyssä sessiossa omana työnään, jolloin se ei sotke pääsession historiaa eikä ole riippuvainen siitä, mitä juuri ennen sitä puhuttiin.

Tämä kuulostaa pieneltä erolta, mutta käytännössä se ratkaisee paljon:

- heartbeat sopii silloin, kun useita pieniä tarkistuksia kannattaa niputtaa yhdeksi kierrokseksi
- cron sopii silloin, kun työn on tapahduttava juuri tiettyyn aikaan tai puhtaasta lähtötilasta

Jos siis kysymys on "pitäisikö agentin silloin tällöin katsoa, onko jotain tärkeää ilmestynyt", heartbeat on yleensä oikea koti. Jos kysymys on "lähetä tämä joka aamu 7:00" tai "aja sunnuntaina raskas analyysi", cron on yleensä oikea ratkaisu.

## Mitä heartbeat tekee paremmin kuin joukko pieniä cron-jobeja

Heartbeat-dokumentaatio korostaa kahta hyötyä, joista ensimmäinen on käytännössä tärkein: se pystyy yhdistämään useita tarkistuksia yhteen agenttivuoroon. Siksi inbox, kalenteri, ilmoitukset ja kevyet projektiseurannat kannattaa usein pitää samassa `HEARTBEAT.md`-tiedostossa eikä pilkkoa viideksi eri scheduler-merkinnäksi.

Toinen hyöty on konteksti. Koska heartbeat ajetaan pääsession sisällä, agentti pystyy suhteuttamaan löydöksen siihen, mitä käyttäjän kanssa on jo puhuttu. Tämä on hyödyllistä silloin, kun tarkistus ei ole pelkkä kyllä/ei-hälytin vaan vaatii arvion siitä, onko asia oikeasti keskeyttämisen arvoinen.

Hyvä heartbeat-työ näyttää yleensä tältä:

- tarkista säännöllisesti useampi pieni signaali yhdellä kertaa
- pysy hiljaa, jos mitään merkittävää ei ole tapahtunut
- reagoi vasta, kun taustalla on oikeasti jotain huomion arvoista

Juuri tätä varten `HEARTBEAT.md` on hyvä paikka lyhyelle checklistalle. Heartbeat-sivu sanoo myös suoraan, että tiedoston kannattaa pysyä pienenä. Jos checklistasta tulee romaani, olet jo syömässä tokenit väärästä paikasta.

## Milloin cron on selvästi parempi valinta

Cronin vahvuus ei ole "enemmän automaatiota" vaan **tarkempi sopimus työn ajasta ja muodosta**. OpenClawin cron-dokumentaatio kuvaa kaksi toteutustapaa: pääsession kautta sisään syötettävä system event ja täysin eristetty ajo omassa `cron:<jobId>`-sessiossaan. Käytännössä näistä jälkimmäinen on kullanarvoinen silloin, kun haluat irrottaa työn muusta keskusteluhistoriasta.

Valitsisin cronin selvästi ainakin näissä tapauksissa:

- raportin tai muistutuksen pitää osua kellonaikaan eikä "sinne päin"
- työn pitää voida käyttää eri mallia kuin pääagentti
- ajo on raskas eikä sitä haluta pääsession historian sekaan
- työ on yksittäinen täsmätehtävä eikä jatkuva tilanteen seuranta

Tässä kohtaa kannattaa erottaa toisistaan myös cronin kaksi eri käyttöä.

Jos haluat vain pistää pääsession muistamaan jotain oikeaan aikaan, `main`-session cron system eventillä on hyvä ratkaisu. Jos taas haluat puhtaan, irrallisen analyysiajon, `isolated`-cron on paljon terveempi valinta.

## Käytännön virhe, jonka näen useimmin

Yleisin huono rakenne on tämä:

- heartbeat jätetään lähes tyhjäksi
- jokaiselle pienelle tarkistukselle tehdään oma cron-jobi
- tuloksena syntyy monta irrallista ajastettua ajoa, jotka kaikki tarkistavat vähän samaa asiaa ilman yhteistä tilannekuvaa

Tämä on kallis ja helposti meluisa tapa käyttää agenttia. OpenClawin automaatiodokumentaatio painottaa, että heartbeat on juuri se paikka, jossa useita toistuvia tarkistuksia kannattaa yhdistää. Cron taas on hyvä silloin, kun täsmällinen ajoitus tai session eristys tuo oikeaa lisäarvoa.

Toinen yleinen virhe on päinvastainen: heartbeatille jätetään raskas viikkoraportti, vaikka sen olisi fiksumpaa juosta omassa cron-ajossaan halvemmalla mallilla. Heartbeatin idea ei ole korvata kaikkea muuta ajastusta, vaan hoitaa jatkuva, kevyt tilannetietoisuus.

## Nopea päätöspuu, jota itse käyttäisin

Kun mietin mihin uusi automaatio kuuluu, käyn nämä kysymykset läpi tässä järjestyksessä:

1. Pitääkö työn osua täsmälliseen kellonaikaan?
2. Tarvitseeko se pääsession täyden keskustelukontekstin?
3. Onko kyse useasta pienestä tarkistuksesta vai yhdestä rajatusta ajosta?
4. Haluanko tämän historian näkyvän pääsession jatkona vai omana työnään?

Jos vastaukset ovat "ei, kyllä, useita pieniä tarkistuksia, pääsession jatkona", laittaisin työn heartbeatille. Jos vastaukset ovat "kyllä, ei välttämättä, yksi rajattu ajo, omana työnään", laittaisin sen cronille, yleensä eristettynä.

Yhteenvedoksi:

- `HEARTBEAT.md`: inbox, kalenteri, ilmoitukset, pienet taustaseurannat, käyttäjän tilanteeseen sidottu priorisointi
- `cron --session main`: täsmäaikainen muistutus, jonka haluat pääsession kontekstiin
- `cron --session isolated`: raskaat raportit, analyysit, erilliset päivittäiset tai viikoittaiset ajot

## Pieni mutta tärkeä sivuhuomio sessioista

Session management -dokumentaatio muistuttaa, että cron-ajot lähtevät oletuksena omasta tuoreesta sessiostaan, kun taas heartbeat on pääsession periodinen vuoro. Tämä on hyvä muistaa etenkin silloin, kun ihmettelet miksi heartbeat "muistaa" viime viikon keskustelun mutta isolated cron ei.

Käytännössä tämä on ominaisuus, ei puute. Eristetty cron on parempi silloin, kun haluat toistettavan ja siistin työnkulun. Heartbeat on parempi silloin, kun automaation arvo syntyy siitä, että agentti tuntee jo tilanteen.

## Oma johtopäätökseni

Jos OpenClaw-setup alkaa tuntua sekavalta, en ensimmäisenä lisäisi uutta promptia vaan tarkistaisin työn sijoittelun. **Heartbeat kuuluu jatkuvaan havahtumiseen. Cron kuuluu täsmäajoihin. Eristetty cron kuuluu töihin, joille haluat puhtaan työpöydän.**

Tämä jako säästää käytännössä kolmea asiaa samaan aikaan:

- pääsession selkeyttä
- automaation kustannusta
- omaa aikaa, koska vikaantunut rakenne löytyy helpommin

Usein paras parannus OpenClaw-automaatioon ei siis ole uusi ominaisuus vaan se, että siirrät yhden väärässä paikassa olevan työn oikeaan lokeroon.

## Lähteet

- https://docs.openclaw.ai/cron-vs-heartbeat/
- https://open-claw.bot/docs/gateway/heartbeat/
- https://docs.openclaw.ai/cron/
- https://docs.openclaw.ai/concepts/session
