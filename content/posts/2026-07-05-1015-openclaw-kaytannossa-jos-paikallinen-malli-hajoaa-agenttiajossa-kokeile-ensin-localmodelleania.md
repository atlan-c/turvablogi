---
title: "OpenClaw käytännössä: jos paikallinen malli hajoaa agenttiajossa, kokeile ensin `localModelLean`ia"
date: "2026-07-05T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Local Models"
  - "Ollama"
  - "Automation"
---
Paikallisen mallin kanssa on helppo tehdä väärä diagnoosi. Kun agentti alkaa sekoilla, moni ajattelee heti että malli on liian tyhmä, VRAM loppuu tai koko paikallinen setup oli virhe. Käytännössä ongelma on usein arkisempi: **malli jaksaa vielä yhden kapean promptin, mutta ei enää koko agentin työkalupintaa, pitkää system promptia ja suurta työkalukatalogia samassa nipussa**. Silloin en ensimmäisenä vaihda rautaa. Kokeilen ensin, auttaako OpenClawin `localModelLean`.

Tiivis sääntöni on tämä: **jos paikallinen malli vastaa suorassa testissä järkevästi mutta agenttivuoro hajoaa vasta työkalujen kanssa, ongelma voi olla prompti- ja työkalukuorma, ei pelkkä raakasuorituskyky**.

## Mitä `localModelLean` oikeasti tekee

OpenClawin experimental features -dokumentaatio kuvaa `agents.defaults.experimental.localModelLean`-asetuksen tilanteisiin, joissa pienempi tai tiukempi paikallinen backend tukehtuu oletustyökalupintaan. Lean-tila pudottaa oletuksena kolme raskasta pintaa pois suorasta työkalulistasta: `browser`, `cron` ja `message`. Lisäksi se ohjaa isompia plugin-, MCP- ja client-työkalukatalogeja Tool Searchin taakse sen sijaan, että kaikki dumpattaisiin kerralla promptiin.

Tämä on käytännössä tärkeä ero. `localModelLean` ei tee mallista älykkäämpää eikä lisää GPU-muistia. Se vain vähentää sitä tavaramäärää, joka mallin pitää hahmottaa ennen kuin se ehtii tehdä mitään hyödyllistä.

## Milloin ongelma on todennäköisesti työkalupinta eikä itse malli

Epäilen työkalupinnan olevan todellinen pullonkaula erityisesti silloin, kun kaikki nämä pitävät paikkansa:

- sama malli läpäisee kapean tekstismoketestin mutta epäonnistuu agenttiajossa
- virheet alkavat vasta silloin, kun mukana on paljon työkaluja tai pitkä keskusteluhistoria
- malli antaa vapaan tekstivastauksen, vaikka sen pitäisi kutsua työkalua
- OpenAI-yhteensopiva paikallinen backend alkaa palauttaa virheitä isoista payload- tai schema-rakenteista

OpenClawin Ollama-dokumentaatio ehdottaa juuri tätä tutkimusjärjestystä. Ensin ajetaan kapea infer-testiprompti, joka ohittaa täyden agenttipinnan. Jos se toimii, kannattaa vasta sitten miettiä agenttiasetuksia kuten `localModelLean`, `num_ctx` ja joidenkin pienten ajattelevien mallien kohdalla `thinking: false`.

## Kolmen askeleen käytännön testi

Jos oma agentti tuntuu epäluotettavalta paikallisen mallin kanssa, etenisin näin:

1. Aja kapea tekstismoketesti ilman täyttä agenttityökalupintaa.
2. Jos se toimii, ota `localModelLean` käyttöön kyseiselle agentille.
3. Vasta sen jälkeen mieti raskaampia ratkaisuja kuten suurempi malli, enemmän VRAMia tai koko backendin vaihto.

Tämä järjestys säästää helposti aikaa ja rahaa. OpenClawin local models -sivu muistuttaa suoraan, että aidosti mukava agenttilooppi paikallisilla malleilla nostaa rautavaatimukset korkealle. Mutta sama dokumentaatio ei sano, että jokainen ongelma ratkeaa ostamalla lisää koneita. Joskus ongelma on se, että yrität ajaa liian leveää agenttipintaa mallilla, joka pärjää vielä aivan hyvin kevyemmässä muodossa.

## Mitä `localModelLean` ei korjaa

Tämä on se kohta, jossa moni pettyy, jos odotukset ovat väärät.

`localModelLean` ei:

- kasvata mallin konteksti-ikkunaa
- tee hitaasta mallista nopeaa
- paranna heikon mallin päättelyä vaikeissa tehtävissä
- korjaa backendiä, joka rikkoo työkaluskeemat systemaattisesti

Ollama-dokumentaatio sanoo tämän aika suoraan: lean-tila ei muuta Ollaman runtime-kontekstia tai thinking-moodia. Jos malli oikeasti loppuu kesken pitkissä syötteissä, `params.num_ctx` tai isompi malli voi silti olla pakollinen seuraava askel. Ja jos malli tai palvelin ei luotettavasti kestä tools-skeemoja lainkaan, `compat.supportsTools: false` voi olla viimeinen stabilointikeino, mutta silloin agenttikykyä myös leikataan pois.

## Milloin ottaisin tämän käyttöön heti

Ottaisin `localModelLean`in testiin nopeasti, jos käytössä on jokin näistä:

- pieni tai aggressiivisesti kvantisoitu paikallinen malli
- Ollama- tai muu OpenAI-yhteensopiva paikallinen palvelin, joka toimii hyvin yksinkertaisissa kokeissa mutta huonosti oikeassa agenttiajossa
- vanhempi GPU tai vähäinen RAM, jolloin jokainen turha kontekstitokeni tuntuu viiveenä

Erityisen järkevä tämä on silloin, kun et vielä tiedä, onko pullonkaula laskennassa vai agenttipinnan leveydessä. Lean-tila on halpa testi. Uusi näytönohjain ei ole.

## Oma nyrkkisääntöni

Jos paikallinen malli hajoaa jo suorassa yhdellä promptilla, `localModelLean` ei todennäköisesti pelasta sitä. Mutta jos malli toimii kapeasti ja hajoaa vasta agenttina, **kokeilisin aina ensin pienempää työkalupintaa ennen kuin julistan koko mallin käyttökelvottomaksi**.

Tämä on varsinkin harrastajalle tärkeä ero. Kaikki paikallisen AI:n ongelmat eivät ole rautaongelmia. Osa on paketointiongelmia.

## Yhteenveto

`localModelLean` kannattaa ajatella diagnostiikkatyökaluna eikä taikakytkimenä. Se auttaa juuri silloin, kun paikallinen malli kompastuu OpenClawin täyteen agenttipintaan mutta ei ole vielä täysin toivoton. Jos kapea infer-testi menee läpi ja varsinainen agentti ei, lean-tila on yksi järkevimmistä seuraavista kokeista. Se ei korvaa isompaa mallia eikä lisää muistia, mutta se voi estää sinua ostamasta lisää rautaa väärästä syystä.

## Lähteet

- https://docs.openclaw.ai/providers/ollama
- https://docs.openclaw.ai/concepts/experimental-features
- https://docs.openclaw.ai/gateway/local-models
