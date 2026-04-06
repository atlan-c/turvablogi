---
title: "AI-rauta kotilabrassa: milloin 12 gigatavua VRAMia loppuu oikeasti kesken?"
date: 2026-03-06T10:15:00+02:00
draft: false
topic_family: "llm-hardware"
---
12 gigatavua VRAMia kuulostaa paperilla ihan kelvolliselta lähtötasolta paikallisille malleille, ja monessa harrastelabrassa se onkin järkevä kompromissi hinnan, virrankulutuksen ja saatavuuden välillä. Ongelma on vain siinä, että **12 Gt riittää hyvin eri tavalla eri käyttöihin**. Jos ajat kompaktia kvantisoitua mallia, pidät kontekstin maltillisena ja hyväksyt sen, ettei jokaista uutta mallia voi testata samana iltana, 12 Gt voi olla täysin käyttökelpoinen. Jos taas haet pidempää kontekstia, isompaa mallia tai väljää pelivaraa, raja tulee vastaan nopeasti.

Käytännössä VRAM ei kulu vain itse malliin. Sitä vievät myös välimuistit, työmuisti ja pidempi konteksti. Siksi aloittelijan yleinen virhe on laskea vain mallitiedoston koko levyllä ja olettaa, että sama luku kertoo koko totuuden GPU-muistista. Ei kerro. Mitä enemmän haluat pitkää keskustelua, rinnakkaisuutta tai joustoa kvantisointitasossa, sitä nopeammin 12 Gt alkaa tuntua ahtaalta.

Minun tiivis suositukseni on tämä: **12 Gt on hyvä kokeilu- ja peruskäyttötaso, mutta huono valinta, jos tiedät jo nyt tavoittelevasi isompia malleja tai pitkää kontekstia päivittäisessä käytössä**. Tällöin on usein halvempaa ostaa kerralla enemmän VRAMia kuin virittää jatkuvaa kompromissia CPU-offloadin, hitaamman vasteen ja rajatun mallivalikoiman kanssa.

## Käytännön arvio

- hyvä: kevyt koodiapuri, pienemmät kvantisoidut mallit, lyhyempi konteksti
- rajat tulee vastaan: pidemmät istunnot, suuremmat mallit, aggressiivinen moniajo
- huono yllätys: levyltä katsottu mallikoko ei kerro koko VRAM-tarvetta

## Lähteet

- https://docs.ollama.com/faq
- https://github.com/ggml-org/llama.cpp
- https://huggingface.co/docs/transformers/en/quantization/bitsandbytes
