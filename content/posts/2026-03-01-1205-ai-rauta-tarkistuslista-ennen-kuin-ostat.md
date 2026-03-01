---
title: "AI-rauta kotikäyttöön: tarkistuslista ennen kuin ostat"
date: 2026-03-01T12:05:00+02:00
draft: false
---

Jos rakennat paikallista AI-ympäristöä kotona, kallein virhe on ostaa väärä pullonkaula. Käy tämä lista läpi ennen tilausta.

## Tarkistuslista

- **Määritä tavoite yhdellä lauseella.**
  Esim. “Ajan 7B–14B mallia paikallisesti chattiin ja kevyeseen koodiapuun.” Ilman tätä ostat helposti ylimitoitettua rautaa.

- **Tarkista ensin VRAM, vasta sitten muut speksit.**
  Harrastajakäytössä käytännön katto tulee usein vastaan juuri näytönohjaimen muistissa, ei CPU:ssa.

- **Varmista järjestelmämuistin määrä (RAM).**
  Jos mallit, välimuistit ja muu työkuorma elävät samassa koneessa, liian pieni RAM tekee käytöstä nykivää vaikka GPU olisi hyvä.

- **Arvioi muistikaista, ei vain laskentatehoa.**
  Token-nopeudessa muistikaista näkyy usein enemmän kuin “teoreettinen TOPS”-luku.

- **Tarkista backend-yhteensopivuus etukäteen.**
  Käytätkö CUDAa, ROCm:ia vai CPU-ajon fallbackia? Väärä oletus tässä vaiheessa maksaa eniten aikaa.

- **Mittaa sähkönkulutus omassa käytössä.**
  Kotikoneessa käyttöaika ja melu ratkaisevat. Hieman hitaampi mutta hiljaisempi kokoonpano voi olla paras oikeassa arjessa.

- **Suunnittele päivitettävyys (PSU, kotelo, jäähdytys).**
  Jos et jätä kasvuvaraa, seuraava GPU-päivitys voi vaatia koko rungon uusimisen.

## Nopea ostosääntö

Jos budjetti on rajallinen, laita eurot ensin **riittävään VRAMiin + vakaaseen virtalähteeseen + hyvään jäähdytykseen**. Hienosäätö (CPU-lisäteho, eksoottiset asetukset) kannattaa vasta kun peruskuorma on mitattu.

## Lähteet

- NVIDIA CUDA GPUs (compute capability / yhteensopivuus): https://developer.nvidia.com/cuda-gpus
- AMD ROCm documentation (asennus ja tuki): https://rocm.docs.amd.com/
- llama.cpp README (paikallisen ajon backendit ja käytännöt): https://github.com/ggml-org/llama.cpp
