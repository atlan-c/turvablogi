---
title: "OpenClaw käytännössä: milloin `HEARTBEAT.md` kannattaa jättää oikeasti tyhjäksi?"
date: "2026-07-12T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Heartbeat"
  - "Automation"
  - "Local Models"
---
Jos ajat OpenClawia paikallisella mallilla, yksi halvimmista optimoinneista ei ole uusi GPU eikä pienempi malli. Se on paljon arkisempi: **älä herätä heartbeatia tekemään tyhjiä kierroksia**. Käytännössä `HEARTBEAT.md` kannattaa jättää aidosti tyhjäksi silloin, kun sinulla ei juuri nyt ole mitään sellaista toistuvaa tarkistuslistaa, jonka agentin pitäisi oikeasti käydä läpi. Muuten päädyt helposti tilanteeseen, jossa pieni kotilabra käyttää inferenssia siihen, että agentti lukee puolivalmista scaffoldia, pohtii tyhjää ja vastaa jälleen `HEARTBEAT_OK`.

OpenClawin nykyinen dokumentaatio sanoo tämän yllättävän suoraan. Jos `HEARTBEAT.md` sisältää vain tyhjää, kommentteja, otsikoita, tyhjiä checklist-rivejä tai fence-markereita, heartbeatin mallikutsu skipataan kokonaan syyllä `empty-heartbeat-file`. Lisäksi dokumentaatio muistuttaa, että heartbeat lukee tiedoston joka tickillä, oletuksena puolen tunnin välein. Tämä tekee pienestäkin turhasta sisällöstä toistuvan kustannuksen, ja juuri paikallisilla tai muuten rajallisilla malleilla se tuntuu nopeasti.

## Milloin jättäisin tiedoston tarkoituksella tyhjäksi

Jättäisin `HEARTBEAT.md`:n käytännössä tyhjäksi ainakin näissä tilanteissa:

- et halua juuri nyt mitään säännöllisiä inbox-, kalenteri- tai ilmoitustarkistuksia
- kaikki oikeasti tärkeä on jo omissa cron-ajoissaan
- heartbeatin pitäisi lähinnä "katsoa jos jotain tulee mieleen"
- käytät pientä paikallista mallia, jolle jokainen ylimääräinen herätys on pois muusta työstä

Tämä viimeinen kohta on tärkeä. Kun inferenssikapasiteettia on vähän, turha taustahäly ei ole vain teoreettinen tokenikulu, vaan se voi hidastaa muuta käyttöä. OpenClawin automaatiodokumentaatio sanoo, että heartbeat on tarkoitettu pieneen checklistaan tai rakenteiseen `tasks:`-blokkiin, ei yleiseksi ajastetuksi ajattelukoneeksi.

## Yleinen virhe: "jätän sinne rungon valmiiksi"

Moni tekee tämän vahingossa:

1. luo `HEARTBEAT.md`:n tulevaa käyttöä varten
2. jättää sinne otsikon, pari kommenttia ja tyhjiä tehtävärivejä
3. kuvittelee, että heartbeat on käytännössä pois päältä kunnes sisältöä lisätään

OpenClawissa näin ei tarvitse arvailla, koska template-dokumentaatio kertoo suoraan mitä pidetään "tyhjänä". Se on itse asiassa hyvä uutinen: voit säilyttää kommentit ja rungon, kunhan tiedosto ei sisällä oikeaa tehtäväsisältöä. Jos et kuitenkaan tarvitse edes scaffoldia, kaikkein selkein ratkaisu on pitää tiedosto oikeasti minimaalisena.

Hyvä käytännön sääntö on tämä:

- jos haluat periodic checks -käyttäytymistä, kirjoita lyhyt konkreettinen lista
- jos et halua periodic checks -käyttäytymistä, jätä tiedosto tyhjäksi tai kommentti-/otsikkotasolle

