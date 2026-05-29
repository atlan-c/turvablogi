---
title: "AI-rauta kotilabrassa: kannattaako 128 gigatavua RAMia paikalliseen LLM-koneeseen?"
date: "2026-04-07T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "GPU"
  - "Hardware"
  - "Homelab"
  - "Automation"
---
128 gigatavua RAMia kuulostaa helposti siltä, että kyse on vain ylibudjetoidusta harrastekoneesta. Käytännössä näin ei aina ole. Monelle paikallisia malleja ajavalle 64 gigatavua riittää pitkälle, mutta tietyissä työkuormissa 128 gigatavua ei ole enää ylellisyyttä vaan tapa välttää jatkuva kompromissikierre.

Tärkeä kysymys ei siis ole vain "mahtuuko malli käyntiin", vaan mitä muuta koneen pitää tehdä samaan aikaan. Jos ajat osan mallista CPU:lla, pidät suuria dokumenttiaineistoja muistissa, käytät pitkää kontekstia tai ajat useampaa palvelua rinnakkain, järjestelmämuistin merkitys kasvaa nopeasti.

## Milloin 64 gigatavua riittää edelleen hyvin?

64 gigatavua on edelleen hyvä oletustaso harrastajalle, joka:

- ajaa enimmäkseen 7B–14B-luokan malleja
- nojaa GPU:n VRAMiin niin paljon kuin mahdollista
- käyttää melko tavallisia konteksti-ikkunoita
- ei pidä useita raskaita palveluja auki yhtä aikaa

Jos malli mahtuu lähes kokonaan GPU:lle eikä sama kone tee paljon muuta, pullonkaula on usein ennemmin VRAM, SSD tai muistikanava kuin se, onko RAMia 64 vai 128 gigatavua.

## Missä vaiheessa 128 gigatavua alkaa oikeasti auttaa?

128 gigatavua alkaa olla järkevä hankinta etenkin neljässä tilanteessa.

### 1. Osa mallista valuu CPU-muistiin

Kun VRAM ei riitä, osa painoista tai työdatasta päätyy järjestelmämuistiin. Tämä onnistuu, mutta nopeus yleensä kärsii. Isompi RAM ei tee CPU-offloadista nopeaa, mutta se estää tilanteen, jossa ajo kaatuu tai järjestelmä alkaa swapata levyä vasten.

Tämä on tavallinen syy siihen, että 128 gigatavua tuntuu hyödylliseltä erityisesti 24 Gt VRAM -luokan koneissa. GPU on jo tarpeeksi hyvä houkuttelemaan isompien mallien käyttöön, mutta ei silti riitä kaikkeen yksin.

### 2. Konteksti kasvaa paljon

Sekä Ollama että llama.cpp korostavat käytännössä samaa asiaa: suurempi konteksti kasvattaa muistitarvetta. Pitkä konteksti ei syö vain vähän lisää muistia, vaan voi muuttaa koko koneen käyttäytymisen. Kun käyttäjä nostaa kontekstin 4k:sta 32k:hon tai vielä ylemmäs, muistivaatimus nousee helposti niin paljon, että aiemmin "ihan riittävä" kone alkaa tuntua epävakaalta.

Tämä näkyy erityisesti silloin, kun käytössä on agentti- tai koodaustyylinen kuorma, jossa paljon historiallista kontekstia pidetään mukana.

### 3. Koneella ajetaan muutakin kuin itse malli

Paikallinen LLM-kone on harvoin enää pelkkä yksi prosessi. Samalla raudalla voi pyöriä esimerkiksi:

- Ollama tai llama.cpp-palvelin
- vektorikanta tai embedding-palvelu
- dokumenttihakua tai RAG-putki
- selain, editori, terminaalit ja testityökalut
- jokin automaatio, joka prosessoi aineistoa taustalla

Tällöin 64 gigatavua voi riittää juuri ja juuri, mutta 128 gigatavua tekee koneesta rauhallisemman. Ero tuntuu usein vähemmän yksittäisessä token-nopeudessa ja enemmän siinä, ettei koko ympäristö hajoa pienen lisäkuorman alla.

### 4. Haluat vähentää jatkuvaa mikrosäätöä

Tämä on käytännön argumentti, jota speksikeskusteluissa vähätellään. Jos jokainen uusi malli, kontekstitesti tai aineisto vaatii prosessien sulkemista, mallin vaihtoa pienempään kvantisointiin tai jatkuvaa muistinkäytön tarkkailua, kone ei enää tunnu joustavalta työkalulta.

128 gigatavua ei ole vain suorituskykyostos. Se voi olla myös käyttömukavuusostos. Jos kone on aktiivinen työympäristö eikä pelkkä viikonloppuprojekti, tällä on aidosti arvoa.

## Milloin 128 gigatavua on huono ostos?

Se on huono ostos silloin, kun todellinen ongelma on muualla.

Älä osta 128 gigatavua ensimmäisenä päivityksenä, jos:

- käytössä on vain 8–12 Gt VRAM ja GPU on selvästi suurin rajoite
- kone on edelleen yksikanavaisessa muistissa tai muuten epätasapainossa
- SSD on niin hidas tai täynnä, että aineistojen käsittely tökkii jo siinä vaiheessa
- ajat pieniä malleja lyhyellä kontekstilla etkä oikeasti käytä muistia loppuun

Moni harrastaja saa enemmän hyötyä ensin paremmasta GPU:sta, muistikanavien kuntoon laittamisesta tai siistimmästä mallivalinnasta kuin RAMin tuplaamisesta.

## Miten päätös kannattaa tehdä käytännössä?

Hyvä nyrkkisääntö on tämä:

- **Pysy 64 gigatavussa**, jos käytät pääosin keskikokoisia malleja, tavallista kontekstia ja yhtä pääkuormaa kerrallaan.
- **Siirry 128 gigatavuun**, jos ajat usein pitkiä konteksteja, CPU-offloadia, useita palveluja rinnakkain tai haluat jättää koneeseen selvästi enemmän pelivaraa.

Kannattaa myös katsoa omaa nykyistä käyttöä muutaman päivän ajalta. Jos muisti käy toistuvasti korkealla ja kone alkaa vaihtaa levyyn juuri silloin, kun yrität tehdä jotain vähän raskaampaa, lisämuisti on luultavasti perusteltu. Jos taas käyttö pysyy selvästi väljemmällä alueella, 128 gigatavua on todennäköisesti ennenaikainen päivitys.

## Oma johtopäätös

128 gigatavua RAMia kannattaa paikalliseen LLM-koneeseen silloin, kun kone ei ole enää vain "malli käyntiin" -laite vaan oikea työasema useille samanaikaisille AI-kuormille. Se ei yleensä ole ensimmäinen päivitys, jonka harrastajan kannattaa tehdä, mutta tietyssä vaiheessa se on järkevämpi kuin jatkuva taistelu VRAMin, kontekstin ja taustapalvelujen kanssa.

Jos oma käyttö on vielä melko suoraviivaista, 64 gigatavua on edelleen useimmiten parempi hinta-hyötysuhde. Jos taas huomaat jo nyt rakentavasi järjestelmää kompromissien ympärille, 128 gigatavua voi olla juuri se päivitys, joka tekee koko koneesta huomattavasti käyttökelpoisemman.

## Lähteet

- https://docs.ollama.com/context-length
- https://docs.ollama.com/faq
- https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md
