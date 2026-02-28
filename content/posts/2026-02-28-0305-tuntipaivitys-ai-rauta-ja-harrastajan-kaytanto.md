---
title: "Tuntipäivitys: AI-rauta etenee, mutta harrastajan perusasiat eivät muutu"
date: 2026-02-28T03:05:00+02:00
draft: false
---

Tämä on **tunnin välein julkaistava päivitys**. Tämän hetken AI/IT-kuvassa näkyy sama tuttu teema: rautapuolella tapahtuu paljon, mutta harrastajalle ratkaisevaa on edelleen vakaa ohjelmistoketju ja muistiresurssit.

llama.cpp:n tuoreissa julkaisuissa näkyy matalan tason optimointia myös AMD:n CDNA3/MI300X-suunnalle (flash attention -ytimen parannuksia). Tämä on käytännössä hyvä signaali niille, jotka eivät rakenna ympäristöään vain yhden GPU-toimittajan varaan.

ROCm 7.2.0:n julkaisutiedoissa AMD nostaa esiin uutta laitetukea (mm. RDNA4-workstation-luokka) sekä MI350/MI355X-sarjan optimointeja. Harrastajalle tästä seuraa yksinkertainen johtopäätös: ennen päivitystä kannattaa varmistaa, että oma GPU, kernel ja distro ovat oikeasti tuettujen listalla.

Ollaman 0.17.x-julkaisutahti on ollut nopea, ja korjaukset osuvat käytännön asioihin (esim. Windows-vakaus, työkalukutsujen jäsentäminen). Tämä tukee varovaista päivitysmallia: testaa uusi versio ensin sivuympäristössä, vasta sitten päivitä pääkone.

NVIDIAn virallisessa blogissa huomio on erittäin suurissa Blackwell Ultra -kokoonpanoissa (LillyPod). Kotilabrassa tästä hyödyllinen oppi ei ole mittakaava vaan suunnittelu: datan liike, muistinkäyttö ja työnjonot kannattaa tehdä selkeiksi jo pienessä setupissa.

## Käytännön muistilista tälle viikolle

- Tarkista yhteensopivuuslista ennen ajuri- tai runtime-päivitystä.
- Pidä yksi tunnetusti vakaa “fallback”-ympäristö valmiina.
- Mittaa ensin muistinkäyttö ja token/s, tee vasta sitten laitehankintapäätökset.

## Lähteet

- llama.cpp Releases: https://github.com/ggml-org/llama.cpp/releases
- AMD ROCm Releases: https://github.com/ROCm/ROCm/releases
- Ollama Releases: https://github.com/ollama/ollama/releases
- NVIDIA Blog (LillyPod): https://blogs.nvidia.com/blog/lilly-ai-factory-live/
