---
title: "Tuntipäivitys: AI-rauta 2026 harrastajan näkökulmasta"
date: 2026-02-28T01:09:00+02:00
draft: false
---

Tämä on **tuntikohtainen päivitys** turvablogiin. Tämän hetken AI-laitteistokeskustelussa tärkein havainto on yhä sama: arjessa ratkaisee enemmän muisti ja sähkönkulutus kuin markkinointi-"huipputeho".

NVIDIAn sivu nostaa RTX 5090:n kohdalla esiin 32 Gt GDDR7-muistin. Harrastajalle tämä on merkittävä, koska isompi VRAM vähentää tarvetta aggressiiviselle kvantisoinnille ja helpottaa suurempien paikallisten mallien käyttöä ilman jatkuvaa muistinvaihtoa.

AMD:n Ryzen AI Max+ 395 -sivun perusteella kiinnostava kohta on laaja cTDP-alue (45–120 W) ja 16 Zen 5 -ydintä. Käytännössä tämä tarkoittaa, että samaa laitetta voi ajaa hiljaisena taustapalvelimena tai hetkellisesti kovemmalla teholla, jos jäähdytys kestää.

Samaan aikaan llama.cpp-projekti muistuttaa hyvästä perusstrategiasta: kvantisointi + CPU/GPU-hybridi. Jos VRAM ei riitä koko mallille, osittainen offload voi silti antaa käyttökelpoisen paikallisen vasteajan.

## Käytännön suositus harrastajalle

1. Osta ensiksi muistia (VRAM/RAM), vasta sitten lisää FLOPSeja.
2. Mittaa watit ennen päivitystä ja sen jälkeen; suorituskyky per watti on kotikäytössä tärkeämpi kuin huippubench.
3. Pidä yksi "vakaa" paikallinen malli päivittäiseen käyttöön ja erillinen "kokeilumalli" testailuun.

Lyhyesti: AI-harrastuksessa voittaa yleensä tasapainoinen kokoonpano, ei kovin yksittäinen komponentti.
