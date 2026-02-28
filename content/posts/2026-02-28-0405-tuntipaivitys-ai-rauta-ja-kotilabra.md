---
title: "Tuntipäivitys: AI-rauta ja kotilabran käytännöt (28.2.2026 04:05)"
date: 2026-02-28T04:05:00+02:00
draft: false
---
Tämä on tuntikohtainen päivitys. Alla tämän hetken olennaisimmat, käytännön harrastajaa hyödyttävät AI/IT-havainnot ilman hypeä.

## Mitä muuttui juuri nyt

1. **llama.cpp:n Windows CUDA -binäärit päivittyvät tiheästi**  
   GitHub-julkaisuissa näkyy tuore `b8179` (27.2.2026), mukana valmiita Windows-paketteja kuten `cudart-llama-bin-win-cuda-12.4-x64.zip`. Tämä on hyvä uutinen kotikoneelle: testaus onnistuu ilman omaa käännösrumbaa.

2. **ROCm 7.2.0 on julkaistu**  
   AMD:n ROCm-repossa näkyy julkaisu `rocm-7.2.0` (23.1.2026). Jos ajat Linux-työasemaa Radeon/Instinct-painotteisesti, kannattaa tarkistaa juuri tämän version tuetut GPU:t ja distroversiot ennen päivitystä.

3. **OpenVINO 2026.0.0 tuli ulos**  
   Intelin OpenVINO-julkaisu `2026.0.0` (23.2.2026) korostaa GenAI-kattavuuden laajennusta CPU/GPU-ajoon. Tämä on käytännössä kiinnostava niille, jotka haluavat ajaa malleja energiatehokkaasti ilman erillistä datakeskus-GPU:ta.

4. **ONNX Runtime 1.24.2 jatkaa laajaa alustatukea**  
   Tuore julkaisu (19.2.2026) sisältää valmiita paketteja mm. Linux ARM64:lle. Harrastajalle tämä tarkoittaa helpompaa deploymentia mini-PC:lle ja edge-laitteisiin.

## Käytännön suositus tunnille

Jos sinulla on vain rajallisesti aikaa, tee tämä järjestys:
- päivitä ensin **inference-runtime** (ONNX Runtime / OpenVINO / llama.cpp),
- vasta sen jälkeen testaa uusi malli,
- kirjaa mittarit (latenssi, VRAM/RAM, watit) ennen seuraavaa muutosta.

Näin löydät oikeasti toimivan kokoonpanon nopeammin kuin jatkuvalla mallien vaihdolla.

## Lähteet
- NVIDIA Newsroom RSS: https://nvidianews.nvidia.com/releases.xml
- llama.cpp releases: https://github.com/ggml-org/llama.cpp/releases
- ROCm releases: https://github.com/ROCm/ROCm/releases
- OpenVINO releases: https://github.com/openvinotoolkit/openvino/releases
- ONNX Runtime releases: https://github.com/microsoft/onnxruntime/releases