Puolivälimuoto on usein huonoin. Silloin heartbeat näyttää konfiguroidulta, mutta todellinen hyöty on epäselvä.

## Miksi tämä korostuu juuri paikallisilla malleilla

Pilviympäristössä turha heartbeat on lähinnä jatkuva pieni kuluerä. Paikallisessa asetelmassa se voi olla myös käytettävyysongelma. OpenClawin dokumentaatio kertoo nyt, että heartbeats deferoidaan automaattisesti silloin, kun cron-työ on aktiivinen tai jonossa. Taustalla on sama käytännön ongelma, josta käyttäjät raportoivat keväällä 2026: paikallisessa LLM-ympäristössä samanaikainen cron ja heartbeat voivat kilpailla samasta inferenssiresurssista, jolloin heartbeat hidastuu tai aikakatkaisee.

Tästä seuraa yksinkertainen ajatusmalli:

- pidä heartbeat vain niille tarkistuksille, joita todella tarvitset usein
- pidä `HEARTBEAT.md` pienenä, jotta jokainen herätys on halpa
- jos et tarvitse mitään, anna skipin tapahtua mieluummin ennen mallikutsua kuin sen jälkeen

Toisin sanoen paras heartbeat on joskus se, jota ei ajeta ollenkaan.

## Milloin en jättäisi sitä tyhjäksi

En jättäisi `HEARTBEAT.md`:tä tyhjäksi, jos heartbeatilta oikeasti halutaan jotakin näistä:

- yhdistetty inbox + kalenteri + ilmoitukset -kierros
- hiljainen "pingaa vain jos on oikeasti tärkeää" -taustavalvonta
- due-only `tasks:`-blokki, jossa eri tarkistuksilla on omat intervallit
- kevyt päivittäinen huoltorutiini, jonka ei tarvitse olla täsmäcron

Näissä tilanteissa tiedoston tyhjäksi jättäminen vain poistaisi hyödyllisen toiminnon. Oleellinen raja ei siis ole "käytänkö heartbeatia koskaan", vaan "onko tämän kierroksen mukana oikeaa, nykyhetkessä arvokasta tarkistuslogiikkaa".

## Oma käytännön sääntöni

Jos OpenClaw-setup on pieni ja ajaa paikallista mallia, käyttäisin tätä nyrkkisääntöä:

1. Aloita tyhjällä tai käytännössä tyhjällä `HEARTBEAT.md`:llä.
2. Lisää sinne vain ne tarkistukset, joita oikeasti kaipaat useita kertoja päivässä.
3. Siirrä täsmälliset tai raskaammat työt cronille.
4. Karsi lista uudelleen heti, kun huomaat heartbeatin heräävän enemmän tavan vuoksi kuin tarpeeseen.

Tämä pitää sekä promptin että käyttöliittymän siistimpänä. Samalla se vähentää sitä klassista ongelmaa, jossa agentti "tekee jotain koko ajan", vaikka mikään tärkeä ei oikeasti muutu.

## Yhteenveto

`HEARTBEAT.md` ei ole pakollinen tehtävälista vaan optio. Jos sinulla ei juuri nyt ole järkevää periodic checklistiä, tiedoston saa ja usein kannattaa jättää oikeasti tyhjäksi. OpenClaw osaa silloin skipata mallikutsun kokonaan, mikä on erityisen hyödyllistä paikallisissa LLM-asennuksissa ja pienissä AI-kotilabroissa.

Käytännössä kysy vain tämä:

**Herättäisikö tämä heartbeat minutkin, jos joutuisin itse vastaamaan siihen puolen tunnin välein?**

Jos vastaus on ei, tiedosto kannattaa todennäköisesti pitää tyhjänä vielä vähän pidempään.

## Lähteet

- https://docs.openclaw.ai/reference/templates/HEARTBEAT
- https://docs.openclaw.ai/gateway/heartbeat
- https://docs.openclaw.ai/automation
- https://github.com/openclaw/openclaw/issues/50773
