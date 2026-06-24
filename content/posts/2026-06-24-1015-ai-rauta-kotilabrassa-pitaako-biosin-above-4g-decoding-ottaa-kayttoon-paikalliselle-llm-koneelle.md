---
title: "AI-rauta kotilabrassa: pitääkö BIOSin Above 4G Decoding ottaa käyttöön paikalliselle LLM-koneelle?"
date: "2026-06-24T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-rauta kotilabrassa"
tags:
  - "AI-rauta"
  - "BIOS"
  - "PCIe"
  - "Paikalliset LLM:t"
---
Kun paikallista LLM-konetta kasaava ihminen käy BIOS-asetuksia läpi, vastaan tulee usein kaksi lähes peräkkäistä kohtaa: `Above 4G Decoding` ja `Resizable BAR`. Moni laittaa jälkimmäisen päälle, jos ylipäätään muistaa, mutta jättää ensimmäisen rauhaan, koska nimi kuulostaa vanhalta yhteensopivuusvivulta. Oma käytännön sääntöni on tämä: **jos koneessa on yksi tehokas GPU, useampi PCIe-laite tai tarkoitus käyttää suuria BAR-muistialueita, Above 4G Decoding kannattaa yleensä ottaa käyttöön.** Se ei tee koneesta itsestään nopeaa, mutta se poistaa yhden turhan resurssirajan muistialueiden allokoinnista.

Paikallisen LLM-harrastajan kannalta tärkein ajatus on yksinkertainen. GPU ei ole vain laskentalaite, vaan myös iso joukko PCIe:n yli kartoitettuja muistialueita ja ohjausrekistereitä. Kun VRAM, BAR-ikkunat tai usean laitteen MMIO-varaukset kasvavat, alle 4 gigatavun osoitealue käy helposti ahtaaksi. Silloin ongelma ei näy muodossa "tokenit sekunnissa putosivat 7 %", vaan paljon tylsempinä oireina: laite ei alustukaan oikein, ReBAR ei aktivoidu, monen kortin kokoonpano käyttäytyy oudosti tai kernel joutuu kikkailemaan resurssien kanssa.

## Mitä Above 4G Decoding oikeasti tekee

AMD:n ROCm-dokumentaatio kuvaa asian hyvin maanläheisesti. BIOS jakaa käynnistyksessä fyysistä osoiteavaruutta sekä järjestelmämuistille että PCIe-laitteiden MMIO-alueille. Nykyaikaisessa 64-bittisessä koneessa näitä alueita voidaan sijoittaa myös yli 4 gigatavun osoitealueelle. Juuri tätä `Above 4G Decoding` käytännössä mahdollistaa: laitteiden muistialueita ei tarvitse ahtaa kokonaan vanhaan alle-4G-tilaan.

NVIDIAn omassa dokumentaatiossa suositus on hyvin suora. `Above 4G Decoding` kannattaa ottaa käyttöön ominaisuuksille, jotka tarvitsevat paljon PCIe-resursseja, ja esimerkeiksi annetaan muun muassa suuret BAR-pyynnöt. Tämä on hyvä käännös harrastajakielelle: jos haluat hyödyntää ReBARia, käytät raskasta GPU:ta tai rakennat koneen, jossa PCIe-laitteita on paljon, kyse ei ole turhasta serveriasetuksesta vaan käytännön yhteensopivuusasiasta.

## Miksi tämä kiinnostaa juuri paikallista LLM-konetta

Paikallisessa LLM-ajossa näytönohjaimella on tavallista enemmän väliä myös muistilaitteena. Vaikka itse inferenssi tapahtuisi siististi GPU:lla, kone voi silti tarvita:

- suuren framebufferin BAR-kartoituksia
- ReBARin tai muun large BAR -tuen aktivoitumista
- usean GPU:n, nopean verkko- tai tallennuskortin rinnakkaista MMIO-tilaa

Jos ajat vain yhdellä maltillisella kortilla eikä BIOSissa ole koskaan ollut ongelmia, et ehkä huomaa mitään eroa. Mutta jos kasaat 24 GB tai 48 GB VRAM -luokan kortin ympärille työasemaa, käytät adaptereita, bifurkaatiota tai useita lisäkortteja, tämä asetus kannattaa tarkistaa ennen kuin syytät käyttöjärjestelmää, ajureita tai itse mallia.

