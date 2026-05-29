---
title: "AI-rauta kotilabrassa: milloin konteksti on liian suuri omalle GPU:lle?"
date: "2026-04-09T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "GPU"
  - "Hardware"
  - "Homelab"
  - "Troubleshooting"
---
Moni paikallista LLM:ää ajava harrastaja ajattelee ensin mallin kokoa, mutta käytännössä myös konteksti syö muistia nopeasti. Siksi arkinen kysymys ei ole vain "mahtuuko tämä 14B-malli koneelleni", vaan myös "mahtuuko tämä malli vielä silloin, kun pyydän siltä 32k tai 64k kontekstia".

Lyhyt vastaus on tämä: konteksti on liian suuri omalle GPU:lle siinä vaiheessa, kun mallin ajo alkaa valua CPU:n puolelle tai vaste romahtaa niin paljon, ettei asetuksesta saa enää oikeaa hyötyä. Käytännössä tämä näkyy hitaana tokennopeutena, epävakaana käyttökokemuksena tai siinä, että joudut tinkimään liikaa joko mallin koosta tai kvantisoinnista vain pitkän kontekstin takia.

## Miksi konteksti syö niin paljon muistia?

Konteksti ei ole pelkkä "asetus", vaan se kasvattaa muistitarvetta koko ajon aikana. Kun syötät mallille pidemmän historian, muistissa pitää säilyttää enemmän tilaa aiemmille tokeneille. Siksi 8k voi tuntua kevyeltä, mutta 32k tai 64k nostaa muistipainetta nopeasti, vaikka itse malli ei vaihtuisikaan.

Ollaman dokumentaatio tekee tästä hyvän nyrkkisäännön näkyväksi. Se asettaa oletuskontekstin VRAM-määrän mukaan näin:

- alle 24 GiB VRAM: tyypillisesti 4k
- 24–48 GiB VRAM: tyypillisesti 32k
- vähintään 48 GiB VRAM: tyypillisesti 256k

Tämä ei tarkoita, että jokainen kone pystyisi näihin lukuihin kaikilla malleilla ilman kompromisseja. Se tarkoittaa lähinnä sitä, että muistibudjetti ratkaisee. Jos VRAM on jo valmiiksi tiukilla mallin painojen kanssa, pitkä konteksti on usein ensimmäinen asia, joka työntää ajon epämukavalle alueelle.

## Mistä tietää, että konteksti meni liian pitkäksi?

Yleensä oireet näkyvät kolmella tavalla.

### 1. Malli ei enää pysy kunnolla GPU:lla

Ollama suosittelee tarkistamaan `ollama ps` -näkymästä, pysyykö ajo aidosti GPU:lla. Jos `PROCESSOR` ei enää näytä täyttä GPU-käyttöä, tai osa ajosta valuu CPU:lle, pitkä konteksti voi olla yksi syy. Tämä on tärkeä käytännön havainto, koska pelkkä "toimii" ei vielä tarkoita, että asetukset olisivat järkevät.

### 2. Tokennopeus romahtaa

llama.cpp:n suorituskykyohjeissa painotetaan, että ajon hitaus ei aina johdu vain GPU:sta, vaan myös siitä, miten säikeet, offload ja muistibudjetti osuvat yhteen. Kun konteksti kasvaa liian suureksi, nopeus voi pudota selvästi jo ennen kuin ajo varsinaisesti kaatuu. Tällöin kone on teknisesti pystyvä, mutta käytännössä epämukava käyttää.

### 3. Joudut tekemään huonoja kompromisseja

Jos 64k konteksti onnistuu vain niin, että vaihdat paljon pienempään malliin, pudotat kvantisoinnin aggressiivisesti tai hyväksyt hitaan CPU-offloadin, lopputulos ei aina ole parempi. Monessa kotilabra-ajossa 8k, 16k tai 32k hyvin toimivaa kontekstia on hyödyllisempi kuin "näennäinen" 64k, joka tekee koko työnkulusta raskaan.

## Käytännön nyrkkisäännöt harrastajalle

Jos käytössäsi on:

- **12–16 GiB VRAM**, pidä odotukset realistisina. Pitkä konteksti syö nopeasti tilan, etenkin jos malli ei ole pieni.
- **24 GiB VRAM**, 32k voi olla jo järkevä tavoite useissa käytännön ajoissa, mutta ei automaattisesti kaikilla malleilla.
- **48 GiB VRAM tai enemmän**, pitkä konteksti muuttuu aidosti käyttökelpoisemmaksi, mutta silti mallin koko ja muut asetukset ratkaisevat paljon.

Hyvä tapa ajatella asiaa on tämä: ensin halutaan malli, joka pysyy mukavasti GPU:lla normaalissa käytössä. Sen jälkeen kontekstia nostetaan vain niin pitkälle kuin hyöty oikeasti kasvaa. Jos pidempi konteksti ei tuo parempia vastauksia vaan vain hitaamman koneen, asetusta ei kannata maksimoida vain siksi, että se on mahdollista.

## Milloin kannattaa valita pienempi konteksti?

Pienempi konteksti on usein parempi valinta, kun:

- käytät mallia lyhyisiin kysymys-vastaus- tai koodiavustustehtäviin
- voit tiivistää aiemman keskustelun etkä tarvitse raakaa historiaa kokonaan mukaan
- teet RAG-tyylisiä hakuja, joissa tärkeä tieto tuodaan mukaan valikoidusti
- arvostat enemmän nopeaa vasteaikaa kuin maksimaalista historian pituutta

Tämä on monelle tärkeä oivallus. Pitkä konteksti ei ole automaattisesti "enemmän laatua". Joskus se on vain enemmän muistikuormaa.

## Yksinkertainen päätössääntö

Voit käyttää tällaista käytännön sääntöä:

1. Aja ensin malli sillä kontekstilla, jota oikeasti tarvitset useimmin.
2. Tarkista pysyykö ajo GPU:lla ja onko nopeus vielä miellyttävä.
3. Nosta kontekstia askel kerrallaan.
4. Lopeta kasvatus siinä kohtaa, kun vaste hidastuu selvästi tai GPU-offload ei enää pysy siistinä.

Silloin konteksti on omalle koneellesi "riittävän suuri" ilman että siitä tulee taakka.

## Mitä tästä kannattaa muistaa?

Paikallisessa LLM-koneessa kontekstin yläraja ei ole vain ohjelmiston sallima numero. Todellinen raja on se piste, jossa VRAM, mallin koko ja käytännön nopeus pysyvät vielä tasapainossa.

Harrastajalle paras konteksti ei siis yleensä ole maksimi, vaan se, joka antaa tarpeeksi muistia tehtävään ilman että koko kone muuttuu tahmeaksi.

## Lähteet

- https://docs.ollama.com/context-length
- https://docs.ollama.com/gpu
- https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md
