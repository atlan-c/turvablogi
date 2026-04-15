---
title: "AI-rauta kotilabrassa: milloin 32k konteksti on turha luksus ja milloin se on oikeasti hyödyllinen?"
date: 2026-04-15T10:15:00+03:00
draft: false
topic_family: llm-hardware
---

Pitkä konteksti kuulostaa paperilla melkein aina hyvältä idealta. Jos 4k on vähän, eikö 32k ole automaattisesti paljon parempi? Käytännössä vastaus on usein yllättävän arkinen: joskus kyllä, mutta monessa kotilabrassa 32k on enemmän muistia syövä mukavuuslisä kuin todellinen hyöty.

Siksi oikea kysymys ei ole "voinko ajaa 32k kontekstia", vaan "ratkaiseeko 32k oikeasti ongelman, jota minulla on".

Lyhyt vastaus: 32k on hyödyllinen silloin, kun tehtävä oikeasti tarvitsee pitkää aktiivista muistia. Se on turha luksus silloin, kun työnkulku olisi yhtä hyvä tai parempi pienemmällä kontekstilla, tiivistyksellä tai RAG-haulla.

## Miksi 32k houkuttelee niin paljon?

Pitkä konteksti on helppo ymmärtää väärin "yleiseksi laatubufferiksi". Ajatus menee helposti näin: jos malli saa nähdä enemmän tekstiä, vastauksen täytyy olla parempi.

Todellisuudessa Ollaman dokumentaatio muistuttaa, että pidempi konteksti kasvattaa muistitarvetta suoraan. Lisäksi dokumentaatio käyttää VRAM-pohjaista oletusta, jossa 24–48 GiB luokan koneille asetetaan oletuksena 32k konteksti. Tämä kertoo enemmän siitä, mikä on usein teknisesti mahdollinen, kuin siitä, mikä on joka tehtävässä järkevää.

Se, että jokin asetus on mahdollinen, ei vielä tee siitä hyödyllistä joka päivä.

## Milloin 32k on oikeasti hyödyllinen?

32k on hyödyllinen silloin, kun tehtävässä on aidosti paljon aktiivista, toisiinsa liittyvää tekstiä, jota ei voi helposti tiivistää pois.

Hyviä esimerkkejä:

- pitkä tekninen keskustelu, jossa aiempi konteksti todella vaikuttaa seuraaviin vastauksiin
- laaja koodipätkä tai useita tiedostoja, joita vertaillaan samassa ajossa
- dokumenttityö, jossa halutaan pitää useita pitkiä osia yhtä aikaa mukana
- agenttimainen työnkulku, jossa mallin on muistettava paljon juuri nyt relevanttia materiaalia

Näissä tilanteissa 32k voi oikeasti vähentää katkoksia ja parantaa vastausten jatkuvuutta.

## Milloin 32k on käytännössä turha luksus?

32k on turha luksus silloin, kun ongelma ei ole muistin puute vaan työnkulun epätarkkuus.

Esimerkiksi näissä tapauksissa:

- kysyt lyhyitä yksittäisiä kysymyksiä
- käytät mallia nopeana kirjoitus- tai koodiapurina
- voisit tiivistää vanhan keskustelun muutamaan kappaleeseen
- voisit hakea relevantit dokumenttiosat mukaan vain tarvittaessa
- vasteaika on sinulle tärkeämpi kuin maksimaalinen historian pituus

Tällöin 32k voi tehdä ajosta vain raskaamman ilman, että lopputulos paranee suhteessa kustannukseen.

## Muisti ei ole ainoa hinta

Moni miettii kontekstia vain VRAMin kautta, mutta hinta näkyy myös käyttökokemuksessa.

Kun konteksti kasvaa, pitää miettiä ainakin näitä:

- mahtuuko ajo edelleen siististi GPU:lle
- hidastuuko vaste liikaa
- joudutko pienentämään mallia vain kontekstin takia
- valuuko osa työstä CPU:lle
- onko säikeistys enää järkevässä suhteessa kuormaan

llama.cpp:n suorituskykyohjeissa korostuu hyvin ajatus siitä, että pelkkä käynnistyminen ei ole hyvä mittari. Jos tokennopeus romahtaa tai CPU alkaa kärsiä liikaa, kontekstin kasvu ei enää palvele käyttäjää, vaikka se olisi teknisesti mahdollinen.

## Käytännön nyrkkisääntö harrastajalle

Jos käytössäsi on kone, jossa VRAM ei ole rajattomasti, 32k kannattaa ansaita käytöllä, ei ottaa oletuksena.

Hyvä päätösrunko on tämä:

### Valitse 32k, jos

- tehtävässä oikeasti viitataan laajaan aiempaan sisältöön
- huomaat pienen kontekstin katkovan työntekoa
- pystyt pitämään mallin edelleen kunnolla GPU:lla
- vaste pysyy vielä miellyttävänä

### Valitse pienempi konteksti, jos

- tehtävät ovat lyhyitä tai keskikokoisia
- 32k pakottaa liiallisiin kompromisseihin mallin koossa
- suorituskyky putoaa selvästi
- voisit ratkaista ongelman paremmin tiivistyksellä tai RAGilla

## 32k vs parempi työnkulku

Tässä kohtaa moni tekee tärkeän oivalluksen: joskus oikea päivitys ei ole pidempi konteksti vaan parempi työnkulku.

Jos sama ongelma voidaan ratkaista näin:

- tiivistä edellinen vaihe
- hae vain relevantit dokumenttiosat
- pilko työ useampaan askelmaan
- pidä aktiivisessa muistissa vain oleellinen

niin 32k ei enää ole välttämätön. Se on vain yksi työkalu muiden joukossa.

Tämä on myös järkevämpää laitebudjetin kannalta. Jos 32k tuo lisäarvoa vain harvoin, sitä ei kannata käyttää oletusasetuksena jokaisessa ajossa.

## Milloin 32k kannattaa silti pitää päällä oletuksena?

On tilanteita, joissa 32k oletuksena on aivan järkevä.

Esimerkiksi jos käytät paikallista mallia pääosin:

- pitkissä agentti- tai automaatiotyönkuluissa
- laajojen dokumenttien analysoinnissa
- monivaiheisissa koodi- tai tutkimustehtävissä
- ympäristössä, jossa VRAMia on riittävästi eikä suorituskyky kärsi liikaa

Silloin 32k voi olla oikea perusasetus eikä vain luksus.

## Mitä tästä kannattaa muistaa?

32k konteksti ei ole automaattisesti hyvä eikä automaattisesti turha. Se on hyödyllinen vain silloin, kun tehtävä todella tarvitsee pitkää aktiivista muistia ja kone pystyy kantamaan sen ilman rumia kompromisseja.

Jos taas sama työ onnistuu pienemmällä kontekstilla yhtä hyvin, 32k on helposti vain kallis tapa tuntea itsensä turvatuksi.

Kotilabrassa järkevin konteksti ei yleensä ole suurin mahdollinen, vaan se, joka tuo oikeaa hyötyä juuri sinun työnkulkuusi.

## Lähteet

- https://docs.ollama.com/context-length
- https://docs.ollama.com/gpu
- https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md
