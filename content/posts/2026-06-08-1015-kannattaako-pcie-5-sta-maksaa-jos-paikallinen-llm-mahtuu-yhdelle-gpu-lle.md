---
title: "Kannattaako PCIe 5.0:sta maksaa, jos paikallinen LLM mahtuu yhdelle GPU:lle?"
date: "2026-06-08T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "PCIe"
  - "GPU"
  - "Local LLM"
  - "Ollama"
  - "Hardware"
---
Paikallista LLM-konetta suunnitellessa yksi helppo ansa on maksaa emolevystä ja alustasta siksi, että laatikossa lukee **PCIe 5.0**. Paperilla kaistaa on enemmän, mutta käytännössä oikea kysymys on paljon arkisempi: **hyötyykö paikallinen LLM-ajosi siitä lainkaan, jos malli mahtuu jo kokonaan yhdelle GPU:lle?** Useimmille harrastajille vastaus on yllättävän tylsä: **ei kovin paljon**. Jos malli pysyy yhdellä näytönohjaimella, tärkeämpiä asioita ovat yleensä VRAM-määrä, jäähdytys, virtalähde ja se, ettei kone pakota ajoa CPU:n puolelle.

Ollaman FAQ antaa tähän hyvän käytännön perussäännön. Jos uusi malli mahtuu kokonaan yhdelle GPU:lle, Ollama yrittää ladata sen yhdelle kortille, koska se antaa tyypillisesti parhaan suorituskyvyn ja vähentää datan siirtämistä PCIe-väylän yli inferenssin aikana. Tämä on tärkein vihje koko ostopäätöstä varten: jos tavoitteesi on ajaa yksi malli yhdellä kortilla, **PCIe-version nosto ei tavallisesti ole ensimmäinen pullonkaula**.

## Mitä PCIe 5.0 oikeasti ostaa sinulle?

NVIDIAn omissa A100-materiaaleissa PCIe Gen4 x16 -yhteyden kaistaksi ilmoitetaan 64 GB/s kaksisuuntaisesti, kun taas vanhemmassa esitystavassa Gen3 x16 on noin puolet tästä. Toisin sanoen kaistaa on sukupolvien välillä paljon enemmän, mutta se ei automaattisesti tarkoita, että jokainen LLM-ajon vaihe hyötyisi siitä suoraan. LLM-inferenssissä arvokkain asia on yleensä se, että mallin painot ja KV-välimuisti pysyvät siellä missä niiden pitääkin: mahdollisimman paljon GPU:n omassa muistissa.

Tästä seuraa käytännön sääntö: **PCIe 5.0 auttaa eniten silloin, kun joudut jatkuvasti liikuttelemaan dataa hostin ja GPU:n välillä.** Jos et tee sitä, lisäkaista jää helposti varmuusmarginaaliksi eikä tunnu vastauksissa juuri lainkaan.

## Tilanne 1: yksi GPU, malli mahtuu kokonaan VRAMiin

Tämä on se tavallisin harrastajakoneen tavoitetila. Esimerkiksi jos ajat kvantisoitua 7B-, 14B- tai sopivasti valittua 32B-luokan mallia niin, että `ollama ps` näyttää `100% GPU`, PCIe 5.0 ei yleensä muuta käyttökokemusta ratkaisevasti. Ollaman dokumentaation perusteella paras suorituskyky tulee jo siitä, että ajo pysyy yhdellä kortilla eikä väylän yli tarvitse siirtää tavaraa kesken inferenssin.

Tässä tilanteessa maksaisin ennen PCIe 5.0 -alustaa mieluummin näistä:

- enemmän VRAMia
- hiljaisempi ja viileämpi kotelo
- enemmän RAMia, jos kone tekee muutakin kuin yhtä mallia
- parempi SSD, jos mallien latausajat ärsyttävät

Jos käyttö on "avaa malli, aja prompti, odota vastaus", PCIe 5.0 on usein luksusta, ei ratkaisu.

## Tilanne 2: osa ajosta vuotaa CPU:n puolelle

Kuva muuttuu heti, jos malli ei enää mahdu siististi yhdelle GPU:lle. Silloin väylän yli siirtyy enemmän dataa, ja PCIe-nopeudella alkaa olla enemmän merkitystä. Mutta tässäkin kohtaa on syytä huomata tärkeä ero: **nopeampi PCIe ei korjaa sitä, että varsinainen ongelma on liian pieni VRAM**.

