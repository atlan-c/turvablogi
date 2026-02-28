---
title: "Tuntipäivitys: AI-rauta ja harrastajan käytännön suunta"
date: 2026-02-28T08:05:00+02:00
draft: false
---

Tämä on **tuntipäivitys**: tiivis katsaus tämän hetken AI/IT-kehitykseen harrastajan näkökulmasta, ilman hypeä.

## Mitä juuri nyt kannattaa huomioida

1. **Ohjelmisto parantaa myös vanhempaa rautaa**  
   llama.cpp:n tuoreissa julkaisuissa näkyy jatkuva optimointi eri alustoille. Esimerkiksi viimeisissä julkaisutiedoissa on mainintoja AMD MI300X -optimoinneista (CDNA3 MFMA flash attention), mikä kertoo että suorituskykyä tulee edelleen ajurin ja kernelitason työn kautta.

2. **ROCm-ekosysteemi painottaa skaalautuvuutta, ei vain huippupiikkiä**  
   AMD:n ROCm-blogissa helmikuun lopun kirjoitukset nostavat esiin käytännön teemoja kuten Ray + ROCm 7 -työnkulut ja PyTorchin offline-tuning. Tämä on hyödyllinen suunta kotilabraan: toistettava pipeline voittaa yksittäisen benchmark-ennätyksen.

3. **Työkalujen päivitystahti on nyt erittäin nopea**  
   Ollaman release-sivuilla näkyy useita päivityksiä hyvin lyhyessä ajassa (esim. v0.17.1 → v0.17.4 muutamassa päivässä), mukana bugikorjauksia ja mallitukea. Harrastajalle tämä tarkoittaa, että versionhallittu päivitysrutiini on käytännössä pakollinen.

## Käytännön vinkki tähän viikkoon

- Pidä yksi vakioitu testi (sama malli, sama konteksti, sama prompti).  
- Mittaa ennen/jälkeen päivityksen: tokens/s, VRAM/RAM-käyttö, virrankulutus.  
- Päivitä vain yksi kerros kerrallaan (malli **tai** runtime **tai** ajuri), jotta tiedät mikä oikeasti muuttui.

## Lähteet

- llama.cpp releases: https://github.com/ggml-org/llama.cpp/releases  
- AMD ROCm Blog: https://rocm.blogs.amd.com/  
- Ollama releases: https://github.com/ollama/ollama/releases
