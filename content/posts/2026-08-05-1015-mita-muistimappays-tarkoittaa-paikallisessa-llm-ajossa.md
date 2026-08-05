---
title: "Mitä muistimäppäys tarkoittaa paikallisessa LLM-ajossa?"
date: "2026-08-05T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "mmap"
  - "ram"
  - "nvme"
---
## Tiivistelmä
Kun paikallinen LLM käynnistyy hitaasti, moni alkaa ensimmäiseksi katsoa nopeampaa NVMe-levyä. Se voi auttaa, mutta vain yhteen osaan ongelmaa. Käytännön sääntöni on tämä: **muistimäppäys nopeuttaa mallin latausta ja voi tehdä käynnistyksestä siistimmän, mutta se ei korvaa puuttuvaa RAMia eikä varsinkaan VRAMia**. Jos tämä ero jää epäselväksi, harrastaja päätyy helposti ostamaan väärän komponentin tai tulkitsemaan levynopeuden vääräksi pullonkaulaksi.

## Mitä muistimäppäys oikeastaan tekee

Muistimäppäys eli `mmap` tarkoittaa käytännössä sitä, että mallitiedostoa ei lueta kerralla tavallisena kopiona muistiin, vaan käyttöjärjestelmä saa hoitaa sivutuksen tiedoston ja muistin välillä. llama.cpp:n CLI-dokumentaatio kuvaa tämän hyvin suoraan: oletus `--load-mode` on `mmap`, ja jos muistimäppäys poistetaan käytöstä, lataus on hitaampi.

LM Studion dokumentaatio sanoo saman sovelluskehittäjän näkökulmasta: `tryMmap` voi parantaa alkuperäistä latausaikaa, koska malli mapataan levyltä suoraan muistiin ja käyttöjärjestelmä hoitaa sivutuksen. Tämä on hyvä uutinen silloin, kun haluat palvelun ylös nopeasti tai vaihdat malleja usein päivän aikana.

## Missä kohtaa moni tekee väärän johtopäätöksen

Väärä johtopäätös on tämä: "jos minulla on nopea NVMe, malli voi olla huoletta RAMin ulkopuolella". Ei voi, ainakaan ilman hintaa.

Sama LM Studion sivu varoittaa myös, että suorituskyky voi heiketä, jos malli on suurempi kuin käytettävissä oleva RAM ja järjestelmä joutuu tekemään jatkuvaa levyhakua. llama.cpp:n ohje puolestaan sanoo, että ilman muistissa pitämistä hitaampi lataus voi joskus vähentää pageout-tilanteita, mikä paljastaa olennaisen asian: tässä ei säädetä tokenointinopeuden ihmettä vaan muistipolitiikkaa.

Toisin sanottuna nopea levy auttaa silloin, kun sivuja pitää hakea tai malli pitää saada käyttöön nopeasti. Se ei muuta sitä, että varsinainen ajo kärsii heti, jos käyttöjärjestelmä alkaa hakea mallin osia levyltä jatkuvasti kesken työn.

## Miksi tämä näkyy erityisesti agentti- ja koodikäytössä

Yksittäisessä lyhyessä chatissa ongelma voi jäädä piiloon. Agentti-, RAG- ja koodityössä kuorma on toisenlainen:

- malli pidetään usein lämpimänä pitkään
- konteksti kasvaa kierros kierrokselta
- samalle koneelle kertyy muutakin muistinkäyttöä
- useampi pyyntö voi osua peräkkäin tai rinnakkain

Silloin tärkeä kysymys ei ole vain "kuinka nopeasti malli avautuu", vaan "pysyykö työjoukko oikeasti muistissa ilman että levy alkaa osallistua jatkuvasti". Jos vastaus on ei, nopeakaan SSD ei tee kokemuksesta sulavaa.

## Milloin käyttäisin muistimäppäystä hyvillä mielin

Pidän `mmap`-oletuksesta silloin, kun tavoite on:

- nopea mallin käynnistys
- yksi tai muutama usein vaihdettava malli
- riittävästi RAMia siihen, ettei järjestelmä joudu jatkuvaan levyhakemiseen
- työasema, jossa haluat käyttöjärjestelmän hoitavan sivutusta fiksusti

Tämä on järkevä oletus monelle harrastajalle, koska se laskee kitkaa arjessa. Malli nousee nopeammin, eikä kaikkea tarvitse ladata kömpelösti yhtenä blokkina.

## Milloin en luottaisi levyyn liikaa

Jos koneessa on jo valmiiksi niukasti RAMia, mallikoko on rajoilla tai samaan aikaan ajetaan muitakin palveluja, en rakentaisi suunnitelmaa sen varaan, että nopea NVMe "pelastaa" tilanteen. Silloin todennäköisempi oikea ratkaisu on jokin näistä:

- pienempi kvantisointi
- pienempi malli
- enemmän RAMia
- enemmän VRAMia tai parempi GPU-offload

Levy voi pehmentää käynnistystä, mutta se ei muuta muistibudjettia toiseksi.

## Käytännön sääntö kotilabraan

Jos mietin omaa paikallista LLM-konetta, käytän tätä yksinkertaista sääntöä:

1. käytä muistimäppäystä nopeaan käynnistykseen, jos RAM-budjetti on kunnossa
2. jos kone alkaa swapata tai tuntuu nykivältä kuorman aikana, älä syytä ensimmäisenä mallia vaan tarkista muistipaine
3. jos ongelma näkyy vasta varsinaisessa ajossa eikä käynnistyksessä, levypäivitys ei todennäköisesti ole tärkein korjaus
4. jos haluat sulavan jatkuvan käytön, osta kapasiteettia sinne missä pullonkaula oikeasti on: RAMiin tai VRAMiin

Tämä säästää rahaa, koska NVMe on helppo ostos mutta usein väärä ensimmäinen vastaus.

## Johtopäätös

Muistimäppäys on hyödyllinen työkalu paikallisessa LLM-ajossa, mutta sitä kannattaa ajatella käynnistys- ja muistinhallintaratkaisuna, ei suorituskyvyn taikatemppuna. llama.cpp:n nykyinen dokumentaatio pitää `mmap`-tilaa oletuksena juuri siksi, että se on käytännöllinen lataustapa. LM Studion dokumentaatio taas muistuttaa aivan oikein, että jos malli ylittää käytettävissä olevan RAMin, jatkuva levyliikenne voi heikentää suorituskykyä. Harrastajalle tärkein opetus on yksinkertainen: nopea SSD on hyvä apuri, mutta huono korvike puuttuvalle muistille.

## Lähteet

- https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md
- https://lmstudio.ai/docs/typescript/api-reference/llm-load-model-config
