---
title: "Swap paikallisessa LLM-koneessa: milloin se on turvaverkko ja milloin virhe?"
date: "2026-06-18T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "Paikallinen LLM käytännössä"
tags:
  - "Local LLM"
  - "Linux"
  - "Swap"
  - "Ollama"
  - "llama.cpp"
---
Moni paikallista LLM-konetta rakentava päätyy ennemmin tai myöhemmin samaan neuvoon: "ota swap kokonaan pois, muuten kone hidastuu". Neuvossa on yksi tosi ydin, mutta se on liian karkea yleissääntö. **Oma suositukseni on tämä: älä rakenna paikallista LLM-työtä swapin varaan, mutta älä myöskään poista swapia automaattisesti joka koneesta. Pieni ja hallittu swap tai zram voi olla hyödyllinen turvaverkko, kunhan ymmärrät ettei se korvaa puuttuvaa RAMia tai VRAMia.**

Tärkein ero on tämä: jos mallisi toimii vain siksi, että käyttöjärjestelmä työntää muistia levylle, kokoonpano on käytännössä liian tiukka. Mutta jos swap on vain hätävara satunnaisia piikkejä, mallin vaihtoa tai muuta työpöytäkäyttöä varten, siitä voi olla enemmän hyötyä kuin haittaa.

## Miksi aihe nousee esiin juuri paikallisissa LLM-koneissa

Paikalliset LLM-työkalut käyttävät muistia tavalla, joka tekee swap-keskustelusta tavallista konkreettisemman. `llama.cpp`:n server-dokumentaatio kertoo suoraan, että `--mlock` pakottaa mallin pysymään RAMissa eikä swapissa tai muistinkompressiossa. Samassa dokumentaatiossa taas todetaan, että `--mmap` on oletuksena käytössä, ja ilman sitä mallin lataus on hitaampaa, vaikka pageout-ongelmat voivat joissain tilanteissa vähentyä.

Käytännön käännös on yksinkertainen:

- malli ei ole vain yksi tavallinen prosessi muiden joukossa
- mallin painot voivat olla kymmeniä gigatavuja
- käyttöjärjestelmän muistipaine näkyy nopeasti vasteessa
- väärä muistipolku ei yleensä tee ajosta vain "vähän hitaampaa" vaan joskus käyttökelvottoman

Juuri siksi moni tulkitsee ensimmäisen swap-hidastumisen niin, että swap itsessään on vihollinen. Usein varsinainen ongelma on kuitenkin se, että koneessa ei ole tarpeeksi oikeaa muistia siihen ajotapaan, jota yrität käyttää.

## Milloin swap on selvästi huono merkki

Jos paikallinen LLM alkaa työntää aktiivista työkuormaa swapin puolelle, en pitäisi sitä optimointina vaan varoitusvalona. Tällöin näkyy yleensä ainakin yksi näistä:

- ensimmäinen vastaus on tuskallisen hidas ja koko kone tahmaa
- mallin vaihto kestää kohtuuttoman kauan
- taustalla pyörivä selain, editori tai vektorikanta tekee tilanteesta paljon pahemman
- tokennopeus vaihtelee oudosti, vaikka CPU tai GPU ei näytä täysin tukossa olevalta

`llama.cpp`:n dokumentaatio vihjaa tähän suoraan: jos `mmap` poistetaan käytöstä, lataus hidastuu, mutta pageout-ongelmat voivat pienentyä, jos `mlock` ei ole käytössä. Se ei siis sano "swap on hyvä", vaan käytännössä tämän: **kun muistia on liian vähän, käyttöjärjestelmän sivutus alkaa jo näkyä inferenssin laadussa**.

Jos olet tässä tilanteessa, oikea johtopäätös on yleensä jokin näistä:

- pienempi malli
- kevyempi kvantisointi
- enemmän RAMia
- enemmän VRAMia
- vähemmän rinnakkaisia pyyntöjä

Ei se, että "lisätään swapia niin ongelma ratkeaa".

## Miksi en silti suosittelisi nollaswapia joka koneeseen

Linux-kernelin dokumentaatio ei kuvaa `swappiness`-asetusta yksinkertaisena on/off-kytkimenä, vaan karkeana suhteellisena arviona sille, mikä on swap-I/O:n ja tiedostopohjaisen sivutuksen kustannus. Dokumentaatio sanoo myös, että arvo `0` ei tarkoita "swap on pois", vaan sitä, että kernel ei aloita swappausta ennen kuin vapaan ja tiedostopohjaisen muistin määrä putoaa tietyn rajan alle.

Tämä on käytännössä tärkeä ero. Moni ajattelee, että:

- swap olemassa = kernel pilaa aina suorituskyvyn
- swap pois = kone toimii aina paremmin

Todellisuus on sotkuisempi. Jos työasemakoneella on paikallinen LLM, selain, editori, pari taustapalvelua ja ehkä upotuskanta, pieni swap tai zram voi pelastaa koko session siinä kohtaa, kun muisti käy hetkellisesti liian tiukaksi. Ilman mitään turvaverkkoa seuraus voi olla suora OOM-killeri, kaatunut prosessi tai pahimmillaan koko työvirran katkeaminen juuri väärällä hetkellä.

