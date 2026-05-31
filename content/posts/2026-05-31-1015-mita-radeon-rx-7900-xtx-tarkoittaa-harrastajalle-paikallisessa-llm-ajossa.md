---
title: "Mitä Radeon RX 7900 XTX tarkoittaa harrastajalle paikallisessa LLM-ajossa?"
date: "2026-05-31T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-rauta kotilabrassa"
tags:
  - "AMD"
  - "Radeon"
  - "Local LLM"
  - "Hardware"
  - "ROCm"
---
Radeon RX 7900 XTX näyttää paikallista LLM-konetta rakentaessa houkuttelevalta juuri siitä syystä, jota harrastajat etsivät: **24 GB VRAMia ilman datakeskus-GPU:n hintaa**. Siksi oikea kysymys ei ole "onko se nopea näytönohjain", vaan **onko se käytännössä järkevä kortti juuri sinun paikalliseen mallipinoosi**. Minun lyhyt vastaukseni on tämä: **7900 XTX on edelleen hyvä ostos, jos tavoittelet 24 GB luokan muistia yhdelle GPU:lle ja hyväksyt ROCm/HIP-polun mukana tulevan käytännön säätämisen.** Jos taas haluat minimoida asennuskitkan ja seurata valmiita ohjeita lähes yksi yhteen, tarkista tavallista tarkemmin, että oma softapolkusi tukee AMD:tä eikä oleta suoraan CUDAa.

## Mitä kortti antaa oikeasti paikalliselle LLM-koneelle

AMD:n omien speksien mukaan Radeon RX 7900 XTX tarjoaa 24 GB GDDR6-muistia, 384-bittisen muistiväylän ja 355 W kokonaiskorttitehon. Käytännössä tämä osuu juuri siihen luokkaan, joka tekee yhdestä kortista kiinnostavan paikallisille malleille: 24 GB on jo tarpeeksi, jotta moni 7B-14B malli toimii mukavasti korkeammillakin konteksteilla, ja myös 20B-32B luokan kvantisoidut mallit muuttuvat realistisiksi ainakin osittain GPU:lle offloadattuina.

Tärkein hyöty ei siis ole vain raakanopeus vaan se, että **24 GB VRAM vähentää tarvetta jatkuville kompromisseille**. Kun et elä 8-12 GB luokan muistibudjetissa, sinun ei tarvitse yhtä usein valita pienimmän kvantisoinnin, matalimman kontekstin tai aggressiivisimman CPU-offloadin välillä.

## Missä 7900 XTX on aidosti hyvä valinta

Kortti on minusta erityisen järkevä kolmessa tilanteessa:

- haluat yhden kuluttajaluokan GPU:n, jolla pääsee selvästi yli 16 GB VRAM -rajan
- käytät Ollamaa tai `llama.cpp`:tä ympäristössä, jossa AMD-tuki on jo dokumentoitu
- rakennat Linux-pohjaista kotilabra- tai työpöytäkoneympäristöä, jossa olet valmis asentamaan ROCm-ajurit kunnolla

Ollaman tämänhetkinen laitetukisivu listaa RX 7900 XTX:n tuettujen AMD-korttien joukkoon sekä Linuxissa että Windowsissa. Se on iso käytännön plussa, koska se poistaa yhden yleisimmistä epävarmuuksista: joudunko heti epäviralliseen viritykseen vai en. Samalla `llama.cpp` kertoo suoraan tukevansa AMD-GPU:ita HIP-polun kautta, ja projektin multi-GPU-ohje huomauttaa vielä erikseen, että ROCm-puolella voidaan käyttää RCCL:ää vastaavaan GPU-jakoon.

Toisin sanoen 7900 XTX ei ole enää "ehkä joskus toimiva AMD-kokeilu", vaan selvästi tuettu vaihtoehto useassa suositussa paikallispinossa.

## Missä harrastaja törmää kitkaan

