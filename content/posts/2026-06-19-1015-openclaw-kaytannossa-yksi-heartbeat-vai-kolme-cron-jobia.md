---
title: "OpenClaw käytännössä: yksi heartbeat vai kolme cron-jobia?"
date: "2026-06-19T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Heartbeat"
  - "Cron"
  - "Automation"
---
Sama ansa näkyy nopeasti, kun OpenClawilla alkaa automatisoida omaa arkea: teet yhden cron-jobin sähköpostille, toisen kalenterille, kolmannen säälle ja neljännen "yleiselle tilannekuvalle", vaikka oikea tarve olisi usein vain yksi kohtuullisen fiksu heartbeat. **Oma nyrkkisääntöni on tämä: jos tarkistukset ovat pehmeitä, toistuvia ja hyötyvät samasta käyttäjäkontekstista, aloita yhdellä heartbeatilla. Jos taas ajo vaatii tarkan kellonajan, eristetyn session tai oman toimituspolun, käytä cronia.**

Tämä jako ei ole vain tyylikysymys. Se vaikuttaa siihen, kuinka paljon taustakohinaa järjestelmään syntyy, missä kontekstissa agentti ajattelee ja kuinka paljon sinun pitää myöhemmin debugata "miksi tämä ajoi juuri nyt".

## Miksi liian moni cron-jobi on usein huonompi alku

OpenClawin automaatiodokumentaatio sanoo tämän melko suoraan: heartbeat on tarkoitettu esimerkiksi inboxin, kalenterin ja notifikaatioiden kaltaisille tarkistuksille, koska se voi **batchata useita tarkistuksia samaan agenttivuoroon täydellä pääsession kontekstilla**. Cron taas on tarkoitettu tarkkaan ajoitukseen ja eristettyyn suoritukseen.

Käytännössä tämä tarkoittaa, että jos rakennat kolme erillistä cron-jobia vain siksi, että haluat tietää:

- tuliko tärkeä viesti
- onko seuraava tapaaminen lähellä
- pitäisikö ihmistä muistuttaa sateesta

...olet usein hajottamassa yhtä luonnollista "tilannekuvavuoroa" kolmeksi erilliseksi ajoksi ilman, että saat vastineeksi mitään erityisen arvokasta.

Se näkyy yleensä neljällä tavalla:

- taustatehtäviä kertyy enemmän kuin tarvitset
- sama tieto pitää rakentaa moneen erilliseen ajoon
- näkyvät ilmoitukset pirstoutuvat
- myöhempi triage on raskaampaa kuin yhden heartbeat-polun seuraaminen

## Milloin yksi heartbeat on selvästi parempi

Automation-sivu antaa jo hyvän vihjeen: "check inbox every 30 min" ja "monitor calendar" ovat nimenomaan heartbeat-käyttöjä. Heartbeat on siis tehty tilanteisiin, joissa tarkistus saa olla **suunnilleen ajallaan**, mutta hyötyy siitä, että agentti näkee saman pääsession taustan, aiemmat päätökset ja muut saman kierroksen tarkistukset.

Valitsisin yhden heartbeatin mieluummin kuin monta cron-jobia, jos nämä pitävät paikkansa:

- tarkistus saa elää noin 30-60 minuutin rytmissä eikä vaadi minuuttitarkkaa ajoa
- useat tarkistukset liittyvät samaan arjen tilanteeseen
- haluat mieluummin yhden koostetun havainnon kuin monta pientä pingausta
- sama työ hyötyy pääsession muistista ja nykyisestä keskustelukontekstista

Tämä on hyvä malli esimerkiksi henkilökohtaiselle agentille, joka seuraa muutamaa "ehkä kannattaa sanoa tästä" -asiaa päivän mittaan. Yksi heartbeat voi tarkistaa sähköpostin, kalenterin ja pari muuta signaalia yhdellä kierroksella, ja jos mitään ei tarvitse nostaa esiin, ajon voi kuitata hiljaa.

## Tärkeä ero: heartbeat ei tee taustatehtäväkirjanpitoa samalla tavalla

Heartbeat-dokumentaatio sanoo suoraan, että heartbeat on **scheduled main-session turn**, eikä se luo background task -rivejä. Taustatehtävädokumentaatio täydentää tämän: taskit ovat kirjanpitoa irrotetulle työlle, eivät itse schedulereita. Cron-jobit luovat taskeja, heartbeat ei.

Tämä on käytännössä iso juttu. Jos rakennat jokaisesta pienestä tarkistuksesta oman cronin, saat samalla enemmän task-historiaa, enemmän run-tietoa ja enemmän erillisiä ajopolkuja tutkittavaksi. Se on hyvä asia silloin, kun oikeasti haluat audit-jäljen tai irrotetun työn tilaseurannan. Mutta jos tavoitteena on vain "katso pari asiaa ja kerro vain jos jotain oikeasti tapahtui", ylimääräinen task- ja run-kerros voi olla turhaa kitkaa.

Lyhyt sääntö:

- heartbeat silloin, kun haluat tietoisuutta
- cron silloin, kun haluat ajoitetun työn

