---
title: "AI-rauta kotilabrassa: milloin 16 gigatavua VRAMia on parempi kuin hitaasti CPU:lle valuva 24 gigatavua?"
date: "2026-04-13T10:15:00+03:00"
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
Paikallisia LLM-koneita vertaillessa isompi VRAM-luku näyttää helposti automaattiselta voitolta. Käytännössä asia ei ole ihan niin yksinkertainen. Jos 24 gigatavun kortilla ajetaan mallia tai kontekstia niin aggressiivisesti, että työ alkaa valua CPU:n puolelle ja vaste muuttuu tahmeaksi, hyvin tasapainotettu 16 gigatavun GPU voi olla oikeassa käytössä parempi valinta.

Tämä kuulostaa ensin oudolta, koska paperilla 24 GB on tietenkin enemmän kuin 16 GB. Mutta harrastajakoneessa ratkaisevaa ei ole pelkkä muistimäärä, vaan se, pysyykö työnkulku siististi GPU:lla ilman että malli, konteksti ja säikeistys alkavat taistella toisiaan vastaan.

## Miksi suurempi VRAM ei aina voita?

Yleinen harha on ajatella, että enemmän muistia tarkoittaa automaattisesti parempaa kokemusta. Todellisuudessa suurempi VRAM vain siirtää rajaa. Jos käyttäjä reagoi tähän nostamalla aina mallikokoa tai kontekstia vielä pykälän ylemmäs, kone voi silti päätyä epämukavaan tilaan.

Ollaman dokumentaatio muistuttaa, että pidempi konteksti kasvattaa muistitarvetta suoraan. Samalla se suosittelee tarkistamaan `ollama ps` -näkymästä, pysyykö ajo aidosti GPU:lla. Jos split ei enää ole kunnolla GPU-painotteinen, "isompi kortti" ei käytännössä tuonut vakautta vaan vain mahdollisti uuden tavan ylittää raja.

## Milloin 16 GB voi tuntua paremmalta?

16 GB voi olla aidosti parempi kokemus silloin, kun käyttäjä pysyy sen rajoissa tietoisesti.

Esimerkiksi näin:

- valitaan malli, joka mahtuu hyvin GPU:lle
- pidetään konteksti realistisena
- vältetään jatkuva CPU-offload
- hyväksytään, ettei joka asetusta tarvitse maksimoida

Tällöin tuloksena voi olla tasaisempi tokennopeus, lyhyempi vasteaika ja vähemmän säätöä. Käytännössä hyvin käyttäytyvä 16 GB -kone voi tuntua mukavammalta kuin 24 GB -kone, jota ajetaan jatkuvasti juuri epämukavuusrajan yläpuolella.

## Missä 24 GB silti voittaa selvästi?

24 GB voittaa silloin, kun lisämuistia käytetään järkevästi eikä ahneudella.

Se auttaa esimerkiksi näissä tilanteissa:

- halutaan hieman suurempi malli ilman aggressiivista kvantisointia
- tarvitaan 32k luokan konteksti käytännön työssä
- halutaan enemmän liikkumavaraa ilman jatkuvaa mallinvaihtoa
- tavoitellaan pidempää käyttöikää ennen seuraavaa laitepäivitystä

Tässä mielessä 24 GB on edelleen vahva harrastajaluokka. Ongelma ei ole 24 GB itsessään, vaan se, että lisäbudjetti houkuttelee joskus asetuksiin, jotka eivät enää pysy siisteinä.

## CPU-offload on usein oikea vedenjakaja

Tärkein käytännön kysymys ei ole "käynnistyykö tämä ajo", vaan "pysyykö tämä ajo miellyttävänä".

llama.cpp:n suorituskykyohjeissa painotetaan kahta asiaa, jotka näkyvät hyvin myös kotikoneissa:

- GPU-offloadin määrä vaikuttaa ratkaisevasti suorituskykyyn
- liian suuri thread-asetus voi pahentaa tilannetta entisestään, jos CPU ylikuormittuu

Tämä tarkoittaa, että jos 24 GB -kortin käyttöstrategia johtaa siihen, että osa työstä valuu jatkuvasti CPU:lle ja säikeitä on liikaa, tulos voi olla oikeasti huonompi kuin 16 GB -kortilla ajettu paremmin rajattu profiili.

## Milloin 16 GB on käytännössä fiksumpi valinta?

16 GB on usein järkevämpi, jos:

- ajat pääosin pieniä tai keskikokoisia kvantisoituja malleja
- käytät paikallista LLM:ää enemmän apurina kuin massiivisena agenttimoottorina
- et tarvitse pitkää kontekstia joka tehtävässä
- haluat hyvän hintatasapainon ja siedettävän sähkönkulutuksen
- hyväksyt sen, että osa suurista malleista ei kuulu tämän luokan koneelle

Tällaisessa profiilissa 16 GB voi olla helpompi optimoida hyvin. Se pakottaa realistisiin päätöksiin, mikä on monesti etu eikä haitta.

## Milloin 24 GB kannattaa valita, vaikka osa ajoista olisi rajoilla?

24 GB on silti oikeampi valinta, jos tiedät jo nyt että työnkulku sisältää usein:

- pidempiä konteksteja
- raskaampia malleja
- toistuvaa dokumentti- tai koodityötä, jossa muistibudjetti kasvaa nopeasti
- halun välttää liian varhaista seuraavaa GPU-päivitystä

Mutta silloinkin tärkeä sääntö säilyy samana: älä arvioi onnistumista vain sillä, että malli saatiin käyntiin. Arvioi sitä sillä, pysyikö ajo tarpeeksi nopeana ja siistinä oikeassa käytössä.

## Yksinkertainen käytännön sääntö

Jos mietit 16 GB:n ja 24 GB:n välillä tai arvioit nykyistä konettasi, käytä tätä sääntöä:

- valitse 16 GB, jos haluat tasapainoisen koneen realistisille malleille ja tiedät pysyväsi kohtuullisessa kontekstissa
- valitse 24 GB, jos tarvitset enemmän liikkumavaraa, mutta käytä sitä kurinalaisesti
- jos 24 GB johtaa jatkuvasti CPU-offloadiin ja tahmeaan vasteeseen, et enää nauti sen lisämuistista vaan kärsit huonosta rajankäytöstä

## Mitä tästä kannattaa muistaa?

24 gigatavua VRAMia on teoriassa enemmän, mutta käytännössä parempi kone on se, joka pysyy omassa käyttöprofiilissaan vakaana, nopeana ja miellyttävänä.

Siksi hyvin rajattu 16 GB voi olla arjessa parempi kuin 24 GB, jota ajetaan jatkuvasti liian kovilla asetuksilla. Lopulta ratkaisevin kysymys ei ole kortin koko, vaan se, kuinka usein joudut pakottamaan työnkulun yli mukavan suorituskykyrajan.

## Lähteet

- https://docs.ollama.com/context-length
- https://docs.ollama.com/gpu
- https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md
