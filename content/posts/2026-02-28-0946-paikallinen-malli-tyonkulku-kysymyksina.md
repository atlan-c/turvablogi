---
title: "Paikallinen malli arjessa: 6 käytännön kysymystä"
date: 2026-02-28T09:46:00+02:00
draft: false
---

Paikallisen mallin saa kyllä käyntiin nopeasti, mutta hyöty syntyy vasta toistettavasta työnkulusta. Tässä tiivis Q&A-muoto, jolla saat asetukset kuntoon ilman turhaa säätöä.

## 1) Millä yhdistelmällä kannattaa aloittaa?
Aloita yhdellä runtime-työkalulla (esim. Ollama tai LM Studio), yhdellä mallilla ja yhdellä testitehtävällä. Älä rakenna kahta rinnakkaista pinoa ensimmäisellä viikolla.

## 2) Miten valitsen mallikoon?
Valitse koko muistirajan mukaan, ei FOMO:n mukaan:
- jos malli swappaa tai vaste heittelee, pienennä kokoa
- jos käyttö on sujuvaa ja vastaukset jäävät vajaiksi, kokeile seuraavaa kokoa

Käytännössä tasainen vaste voittaa satunnaisen huippunopeuden.

## 3) Mitä kannattaa mitata joka päivityksessä?
Pidä vakiona kolme mittaria:
- ensimmäisen vastauksen viive
- tokeneita sekunnissa
- RAM/VRAM-huippu

Kirjaa tulokset samaan tiedostoon ennen/jälkeen päivityksen. Näet heti, oliko muutos oikeasti parempi.

## 4) Miten pidän promptit hallinnassa?
Tee 3–5 "vakio-promptia" omaan käyttöön (esim. tiivistys, koodiarvio, luonnostelu). Testaa aina niillä samoilla syötteillä. Näin et sekoita mallin laatua satunnaiseen promptin vaihteluun.

## 5) Milloin vaihdan työkalua enkä mallia?
Jos ongelma on:
- **hallinta/automaatio** → vaihda runtimea tai API-kerrosta
- **faktatarkkuus/tyyli** → vaihda mallia tai prompt-rakennetta

Usein kitka on työnkulussa, ei itse mallissa.

## 6) Mikä on pienin toimiva "production kotona" -malli?
Yksi kansio, jossa on:
- versioitu asetustiedosto
- testipromptit
- lyhyt changelog (mitä päivitit, mitä hajosi, mitä parani)

Kun tämä on olemassa, päivitykset muuttuvat kokeiluista rutiiniksi.

## Lähteet

- Ollama Docs: https://docs.ollama.com/
- LM Studio Docs: https://lmstudio.ai/docs
- llama.cpp server examples: https://github.com/ggml-org/llama.cpp/tree/master/examples/server
