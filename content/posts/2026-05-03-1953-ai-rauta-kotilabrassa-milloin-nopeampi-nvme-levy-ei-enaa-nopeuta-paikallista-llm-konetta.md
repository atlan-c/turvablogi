---
title: "AI-rauta kotilabrassa: milloin nopeampi NVMe-levy ei enää nopeuta paikallista LLM-konetta?"
date: 2026-05-03T19:53:23+03:00
draft: false
topic_family: "llm-hardware"
---

Paikallista LLM-konetta rakentaessa NVMe-levy tuntuu usein helpolta päivitykseltä. Numeroita on helppo verrata, paketissa luvataan valtavia gigatavuja sekunnissa ja päivitys kuulostaa modernilta. Käytännössä nopeampi NVMe ei kuitenkaan aina nopeuta itse LLM-arkea juuri siinä kohdassa, jossa käyttäjä sen huomaa.

Lyhyt käytännön sääntö on tämä: nopeampi NVMe auttaa paljon silloin, kun nykyinen levy on selvä pullonkaula mallien latauksessa, datan siirrossa tai RAG-aineiston käsittelyssä. Jos taas varsinainen työ hidastuu VRAMin, RAMin, CPU:n tai GPU:n vuoksi, pelkkä levy päivittyy mutta kokemus ei juuri muutu.

## Mitä NVMe oikeasti tekee hyvin

NVMe on avoin looginen rajapinta pysyvälle tallennukselle, yleensä PCI Express -väylän päällä. Sen idea on hyödyntää SSD-levyjen matalaa latenssia ja sisäistä rinnakkaisuutta paremmin kuin vanhemmat rajapinnat. Käytännössä tämä tarkoittaa sitä, että NVMe on erittäin hyvä siirtämään dataa nopeasti ja pitämään I/O-kuorman pienenä verrattuna vanhempiin levyratkaisuihin.

Kotilabran AI-käytössä tämä näkyy erityisesti silloin, kun:

- lataat isoja mallifilejä levyltä muistiin
- vaihdat malleja usein päivän aikana
- rakennat tai päivität vektoritietokantaa
- käsittelet isoja datasetti- tai mediatiedostoja paikallisesti
- käytät samaa konetta sekä malliajoon että muuhun raskaan I/O:n työhön

Näissä tilanteissa hidas levy tuntuu oikeasti hitalta.

## Missä kohtaa levy lakkaa olemasta tärkein asia

LLM:n ajon aikana varsinainen pullonkaula ei usein ole levy vaan laskenta ja muisti. Kun malli on jo ladattu RAMiin tai VRAMiin, tokenien generointi ei enää yleensä odota SSD:tä vaan prosessoria, näytönohjainta, muistimäärää tai muistiväylää.

Tässä kohtaa moni tekee kalliin mutta vähän vaikuttavan päivityksen: vaihdetaan jo valmiiksi kelvollinen NVMe vielä nopeampaan, vaikka arjen hitaus johtuu oikeasti siitä, että:

- VRAM ei riitä isommalle mallille
- RAM loppuu kesken
- CPU on heikko pitkissä prompti- tai ingest-kuormissa
- GPU on varsinainen rajoite inferenssissä
- PCIe-kaistat tai kotelon lämpöbudjetti rajoittavat muuta rautaa enemmän

Silloin CrystalDiskMark näyttää hienolta, mutta käytännön promptivaste ei juuri muutu.

## PCIe-numeroita kannattaa tulkita rauhallisesti

PCI Express on nopea sarjaväylä, jossa laitteet käyttävät yhtä tai useampaa lanea. NVMe-levyt hyödyntävät tätä kaistaa, mutta koko järjestelmä ei elä vain levyn maksimiluvusta. Myös emolevyn kaistajako, M.2-paikkojen toteutus ja muiden laitteiden käyttö voivat vaikuttaa siihen, mitä nopeutta oikeasti saadaan ulos.

Tämä on hyvä muistutus kotilabraan: paperilla nopeampi sukupolvi tai suurempi kaistamäärä ei automaattisesti tarkoita näkyvästi nopeampaa LLM-työtä. Jos nykyinen levy ei ole se kohta, jossa odotat, lisäkaista ei ratkaise muuta pullonkaulaa puolestasi.

## Milloin NVMe-päivitys on silti perusteltu

Nopeampi tai parempi NVMe on usein järkevä päivitys, jos huomaat käytännössä jotain näistä:

- mallin lataus kestää ärsyttävän kauan joka kerta
- useiden gigatavujen aineistot liikkuvat päivittäin
- vanha levy on pieni, täynnä tai lämpenee rajusti
- käytössä on vielä SATA SSD tai heikko vanha NVMe
- sama levy joutuu palvelemaan sekä OS:ää, swapia, mallikirjastoa että ingest-työtä yhtä aikaa

Tällöin levy voi olla oikeasti arkea hidastava osa, ja päivitys tuntuu heti.

## Oma nyrkkisääntö

Minun käytännön sääntöni olisi tämä:

1. jos ongelma näkyy mallin latauksessa ja aineiston käsittelyssä, katso levyä ensin
2. jos ongelma näkyy tokenien generoinnissa, katso ensin GPU:ta, CPU:ta ja muistia
3. jos nykyinen levy on jo kohtuullinen NVMe, älä oleta että vielä nopeampi malli muuttaa koko koneen tuntumaa
4. päivitä levy mielellään silloin, kun saat samalla lisää kapasiteettia, parempaa luotettavuutta tai vähemmän lämpöongelmia

Näin rahaa ei huku paperinopeuteen, joka ei osu arjen todelliseen kipukohtaan.

## Yhteenveto

Milloin nopeampi NVMe-levy ei enää nopeuta paikallista LLM-konetta? Silloin, kun levyn jälkeen varsinainen pullonkaula on jo siirtynyt laskentaan tai muistiin.

Nopea levy on tärkeä osa hyvää AI-konetta, mutta se ei korvaa puuttuvaa VRAMia, RAMia tai laskentatehoa. Lyhyt muistilappu on tämä: NVMe nopeuttaa datan liikettä, ei automaattisesti itse ajattelutyötä.

## Lähteet

- https://en.wikipedia.org/wiki/NVMe
- https://en.wikipedia.org/wiki/PCI_Express
