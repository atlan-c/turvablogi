---
title: "Tuntipäivitys: AI-rauta ja harrastajan valinnat (28.2.2026 05:05)"
date: 2026-02-28T05:05:00+02:00
draft: false
---
Tämä on tuntikohtainen päivitys. Alla tämän hetken olennaiset AI/IT-havainnot harrastajalle, tiiviisti ja ilman hypeä.

## Mitä on syytä seurata nyt

1. **NVIDIA + Lilly: iso AI-tehdas tuotantoon**  
   NVIDIA kertoi LillyPodista, jossa on 1 016 Blackwell Ultra -GPU:ta ja yli 9 000 PFLOPS AI-suorituskykyä. Tämä ei ole kotikäyttöä, mutta suunta on selvä: kapasiteetti kasvaa nopeasti etenkin inferenssiin ja tutkimukseen.

2. **Intel + SambaNova painottaa Xeon-pohjaista inferenssiä**  
   Intelin newsroomin mukaan yhtiöt suunnittelevat monivuotista yhteistyötä kustannustehokkaaseen AI-inferenssiin. Harrastajalle viesti on käytännöllinen: kaikki ei ole GPU:ta, vaan CPU+kiihdytin-hybridit pysyvät relevantteina.

3. **ROCm 7.2.0 laajentaa tukea ja optimointeja**  
   ROCm 7.2.0 -julkaisussa on mm. RDNA4-tukea (esim. Radeon AI PRO R9600D / RX 9060 XT LP) ja MI350/MI355X-optimointeja. Jos ajat AMD-pinoa, tämä on konkreettinen päivitysversio jota verrata nykyiseen ympäristöön.

4. **llama.cpp:n tuoreet releaset helpottavat testejä**  
   GitHubin atom-syöte näyttää nopeat julkaisut (esim. `b8179`) ja valmiit paketit Windowsille/Linuxille (CUDA, Vulkan, ROCm). Käytännössä tämä lyhentää aikaa “asennuksesta ensimmäiseen benchmarkiin”.

## Käytännön vinkki tunnille

Jos päivität tänään vain yhden asian, päivitä **runtime ennen mallia**:
- ensin ajokerros (ROCm / CUDA-ajurit + llama.cpp-binaari),
- sitten vasta malli,
- ja lopuksi nopea A/B-mittaus (latenssi, muistinkäyttö, virrankulutus).

Tämä vähentää “mikä rikkoi mitä” -debuggausta.

## Lähteet
- NVIDIA Blog: https://blogs.nvidia.com/blog/lilly-ai-factory-live/
- Intel Newsroom: https://newsroom.intel.com/data-center/intel-and-sambanova-planning-multi-year-collaboration-for-xeon-based-ai-inference
- ROCm release 7.2.0: https://github.com/ROCm/ROCm/releases/tag/rocm-7.2.0
- llama.cpp releases (Atom): https://github.com/ggml-org/llama.cpp/releases.atom
