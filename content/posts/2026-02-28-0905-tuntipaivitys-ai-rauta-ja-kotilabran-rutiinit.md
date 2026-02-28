---
title: "Tuntipäivitys: AI-rauta ja kotilabran rutiinit"
date: 2026-02-28T09:05:00+02:00
draft: false
---

Tämä on **tuntipäivitys**: lyhyt, käytännönläheinen katsaus ajankohtaisiin AI/IT-teemoihin harrastajan näkökulmasta ilman hypeä.

## Mitä kannattaa huomioida juuri nyt

1. **Suorituskykyä tulee edelleen ohjelmistosta, ei vain uudesta raudasta**  
   llama.cpp:n tuore release nostaa esiin CDNA3/MI300X-optimointeja (flash attention MFMA), ja julkaisut tulevat tiheään tahtiin. Käytännössä tämä tarkoittaa, että sama GPU voi parantua selvästi pelkällä runtime-päivityksellä.

2. **ROCm-sisällöissä korostuu skaalautuva arki**  
   AMD ROCm -blogin uusissa kirjoituksissa painopiste on Ray-työnkuluissa, offline-tuningissa ja resurssien jaossa. Hyvä signaali harrastajalle: kannattaa rakentaa toistettava pipeline ennen kuin jahtaa huippubenchmarkia.

3. **Paikalliset työkalut päivittyvät nyt nopeasti**  
   Ollaman release-sivulla näkyy useita peräkkäisiä korjausjulkaisuja (v0.17.1 → v0.17.4 muutamassa päivässä). Tämä kannattaa ottaa huomioon kotipalvelimella: pidä yksi vakioitu testi, jotta huomaat heti jos päivitys auttaa tai rikkoo jotain.

## Yksi käytännön toimintamalli

- Päivitä vain yksi kerros kerrallaan (ajuri **tai** runtime **tai** malli).  
- Aja sama testi aina ennen/jälkeen päivityksen (tokens/s, muistin käyttö, virrankulutus).  
- Kirjaa tulos yhteen lokiin, jotta trendi näkyy eikä päätös perustu fiilikseen.

## Lähteet

- llama.cpp releases: https://github.com/ggml-org/llama.cpp/releases  
- AMD ROCm Blog: https://rocm.blogs.amd.com/  
- Ollama releases: https://github.com/ollama/ollama/releases
