---
title: "AI-rauta kotilabrassa: milloin käytetty datakeskus-GPU muuttuu halvasta löydöstä kalliiksi kompromissiksi?"
date: "2026-05-10T10:15:00+03:00"
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
Käytetty datakeskus-GPU näyttää paikallisen LLM-harrastajan silmissä usein täydelliseltä oikotieltä. Hintaan voi saada paljon VRAMia, kortti on alun perin tehty AI-kuormille ja speksit näyttävät paperilla houkuttelevilta. Käytännössä halpa löytö voi kuitenkin muuttua nopeasti kalliiksi kompromissiksi, jos kortti olettaa aivan erilaisen kotelon, ilmankierron ja virtaympäristön kuin tavallinen kotilabra.

Lyhyt käytännön sääntö on tämä: käytetty datakeskus-GPU on houkutteleva ostos vain silloin, kun koko muu kone pystyy tukemaan sitä. Jos joudut samalla ratkaisemaan jäähdytyksen, virtaliittimet, melun, fyysisen tilan ja ajurituen uusiksi, halpa kortti ei ole enää oikeasti halpa.

## Miksi datakeskus-GPU houkuttelee niin paljon

Tähän on hyvä syy. Moni käytetty datakeskuskortti tarjoaa enemmän muistia kuin kuluttajapään halvemmat näytönohjaimet. Paikallisessa LLM-käytössä tämä on aidosti tärkeää, koska VRAM määrää usein suoraan sen, kuinka suuria malleja voit ajaa mukavasti ilman aggressiivista kompromissia kvantisoinnissa tai CPU-offloadissa.

Siksi esimerkiksi vanha Tesla- tai muu palvelinkortti voi näyttää paremmalta diililtä kuin uusi pelaajaluokan kortti, jossa on vähemmän muistia mutta korkeampi hinta. Ongelma on, että palvelinkortin speksi ei kerro vain laskentatehosta, vaan myös siitä millaisessa ympäristössä kortin oletetaan elävän.

## Ensimmäinen sudenkuoppa: passiivijäähdytys ei tarkoita "ei tarvitse miettiä jäähdytystä"

Tämä on ehkä yleisin väärinymmärrys. Esimerkiksi NVIDIA Tesla P40 on valmistajan mukaan 250 watin passiivisesti jäähdytetty kortti, joka **vaatii järjestelmän ilmavirran** toimiakseen lämpörajojen sisällä. Myös NVIDIA T4 on passiivisesti jäähdytetty kortti, vaikka se on paljon kevyempi 70 watin low-profile-malli. Passiivinen tässä yhteydessä ei siis tarkoita hiljaista työpöytäkäyttöä, vaan sitä että jäähdytys oletetaan tulevan palvelinrungon hallitusta, voimakkaasta ilmavirrasta.

Kotikotelossa tämä on ratkaiseva ero. Tavallinen torni ei yleensä puhalla ilmaa samalla tavalla suoraan kortin yli kuin palvelin. Jos kortti on suunniteltu elämään etu-taka-suunnan kovassa ilmavirrassa, mutta kotelossa ilma kiertää pehmeämmin ja epäsuoremmin, seurauksena voi olla throttlaus, epävakaus tai jatkuva virittely lisätuulettimilla.

Käytännön johtopäätös: jos kortti on passiivinen datakeskusmalli, osta sitä vasta sitten kun tiedät täsmälleen miten tuot sille riittävän ilmavirran.

## Toinen sudenkuoppa: kortin watit eivät ole vain sähkölaskua

250 watin palvelinkortti ei rasita vain pistorasiaa. Se kuormittaa myös virtalähdettä, kotelon lämpöbudjettia ja huoneen melutasoa. Kun kortti puskee lämpöä ulos pitkissä inferenssi- tai embedding-ajoissa, koko koneen jäähdytys joutuu tekemään enemmän töitä. Silloin ongelma ei enää ole pelkkä GPU, vaan koko järjestelmän tasapaino.

Tässä 70 watin T4 ja 250 watin P40 näyttävät hyvin, miksi pelkkä VRAM per euro ei riitä ostokriteeriksi. T4:n laskentateho ja muistimäärä eivät tee siitä automaattisesti parempaa korttia kaikkiin tilanteisiin, mutta sen teho- ja kokoluokka voivat sopia paljon useampaan kotikoneeseen ilman, että koko kokoonpano pitää rakentaa uudelleen kortin ympärille. P40 taas voi olla erinomainen löydös vain silloin, kun muu rauta oikeasti tukee sitä.

