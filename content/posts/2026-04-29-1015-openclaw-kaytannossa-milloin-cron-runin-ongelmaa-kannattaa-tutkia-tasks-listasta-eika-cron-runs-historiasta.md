---
title: "OpenClaw käytännössä: milloin cron-runin ongelmaa kannattaa tutkia tasks-listasta eikä cron runs -historiasta?"
date: 2026-04-29T10:15:00+03:00
draft: false
topic_family: "openclaw"
---

Kun OpenClawin ajastettu työ alkaa käyttäytyä oudosti, ensimmäinen vaisto on usein avata `openclaw cron runs` ja katsoa historiaa. Se on hyvä alku, mutta ei aina oikea ensimmäinen työkalu. Käytännössä kannattaa erottaa kaksi eri kysymystä: haluatko nähdä mitä scheduler teki vai haluatko nähdä mitä irrotettu työ oikeasti tekee juuri nyt.

Lyhyt sääntö on tämä: käytä `cron runs` silloin, kun tutkit ajastuksen historiaa ja lopputulosta. Käytä `tasks list` silloin, kun epäilet että itse taustatyö on jumissa, vielä käynnissä tai muuten käyttäytyy oudosti irrallaan cronista.

## Mitä `cron runs` kertoo hyvin

`openclaw cron runs` on hyvä silloin, kun kysymys on tällainen:

- käynnistyikö jobi ajallaan
- montako kertaa se on ajettu
- päättyikö ajo onnistuneesti vai virheeseen
- kuinka pitkään viime ajot kestivät

Tämä on schedulerin näkökulma. Se kertoo, mitä cron-jobille tapahtui ajokertojen tasolla. Jos haluat nopeasti nähdä, onko päivittäinen reminder ylipäätään toiminut viime päivinä, tämä on yleensä oikea näkymä.

## Mitä `tasks list` tuo lisää

OpenClawin task-dokumentaatio korostaa, että taskit ovat detached workin aktiivisuusloki. Ne eivät ole scheduleri, vaan kirjanpito siitä mitä taustalla käynnistynyt työ teki. Tämä ero on käytännössä tärkeä.

`openclaw tasks list` on hyödyllinen erityisesti silloin, kun cron-jobi on jo laukaissut työn, mutta haluat tietää mitä sille tapahtuu nyt. Se auttaa esimerkiksi näissä tilanteissa:

- ajo näyttää jääneen `running`-tilaan
- haluat erottaa cron-jobin ja sen käynnistämän lapsityön
- epäilet, että subagentti tai eristetty ajo jäi elämään taustalle
- haluat nähdä detached workin tilan yli eri runtimejen

Toisin sanoen `tasks list` ei vastaa vain siihen "ajoinko jobin", vaan enemmän siihen "mitä tämä taustatyö oikeasti tekee".

## Missä kohtaa väärä työkalu hidastaa vianrajausta

Jos cron-jobi näyttää terveeltä mutta käyttäytyminen on silti outoa, pelkkä `cron runs` voi jäädä liian ylätasoiseksi. Se voi kertoa, että ajo käynnistyi, mutta ei välttämättä anna parasta ensimmäistä näkymää siihen, onko irrallinen taski jäänyt roikkumaan, mennyt lost-tilaan tai käyttänyt eri runtimea kuin odotit.

Toisaalta `tasks list` ei korvaa cron-historiaa. Jos ongelma liittyy siihen, ettei jobi laukea oikeaan aikaan tai schedulerin tila on epäselvä, cron-historia on edelleen oikeampi aloituspaikka.

## Oma nyrkkisääntö

Minun käytännön sääntöni olisi tämä:

1. aloita `cron runs`-näkymästä, jos epäilet ajoitus- tai jobihistoriaongelmaa
2. siirry `tasks list`-näkymään, jos epäilet että varsinainen taustatyö jäi elämään, jumittui tai hajosi cronin jälkeen
3. käytä `tasks show`-porautumista, kun löydät yksittäisen epäilyttävän taskin
4. pidä mielessä, että cron vastaa kysymykseen milloin työ laukaistiin, taskit vastaavat kysymykseen mitä detached workille tapahtui

Tämä yksinkertainen jako nopeuttaa käytännössä monia selvityksiä.

## Miksi tämä on hyödyllinen ajattelumalli

OpenClaw erottaa tarkoituksella schedulerin ja task-ledgerin. Se on hyvä suunnitteluvalinta, koska kaikki detached work ei ole cronia, eikä kaikki cron-ongelmat ole taskiongelmia. Kun tämän erotuksen ymmärtää, diagnostiikka tuntuu paljon vähemmän sumuiselta.

Käytännössä tämä säästää aikaa. Et yritä lukea task-ledgeristä schedulerin ongelmaa etkä puristaa cron-historiasta yksityiskohtia, jotka kuuluvat taustatyön omaan kirjanpitoon.

## Yhteenveto

Milloin cron-runin ongelmaa kannattaa tutkia `tasks list`-näkymästä eikä `cron runs` -historiasta? Silloin, kun epäilet että varsinainen detached work on jumissa, edelleen käynnissä tai käyttäytyy oudosti cronin laukaisun jälkeen.

Jos taas kysymys on siitä laukeaako jobi, milloin se laukeaa ja miten viime ajot päättyivät, `cron runs` on edelleen paras ensimmäinen näkymä. Lyhyt muistilappu on tämä: cron kertoo jobin historian, taskit kertovat taustatyön todellisen elämän.

## Lähteet

- https://docs.openclaw.ai/automation/tasks
- https://docs.openclaw.ai/automation/cron-jobs
