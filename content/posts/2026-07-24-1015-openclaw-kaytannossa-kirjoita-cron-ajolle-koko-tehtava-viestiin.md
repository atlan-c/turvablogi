---
title: "OpenClaw käytännössä: kirjoita cron-ajolle koko tehtävä viestiin"
date: "2026-07-24T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Cron"
  - "Sessions"
  - "Automation"
---
Yksi yleisimmistä OpenClaw-cronin virheistä ei ole tekninen vaan kielellinen: ajastetulle ajolle kirjoitetaan liian lyhyt viesti ja oletetaan, että agentti kyllä muistaa loput. Käytännössä tämä näkyy näin: cronille annetaan ohje kuten "tarkista sähköpostit ja kerro jos jotain tärkeää" tai "tee aamubriiffi", mutta viestissä ei sanota mistä kontekstista tieto pitäisi hakea, millä session-tyylillä ajo toimii tai millä kielellä vastauksen pitää tulla. Minun peukalosääntöni on tämä: **jos cron-ajon onnistuminen riippuu taustaoletuksesta, kirjoita se näkyviin samaan viestiin.**

OpenClawin oma dokumentaatio tukee tätä suoraan. Cron-ajot eivät oletusarvoisesti peri kaikkea ympärillä olevaa keskustelukontekstia, vaan session tyyppi ratkaisee paljon. Main-session cronit ovat itseään selittäviä system event -muistutuksia, kun taas eristetty ajo käynnistyy uutena sessiona. Silloin "kyllä se tietää mitä tarkoitin" on huono automaatiostrategia, etenkin jos tehtävä pyörii ilman ihmistä paikalla.

## Missä kohdassa oletus alkaa hajota

Kolme käytännön kompastuskiveä toistuvat yllättävän usein:

- cron-viesti olettaa, että `HEARTBEAT.md` tai joku aiempi keskustelu luetaan automaattisesti
- eristetylle ajolle annetaan liian lyhyt ohje, vaikka se alkaa tuoreesta sessionista
- kieltä, formaattia tai pysäytysehtoja ei kirjoiteta viestiin lainkaan

OpenClawin cron-dokumentaatio sanoo tämän aika suoraan: main-session cron event ei sisällä heartbeat-promptia tai heartbeat-scratchia itsestään, vaan ne pitää mainita erikseen jos ajo tarvitsee niitä. Samassa dokumentaatiossa myös todetaan, että cronit eivät päättele vastauskieltä kanavasta, lokaaleista tai vanhoista viesteistä. Tämä on hyvä asia, koska se tekee automaatiosta ennustettavamman, mutta vain jos kirjoitat pyynnön täsmällisesti.

## Valitse ensin session tyyli, vasta sitten prompti

Minusta paras tapa kirjoittaa cron on aloittaa yhdestä kysymyksestä: **pitääkö tämän ajon rakentaa vanhan keskustelun päälle vai ei?**

Jos vastaus on ei, käytä eristettyä ajoa ja kirjoita viestiin koko tehtävä:

- mitä tarkistetaan
- mitä tiedostoja tai muistia saa käyttää
- millä kielellä raportoidaan
- milloin pitää lopettaa eikä improvisoida

Jos taas vastaus on kyllä, `main`, `current` tai nimetty `session:<id>` voi olla oikea malli. Silloinkin itse viestin pitää olla itsenäinen muistutus, ei telepaattinen vihje. Dokumentaatio korostaa, että main-session cron käyttää omaa cron-laneaan eikä pidennä kohdesession daily- tai idle-tuoreutta. Toisin sanoen kyse ei ole samasta asiasta kuin tavallinen ihmisen lähettämä uusi viesti samaan keskusteluun.

## Hyvä cron-viesti näyttää usein pidemmältä kuin haluaisit

Moni yrittää säästää tokeneita lyhentämällä ajastettua pyyntöä liikaa. Usein säästö menee väärään paikkaan. Halpa cron on sellainen, joka onnistuu yhdellä ajolla ilman tulkintakierrosta.

Hyvä käytännön runko näyttää tältä:

1. kuvaa tavoite yhdellä lauseella
2. nimeä lähteet tai tiedostot, joita ajo saa käyttää
3. kerro tarkka ulostulo, esimerkiksi "vastaa suomeksi kolmella bulletilla"
4. lisää pysäytysehdot, esimerkiksi "jos credsit puuttuvat tai tarkistus epäonnistuu, lopeta ja raportoi"
5. sano erikseen, jos heartbeat- tai memory-konteksti pitää lukea

Tämä on erityisen tärkeää unattended-ajossa. OpenClawin automaatiodokumentaatio muistuttaa, että eristetty cron toimii ilman paikalla olevaa ihmistä: lopputuloksen pitää olla valmis deliverable, ei lisäkysymys tai puolikas suunnitelma. Siksi epäselvä prompti ei ole vain pieni laatuvirhe, vaan se kasvattaa suoraan riskiä, että ajo päätyy palauttamaan väärän muotoisen vastauksen tai turhan "tarvitsen lisätietoa" -kierroksen.

## Milloin `--light-context` auttaa

Cron-CLI:n dokumentaatio nostaa esiin myös `--light-context`-vaihtoehdon eristetyille agenttiajolle. Se on minusta hyvä oletus silloin, kun haluat nimenomaan rajata bootstrap-kontekstia etkä vahingossa ruokkia mallille liikaa taustaa. Kevyt konteksti ei pelasta huonoa tehtävänantoa, mutta se tekee yhden asian näkyväksi: jos ajo toimii vain silloin kun taustalle ladataan paljon workspace-ohjeita, ongelma voi olla promptissa eikä mallissa.

Tämä on myös hyvä diagnoosityökalu. Jos sama cron alkaa hajota `--light-context`-tilassa, kysy ensin:

- puuttuuko viestistä lähdepolku tai tiedostonimi
- oletanko aiemman keskustelun tietoa ilman että session tyyli tukee sitä
- jätinkö vastauskielen tai formaatin sanomatta

Yllättävän usein korjaus löytyy jo näistä kolmesta.

## Oma sääntöni: tee cron-viestistä siirrettävä

Pidän parhaana testinä sitä, voisiko saman cron-viestin näyttää toiselle ylläpitäjälle ilman lisäselitystä. Jos toinen ihminen ei ymmärtäisi siitä tehtävää, myöskään agentin ei pitäisi joutua arvaamaan sitä. Hyvä ajo on siirrettävä: sen viesti kertoo mitä tehdään, mistä tieto otetaan, mitä ei saa tehdä ja milloin työn kuuluu pysähtyä.

Sama ajatus tekee automaatioista helpompia huoltaa myöhemmin. Kun viesti on itsenäinen, cronin voi ajaa käsin, siirtää toiseen sessiotyyliin tai korjata ilman että koko logiikka riippuu hiljaisesta taustatiedosta.

## Yhteenveto

OpenClaw-cron ei tarvitse runollista promptia, mutta se tarvitsee täydellisen tehtävänannon. Kirjoita viestiin tavoite, lähteet, kieli, formaatti ja pysäytysehdot. Mainitse heartbeat- tai muu erityiskonteksti suoraan. Kun cron ei joudu arvaamaan mitä tarkoitit, se käyttää vähemmän kierroksia, epäonnistuu rehellisemmin ja tekee huomattavasti useammin juuri sen työn jonka oikeasti pyysit.

## Lähteet

- https://docs.openclaw.ai/automation/cron-jobs
- https://docs.openclaw.ai/cli/cron
- https://docs.openclaw.ai/concepts/session
