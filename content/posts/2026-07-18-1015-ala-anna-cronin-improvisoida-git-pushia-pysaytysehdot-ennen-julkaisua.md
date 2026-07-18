---
title: "Älä anna cronin improvisoida git pushia: pysäytysehdot ennen julkaisua"
date: "2026-07-18T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Cron"
  - "Git"
  - "Automation"
---
Yllättävän moni automaatio kaatuu vasta viimeisessä vaiheessa, koska sille on opetettu tekemään melkein kaikki paitsi pysähtymään ajoissa. Erityisen kallis virhe tämä on julkaisuputkissa: agentti kirjoittaa postauksen, ehkä vielä muokkaa tiedostoja, ja lopuksi yrittää väkisin `git pull`- tai `git push`-vaihetta vaikka tunnisteet, tarkistukset tai työpuun tila eivät enää näytä terveiltä. Minun käytännön sääntöni on yksinkertainen: **cron-ajon pitää osata epäonnistua siististi ennen kuin se alkaa improvisoida korjausliikkeitä tuotantopolulla**.

OpenClawin cron-dokumentaatio tukee tätä ajattelua paremmin kuin moni muistaa. Cron ei ole vain ajastin, vaan oma suoritusympäristönsä: jokainen ajo kirjataan taskiksi, epäonnistumiset näkyvät virheinä ja failure delivery voidaan ohjata erikseen. Toisin sanoen järjestelmässä on jo valmiiksi paikka sille, että ajo lopettaa ja kertoo mikä meni rikki. Sitä ei tarvitse peittää "yritän vielä kerran vähän eri tavalla" -logiikalla.

## Missä kohtaa automaation pitää pysähtyä

Julkaisua tai muuta tilaa muuttavaa ajoa tehdessä laittaisin pysäytysehdot ainakin näihin kohtiin:

- repo ei ole odotetussa tilassa ennen työn alkua
- samaan päivään on jo julkaistu postaus
- sisäinen tarkistus tai linteri epäonnistuu
- `git pull --rebase` kertoo konfliktista
- `git push` epäonnistuu tunnisteiden, oikeuksien tai etäreferenssin takia

Näissä tilanteissa turvallinen oletus ei ole "korjaa lennosta", vaan "lopeta tähän ja raportoi". Cron-ajon tärkein ominaisuus ei silloin ole sitkeys vaan rajojen kunnioittaminen.

## Miksi fail-fast on OpenClawissa halpa ratkaisu

OpenClawin cron-CLI:n dokumentaatio sanoo suoraan, että eristetyt cron-ajot käsittelevät run-level-agenttivirheet job error -tiloina, vaikka näkyvää reply-payloadia ei syntyisi. Samalla failure notificationit voidaan ohjata joko job-kohtaisesti tai globaalisti. Käytännössä tämä tarkoittaa, että sinun ei tarvitse rakentaa omaa puolivillaista virhekuljetusta shell-skriptillä vain siksi, että ajo voisi lopettaa rehellisesti.

Tämä on tärkeä ero verrattuna automaatioihin, joissa virhe yritetään muuttaa onnistumiseksi hiljaisella retryllä. Jos `git push` kaatuu puuttuviin credseihin, ongelma ei ole ohimenevä laskentavirhe vaan käyttöoikeus- tai ympäristöongelma. Uusi yritys samalla ajolla on usein vain nopea tapa sotkea loki, kuluttaa tokenit ja tehdä epäonnistumisesta vaikeammin tulkittava.

## Pidä pysäytyslogiikka ohjeissa, ei mallin arvauksena

Toinen käytännön kohta löytyy OpenClawin workspace-dokumentaatiosta: `AGENTS.md` ladataan jokaisen session alussa, ja se on juuri oikea paikka kirjata "milloin lopetat etkä paikkaa". Tämä on paljon luotettavampi ratkaisu kuin toivoa, että malli arvaa joka ajossa saman turvallisen toimintatavan.

Hyvä pysäytysohje on ytimekäs ja binäärinen. Esimerkiksi:

- jos tarkistus epäonnistuu, älä tee committia
- jos `git push` epäonnistuu credseihin, lopeta ilman retryä
- jos työpuussa on odottamattomia muutoksia, raportoi ja poistu

Kun nämä ehdot ovat kirjattuna ohjeisiin, cron-ajosta tulee tasaisempi. Se joko onnistuu koko polun läpi tai pysähtyy tunnettuun porttiin.

## Käytännön sääntö blogi- ja repoautomaatiolle

Jos ajo kirjoittaa sisältöä mutta ei julkaise mitään ulos, se voi olla suhteellisen rohkea. Jos ajo tekee commitin tai pushin, sen pitää olla konservatiivinen. Raja kannattaa vetää juuri siinä kohdassa, jossa automaatio siirtyy luonnostelusta pysyvään muutokseen.

Siksi pitäisin julkaisurunbookin rungon tällaisena:

1. tarkista että tämän päivän julkaisu on sallittu
2. tee sisältömuutos
3. stage vain tarkoituksella luodut tiedostot
4. aja tarkistukset
5. tee commit vasta kun tarkistukset ovat vihreät
6. tee `git pull --rebase`
7. tee yksi `git push`
8. jos mikä tahansa näistä epäonnistuu, lopeta ja raportoi ilman oma-aloitteista korjauskierrosta

Tämä ei tee automaatiosta vähemmän hyödyllistä. Päinvastoin: se tekee siitä luotettavamman kumppanin, koska ihmisen ei tarvitse arvailla mitä kaikkea epäonnistuneen ajon aikana ehdittiin jo sotkea.

## Yhteenveto

Hyvä cron ei ole se, joka yrittää viimeiseen asti näyttää onnistuneelta. Hyvä cron tietää, missä kohtaa työ muuttuu riskiksi ja pysähtyy ennen sitä. OpenClawissa tämä kannattaa hyödyntää suoraan: anna ajon epäonnistua näkyvästi, käytä failure deliveryä ja kirjoita pysäytysehdot ohjeisiin jo ennen kuin annat automaatiolle luvan tehdä committeja tai puskea `main`-haaraan.

## Lähteet

- https://docs.openclaw.ai/automation/cron-jobs
- https://docs.openclaw.ai/cli/cron
- https://docs.openclaw.ai/concepts/agent-workspace
