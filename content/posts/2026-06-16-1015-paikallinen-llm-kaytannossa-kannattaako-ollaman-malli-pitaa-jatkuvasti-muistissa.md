---
title: "Paikallinen LLM käytännössä: kannattaako Ollaman malli pitää jatkuvasti muistissa?"
date: "2026-06-16T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "Paikallinen LLM käytännössä"
tags:
  - "Ollama"
  - "Local LLM"
  - "Memory"
  - "VRAM"
  - "Performance"
---
Yksi yllättävän käytännöllinen paikallisen LLM-koneen kysymys ei olekaan "mikä malli" vaan **kannattaako sama malli pitää lämpimänä muistissa vai antaa sen purkautua aina käytön välissä**. Oma nyrkkisääntöni on tämä: **jos käytät samaa mallia monta kertaa tunnissa ja koneessa on oikeasti muistivaraa, pidä se muistissa. Jos taas vaihdat malleja usein, ajat useita palveluita samalla koneella tai VRAM on muutenkin tiukka, jatkuva warm-tila muuttuu nopeasti kalliiksi mukavuudeksi.**

Ollaman dokumentaatio kertoo suoraan kaksi tärkeää asiaa. Ensinnäkin malli pysyy oletuksena muistissa viisi minuuttia ennen purkua. Toiseksi tätä voi ohjata sekä `keep_alive`-parametrilla että palvelimen `OLLAMA_KEEP_ALIVE`-asetuksella. Tämä on hyvä oletus, koska se nopeuttaa toistuvia pyyntöjä ilman että kone jää pysyvästi täyteen jokaisen testimallin jäljiltä.

## Milloin lämmin malli oikeasti auttaa

Pidä malli muistissa ainakin silloin, kun kipu näkyy nimenomaan ensimmäisessä pyynnössä eikä jatkuvassa generoinnissa. Ollaman API palauttaa erikseen `load_duration`-kentän, joten näet käytännössä, paljonko aikaa meni pelkkään mallin lataamiseen. Jos ensimmäinen vastaus on aina selvästi hidas mutta seuraavat pyynnöt tuntuvat sujuvilta, warm-malli on usein oikea ja halpa parannus.

Tämä korostuu erityisesti kolmessa tilanteessa:

- samaa mallia kutsutaan pienissä purskeissa pitkin päivää
- työkaluketju tai agentti osuu aina samaan malliin
- levy on hidas tai malli on suuri, mutta varsinainen ajo on muuten sujuva

Tällöin kannattaa yleensä joko esiladata malli tyhjällä pyynnöllä tai pidentää `keep_alive`-aikaa maltillisesti, esimerkiksi minuuteista tuntiin. Näin poistat turhia kylmäkäynnistyksiä ilman että koko palvelin muuttuu "kaikki aina muistissa" -ratkaisuksi.

## Milloin jatkuva muistissa pitäminen alkaa kääntyä itseään vastaan

Yleisin virhe on vetää `keep_alive: -1` käyttöön vain siksi, että lämmin malli tuntui kerran mukavalta. Se toimii, mutta vain jos muistibudjetti kestää sen myös huonoina hetkinä.

Ollaman FAQ muistuttaa, että useita malleja voidaan pitää ladattuina yhtä aikaa vain jos muistia on aidosti tarpeeksi. GPU-ajossa uuden mallin pitää mahtua kokonaan VRAMiin, jotta useita malleja voidaan ladata rinnakkain. Sama dokumentti muistuttaa myös, että rinnakkaispyynnöt kasvattavat muistitarvetta, koska konteksti skaalautuu `OLLAMA_NUM_PARALLEL * OLLAMA_CONTEXT_LENGTH` -logiikalla.

Käytännön käännös harrastajalle on yksinkertainen:

- yksi lämmin malli on usein hyvä idea
- kaksi voi olla vielä ok, jos tiedät niiden mahtuvan
- "pidetään kaikki suosikit ladattuina" loppuu helposti jonotukseen, unloadaukseen tai siihen että muu kone alkaa kärsiä

Jos käytössä on 12-16 Gt VRAM ja lisäksi pitkä konteksti tai useampi rinnakkainen pyyntö, ikuinen warm-tila kannattaa nähdä poikkeuksena, ei oletuksena.

## Tämä ei ole sama asia kuin `mlock`

On myös hyödyllistä erottaa kaksi asiaa toisistaan. Ollaman `keep_alive` kertoo kauanko runtime yrittää pitää mallin ladattuna käyttöjen välissä. `llama.cpp`:n puolella taas `--mlock` ja `--mmap` liittyvät siihen, miten mallitiedosto ja muistinkäyttö käsitellään käyttöjärjestelmän tasolla.

`llama.cpp`:n server-dokumentaatio sanoo suoraan, että `--mlock` pakottaa mallin pysymään RAMissa eikä swapissa, kun taas `--mmap` on oletuksena päällä ja vaikuttaa siihen, miten tiedosto mapitetaan muistiin. Tämä on tärkeä ero: **warm-malli ei tarkoita automaattisesti samaa asiaa kuin aggressiivinen RAM-lukitus**. Jos koneella tehdään muutakin kuin yhtä inferenssityötä, liian innokas muistissa pitäminen voi tehdä koko ympäristöstä tahmean.

## Kolme käytännön sääntöä, joilla valitsisin asetuksen

1. Jos käytät samaa mallia jatkuvasti ja `load_duration` on ärsyttävän suuri, pidennä `keep_alive`-aikaa.
2. Jos vaihtelet malleja usein tai kone tekee muutakin, pidä oletus lyhyenä tai vapauta malli heti käytön jälkeen.
3. Jos huomaat jonotusta, VRAM-painetta tai turhaa rinnakkaista muistikuormaa, älä lämmitä useita malleja "varmuuden vuoksi".

Minun mielestäni paras oletus useimmille kotilabroille ei ole ikuinen warm-tila eikä jatkuva cold start, vaan **maltillinen välitila**: pidä aktiivinen työmalli muistissa hetken, mutta tee muistista taas vapaata heti kun työvirta oikeasti vaihtuu.

## Lähteet

- https://docs.ollama.com/faq
- https://docs.ollama.com/api/generate
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md?plain=1
