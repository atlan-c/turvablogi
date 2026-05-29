---
title: "Paikallinen LLM käytännössä: kannattaako Q4 vai Q5, kun VRAM on tiukka?"
date: "2026-03-09T10:15:00+02:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "GPU"
  - "Hardware"
  - "Troubleshooting"
  - "Homelab"
---
Kun paikallinen malli ei meinaa mahtua GPU:lle, monen ensimmäinen ajatus on pudottaa kvantisointia mahdollisimman alas ja toivoa parasta. Käytännössä järkevin kysymys ei yleensä ole "mikä on pienin mahdollinen tiedosto", vaan **mikä kvantisointitaso antaa vielä siedettävän laadun ilman että joudut jatkuvaan CPU-offloadiin**. Tästä syystä Q4 ja Q5 ovat harrastajalle usein ne oikeat vertailukohdat.

Q4 voittaa yleensä siinä, että se säästää VRAMia ja mahdollistaa suuremman mallin tai pidemmän kontekstin samalla kortilla. Q5 taas voi olla hyvä kompromissi silloin, kun mallin laatu tai vakaus on juuri siinä käyttötarkoituksessa hieman parempi, mutta muisti ei vielä paina seinään asti. Olennaista on ymmärtää, että **liian kunnianhimoinen Q5 voi olla arjessa huonompi kuin sopivan kokoinen Q4**, jos vaihtoehto on jatkuva hybridiajo ja tahmea vaste.

Minun suositukseni on aloittaa käytännön testillä: aja sama tehtävä kerran Q4-versiolla, kerran Q5-versiolla, ja katso sekä vastauslaatu että se pysyykö työ aidosti GPU:ssa. Jos Q5 pakottaa CPU+GPU-sekoitukseen, teoreettinen laatuhyöty voi haihtua hitauteen. Silloin parempi kokonaiskokemus tulee usein kevyemmästä kvantisoinnista.

## Muista tämä

- valitse kvantisointi koko järjestelmän, ei vain mallitiedoston perusteella
- pitkä konteksti syö muistia myös mallin ympäriltä
- hieman pienempi mutta sulava malli on usein hyödyllisempi kuin paperilla parempi mutta hidas vaihtoehto

## Lähteet

- https://github.com/ggml-org/llama.cpp
- https://docs.ollama.com/faq
- https://huggingface.co/docs/transformers/en/quantization/concept_guide
