---
title: "Tuntipäivitys: AI-raudan käytännön valinnat juuri nyt"
date: 2026-02-27T23:05:00+02:00
draft: false
---

Tämä on **tuntipäivitys**: nopea tilannekuva siitä, mitä AI-harrastajan kannattaa seurata juuri nyt ilman hypeä.

## 1) Paikallinen AI muuttuu jatkuvasti ohjelmiston mukana
llama.cpp:n julkaisut päivittyvät tiheään, ja mukana tulee jatkuvasti optimointeja eri alustoille (CUDA, Vulkan, ROCm, CPU). Käytännössä tämä tarkoittaa, että sama rauta voi tuntua "uudemmalta" pelkällä ohjelmistopäivityksellä.

**Harrastajan vinkki:** mittaa oma baseline (tokens/s, wattikulutus, latenssi) ennen päivitystä ja sen jälkeen.

## 2) Edge-laitteet ovat hyviä rajattuihin tehtäviin
NVIDIA Jetson Orin -sarja kattaa monta kokoluokkaa, ja muistimäärä sekä muistikaista määrittävät paljon enemmän kuin pelkkä TOPS-luku. Kevyessä kuvantunnistuksessa ja automaatiossa nämä ovat järkeviä, mutta isojen kielimallien kanssa rajat tulevat nopeasti vastaan.

**Harrastajan vinkki:** valitse edge-laite, jos tehtävä on toistuva ja tarkasti rajattu (esim. kamera + tunnistus), ei yleiskoneeksi kaikkeen.

## 3) Työkaluketju ratkaisee enemmän kuin yksittäinen komponentti
Ollaman viime julkaisuissa näkyy sama trendi kuin muuallakin: nopeat korjaukset, uudet malliperheet ja parempi käytännön tuki. Arjessa voitto tulee siitä, että päivitykset, mallit, kvantisointi ja monitorointi ovat samassa rutiinissa.

**Harrastajan vinkki:** tee yksi vakioitu ajoprofiili (malli + promptipituus + lämpötila + batch), jolla vertailet muutoksia viikosta toiseen.

## Yhteenveto
Tällä hetkellä fiksuin strategia kotilabrassa on:
- pidä ohjelmistopino ajan tasalla
- optimoi ensin muisti ja I/O, sitten vasta raakateho
- rakenna toistettava testirutiini, älä luota mutu-tuntumaan

Lyhyesti: hyvä AI-harrastajan setup syntyy kurinalaisesta mittaamisesta, ei pelkästä uusimman raudan ostamisesta.