## Kolmas sudenkuoppa: fyysinen yhteensopivuus ei ole sama asia kuin käytännön yhteensopivuus

Moni tarkistaa vain tämän: mahtuuko kortti PCIe-paikkaan ja löytyykö tarvittava virtaliitin. Se ei vielä riitä.

Käytännössä kannattaa tarkistaa ainakin nämä:

- onko kortti täyskorkea vai low-profile
- onko se yksi- vai kaksipaikkainen
- mihin suuntaan kotelon ilmavirta oikeasti kulkee
- jääkö kortin ympärille tilaa ilman liikkeelle
- kestääkö virtalähde jatkuvan kuorman eikä vain hetkellistä piikkiä
- nouseeko muun koneen lämpö samalla liikaa

Datakeskuskortti voi siis olla teknisesti yhteensopiva mutta silti huono valinta, jos kotelon sisäinen aerodynamiikka, kaapelointi tai virtabudjetti muuttuvat epäsiisteiksi kompromisseiksi.

## Milloin käytetty datakeskus-GPU voi silti olla hyvä ostos

Se voi olla oikein hyvä ostos, jos sinulla on jo valmiiksi ympäristö, joka muistuttaa enemmän pientä palvelinta kuin tavallista pöytäkonetta. Hyviä merkkejä ovat esimerkiksi:

- kotelossa on vahva ja ennakoitava etu-taka-ilmavirta
- tiedät miten mittaat lämpöjä myös pitkän kuorman aikana
- virtalähteessä on oikea reservi jatkuvalle kuormalle
- siedät tai odotat palvelinhenkistä melua
- tavoittelet nimenomaan paljon VRAMia suhteessa hintaan
- ymmärrät etukäteen, että kortti voi vaatia enemmän käsityötä kuin kuluttajakortti

Tällaisessa ympäristössä käytetty datakeskus-GPU voi olla erittäin järkevä tapa päästä isompaan muistiluokkaan ilman uuden kortin hintaa.

## Milloin se on todennäköisesti huono ostos

Huono merkki on se, että kortti näyttää hyvältä vain yhdellä rivillä: "24 GB VRAM todella halvalla". Jos muu kokonaisuus ei tue korttia, säästö valuu nopeasti oheisongelmiin.

Jättäisin kauppaan ainakin tilanteissa, joissa:

- haluat hiljaisen työpöytäkoneen
- kotelo on ahdas tai ilmavirta heikko
- et halua askarrella lisätuulettimien, 3D-printattujen ilmakanavien tai erikoiskaapeleiden kanssa
- virtalähde on jo valmiiksi rajalla
- koneen pitää olla huoleton arjen työkalu eikä projekti

Silloin tavallinen kuluttajakortti vähemmälläkin VRAMilla voi olla oikeasti parempi ostos, koska koko järjestelmä pysyy yksinkertaisempana, hiljaisempana ja ennustettavampana.

## Käytännön ostosääntö kotilabraan

Jos harkitset käytettyä datakeskus-GPU:ta paikalliseen LLM-koneeseen, älä kysy ensimmäisenä "paljonko VRAMia tällä saa eurolla". Kysy ensin nämä kolme kysymystä:

1. **Miten tämä kortti jäähdytetään juuri minun kotelossani?**
2. **Mitä tämä kortti tekee koko koneen lämpö- ja virtabudjetille?**
3. **Haluanko työkalun vai uuden sivuprojektin?**

Jos kaikki kolme saavat hyvän vastauksen, käytetty datakeskus-GPU voi olla erinomainen löytö. Jos yksikin jää epäselväksi, halpa hinta on helposti ansa eikä etu.

Paikallisessa LLM-käytössä paras rauta ei ole se, joka näyttää eksoottisimmalta käytettyjen osien listassa. Paras rauta on se, joka jaksaa ajaa omaa työkuormaasi vakaasti, viileästi ja ennustettavasti päivästä toiseen.

## Lähteet

- https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/Tesla-P40-Product-Brief.pdf
- https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-t4/t4-tensor-core-product-brief.pdf
- https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/cooling.html
