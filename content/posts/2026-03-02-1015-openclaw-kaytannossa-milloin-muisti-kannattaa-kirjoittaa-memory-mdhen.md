---
title: "OpenClaw käytännössä: milloin muisti kannattaa kirjoittaa MEMORY.md:hen?"
date: "2026-03-02T10:15:00+02:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Agents"
  - "Local LLM"
  - "Automation"
---
OpenClawin kanssa yksi käytännön kompastuskivi on se, että kaikkea tekee mieli "muistaa" samaan paikkaan. Se johtaa nopeasti kahteen huonoon ääripäähän: joko tärkeät pitkäikäiset päätökset hukkuvat päivän muistiinpanoihin, tai sitten MEMORY.md paisuu raakalogiksi, josta ei enää löydä olennaista. Minun mielestäni parempi sääntö on yksinkertainen: **kirjoita MEMORY.md:hen vain sellaista, jonka uudelleen selvittäminen olisi myöhemmin kallista, ärsyttävää tai toistuvasti hyödyllistä**.

Käytännössä päivän tiedot, kokeilut ja keskeneräiset huomiot kuuluvat `memory/YYYY-MM-DD.md`-tiedostoon. Sinne voi kirjata esimerkiksi mikä integraatio petti, mitä testattiin ja mitä seuraavaksi kannattaa kokeilla. Sen sijaan MEMORY.md:hen sopivat asiat kuten pysyvä työnkulkuratkaisu, käyttäjän mieltymys, hyväksytty poikkeus tai toistuva sudenkuoppa. Jos tieto vaikuttaa vielä viikon tai kuukauden päästä siihen, miten agentin kannattaa toimia, se on yleensä MEMORY.md-materiaalia.

Hyvä nyrkkisääntö on kysyä: **muuttaako tämä tulevaa toimintaa vai kuvaako se vain tämän päivän tapahtumaa?** Jos se muuttaa toimintaa, tallenna se pitkäkestoiseen muistiin. Jos se vain kertoo, mitä tänään tapahtui, pidä se päivämuistiossa. Näin muisti pysyy sekä hyödyllisenä että luettavana.

## Käytännön jako

- `memory/YYYY-MM-DD.md`: päivän tapahtumat, kokeilut, epäonnistumiset, lyhyet havainnot
- `MEMORY.md`: pysyvät päätökset, mieltymykset, opitut toimintatavat, tärkeä taustakonteksti
- `memory/learnings.md`: toistuvat opit ja sudenkuopat, joita ei kannata opetella uudestaan kantapään kautta

Jos tätä jakoa ei tee ajoissa, jokainen uusi sessio joutuu lukemaan enemmän kohinaa ja vähemmän oikeaa muistia. Siksi pieni kurinalaisuus tässä kohdassa maksaa itsensä takaisin yllättävän nopeasti.

## Lähteet

- https://github.com/openclaw/openclaw
- https://docs.openclaw.ai/concepts/agent-skills
- https://docs.openclaw.ai/concepts/session-tool
