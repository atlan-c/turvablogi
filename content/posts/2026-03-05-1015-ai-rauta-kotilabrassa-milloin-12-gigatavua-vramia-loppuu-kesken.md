---
title: "OpenClaw käytännössä: milloin muutos kannattaa kirjata AGENTS.md:hen eikä vain keskusteluun?"
date: "2026-03-05T10:15:00+02:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Agents"
  - "Troubleshooting"
  - "Automation"
---
Yksi käytännön virhe OpenClaw-ympäristössä on olettaa, että tärkeä toimintatapa pysyy muistissa vain siksi, että siitä puhuttiin kerran hyvin. Ei pysy. Siksi AGENTS.md on arvokas juuri silloin, kun halutaan säilyttää sellainen työskentelytapa, jonka pitäisi ohjata tulevia sessioita ja tulevaa toimintaa luotettavasti. **Jos muutos vaikuttaa siihen, miten agentin pitäisi jatkossa toimia tässä workspace-ympäristössä, se kannattaa kirjata AGENTS.md:hen eikä jättää sitä irralliseksi keskustelumuistoksi.**

Käytännössä AGENTS.md:hen sopivat esimerkiksi paikalliset pelisäännöt, dokumentointikäytännöt, hyväksytyt varovaisuusrajat ja toistuvat työnkulut. Keskustelu taas on huono paikka sellaiselle tiedolle, jonka pitäisi olla löydettävissä myös myöhemmin ilman, että kukaan muistaa tarkkaa päivää tai avainsanaa. Tässä mielessä AGENTS.md toimii enemmän työtilan käsikirjana kuin päiväkirjana.

Minun mielestäni hyvä testi on tämä: jos sama asia pitäisi selittää tulevalle sessiolle uudestaan, se kuuluu todennäköisesti tiedostoon. Ja jos se ohjaa käytännön työtä tässä repossa tai workspace:ssa, AGENTS.md on usein oikea koti. Näin tieto ei jää keskustelun varaan, vaan muuttuu pysyväksi työvälineeksi.

## Millaiset asiat kuuluvat AGENTS.md:hen

- paikalliset toimintatavat, jotka vaikuttavat tuleviin sessioihin
- dokumentointi- ja muistikäytännöt
- varovaisuusrajat tai hyväksytyt poikkeukset
- toistuvat työnkulut, joiden unohtaminen olisi kallista

## Lähteet

- https://github.com/openclaw/openclaw
- https://docs.openclaw.ai/concepts/agent-skills
- https://docs.openclaw.ai/concepts/session-tool