Tähän korttiin liittyvä käytännön varoitus ei ole VRAM vaan ympäröivä ohjelmistopolku. Ollaman dokumentaatio sanoo suoraan, että AMD-käyttö nojaa ROCm-ajureihin, ja Linuxissa suositus on käyttää AMD:n ajankohtaista ROCm-polkuja eikä luottaa vain jakelun vanhempiin oletusajureihin. ROCm:n oma Linux-asennusdokumentaatio taas listaa RX 7900 XTX:n tuettuna RDNA3-laitteena, mikä on hyvä uutinen, mutta samalla muistutus siitä, että **AMD-polku toimii parhaiten, kun seuraat juuri ROCm:n tukematriisia etkä vanhaa satunnaista blogiopasta**.

Käytännössä tämä tarkoittaa:

- ajuriversioilla on enemmän merkitystä kuin moni ensikertalainen arvaa
- kaikki ohjeet eivät ole siirrettävissä suoraan NVIDIAlta AMD:lle
- päivityksissä kannattaa tarkistaa sekä inferenssityökalu että ROCm-versio

En siis ostaisi 7900 XTX:ää ihmiselle, joka haluaa "asennan tämän kerran ja unohdan koko pinon". Ostaisin sen ihmiselle, joka haluaa paljon VRAMia kuluttajahintaan ja hyväksyy sen, että ohjelmistopino on osa harrastusta.

## Entä teho, lämpö ja virtalähde

AMD:n omat speksit kertovat 355 W kokonaiskorttitehosta ja vähintään 800 W suositellusta virtalähteestä. Tämä on tärkeä realismitarkistus, koska 7900 XTX voi näyttää paperilla "edulliselta 24 GB kortilta", mutta koko koneen budjetti ei ole vain GPU:n hinta. Tarvitset myös:

- kunnollisen virtalähteen
- kotelon ja ilmankierron, jotka kestävät kuorman
- emolevyn ja alustan, joilla kortti mahtuu järkevästi käyttöön

Jos nykyinen koneesi on pieni, heikolla ilmanvaihdolla varustettu tai rajalla jo nykyisen GPU:n kanssa, 7900 XTX voi muuttua hyvästä diilistä kalliiksi sivupäivitykseksi. Silloin ostoslistaan tulee helposti mukaan uusi PSU ja joskus myös uusi kotelo.

## Milloin en suosittelisi tätä korttia

Jättäisin 7900 XTX:n väliin ainakin näissä tilanteissa:

- haluat mahdollisimman pienellä säätämisellä liikkeelle juuri nyt
- koneesi virtalähde ja jäähdytys ovat jo valmiiksi äärirajoilla
- todellinen mallitarpeesi mahtuu hyvin 12-16 GB luokkaan
- et ole valmis tarkistamaan ROCm-yhteensopivuutta aina kun vaihdat distroa, kernelversiota tai inferenssityökalua

Silloin kortin tärkein etu, 24 GB VRAM, ei välttämättä maksa itseään takaisin.

## Käytännön ostosuositus

Minun johtopäätökseni on tämä: **Radeon RX 7900 XTX on järkevä paikallisen LLM-koneen kortti silloin, kun tavoite on nimenomaan paljon VRAMia yhdelle GPU:lle ilman workstation-hintaluokkaa.** Se ei ole aloittelijan huolettomin mahdollinen polku, mutta se on selvästi realistinen ja tuettu polku.

Jos harkitset tätä korttia juuri nyt, tekisin päätöksen tällä lyhyellä tarkistuslistalla:

1. Tarvitsenko oikeasti 24 GB VRAMia vai ratkeaako nykyinen pullonkaula ensin RAM-, SSD- tai jäähdytyspäivityksellä?
2. Olenko valmis käyttämään Ollaman tai `llama.cpp`:n kanssa ROCm/HIP-pohjaista ympäristöä enkä vain CUDA-esimerkkejä?
3. Kestääkö nykyinen kone 355 W luokan GPU:n myös PSU:n ja lämpöjen kannalta?

Jos kaikkiin kolmeen tulee rehellinen kyllä, 7900 XTX on minusta edelleen yksi kiinnostavimmista harrastajatason korteista paikalliseen LLM-ajoon. Jos yksikin kohta tökkii, säästyneellä rahalla voi joskus tehdä kokonaisuutena paremman päivityksen muualle.

## Lähteet

- https://www.amd.com/en/products/graphics/desktops/radeon/7000-series/amd-radeon-rx-7900xtx.html
- https://docs.ollama.com/gpu
- https://github.com/ggml-org/llama.cpp
- https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md
- https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html