Käytännössä tämä tarkoittaa:

1. Jos ajo on osittain CPU/GPU-hybridiä, PCIe 5.0 voi lieventää haittaa.
2. Se ei silti tee hybridiajosta samaa asiaa kuin "malli mahtuu kokonaan GPU:lle".
3. Jos budjetti on rajallinen, suurempi VRAM-kortti on usein arvokkaampi kuin hienompi PCIe-sukupolvi.

Toisin sanoen PCIe 5.0 auttaa enemmän kompromissin siivoamisessa kuin varsinaisen pullonkaulan poistamisessa.

## Tilanne 3: useita GPU:ita tai leveämpi kotilabra

Moni alkaa miettiä PCIe 5.0:aa vasta silloin, kun koneessa on kaksi korttia, useita NVMe-levyjä ja ehkä verkkokortti samalla alustalla. Tässä kohdassa väylä- ja kaistajakoon liittyvät päätökset ovat oikeasti kiinnostavia. NVIDIAn sertifioitujen PCIe-palvelimien ohjeissa todetaan suoraan, että yksi Gen5 x16 tai Gen4 x16 -linkki per GPU on ihannetila, mutta myös Gen5 tai Gen4 x8 -linkit ovat tuettuja. Harrastajalle tämä on hyvä muistutus siitä, että pelkkä "kortti ei saa täyttä x16-kaistaa" ei vielä tarkoita katastrofia.

Käytännössä kannattaa kysyä:

- Onko sinulla yksi GPU vai kaksi?
- Jaatko kaistat usean NVMe-levyn, capture-kortin tai nopean verkon kanssa?
- Aiotko ajaa mallia yhdellä kortilla vai levittää sitä usealle GPU:lle?

Jos vastaus on "yksi GPU ja pari levyä", PCIe 5.0 on usein helpompi markkinointilause kuin todellinen nopeusetu. Jos vastaus on "kaksi GPU:ta ja ahdas kaistabudjetti", alustan laatu alkaa vaikuttaa oikeasti.

## Milloin maksaisin PCIe 5.0:sta ilman mutinaa?

Maksaisin siitä todennäköisemmin, jos ainakin kaksi seuraavista pitää paikkansa:

- rakennat uutta konetta nimenomaan usean GPU:n käyttöön
- tiedät jo nyt ajavasi malleja, jotka vuotavat usein hostimuistiin
- tarvitset paljon nopeaa I/O:ta samaan aikaan
- haluat pitää alustan käytössä useamman GPU-sukupolven yli

Silloinkin perustelu on usein enemmän **alustan jousto** kuin välitön token/s-hyppy.

## Oma nyrkkisääntö

Jos paikallinen LLM mahtuu yhdelle GPU:lle ja tavoitteena on hyvä hinta-suorituskykysuhde, en maksaisi PCIe 5.0:sta ennen kuin nämä ovat kunnossa:

1. riittävä VRAM
2. riittävä RAM
3. vakaa jäähdytys ja virransyöttö
4. järkevä levytila malleille

Vasta tämän jälkeen kysyisin, rajoittaako alusta oikeasti käyttöäni. Monessa kotilabrassa vastaus on edelleen "ei vielä".

## Tiivis johtopäätös

Jos paikallinen LLM mahtuu kokonaan yhdelle GPU:lle, **PCIe 5.0 ei yleensä ole paras ensimmäinen paikka käyttää rahaa**. Se muuttuu kiinnostavammaksi vasta silloin, kun koneessa on useita GPU:ita, raskas I/O-kuorma tai jatkuvaa CPU/GPU-offloadia. Useimmille harrastajille nopein parannus tulee edelleen siitä, että malli pysyy kokonaan oikean kokoisessa VRAMissa, ei siitä että väylä päivittyy paperilla seuraavaan sukupolveen.

## Lähteet

- https://docs.ollama.com/faq
- https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet.pdf
- https://docscontent.nvidia.com/dita/00000186-f233-d445-afc6-fa7767080000/ngc/ngc-deploy-on-premises/pdf/nvidia-certified-configuration-guide.pdf
