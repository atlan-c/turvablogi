---
title: "Kenttämuistiinpanot: mitä konteksti-ikkuna tarkoittaa aloittelijalle"
date: 2026-03-01T08:05:00+02:00
draft: false
---

Aamun testikierroksella sama ilmiö toistui: malli “unohti” alkupään ohjeet, kun keskustelu venyi. Syy ei yleensä ole taikuus vaan konteksti-ikkuna.

## Mitä se on, käytännössä?

Konteksti-ikkuna on se määrä tekstiä, jonka malli pystyy käsittelemään kerralla (prompt + aiempi keskustelu + vastaus). Kun raja täyttyy, vanhinta sisältöä putoaa pois tai sitä tiivistetään.

## Kenttämuistiinpanot: kolme käytännön sääntöä

- **Pidä ohjeet edessä:** tärkein ohje kannattaa toistaa lyhyenä versiona myöhemmissä viesteissä.
- **Tiivistä välissä:** pitkissä ketjuissa tee 3–5 rivin yhteenveto ja jatka sen päältä.
- **Erottele data ja ohjaus:** laita pitkä lähdemateriaali erikseen, älä sekoita sitä pitkiin metakeskusteluihin.

## Mistä tiedän, että raja tuli vastaan?

Tyypillisiä merkkejä:

- malli alkaa rikkoa aiemmin sovittua formaattia
- nimet, luvut tai rajaukset vaihtuvat kesken tehtävän
- vastaus muuttuu yleiseksi, vaikka aiemmin oltiin tarkkoja

Nopea korjaus: anna uusi “miniprompt”, jossa on tavoite, rajat ja tärkeimmät faktat yhdessä paketissa.

## Milloin tämä riittää aloittelijalle?

Useimmissa kotiprojekteissa riittää, että hallitset:

1. lyhyen peruspromptin,
2. välitiivistelmän,
3. uuden minipromptin, jos laatu alkaa hajota.

Tällä pääsee pitkälle ilman mallin vaihtoa tai raskasta optimointia.

## Lähteet

- Anthropic Docs, Context windows: https://docs.anthropic.com/en/docs/build-with-claude/context-windows
- Google for Developers, Prompt design strategies: https://developers.google.com/machine-learning/resources/prompt-eng
- Cloudflare Learning Center, What are LLMs: https://www.cloudflare.com/learning/ai/what-is-large-language-model/
