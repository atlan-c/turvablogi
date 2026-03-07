---
title: "AI-rauta 2026: harrastajan käytännön tarkistuslista ennen ostoa"
date: 2026-03-07T11:31:00+02:00
draft: false
---

Jos paikallinen AI tuntuu hitaalta tai epävakaalta, ongelma on usein raudassa eikä promptissa. Ennen seuraavaa hankintaa käy läpi tämä lista.

## Tarkistuslista: mitä oikeasti kannattaa varmistaa

- **VRAM ensin, TFLOPS vasta sitten.**
  Moni käytännön ongelma ratkeaa sillä, että malli mahtuu GPU-muistiin ilman aggressiivista kvantisointia.

- **Tarkista muistiväylä ja kaista, ei vain muistimäärää.**
  Sama VRAM-määrä voi käyttäytyä eri tavalla, jos kaista on pullonkaula.

- **Varmista ohjelmistotuki omalle pinolle.**
  Linux/Windows, CUDA/ROCm/DirectML ja käyttämäsi runtime (esim. Ollama, llama.cpp) ratkaisevat enemmän kuin yksittäinen benchmark.

- **Laske koko koneen virta- ja lämpöbudjetti.**
  PSU, kotelon ilmankierto ja melutaso vaikuttavat suoraan siihen, käytätkö konetta oikeasti päivittäin.

- **Suosi mitattua token/s-suorituskykyä omalla mallikoolla.**
  Yleiset pelibenchmarkit eivät kerro käytännön inferenssinopeutta.

- **Jätä kasvunvara.**
  Jos ostat aivan minimin, joudut päivittämään nopeasti uudestaan. Pieni marginaali säästää rahaa pitkällä aikavälillä.

## Nopea ostologiikka (harrastajalle)

1. Päätä ensin käyttötapa: chat, koodi, kuvagenerointi vai sekoitus.
2. Valitse tavoitemallikoko, jota ajat arjessa (ei vain testissä).
3. Tarkista, mahtuuko se VRAMiin käytännöllisellä kvantisoinnilla.
4. Vasta tämän jälkeen vertaa hinta–suorituskykyä.

Yksinkertainen sääntö: osta laite, jolla päivittäinen workflow toimii ilman jatkuvaa säätöä.

## Lähteet

- Ollama Docs, Hardware requirements: https://github.com/ollama/ollama/blob/main/docs/faq.md
- llama.cpp README ja backend-tuki: https://github.com/ggerganov/llama.cpp
- AMD ROCm Documentation: https://rocm.docs.amd.com/