## Erityistapaus: zram voi olla järkevämpi kuin levy-swap

Kernelin dokumentaatio sanoo suoraan, että in-memory swapin, kuten zramin tai zswapin, kanssa `swappiness` voi olla jopa yli 100, jos swap on käytännössä tiedostojärjestelmää nopeampi vaihtoehto. Tämä on hyvä muistutus siitä, ettei "swap" tarkoita aina yhtä asiaa.

Tavalliselle harrastajalle tästä seuraa käytännön sääntö:

- hidas levy-swap ei ole hyvä paikka aktiiviselle LLM-työlle
- pieni zram voi olla ihan järkevä pehmuste kevyille muistipiikeille
- kumpikaan ei tee alimitoitetusta koneesta oikeasti sopivaa isolle mallille

Jos koneessa on vähän RAMia mutta tavoitteena on silti ajaa kohtuullisen pieniä paikallisia malleja muun työpöytäkäytön rinnalla, valitsisin itse mieluummin hallitun zramin kuin täysin nollaswapin.

## Entä Ollama, useat mallit ja rinnakkaiset pyynnöt?

Ollaman FAQ tekee tästä vielä käytännöllisemmän. Dokumentaatio sanoo, että mallit pidetään oletuksena muistissa viisi minuuttia, useita malleja voidaan pitää ladattuna jos muistia on tarpeeksi, ja rinnakkaispyynnöt kasvattavat muistitarvetta suhteessa `OLLAMA_NUM_PARALLEL * OLLAMA_CONTEXT_LENGTH`.

Tästä tulee yksi yleinen ansa: käyttäjä luulee testanneensa "yhtä mallia", mutta oikeasti koneella on:

- lämmin malli muistissa
- toinen juuri ladattava malli jonossa
- kasvatettu konteksti
- rinnakkaisia pyyntöjä tai agenttityötä

Silloin swapin ilmestyminen ei ole merkki siitä, että swap pitäisi ensimmäisenä tappaa. Se on usein merkki siitä, että **muistibudjetti on suunniteltu liian optimistisesti suhteessa todelliseen käyttöön**.

## Milloin poistaisin swapin kokonaan?

Poistaisin swapin vain, jos nämä ehdot täyttyvät yhtä aikaa:

- kone on lähes yksikäyttöinen LLM-palvelin
- tunnet muistibudjetin hyvin
- mallikoko, konteksti ja rinnakkaisuus ovat tiukasti hallinnassa
- hyväksyt mieluummin nopean epäonnistumisen kuin hitaan tahmaamisen

Tällaisessa koneessa nollaswap voi olla perusteltu. Jos muisti loppuu, haluat tietää sen heti. Se on järkevä filosofia etenkin silloin, kun kone tekee vain yhtä tehtävää ja virhe pitää havaita nopeasti.

## Milloin pitäisin pienen swapin tai zramin?

Pitäisin sen melkein aina, jos jokin näistä on totta:

- sama kone on myös työasema
- käytät Ollamaa usealla mallilla tai agenttityössä
- ajat välillä CPU-painotteisia töitä ja välillä GPU-offloadia
- haluat välttää turhia kaatumisia satunnaisissa muistipiikeissä

Tässä mallissa swap ei ole suorituskykyominaisuus vaan törmäystyyny. Sen tehtävä on ostaa vähän aikaa ja estää pahin, ei mahdollistaa jatkuvaa muistivajetta.

## Oma nyrkkisääntöni

En kysyisi ensimmäisenä "onko swap päällä", vaan tätä:

1. mahtuuko normaali työkuorma RAMiin ja VRAMiin ilman temppuja
2. pidetäänkö malleja lämpimänä pidempään kuin oikeasti tarvitaan
3. kasvattaako rinnakkaisuus tai pitkä konteksti muistia salaa liikaa
4. onko kone palvelin vai sekalainen työasema

Jos normaali kuorma ei mahdu ilman sivutusta, korjaa kuorma tai rauta. Jos taas kaikki toimii normaalisti ja haluat vain pienen turvaverkon outoja piikkejä vastaan, pieni swap tai zram on minusta aivan puolustettava ratkaisu.

## Johtopäätös

**Älä rakenna paikallista LLM-konetta swapin varaan. Mutta älä myöskään poista swapia rituaalina vain siksi, että joku benchmarkkaaja sanoi niin internetissä.** Paras ratkaisu riippuu siitä, onko kone puhdas inferenssipalvelin vai tavallinen kotilabran työasema.

Jos haluat yksinkertaisen käytännön ohjeen, se on tämä:

- palvelin, yksi selkeä työkuorma, tarkka kapasiteetti: swap voi olla pois
- työasema tai monikäyttökone: pidä pieni turvaverkko, mieluiten hallittuna
- jos swap on jatkuvasti käytössä inferenssin aikana: sinulla ei ole swap-ongelma vaan kapasiteettiongelma

Se on yleensä hyödyllisempi johtopäätös kuin mustavalkoinen "aina pois" tai "aina päälle".

## Lähteet

- https://docs.kernel.org/admin-guide/sysctl/vm.html
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- https://docs.ollama.com/faq
