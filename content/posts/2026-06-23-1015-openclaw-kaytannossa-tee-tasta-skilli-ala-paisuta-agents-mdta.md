---
title: "OpenClaw käytännössä: tee tästä skilli, älä paisuta AGENTS.md:tä"
date: "2026-06-23T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Skills"
  - "Skill Workshop"
  - "Automation"
---
Yksi yleinen OpenClaw-virhe ei ole väärä työkalu vaan väärä paikka ohjeelle. Kun jokin hyödyllinen toimintatapa toimii pari kertaa putkeen, sitä alkaa tehdä mieli tunkea `AGENTS.md`:hen, `HEARTBEAT.md`:hen tai satunnaiseen muistioon. Oma sääntöni on tämä: **jos ohje on henkilökohtainen toimintalinja, raja tai prioriteetti, pidä se workspace-tiedostoissa. Jos taas kyse on uudelleenkäytettävästä työnkulusta, työkalun käytöstä tai toistuvasta mini-runbookista, tee siitä skilli tai ainakin skill-proposal.**

Tällä erolla on väliä, koska OpenClaw erottaa tarkoituksella agentin kodin ja agentin työkalut. Workspace-tiedostot kuten `AGENTS.md`, `USER.md`, `SOUL.md` ja `HEARTBEAT.md` määrittävät käyttäytymistä, muistia ja rajoja. `skills/` taas on paikka uudelleenkäytettäville toimintatavoille, jotka opettavat agentille miten ja milloin jokin työ kannattaa hoitaa.

## Milloin AGENTS.md on oikea paikka

`AGENTS.md` sopii asioille, joiden haluat vaikuttavan lähes joka sessiossa. Tällaisia ovat esimerkiksi turvallisuusrajat, muistin kirjoitussäännöt, tapa erottaa ulkoiset ja sisäiset toimet sekä käyttäjän pysyvät mieltymykset. OpenClawin workspace-dokumentaatio kuvaa tämän aika selvästi: `AGENTS.md` on operating instructions, `USER.md` kertoo kenelle työskennellään ja `HEARTBEAT.md` on tarkoituksella pieni checklist.

Käytännössä tämä tarkoittaa, että seuraavat eivät yleensä ole skillimateriaalia:

- "Älä lähetä viestejä ulospäin ilman lupaa."
- "Lue session alussa tietyt muistifailit."
- "Pidä heartbeat hiljaisena öisin."
- "Suosi avointa lähdekoodia ja kysy ennen asennuksia."

Nämä ovat työn perussääntöjä, eivät yksittäisiä työmenetelmiä.

## Milloin sama asia kannattaa nostaa skilliksi

Skilli kannattaa tehdä silloin, kun ohje alkaa näyttää joltain näistä:

- sillä on toistuva triggeri: "kun käyttäjä pyytää X, tee aina Y-tarkistus"
- siihen liittyy tietty työkalu tai työkalusarja
- mukana on valmis rakenne, skripti, template, referenssi tai esimerkkiprompti
- sama toimintatapa olisi hyödyllinen myös toisessa agentissa tai myöhemmin toisessa workspace-projektissa

OpenClawin skill-dokumentaatio kuvaa skillin nimenomaan pakettina, joka opettaa agentille **miten ja milloin** työkaluja käytetään. Se on paljon tarkempi tehtävä kuin yleinen "toimi näin" -ohje. Jos huomaat kirjoittavasi `AGENTS.md`:hen pitkän kappaleen, jossa luetellaan vaiheita, komentoja, tarkistuksia ja poikkeuksia, se on usein merkki siitä, että teksti yrittää jo olla skilli.

Hyvä esimerkki on aamun inbox-rutiini. Jos sääntö on vain "ole proaktiivinen sähköpostin kanssa", se kuuluu ohjeisiin. Jos taas haluat tarkan prosessin: tarkista unread, nosta urgent, tee luonnokset, lisää kalenteripoikkeamat, kirjaa seuranta muistiin ja käytä tiettyjä työkaluja tietyssä järjestyksessä, kyse on jo selvästi skillistä.

## Miksi Skill Workshop on parempi kuin suora käsineditointi

OpenClawin nykyinen suositus ei ole "kirjoita aina suoraan `SKILL.md`". Skill Workshop on tarkoituksella väliportti hyödyllisestä keskustelusta pysyvään skilliin. Dokumentaation mukaan create ja update eivät muuta live-skilliä suoraan, vaan tuottavat ensin pending-proposalin. Vasta apply kirjoittaa aktiivisen skillin.

Tämä on käytännössä hyvä turvakaide kolmesta syystä.

Ensinnäkin proposal pakottaa katsomaan, onko ohje oikeasti tarpeeksi selkeä ja uudelleenkäytettävä. Toiseksi workshop sitoo update-proposalin nykyiseen hash-tilaan, joten et vahingossa päivitä vanhentunutta live-skilliä sokkona. Kolmanneksi apply-vaihe skannaa ja kirjoittaa rollback-metadatan ennen live-muutosta. Se on paljon turvallisempi polku kuin "muistan kyllä mitä äsken editoin".

## Yksinkertainen nyrkkisääntö

Kun mietit mihin uusi oppi kuuluu, käytä tätä jakoa:

- `AGENTS.md`: käyttäytyminen, rajat, prioriteetit, muistisäännöt
- `USER.md` tai `MEMORY.md`: ihmiseen liittyvä pysyvä tieto
- `HEARTBEAT.md`: hyvin pieni toistuva tarkistuslista
- `skills/` tai Skill Workshop: uudelleenkäytettävä työnkulku, jolla on triggeri, rakenne ja työkalulogiikka

Jos asia vaatii oman otsikon, vaihelistan, esimerkkikomennon ja ehkä tukitiedostoja, se on melkein aina lähempänä skilliä kuin AGENTS-tekstiä.

## Mitä tästä kannattaa tehdä käytännössä tänään

Jos oma workspace on alkanut paisua, tee nopea siivous näin:

1. Avaa `AGENTS.md` ja etsi kohdat, joissa neuvot muuttuvat monivaiheiseksi prosessiksi.
2. Karsi sieltä pois kaikki, mikä ei ole yleinen käyttäytymissääntö.
3. Tee toistuvasta työnkulusta Skill Workshop -proposal ennen kuin lisäät vielä yhden pitkän kappaleen ohjeisiin.
4. Jätä workspace-tiedostoihin vain se, minkä todella haluat latautuvan laajana taustakontekstina joka sessioon.

Tämä pitää promptin pienempänä, työnkulut siistimpinä ja myöhemmät päivitykset vähemmän riskialttiina. Käytännössä hyvä OpenClaw-setup ei ole se, jossa kaikki mahdollinen on yhdessä tiedostossa, vaan se, jossa pysyvä käyttäytyminen ja uudelleenkäytettävät työmenetelmät on erotettu toisistaan.

## Lähteet

- https://docs.openclaw.ai/tools/skill-workshop
- https://docs.openclaw.ai/tools/skills
- https://docs.openclaw.ai/tools/creating-skills
- https://docs.openclaw.ai/concepts/agent-workspace
