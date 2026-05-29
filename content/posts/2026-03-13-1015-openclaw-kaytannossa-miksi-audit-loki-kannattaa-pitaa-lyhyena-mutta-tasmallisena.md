---
title: "Paikallinen LLM käytännössä: milloin pitkä konteksti kannattaa korvata RAGilla?"
date: "2026-03-13T10:15:00+02:00"
draft: false
topic_family: "llm-hardware"
series:
  - "Paikalliset LLM:t"
tags:
  - "Local LLM"
  - "Hardware"
---
Pitkä konteksti kuulostaa houkuttelevalta, koska se lupaa yksinkertaisen ratkaisun: syötä vain enemmän materiaalia mallille. Käytännössä tämä ei ole aina fiksuin tie. Mitä pidempi konteksti, sitä enemmän muistia, välimuistia ja usein myös latenssia kuluu. Siksi harrastajalle tärkeä kysymys ei ole vain "tukeeko malli pitkää kontekstia", vaan **onko koko aineisto oikeasti tarpeen pitää yhtä aikaa mallin näkyvillä**.

Jos tehtävä tarvitsee vain muutaman relevantin dokumenttipätkän kerrallaan, RAG-tyyppinen haku on usein järkevämpi kuin kontekstin jatkuva venyttäminen. Se voi säästää muistia, pitää vasteen tasaisempana ja helpottaa myös sitä, että mallille annetaan juuri olennaiset kohdat eikä kaikkea mahdollista taustaa. Pitkä konteksti taas on hyödyllinen, kun keskustelun tai aineiston kokonaisuus todella tarvitsee laajan jatkuvuuden eikä sitä voi helposti pilkkoa haulla.

Minun käytännön sääntöni on tämä: **jos huomaat kasvattavasi kontekstia vain siksi, ettet vielä tiedä mikä osa tiedosta on tärkeä, harkitse ensin hakua**. Pitkä konteksti on hyvä työkalu, mutta siitä tulee nopeasti kallis tapa välttää tiedon valikointia.

## Käytä pitkää kontekstia kun

- yhtenäinen keskustelu tai asiakirja oikeasti vaatii pitkää jatkuvuutta
- haku hajottaisi liikaa kokonaisuutta

## Käytä RAGia kun

- aineisto on suuri, mutta vain osa siitä on kerralla relevanttia
- muistipaine tai vasteaika alkaa kasvaa liikaa
- haluat pitää paikallisen setupin kevyempänä

## Lähteet

- https://docs.ollama.com/faq
- https://github.com/ggml-org/llama.cpp
- https://huggingface.co/docs/transformers/en/tasks/retrieval
