---
title: "Tarvitsetko NVLinkiä kahden GPU:n paikalliseen LLM-koneeseen?"
date: "2026-08-28T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "llm-hardware"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "gpu"
  - "nvlink"
  - "llama-cpp"
  - "vllm"
---
## Tiivistelmä
Et yleensä tarvitse NVLinkiä siksi, että saisit kahden GPU:n paikallisen LLM-koneen ylipäätään toimimaan. **Tarvitset sitä lähinnä silloin, kun tavoite ei ole vain saada malli mahtumaan, vaan myös pitää GPU:iden välinen liikenne tarpeeksi nopeana tensoririnnakkaisuudelle tai muuten viestintäherkälle ajolle.** Tavalliselle harrastajalle käytännön sääntö on tämä: **jos kaksi korttia kiinnostaa kapasiteetin takia, kokeile ensin tavallista PCIe-pohjaista layer- tai pipeline-jakoa. Jos taas haet nimenomaan parempaa token-nopeutta monen GPU:n ajossa, NVLinkin puute alkaa tuntua paljon enemmän.**

## Mikä NVLinkissä on paikalliselle LLM-harrastajalle olennaista

NVLink kuulostaa helposti maagiselta ominaisuudelta, joka "yhdistää kaksi GPU:ta yhdeksi isoksi". Käytännössä se ei tee sitä. Se antaa GPU:ille nopeamman tavan siirtää dataa keskenään kuin tavallinen PCIe-pohjainen liikenne, jos ohjelmisto ja rauta osaavat hyödyntää sitä.

NVIDIA kuvaa CUDA-ohjeessaan asian varsin suoraan: kun peer-to-peer-muistipääsy on mahdollinen, CUDA voi hyödyntää siihen omia siirtomoottoreita ja NVLink-rautaa paremman suorituskyvyn saamiseksi. Tästä ei kuitenkaan seuraa, että kaikki paikallinen LLM-ajo tarvitsee NVLinkiä. Siitä seuraa vain, että **GPU:iden välinen keskustelu on arvokkaampaa silloin, kun sitä todella tapahtuu paljon**.

Siksi ensimmäinen kysymys ei ole "onko koneessa NVLink", vaan:

1. pitääkö malli jakaa usealle GPU:lle lainkaan
2. millä tavalla backend jakaa mallin
3. syntyykö työkuormassa paljon GPU:iden välistä liikennettä

## Milloin kaksi GPU:ta toimii ihan hyvin ilman NVLinkiä

`llama.cpp`:n nykyinen multi-GPU-ohje sanoo, että monen GPU:n käyttöä kannattaa harkita kahdessa tilanteessa: kun malli ei mahdu yhden GPU:n VRAMiin tai kun halutaan lisää throughputia. Samassa ohjeessa tärkeä yksityiskohta on se, että oletusmalli `layer` eli pipeline-rinnakkaisuus on nimenomaan se turvallisempi ja yhteensopivampi polku. Dokumentaatio sanoo myös suoraan, että tämä tila sietää hitaitakin GPU-välisiä yhteyksiä paremmin.

Tämä on tavalliselle kotilabralle hyvä uutinen. Jos ongelmasi on:

- 24 Gt ei enää riitä mallille ja KV-cachelle
- haluat pitää mallin poissa järjestelmämuistista
- hyväksyt sen, ettei kahden GPU:n ratkaisu ole automaattisesti nopeusihme

silloin kaksi korttia voi olla täysin järkevä ratkaisu ilman NVLinkiäkin. Tavoite on tällöin ennen kaikkea saada koko malli pysymään kiihdytettynä, ei rakentaa täydellistä HPC-väylää työpöydälle.

## Milloin NVLinkin puute alkaa oikeasti haitata

NVLink alkaa merkitä enemmän silloin, kun valittu ajotapa vaihtuu kapasiteettiratkaisusta suorituskykyratkaisuksi.

`llama.cpp`:n dokumentaatiossa `tensor`-split on merkitty kokeelliseksi mutta samalla juuri nopeampaa token-generaatiota hakevaksi tilaksi. Samassa kohdassa todetaan, että hyöty riippuu paljon GPU-interconnectin nopeudesta. Tämä on käytännössä suora vihje siitä, että **mitä enemmän työkuorma nojaa hienojakoiseen GPU-yhteistyöhön, sitä vähemmän "ihan tavallinen PCIe kyllä riittää" on varma oletus**.

vLLM sanoo saman vielä selkeämmin palvelinpuolen näkökulmasta. Sen virallinen rinnakkaisuusohje neuvoo käyttämään tensoririnnakkaisuutta, jos malli ei mahdu yhdelle GPU:lle mutta mahtuu yhdelle monen GPU:n solmulle. Mutta sama ohje lisää tärkeän poikkeuksen: **jos saman koneen GPU:illa ei ole NVLink-yhteyttä, pipeline parallelism voi olla parempi valinta korkeamman läpimenon ja pienemmän viestintäkulun takia**.

Tästä vedän harrastajalle hyvin käytännöllisen johtopäätöksen:

- **ei NVLinkiä + tavoite on vain mahtuminen** -> kahden GPU:n kone voi silti olla hyvä
- **ei NVLinkiä + tavoite on aggressiivinen tensoririnnakkaisuus** -> odota enemmän säätöä ja vähemmän varmaa nopeushyötyä

## Missä moni tulkitsee kahden GPU:n koneen väärin

Yleinen virhe on ajatella, että kaksi GPU:ta ilman NVLinkiä olisi automaattisesti "väärä" kokoonpano. Minusta se on liian jyrkkä tulkinta. Väärä kokoonpano on ennemmin sellainen, jossa odotukset ja todellinen käyttö eivät kohtaa.

Jos haluat ajaa suurempaa mallia paikallisesti ja hyväksyt, että nopeus ei skaalaudu lineaarisesti, tavallinen PCIe-pohjainen kahden GPU:n kone voi olla täysin hyvä harrastajaratkaisu. Jos taas ostat toisen kortin siinä toivossa, että yksittäinen keskustelu muuttuu lähes kaksinkertaisen nopeaksi ilman erityistä optimointia, petyt helpommin.

Toinen usein unohdettu asia tulee `llama.cpp`:n build-ohjeesta. Siellä `GGML_CUDA_P2P` kuvataan keinoksi sallia GPU:iden suorat siirrot ilman että data kiertää järjestelmämuistin kautta, mutta dokumentaatio varoittaa samalla että tuki riippuu ajureista ja on usein enemmän workstation- tai datacenter-luokan etu. Lisäksi se voi joissain kokoonpanoissa aiheuttaa kaatumisia tai vioittunutta tulostetta.

Tämä on tärkeä realismitarkistus: **NVLinkin puute ei ole ainoa monen GPU:n ongelma, eikä NVLinkin olemassaolo yksin tee rakenteesta huoletonta.**

## Miten päättäisin ostoksen käytännössä

Jos rakentaisin tänään kahden GPU:n paikallista LLM-konetta, käyttäisin tätä päätöspolkua:

1. Jos malli mahtuu yhdelle järkevän hintaiselle GPU:lle, ostaisin mieluummin yhden isomman kortin.
2. Jos malli ei mahdu yhdelle GPU:lle, mutta backend tukee layer- tai pipeline-jakoa hyvin, hyväksyisin kahden GPU:n PCIe-koneen ilman NVLinkiä.
3. Jos tavoite on nimenomaan puristaa parempaa token-nopeutta tensoririnnakkaisuudella, pitäisin NVLinkiä tai muuten erittäin hyvää GPU-välistä yhteyttä selvästi arvokkaampana.
4. Jos koko suunnitelma nojaa peer-to-peer-ominaisuuksiin, tarkistaisin etukäteen ajurit, emolevyn, BIOS-asetukset ja backendin oikean tuen enkä luottaisi pelkkään markkinointisanaan.

Toisin sanoen NVLink kannattaa ajatella suorituskyvyn ja viestintätehokkuuden parantajana, ei pääsylippuna siihen että multi-GPU olisi mahdollinen.

## Milloin en maksaisi NVLinkistä ekstraa

En maksaisi NVLinkistä tai sitä vastaavasta premiumista, jos:

- ajat pääosin yhtä mallia interaktiivisesti
- tavoite on vain saada suurempi malli mahtumaan
- käytät pipeline-tyyppistä jakoa
- koko budjetti on muutenkin kireä

Näissä tilanteissa raha tuottaa usein enemmän hyötyä lisä-VRAMina, hiljaisempana jäähdytyksenä, parempana virtalähteenä tai yksinkertaisesti vähemmän ongelmallisena kokonaisuutena.

## Milloin pitäisin sitä oikeasti arvokkaana

Pitäisin NVLinkiä aidosti hyödyllisenä, jos:

- ajat toistuvasti monen GPU:n tensoririnnakkaisuutta
- työkuormassa on paljon GPU:iden välistä liikennettä
- haluat maksimoida läpimenon etkä vain saada mallia käyntiin
- rakennat enemmän palvelinta kuin harrastelutyöasemaa

Tässä kohtaa puhutaan jo eri luokan prioriteeteista kuin tavallisessa "saanko 70B-luokan mallin pyörimään kotona" -projektissa.

## Johtopäätös

Tarvitsetko NVLinkiä kahden GPU:n paikalliseen LLM-koneeseen? **Useimmiten et, jos päätavoite on kapasiteetti.** Tarvitset sitä paljon todennäköisemmin silloin, kun yrität tehdä monen GPU:n ajosta myös aidosti tehokasta viestinnän kannalta, etenkin tensoririnnakkaisuudessa. Harrastajalle paras nyrkkisääntö on siis tylsä mutta hyödyllinen: **osta ensin ratkaisu, jolla malli mahtuu ja backend toimii vakaasti; maksa nopeammasta GPU-interconnectista vasta, jos mittaukset näyttävät sen olevan oikea pullonkaula.**

## Lähteet

- llama.cpp multi-GPU docs: https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md
- llama.cpp build docs: https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md
- NVIDIA CUDA Programming Guide, multi-GPU systems: https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/multi-gpu-systems.html
- vLLM Parallelism and Scaling: https://docs.vllm.ai/en/stable/serving/parallelism_scaling/