## Milloin cron on silti oikea ratkaisu

Cron voittaa heti, kun ajoitus tai eristys on itse tehtävän ydin. OpenClawin automation-opas sanoo tämän eksplisiittisesti: cron on oikea valinta, kun tarvitset tarkan ajan tai eristetyn suorituksen.

Valitsisin cronin enkä heartbeatia, jos jokin näistä osuu:

- raportin pitää lähteä juuri kello 9.00
- muistutuksen pitää osua tiettyyn kellonaikaan
- työn pitää käyttää eri mallia tai eri toimituspolkua
- haluat ajon omaan, eristettyyn run-sessioniin
- haluat task-historian, run-listauksen ja helpomman auditoinnin juuri tälle yhdelle työlle

Tämä ero näkyy myös sessionhallinnassa. OpenClawin session management -dokumentaatio kertoo, että kun cron luo uuden eristetyn `cron:<jobId>`-session, se sanitizoi vanhan session ja pudottaa pois ambienttia toimitus- ja runtime-kontekstia. Se on erinomainen ominaisuus silloin, kun nimenomaan haluat, ettei uusi ajo peri vahingossa vanhaa reititystä tai muuta tilaa. Mutta samalla se kertoo, miksi cron ei ole aina paras ratkaisu "kevyisiin arkirutiineihin": cronin vahvuus on eristys, heartbeatin vahvuus on jatkuvuus.

## Hyvä käytännön testi ennen kuin lisäät uuden cronin

Kysyn itseltäni yleensä nämä kolme kysymystä:

1. Haittaako, jos tarkistus tapahtuu noin puolen tunnin ikkunassa eikä sekuntitarkasti?
2. Onko tämä vain yksi osa laajempaa tilannekuvaa, jonka agentti voisi arvioida samalla kierroksella?
3. Tarvitsenko tästä aidosti oman run-historyn ja task-kirjanpidon?

Jos vastaukset ovat:

- kyllä
- kyllä
- en

...teen sen heartbeatilla.

Jos taas vastaukset ovat:

- ei
- ei
- kyllä

...teen cronin.

## Yksi heartbeat vähentää myös ilmoitusroskaa

OpenClawin heartbeat-malli on minusta aliarvostettu juuri siksi, että se sallii hiljaisuuden luonnollisesti. Dokumentaatiossa näkyy useampi tapa tehdä heartbeat "ei mitään näkyvää" -muodossa, jos mikään ei vaadi huomiota. Tämä sopii hyvin henkilökohtaiseen agenttiin, jossa et halua joka tarkistuksesta omaa "kaikki ok" -viestiä.

Jos sama logiikka pilkotaan moneen cron-jobiin, käy helposti näin:

- yksi ajo tarkistaa sähköpostin
- toinen ajo tarkistaa kalenterin
- kolmas ajo tarkistaa muun tilan

Silloin jokainen pitää erikseen miettiä: mihin tulos toimitetaan, pitääkö siitä syntyä ilmoitus, entä jos kaksi ajoa löytää jotain samaan aikaan? Yksi heartbeat ratkoo tämän siistimmin, koska se voi nähdä useamman signaalin yhdessä ja päättää, onko tästä oikeasti syytä pingata ihmistä juuri nyt.

## Missä moni menee pieleen

Yleisin virhe ei ole se, että cronia käytetään liikaa teknisesti, vaan se, että cronia käytetään väärän muotoiseen ongelmaan. "Haluan seurata tilannetta päivän mittaan" ei vielä tarkoita "tarvitsen kolme scheduleria". Usein se tarkoittaa vain, että agentilla pitäisi olla pieni, hyvin rajattu `HEARTBEAT.md`, jossa on 2-4 tarkistusta ja selkeä sääntö siitä, milloin ollaan hiljaa.

Toinen yleinen virhe on luulla, että task-historia itsessään on hyöty. Vain osa automaatioista tarvitsee sen. Jos työ on enemmän jatkuvaa huomiokykyä kuin erillinen jobi, heartbeat on usein kevyempi ja lähempänä sitä, miten henkilökohtainen agentti luonnostaan toimii.

## Oma suositukseni

Jos mietit juuri nyt, pitäisikö tehdä kolme pientä cron-jobia vai yksi heartbeat, valitse oletuksena yksi heartbeat silloin, kun:

- työ on pehmeää seurantaa
- ajoituksen ei tarvitse olla tarkka
- haluat hyödyntää pääsession kontekstia
- haluat minimoida ilmoitusmelun

Tee sen sijaan cron, kun tarvitset tarkan ajan, oman eristetyn ajon tai aidon taustatehtävän audit-jäljen.

Yksinkertaisin muistilappu on tämä: **heartbeat kokoaa tilanteen, cron suorittaa yksittäisen tehtävän**. Kun tämän eron pitää kirkkaana, automaatiorakenne pysyy kevyempänä ja myöhempi ylläpito helpottuu.

## Lähteet

- https://docs.openclaw.ai/automation
- https://docs.openclaw.ai/gateway/heartbeat
- https://docs.openclaw.ai/automation/tasks
- https://docs.openclaw.ai/reference/session-management-compaction
