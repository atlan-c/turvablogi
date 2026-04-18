---
title: "OpenClaw käytännössä: milloin cron-job kannattaa sitoa nykyiseen sessioon?"
date: 2026-04-18T10:15:00+03:00
draft: false
topic_family: "openclaw"
---

OpenClawin cronissa on yksi pieni mutta käytännössä tärkeä valinta, jonka moni ohittaa alussa: ajetaanko työ main-sessiona, eristettynä ajona vai sidotaanko se nykyiseen sessioon. Oma nyrkkisääntöni on yksinkertainen: jos tehtävä hyötyy oikeasti aiemmasta kontekstista, `--session current` tai nimetty sessio voi olla erinomainen. Jos taas haluat ennustettavan, siistin ja helposti rajattavan automaation, eristetty ajo on yleensä parempi oletus.

Tämä ero kuulostaa pieneltä, mutta näkyy nopeasti arjessa. Sama muistutus tai automaatio voi joko tuntua fiksulta jatkumolta tai muuttua sekavaksi, jos sessiovalinta on väärä.

## Mitä eri vaihtoehdot käytännössä tekevät

OpenClawin cron tukee ainakin neljää olennaista sessiotapaa:

- `main`, joka menee pääsession seuraavaan heartbeat-kierrokseen
- `isolated`, joka ajaa työn omassa `cron:<jobId>`-sessiossa
- `current`, joka sitoo työn siihen sessioon, jossa cron luotiin
- `session:<id>`, joka käyttää nimettyä pysyvää sessiota

Dokumentaation perusteella nämä eivät ole vain teknisiä nimiä, vaan eri työnkulkuja varten tehtyjä valintoja. Main-session cron toimii hyvin muistutuksissa ja system-event-tyyppisissä herätteissä. Isolated taas sopii raporteille ja taustatöille, joissa halutaan puhdas ja rajattu suoritusympäristö.

## Milloin `--session current` on oikeasti hyvä idea

Nykyiseen sessioon sitominen toimii hyvin silloin, kun automaation täytyy jatkaa samaa keskustelua eikä vain suorittaa yksittäistä komentoa. Hyviä esimerkkejä ovat:

- projektikohtainen päivittäinen tarkistus, jossa sama sessio on jo täynnä olennaista taustaa
- pitkäkestoinen työketju, jossa halutaan säilyttää päätökset, rajaukset ja aiemmat havainnot
- toistuva yhteenveto, jonka pitää rakentua edellisten ajojen päälle ilman, että joka kerta selitetään kaikki alusta

Tällöin sessioon sidottu cron voi tuntua melkein samalta kuin luotettava työparin muistutus: se tietää jo, mistä puhuttiin, eikä aloita joka aamu tyhjästä.

## Milloin se on huono idea

`--session current` on huono oletus, jos tehtävästä halutaan myöhemmin helposti siirrettävä, rajattava tai auditoitava. Ongelmia tulee erityisesti silloin, kun:

- alkuperäinen sessio oli tilapäinen tai sotkuinen
- samaan sessioon kertyy useita eri aiheita
- tehtävä pitäisi voida debugata ilman vanhaa keskusteluhistoriaa
- halutaan minimoida kontekstikustannus ja yllätykset

Tässä kohtaa eristetty ajo voittaa usein selvästi. Isolated-run antaa puhtaamman rajauksen: yksi tehtävä, yksi tarkoitus, vähemmän historiallista painolastia. Dokumentaatio myös korostaa, että isolated-ajot sopivat juuri raporteille ja taustatöille, mikä vastaa hyvin käytännön kokemusta.

## Oma käytännön sääntö

Käytän tätä nopeaa valintaa:

1. jos kyse on muistutuksesta itselle tai pääsession herättelystä, valitse `main`
2. jos kyse on raportista, auditista tai muusta siististi rajattavasta automaatiosta, valitse `isolated`
3. jos tehtävä kuuluu selvästi yhteen tiettyyn käynnissä olevaan työketjuun, harkitse `current`
4. jos haluat jatkuvan mutta erillisen historian, käytä `session:<id>`

Tärkein havainto on tämä: `current` ei ole "älykkäämpi default", vaan tietoinen valinta kontekstin säilyttämiseksi. Jos et tarvitse sitä varmasti, älä käytä sitä vain siksi, että se kuulostaa kätevältä.

## Miksi tämä säästää vaivaa myöhemmin

Moni automaatio alkaa pienenä. Ensin tulee yksi muistutus, sitten päivittäinen raportti, sitten joku toistuva ylläpitotehtävä. Jos ne kaikki sidotaan summittaisesti samaan sessioon, myöhemmin on vaikeampi hahmottaa, mikä tieto kuuluu mihinkin työnkulkuun.

Siksi paras oletus on usein konservatiivinen: eristä se mikä voidaan eristää, ja sido sessioon vain se mikä oikeasti hyötyy jatkuvuudesta. Tämä sopii hyvin myös OpenClawin laajempaan käyttötapaan, jossa topic/thread isolation ja selkeä työn erottelu ovat yleensä vahvuuksia, eivät hidasteita.

## Yhteenveto

Milloin cron-job kannattaa sitoa nykyiseen sessioon? Silloin, kun sama tehtävä tarvitsee aidosti saman keskustelun muistia ja päätöshistoriaa. Muulloin `isolated` on usein turvallisempi ja siistimpi valinta.

Jos haluat nopean oletuksen, valitse ensin `isolated` ja perustele poikkeukset. Se tuottaa yleensä vähemmän yllätyksiä, vähemmän tokenikuormaa ja selkeämmän automaatiopolun.

## Lähteet

- https://docs.openclaw.ai/cli/cron
- https://docs.openclaw.ai/automation/cron-jobs
