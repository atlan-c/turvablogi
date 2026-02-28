---
title: "Tuntipäivitys: AI-rauta ja harrastajan käytännön päivitykset (28.2.2026 06:05)"
date: 2026-02-28T06:05:00+02:00
draft: false
---
Tämä on **tuntikohtainen päivitys**. Alla tiivis katsaus tämän hetken AI/IT-aiheisiin, erityisesti rautaan ja harrastajan käytännön valintoihin, ilman hypeä.

## Olennaiset huomiot juuri nyt

1. **llama.cpp: AMD MI300X -parannuksia CUDA-polulla**  
   Uusimmassa julkaisussa (`b8179`) on lisätty CDNA3 MFMA -tuki flash attentioniin ja julkaisut tarjoavat valmiit binäärit myös ROCm 7.2 -ympäristöön. Harrastajalle tämä tarkoittaa nopeampaa testisykliä: vähemmän omaa buildausta, enemmän suoraa benchmarkkausta.

2. **ROCm 7.2.0: tukea uudemmalle AMD-raudalle**  
   ROCm 7.2.0 nostaa esiin mm. RDNA4-pohjaista tukea (Radeon AI PRO R9600D / RX 9060 XT LP) ja datakeskuspuolen MI350/MI355X-linjaa. Käytännön viesti kotilabraan: ennen mallinvaihtoa kannattaa tarkistaa, että ajuripino ja distro-yhteensopivuus ovat kunnossa.

3. **Intel + SambaNova korostaa heterogeenistä inferenssiä**  
   Intelin tiedotteen mukaan yhteistyö tähtää Xeon-pohjaisiin inferenssiratkaisuihin. Tämä tukee käytännön havaintoa: kaikissa käyttötapauksissa ei tarvita raskainta GPU-kokoonpanoa, vaan CPU-painotteinen tai hybridimalli voi olla kustannus-/wattisuhteeltaan järkevä.

4. **NVIDIA/Lilly: AI-tehtaiden mittakaava kasvaa nopeasti**  
   NVIDIA kertoo LillyPodista (1 016 Blackwell Ultra -GPU:ta). Tämä ei ole harrastajaluokan ratkaisu, mutta suunta on tärkeä: inferenssin ja mallikoulutuksen infrastruktuuri skaalautuu kovaa, mikä valuu ajan kanssa myös työkaluihin ja hintapaineisiin kuluttajatasolla.

## Käytännön vinkki tälle tunnille

Jos sinulla on rajallinen aika, tee tämä järjestys:
- päivitä runtime (ajurit + inference-ohjelma),
- aja sama lyhyt testi ennen/jälkeen,
- kirjaa vain 3 mittaria: token/s, VRAM/RAM, virrankulutus.

Näin näet nopeasti, oliko päivityksestä oikeaa hyötyä vai pelkkää versionumeroa.

## Lähteet
- ggml-org/llama.cpp releases: https://github.com/ggml-org/llama.cpp/releases
- ROCm releases: https://github.com/ROCm/ROCm/releases
- Intel Newsroom (Intel + SambaNova): https://newsroom.intel.com/data-center/intel-and-sambanova-planning-multi-year-collaboration-for-xeon-based-ai-inference
- NVIDIA Blog (LillyPod): https://blogs.nvidia.com/blog/lilly-ai-factory-live/
