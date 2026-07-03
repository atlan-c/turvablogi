---
title: "OpenClaw käytännössä: milloin isolated heartbeat kannattaa ottaa käyttöön?"
date: "2026-07-03T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Heartbeat"
  - "Automation"
  - "Sessions"
---
Moni OpenClaw-käyttäjä huomaa jossain vaiheessa saman ristiriidan: heartbeat on kätevä tapa niputtaa sähköposti-, kalenteri- ja muut taustatarkistukset yhteen, mutta samalla pääsession historia kasvaa nopeasti ja jokainen ajo alkaa maksaa enemmän tokeneita. Silloin vastaan tulee yksi käytännöllinen vipu: `isolatedSession`. Oma sääntöni on yksinkertainen: **ota isolated heartbeat käyttöön vasta silloin, kun heartbeat ei oikeasti tarvitse keskusteluhistoriaa päätöksentekoon**. Jos työ on lähinnä tarkistuslista ja pieni toimitus, eristys on usein hyvä. Jos työ taas nojaa siihen, mitä käyttäjän kanssa puhuttiin eilen, eristys katkaisee juuri sen tiedon, jota heartbeatilta odotit.

OpenClawin dokumentaatio sanoo tämän aika suoraan. Heartbeat ajaa oletuksena agentin pääsession kontekstissa, mutta `isolatedSession: true` tekee jokaisesta heartbeatista tuoreen session ilman aiempaa keskusteluhistoriaa. Samalla dokumentaatio korostaa, että `lightContext: true` voi pudottaa bootstrap-kontekstin minimiin niin, että mukana pysyy käytännössä vain `HEARTBEAT.md`. Tämä on hyvä yhdistelmä silloin, kun haluat halvan ja ennustettavan huoltoajon etkä "muistavaa apuria".

## Mitä isolated heartbeat oikeasti muuttaa

Käytännössä muutos on isompi kuin pelkkä tokenisäästö:

- heartbeat ei näe vanhaa keskustelua oletusmuodossaan
- ajo käyttää samaa eristyksen ideaa kuin isolated cron
- toimitus voi silti reitittyä pääsession viimeiseen kanavaan

Tämä viimeinen kohta on tärkeä. Eristys koskee ajon kontekstia, ei sitä minne valmis viesti lopulta menee. Siksi isolated heartbeat sopii hyvin esimerkiksi tilanteeseen, jossa haluat saman Telegram-topic-reitin tai muun toimituskanavan säilyvän, mutta et halua koko pääsession muistia mukaan jokaiseen puolen tunnin tarkistukseen.

## Milloin ottaisin sen käyttöön heti

Ottaisin `isolatedSession`in käyttöön melkein heti, jos heartbeat tekee tämän tyyppistä työtä:

- tarkistaa inboxin, kalenterin tai säätiedon vakioehdoilla
- lukee `HEARTBEAT.md`:stä pienen checklistin
- tekee toistuvan ylläpitotehtävän, jossa tärkeintä on matala kustannus ja ennustettava prompti
- pyörii paikallisella mallilla tai muuten rajallisella koneella, jossa jokainen turha kontekstitokeni tuntuu

Juuri tällaisissa töissä eristys tuo usein enemmän hyötyä kuin haittaa. OpenClawin automaatiodokumentaatio suosittelee muutenkin heartbeatia tilanteisiin, joissa halutaan tehdä useita rutiinitarkistuksia yhdessä ajossa, ja cronia silloin kun ajo tarvitsee tarkan kellonajan tai itsenäisen taustatyön. Jos heartbeatisi ei tarvitse "jatkuvaa keskustelumuistia", sitä ei kannata väkisin maksaa joka kierroksella.

## Milloin en ottaisi sitä käyttöön

Jättäisin eristyksen pois, jos heartbeat tekee mitään tällaista:

- seuraa käyttäjän aiemmista viesteistä nousseita avoimia lupauksia tai sävyä
- päättää, pitäisikö nyt keskeyttää hiljaisuus vai olla hiljaa, aiemman keskustelun perusteella
- rakentaa tarkistuslistaa lennossa viime päivien työn perusteella
- toimii käytännössä pääsession "toisena muistikerroksena"

Silloin oletus-heartbeat on yleensä parempi, koska se saa koko session historian. OpenClawin sessionhallintadokumentaatio muistuttaa lisäksi, että heartbeat-, cron- ja muut system-event-ajot eivät pidä sessiota tuoreena daily- tai idle-resetin näkökulmasta. Toisin sanoen: heartbeat voi kirjoittaa metatietoa, mutta se ei korvaa normaalia käyttäjävuorovaikutusta session jatkuvuuden lähteenä. Jos siis luotat liikaa siihen, että heartbeat "pitää keskustelun lämpimänä", suunnittelet väärän asian varaan.

## Paras käytännön yhdistelmä pienelle kotilabralle

Jos ajan OpenClawia paikallisella mallilla tai muuten niukalla koneella, pitäisin nyrkkisääntönä tätä:

1. Aloita tavallisella heartbeatilla, jos et vielä tiedä mitä kontekstia tarvitset.
2. Kun huomaat, että ajo on pelkkä vakioitu tarkistuslista, siirrä se malliin `isolatedSession: true` + `lightContext: true`.
3. Jos tarvitset silti pitkäikäistä muistia tai monivaiheista orkestrointia, älä väkisin tunge sitä heartbeatin sisään, vaan siirrä työ cronin, Task Flow'n tai muun tarkoitukseen sopivan mekanismin puolelle.

Tämä viimeinen kohta säästää paljon turhaa säätöä. Heartbeat on hyvä huoltokierros, ei maaginen workflow-kone kaikkeen.

## Oma johtopäätökseni

`isolatedSession` on hyvä työkalu silloin, kun heartbeatin pitää olla halpa, toistuva ja lähes mekaaninen. Se on huono työkalu silloin, kun heartbeatin pitäisi ymmärtää keskustelun jatkumoa, rivien väliä tai viime päivien tilannetta ilman että kaikkea kirjoitetaan erikseen `HEARTBEAT.md`:hen.

Jos haluat nopean päätösohjeen, käytä tätä: **eristä checklisti, älä eristä muistia tarvitsevaa harkintaa**. Useimmissa harrastaja- ja kotilabra-asennuksissa juuri tämä raja tekee heartbeatista sekä halvemman että luotettavamman.

## Lähteet

- https://docs.openclaw.ai/gateway/heartbeat
- https://docs.openclaw.ai/automation
- https://docs.openclaw.ai/concepts/session
- https://docs.openclaw.ai/gateway/configuration
