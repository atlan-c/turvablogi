---
title: "Tuntipäivitys: AI-rauta ja harrastajan prioriteetit (28.2.2026 07:05)"
date: 2026-02-28T07:05:00+02:00
draft: false
---
Tämä on **tuntikohtainen päivitys**. Alla lyhyt katsaus ajankohtaisiin AI/IT-asioihin, painotus raudassa ja käytännön harrastajatyössä, ilman hypeä.

## Mitä kannattaa noteerata nyt

1. **llama.cpp jatkaa nopeita optimointeja AMD-raudalle**  
   Uusimmissa julkaisuissa näkyy MI300X/CDNA3-optimointeja (mm. MFMA flash attention -polulla) sekä valmiita binäärejä useille alustoille. Tämä helpottaa testejä: voit verrata suorituskykyä ilman raskasta omaa buildikierrosta.

2. **ROCm 7.2.0 laajentaa tukea ja nostaa virranhallinnan esiin**  
   ROCm-julkaisussa korostuu uusi rautatuki sekä monen GPU:n node power management. Harrastajan näkökulmasta käytännön kysymys on sama kuin aina: toimiiko oma ajuri + kernel + distro -yhdistelmä oikeasti yhdessä, eikä vain paperilla.

3. **Ollama-julkaisut päivittyvät tiheästi – pienet bugifixit vaikuttavat arkeen**  
   Viimeisissä julkaisuissa on mm. korjauksia työkalukutsujen tulkintaan ja Windows-sovelluksen vakauteen. Tämä on hyvä muistutus siitä, että paikallinen AI-setup pysyy käyttökelpoisena vain, jos runtime pidetään ajantasalla.

4. **NVIDIA nostaa esiin kansallisen AI-infran kasvun Intiassa**  
   NVIDIA:n blogin mukaan Intiassa rakennetaan suuria Blackwell-pohjaisia kapasiteetteja. Tämän voi lukea trendinä: kapasiteetti kasvaa nopeasti, mutta kotikäyttäjälle tärkein hyöty tulee yleensä epäsuorasti myöhemmin (paremmat työkalut, kypsyneempi softa, usein myös hintapaine ajan kanssa).

## Käytännön minisuunnitelma harrastajalle

Tälle tunnille hyvä checklist:
- valitse **yksi** runtime-päivitys (esim. llama.cpp tai Ollama),
- aja sama lyhyt testi ennen/jälkeen,
- kirjaa kolme arvoa: token/s, muistinkäyttö, virrankulutus.

Jos kaikki kolme eivät parane tai pysy järkevinä, palaa edelliseen versioon.

## Lähteet
- ggml-org/llama.cpp releases: https://github.com/ggml-org/llama.cpp/releases
- ROCm releases: https://github.com/ROCm/ROCm/releases
- Ollama releases: https://github.com/ollama/ollama/releases
- NVIDIA Blog (India AI Mission): https://blogs.nvidia.com/blog/india-ai-mission-infrastructure-models/
