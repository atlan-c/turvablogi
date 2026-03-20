---
title: "AI-rauta kotilabrassa: nopea SSD ei yleensä nopeuta paikallista LLM:ää niin paljon kuin luulet"
date: 2026-03-20T10:15:00+02:00
draft: false
---
Kun paikallinen LLM tuntuu hitaalta, ensimmäinen ostosimpulssi voi olla “laitetaan nopeampi NVMe”. Se on ymmärrettävä ajatus, koska mallit ovat isoja tiedostoja ja niiden lataus näyttää levyoperaatiolta. Käytännössä nopea SSD auttaa eniten silloin, kun malli ladataan muistiin, vaihdetaan mallia usein tai palvelu joutuu käynnistämään mallin vähän väliä uudestaan. Varsinainen tokenien generointi ei kuitenkaan tavallisesti ole SSD:n vaan VRAMin, järjestelmämuistin, muistiväylän ja laskentatehon varassa.

Tämä ero kannattaa ymmärtää ennen kuin käyttää rahaa väärään pullonkaulaan. Jos mallin vaste on hidas jokaisessa promptissa, SSD ei yleensä ole ensimmäinen korjaus. Jos taas ensimmäinen vastaus alkaa hitaasti mutta sen jälkeen teksti virtaa normaalisti, levy voi hyvinkin olla osa ongelmaa.

## Missä SSD oikeasti auttaa?

Paikallisessa malliajossa levy osallistuu yleensä kolmeen vaiheeseen:

- mallin ensimmäinen lataus levyllä olevasta tiedostosta muistiin
- mallin uudelleenlataus, jos prosessi tai palvelu vapauttaa mallin muistista
- isojen mallien kopiointi, päivitys ja hallinta arjessa

Ollaman dokumentaatio kertoo suoraan, että mallin voi esiladata muistiin ja että malli pidetään oletuksena muistissa viisi minuuttia ennen purkua. Tämä on käytännöllinen vihje: jos nopeusongelma näkyy vain ensimmäisessä pyynnössä, pullonkaula voi olla latauksessa eikä itse inferenssissä. Silloin nopeampi levy tai aggressiivisempi mallin pitäminen muistissa voi auttaa selvästi.

Myös llama.cpp korostaa minimal setup -mallia ja tukee CPU+GPU-hybridiä, kvantisointeja ja erilaisia muistinkäyttötapoja. Käytännössä tämä tarkoittaa, että kun malli on saatu käyttömuistiin ja laskenta alkaa, suorituskykyä rajoittaa yleensä enemmän se, kuinka paljon mallista mahtuu VRAMiin ja kuinka paljon dataa joudutaan siirtelemään CPU:n ja GPU:n välillä, ei se kuinka nopea levy koneessa on.

## Missä SSD ei yleensä auta juuri lainkaan?

Nopea SSD ei tavallisesti korjaa näitä ongelmia:

- tokeneita syntyy vähän sekunnissa koko generoinnin ajan
- pitkä konteksti hidastaa jokaista vastausta
- malli ei mahdu VRAMiin ja osa jää järjestelmämuistiin
- GPU on liian pieni malliluokkaan nähden
- RAM loppuu ja järjestelmä alkaa sivuttaa

Jos 7B- tai 14B-malli generoi hitaasti joka kierroksella, kannattaa katsoa ensin paljonko mallista oikeasti mahtuu GPU:lle. Jos ajo on osittain CPU:n ja osittain GPU:n varassa, tai jos konteksti on suuri, todellinen hidaste löytyy usein muistihierarkiasta eikä levystä. Tässä tilanteessa SSD:n vaihto PCIe 3.0:sta PCIe 4.0:aan voi tuntua arjessa yllättävän pieneltä parannukselta.

## Mistä tunnistat oikean pullonkaulan?

Käytännön nyrkkisääntö:

- **Hidas vain alussa:** epäile mallin latausta, kylmää käynnistystä tai sitä, että malli puretaan muistista liian aggressiivisesti.
- **Hidas koko ajan:** epäile VRAMin määrää, kvantisointivalintaa, liian suurta kontekstia tai CPU/GPU-jakoa.
- **Hidas mallia vaihtaessa:** nopeampi SSD voi auttaa ihan aidosti.
- **Hidas usean käyttäjän tai prosessin ympäristössä:** ongelma voi olla myös muistipaineessa, jolloin malli joudutaan lataamaan yhä uudelleen.

Hyvä testi on ajaa sama prompti kahdesti peräkkäin. Jos ensimmäinen käynnistyy hitaasti mutta toinen selvästi nopeammin, levy- ja latauspolku on todennäköisesti merkittävä tekijä. Jos molemmat ovat yhtä hitaita, etsi katse VRAMista, RAMista ja mallivalinnasta.

## Mihin raha kannattaa laittaa ensin?

Harrastajalle järkevä prioriteetti on yleensä tämä:

1. riittävästi VRAMia siihen malliluokkaan, jota oikeasti aikoo käyttää
2. tarpeeksi järjestelmämuistia, ettei kone ala sivuttaa
3. vasta sen jälkeen levy, joka on “riittävän nopea” mallien lataukseen

Tämä ei tarkoita, että SSD olisi yhdentekevä. Hidas SATA-levy tai lähes täynnä oleva heikko SSD voi tehdä käyttökokemuksesta tahmean, etenkin jos vaihtelet malleja paljon. Mutta jos koneessa on jo asiallinen NVMe, seuraava iso hyöty tulee useimmiten muualta kuin levystä.

## Käytännön suositus

Jos rakennat ensimmäistä paikallista LLM-konetta, osta mieluummin tasapainoinen kokonaisuus kuin paperilla nopein levy. Hyvä NVMe on mukava, mutta paikallisen mallin “tuntuma” paranee yleensä enemmän siitä, että malli mahtuu paremmin GPU:lle ja pysyy muistissa. SSD nopeuttaa oven avaamista; VRAM ja muistikaista ratkaisevat, kuinka rivakasti työ sisällä etenee.

## Lähteet

- Ollama FAQ: mallien esilataus, muistissa pitäminen ja GPU/CPU-latauksen tarkistus: https://docs.ollama.com/faq
- llama.cpp README: paikallinen inferenssi, kvantisointi ja CPU+GPU-hybridi: https://github.com/ggml-org/llama.cpp
