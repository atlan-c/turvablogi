---
title: "OpenClaw käytännössä: milloin recurring workflow tarvitsee session:id:n eikä isolated-ajon?"
date: "2026-04-27T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Agents"
  - "Local LLM"
  - "Automation"
  - "Troubleshooting"
---
OpenClawin toistuvissa automaatioissa yksi käytännössä tärkeä valinta on tämä: ajetaanko workflow aina eristettynä uutena suorituksena vai sidotaanko se pysyvään `session:<id>`-sessioon. Lyhyt käytännön sääntö on tämä: jos jokaisen ajon pitää alkaa puhtaalta pöydältä, `isolated` on yleensä oikea oletus. Jos taas työn pitää rakentua aiempien ajojen historian, muistioiden tai jatkuvan kontekstin päälle, `session:<id>` alkaa olla oikea työkalu.

Tämä kuulostaa pieneltä asetukselta, mutta sillä on iso vaikutus siihen tuntuuko automaatio vakaalta työnkululta vai satunnaiselta irtoajolta.

## Mitä `isolated` tekee hyvin

`isolated` on hyvä oletus silloin, kun haluat jokaisesta ajosta itsenäisen. Tällöin yksi cron-run luo oman erillisen session, tekee työnsä ja voi päättyä ilman että vanha keskusteluhistoria vaikuttaa seuraavaan kertaan.

Tämä sopii hyvin esimerkiksi:

- yksittäisiin raportteihin
- puhtaisiin health-checkeihin
- selvästi rajattuihin taustatöihin
- tilanteisiin joissa kaikki tarvittava tila tulee promptista tai ulkoisesta datasta

Hyvä puoli on ennustettavuus. Kun ajo alkaa aina tuoreena, vanhat sivuraiteet eivät pääse sotkemaan työn logiikkaa.

## Milloin `session:<id>` on parempi

Dokumentaatio nostaa tämän esiin erityisesti recurring workflow -kuviossa: käytä `session:<id>` silloin, kun työn pitää hyödyntää aiempaa historiaa tarkoituksella. Tämä voi tarkoittaa esimerkiksi sitä, että workflow rakentaa päivästä toiseen yhteenvetoa, seuraa edellisten ajokertojen päätöksiä tai säilyttää tarkoituksellisen muistijäljen siitä, mitä jo tehtiin.

Hyviä esimerkkejä ovat:

- päivittäinen brief, joka vertailee tämän päivän tilannetta eiliseen
- jatkuva seurantatyö, jossa aiemmat havainnot pitää muistaa
- recurring workflow, jonka prompti olisi muuten täynnä toistuvaa taustakontekstia
- ohjelma, jossa sama sessio toimii käytännössä työn muistikirjana

Tällöin `session:<id>` ei ole vain kätevä, vaan voi tehdä koko työnkulusta paljon siistimmän.

## Missä kohtaa ihmiset valitsevat väärin

Yleinen virhe on käyttää `session:<id>` vain siksi, että "ehkä historia auttaa". Jos historiaa ei oikeasti tarvita, tuloksena on helposti paisuva sessio, lisää tokenikuormaa ja enemmän yllätyksiä. Vanhoja oletuksia voi jäädä elämään liian pitkään, vaikka itse työn pitäisi olla tuore joka kerta.

Toinen yleinen virhe on pitää kaikki `isolated`-tilassa, vaikka workflow oikeasti tarvitsee jatkuvuutta. Silloin sama tausta täytyy ladata promptiin uudestaan ja uudestaan tai rakentaa ulkoisiin tiedostoihin kiertoteitse. Tämä toimii, mutta on kömpelömpää kuin tarkoituksellinen pysyvä sessio.

## Oma nyrkkisääntö

Minun käytännön sääntöni olisi tämä:

1. aloita `isolated`-oletuksella
2. siirry `session:<id>`-malliin vasta kun voit nimetä selvästi mitä historiaa tarvitaan
3. jos workflow vertailee aiempia ajoja tai rakentaa jatkuvaa kontekstia, pysyvä sessio on usein perusteltu
4. jos työn kaikki tila on eksplisiittisesti datassa tai workflow-steppeissä, eristetty ajo on yleensä siistimpi

Tämä pitää automaation yksinkertaisena niin pitkään kuin mahdollista, mutta sallii jatkuvuuden silloin kun siitä on oikeasti hyötyä.

## Miten tämä liittyy Task Flow -ajatteluun

Task Flow -dokumentaatio korostaa, että ajoitus, orkestrointi ja seuranta ovat eri kerroksia. Sama pätee tähän sessiovalintaan. Cron kertoo milloin workflow käynnistyy. Task Flow voi seurata monivaiheista suoritusta. Mutta `isolated` vs `session:<id>` ratkaisee ennen kaikkea sen, elääkö työ yhdessä jatkuvassa muistissa vai ei.

Se on siis enemmänkin kontekstisuunnittelua kuin pelkkä tekninen detalji.

## Yhteenveto

Milloin recurring workflow tarvitsee `session:<id>`-session eikä `isolated`-ajoa? Silloin, kun työn arvo syntyy tarkoituksellisesta jatkuvuudesta: aiemmista havainnoista, vertailuista, muistijäljistä tai pitkäkestoisesta keskustelukontekstista.

Jos taas jokaisen ajon pitää olla puhdas, rajattu ja helposti debugattava, `isolated` on yleensä parempi oletus. Lyhyin muistilappu on tämä: `isolated` suojaa tuoreutta, `session:<id>` säilyttää tarkoituksellisen jatkuvuuden.

## Lähteet

- https://docs.openclaw.ai/automation/tasks
- https://docs.openclaw.ai/automation/taskflow