## Milloin ottaisin sen käyttöön epäröimättä

Ottaisin `Above 4G Decodingin` käyttöön lähes automaattisesti näissä tilanteissa:

- käytössä on moderni erillinen GPU ja BIOS tukee myös `Resizable BAR` -asetusta
- koneessa on useampi PCIe-laite, joilla on isoja muistialueita
- suunnittelet kahden GPU:n tai GPU + nopea NIC / HBA -kokoonpanoa
- yrität selvittää, miksi large BAR tai ReBAR ei aktivoidu oikein

Jättäisin asetuksen rauhaan lähinnä silloin, jos laitteisto on vanha, BIOS on tunnetusti herkkä tai valmistaja dokumentoi juuri kyseiseen kokoonpanoon poikkeuksen. Tavallisessa 2026 harrastajakoneessa oletusarvo on minusta päinvastainen: tämä kannattaa ennemmin laittaa päälle kuin jättää pois.

## Milloin tämä ei auta

On hyvä pitää odotukset oikeina. `Above 4G Decoding`:

- ei lisää VRAM-määrää
- ei nopeuta mallia yksinään samalla tavalla kuin suurempi GPU
- ei korjaa liian hidasta RAMia tai liian kapeaa PCIe-linkkiä
- ei ratkaise sitä, että malli ei mahdu järkevästi GPU:lle

Linux-kernelin dokumentaatiossa näkyy myös toinen hyödyllinen opetus: jos PCIe-resurssit eivät muuten riitä, kernelissä on olemassa jopa erillisiä mekanismeja kuten `big_root_window`, joilla voidaan yrittää lisätä isoa 64-bittistä muistialuetta root complexille AMD-koneissa. Minun tulkintani tästä on käytännöllinen: **oikea ratkaisu on ensisijaisesti kuntoon laitettu BIOS, ei se että käyttöjärjestelmä pakotetaan paikkaamaan huonoa firmware-konfiguraatiota jälkikäteen**.

## Käytännön tarkistuslista

Jos rakennat tai päivität paikallista LLM-konetta, tekisin tämän järjestyksessä:

1. Päivitä emolevyn BIOS uusimpaan vakaaseen versioon.
2. Varmista, että kone käynnistyy UEFI-tilassa eikä vanhassa CSM/Legacy-tilassa.
3. Ota käyttöön `Above 4G Decoding`.
4. Ota sen jälkeen käyttöön `Resizable BAR`, jos laitteisto tukee sitä.
5. Käynnistyksen jälkeen tarkista käyttöjärjestelmästä tai valmistajan työkaluista, että laitteet näkyvät oikein eikä ajuri raportoi resurssiongelmia.

Jos jokin näistä epäonnistuu, en lähtisi ensimmäiseksi metsästämään "taika-asetuksia" kernel-parametreista. Pysähtyisin tarkistamaan, onko ongelma oikeasti BIOS-tasolla, laitteiden fyysisessä kokoonpanossa vai yksinkertaisesti siinä, että emolevy ei tue tavoiteltua yhdistelmää kunnolla.

## Yhteenveto

**Above 4G Decoding on paikallisen LLM-koneen näkökulmasta perusasetuksia, ei eksoottinen palvelinviritys.** Se on erityisen järkevä, kun käytössä on paljon GPU-muistia, ReBAR, useita lisäkortteja tai muuten vain kunnianhimoinen PCIe-kokoonpano. Jos kone on moderni ja BIOS tarjoaa asetuksen, laittaisin sen yleensä päälle jo ennen varsinaisia suorituskykytestejä.

Tämä ei ehkä ole näyttävin optimointi, mutta juuri tällaiset ilmaiset BIOS-valinnat erottavat usein siistin LLM-työaseman siitä, että samaa ongelmaa yritetään myöhemmin korjata ostamalla lisää rautaa.

## Lähteet

- https://docs.nvidia.com/networking/display/winof2v280/bios+settings+configuration
- https://rocm.docs.amd.com/en/latest/how-to/Bar-Memory.html
- https://docs.kernel.org/6.15/admin-guide/kernel-parameters.html
- https://docs.kernel.org/6.2/admin-guide/abi-testing.html
