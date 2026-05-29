---
title: "AI-rauta kotilabrassa: kannattaako DDR5-6000 paikalliseen LLM-ajoon?"
date: "2026-03-28T10:15:00+02:00"
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
Kun paikallista LLM-konetta suunnitellaan, huomio menee lähes aina ensimmäisenä GPU:hun ja VRAMiin. Se on yleensä oikea lähtökohta, mutta CPU-painotteisessa ajossa moni jättää yhden käytännön kysymyksen liian vähälle huomiolle: **kannattaako nopeammasta DDR5-muistista oikeasti maksaa?**

Lyhyt vastaus on tämä: **jos ajat mallia pääosin järjestelmämuistista CPU:lla, DDR5-nopeudella voi olla selvä vaikutus tokeninopeuteen. Jos taas ajat mallin kunnolla GPU:lla, RAM-nopeus on yleensä paljon pienempi tekijä kuin VRAMin määrä ja näytönohjaimen oma muistiväylä.**

Tämä on tärkeä ero, koska moni rakentaa väärän koneen väärään käyttötapaan. Ostetaan kallis DDR5-kit toivoen ihmettä, vaikka todellinen pullonkaula olisi edelleen 12 Gt VRAM. Tai toisin päin: yritetään säästää muistissa, vaikka juuri CPU-ajossa muistibandwidth ratkaisee paljon enemmän kuin muutama lisäkellotaajuus prosessorissa.

## Mitä nopeampi DDR5 käytännössä antaa?

Maxim Saplinin julkaisemassa käytännön testissä verrattiin DDR5-4800- ja DDR5-6000-muisteja paikallisen LLM-ajon yhteydessä. Tulokset olivat harrastajan näkökulmasta yllättävän isoja: siirtymä 4800 MT/s -tasolta 6000 MT/s -tasolle toi noin **20–23 prosentin parannuksen generointinopeuteen** CPU-painotteisessa ajossa kahdella eri mallilla.

Se on tarpeeksi suuri ero, että sen huomaa oikeassa käytössä. Jos kone tuottaa esimerkiksi 4 tokenia sekunnissa, 20 prosentin parannus ei tee siitä rakettia, mutta se voi siirtää kokemuksen sietämättömästä juuri ja juuri käyttökelpoiseksi. Jos taas puhutaan 9–10 tokenin sekuntinopeudesta, sama prosenttiero tekee keskustelusta jo selvästi sulavamman.

Käytännön opetus ei kuitenkaan ole vain "osta mahdollisimman nopeat muistit". Vielä tärkeämpi havainto samasta testistä oli tämä: **kahden muistikamman kokoonpano oli parempi kuin neljän kamman kokoonpano**, koska neljällä kammalla kuluttaja-alustalla ei yleensä päästä yhtä korkeisiin muistinopeuksiin vakaasti. Toisin sanoen oikein valittu 2 x 32 Gt voi olla LLM-käytössä järkevämpi kuin 4 x 16 Gt, vaikka kokonaiskapasiteetti näyttäisi paperilla samalta.

## Missä tilanteessa DDR5-6000 on järkevä valinta?

DDR5-6000 alkaa olla järkevä, kun kaikki seuraavat pitävät edes suunnilleen paikkansa:

- ajat mallia usein kokonaan tai suurelta osin CPU:lla
- käytössäsi on paljon RAMia mutta niukasti VRAMia
- haluat puristaa kuluttaja-alustasta kaiken irti ilman siirtymistä työasema- tai palvelinrautaan
- rakennat uutta AM5- tai muuta DDR5-kokoonpanoa muutenkin

Tällöin nopeampi RAM ei ole kosmeettinen lisä vaan osa varsinaista suorituskykyä. Paikallinen LLM ei CPU-ajossa odota niinkään uusia ALU-ihmeitä vaan sitä, että mallin painoja saadaan liikutettua muistista tarpeeksi nopeasti.

## Milloin DDR5-6000 ei ole se oikea päivitys?

Monessa kotilabrassa vastaus on silti: **ei vielä**.

Jos ajat 7B–14B malleja pääosin näytönohjaimella ja malli mahtuu hyvin VRAMiin, järjestelmämuistin nopeus ei yleensä ole paras paikka käyttää rajallista budjettia. Silloin käytännön hyöty tulee useammin näistä:

- enemmän VRAMia
- parempi GPU:n muistibandwidth
- riittävästi järjestelmä-RAMia, jotta offload ei kaadu kapasiteettirajaan
- nopea NVMe, jos vaihdat malleja usein

LocalAI Computerin laaja laiteopas tiivistää tämän hyvin: **DDR5 on CPU-inferenssissä selvästi DDR4:ää nopeampi, mutta GPU-ajossa RAMin nopeus merkitsee vähemmän kuin GPU-valinta itse.** Tämä on hyvä vastalääke yliyksinkertaistetulle "osta vain nopein muisti" -neuvolla.

## Aloittelijan yleinen virhe

Tavallinen virhe näyttää tältä:

1. hankitaan 12 Gt tai 16 Gt GPU
2. huomataan, että suuremmat mallit eivät oikein mahdu tai offload hidastaa
3. päätellään, että ongelma ratkeaa nopeammalla DDR5:llä

Jos malli ei mahdu kunnolla VRAMiin, DDR5-6000 voi kyllä auttaa CPU-puolen hitautta, mutta se ei poista perusongelmaa. Se tekee usein hitaasta ajosta vähemmän hidasta, ei taio siitä GPU-tasoista kokemusta.

Siksi muistipäivitystä kannattaa arvioida näin:

- **CPU-painotteinen ajo:** nopeampi DDR5 voi olla aidosti hyvä sijoitus
- **GPU-painotteinen ajo:** priorisoi ensin VRAM ja GPU
- **Sekakäyttö / osittainen offload:** hyötyä voi tulla, mutta ihmettä ei kannata odottaa

## Entä kapasiteetti vastaan nopeus?

Tässä kohtaa moni joutuu oikeaan kompromissiin. Paikallisessa LLM-ajossa kapasiteetti on edelleen portinvartija: jos RAM ei riitä, ajo ei onnistu tai se menee levyvatkaukseksi. Mutta kun kapasiteetti on jo riittävä, nopeus alkaa vaikuttaa oikeasti käyttökokemukseen.

Käytännöllinen nyrkkisääntö kotilabraan voisi olla tämä:

- 32 Gt on pieni mutta usein käyttökelpoinen aloitustaso kevyemmille malleille
- 64 Gt on paljon mukavampi taso, jos kokeilet useampia malleja tai teet CPU-offloadia
- sen jälkeen kannattaa miettiä, saatko enemmän hyötyä lisäkapasiteetista vai nopeammasta muistista

Jos valinta on 96 Gt hitaampaa neljällä kammalla vastaan 64 Gt nopeampaa kahdella kammalla, oikea vastaus riippuu siitä, törmäätkö nykyään useammin kapasiteettirajaan vai odotatko vain tuskastuttavan hitaasti vastauksia. LLM-käytössä nämä ovat eri ongelmia, eikä niitä kannata sekoittaa keskenään.

## Oma käytännön johtopäätökseni

Jos rakentaisin tänään **kuluttajahintaisen CPU-painotteisen paikallisen LLM-koneen**, yrittäisin osua ensin riittävään kapasiteettiin ja sen jälkeen mahdollisimman järkevään kaksikampaiseen DDR5-nopeuteen, en maksimoisi muistitikkujen määrää. DDR5-6000 ei ole taikatemppu, mutta se näyttää olevan tarpeeksi iso parannus, että sillä on merkitystä oikeassa käytössä.

Jos taas rakentaisin **ensisijaisesti GPU-koneen**, käyttäisin saman budjetin mieluummin parempaan näytönohjaimeen tai suurempaan VRAM-luokkaan kuin muistien hienosäätöön.

Toisin sanoen kysymys ei ole "onko DDR5-6000 nopea", vaan **mihin pullonkaulaan yrität oikeasti osua**. Juuri siinä kohtaa moni paikallisen AI-raudan hankinta onnistuu tai menee vähän vinoon.

## Lähteet

- Maxim Saplin, DDR5 Speed, CPU and LLM Inference: https://dev.to/maximsaplin/ddr5-speed-and-llm-inference-3cdn
- LocalAI Computer, LLM Hardware Guide: https://localai.computer/learn/llm-hardware-guide
- Hardware Corner, Memory Bandwidth: How Does It Boost Tokens per Second in Local LLM Inference?: https://www.hardware-corner.net/memory-bandwidth-llm-speed/
