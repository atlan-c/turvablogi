---
title: "AI-rauta kotilabrassa: milloin CPU-muistikaista ratkaisee enemmän kuin GPU:n huipputeho?"
date: 2026-03-11T10:15:00+02:00
draft: false
topic_family: "llm-hardware"
---
Paikallista LLM-konetta suunnitellessa huomio menee helposti vain GPU:hun. Se on ymmärrettävää, koska VRAM ja laskentateho ratkaisevat paljon. Silti on tilanteita, joissa **CPU-puolen muistikaista tuntuu enemmän kuin GPU:n paperilla näyttävä huipputeho**. Tämä korostuu etenkin silloin, kun malli ei mahdu siististi kokonaan VRAMiin, osa laskennasta tai välimuistista valuu järjestelmämuistiin ja ajo muuttuu hybridiksi.

Tällöin ongelma ei ole vain "GPU on liian hidas", vaan se, että data liikkuu hitaasti muistihierarkiassa. Jos CPU-muisti ja sen kaista ovat vaatimattomat, offload muuttuu tahmeaksi riippumatta siitä, kuinka hienolta näytönohjaimen tuotesivu näyttää. Siksi käytetty työasema tai vanhempi palvelin voi joskus tuntua paremmalta kuin kuluttajakone, jonka GPU on kelpo mutta muu alusta kapea.

Käytännön johtopäätös on tämä: **jos tiedät jo etukäteen nojaavasi CPU+GPU-ajoon, älä osta konetta vain GPU:n perusteella**. Tarkista muistikanavat, realistinen RAM-määrä ja se, onko alusta tarkoitettu jatkuvaan datan liikutteluun, ei vain yksittäiseen peli- tai renderöintipiikkiin.

## Milloin tämä näkyy arjessa

- liian iso malli suhteessa VRAMiin
- pitkä konteksti kasvattaa muistipainetta
- GPU:n käyttöaste jää oudon matalaksi, vaikka vaste on hidas
- nopeampi GPU ei poista tahmeutta, koska pullonkaula on muualla

## Lähteet

- https://github.com/ggml-org/llama.cpp
- https://arxiv.org/abs/2404.12272
- https://docs.ollama.com/faq
