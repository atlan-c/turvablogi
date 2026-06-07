---
title: "OpenClaw käytännössä: milloin `localModelLean` kannattaa ottaa käyttöön?"
date: "2026-06-07T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Local LLM"
  - "Ollama"
  - "Troubleshooting"
---
Jos paikallinen malli vastaa kyllä pieneen testipromptiin mutta oikea OpenClaw-ajo alkaa silti hajota, ensimmäinen vaisto on usein väärä. Moni vaihtaa mallia, kasvattaa timeoutteja tai alkaa kirjoittaa promptia uusiksi, vaikka ongelma on käytännössä paljon arkisempi: **agentille näkyvä työkalupinta on paikalliselle backendille liian raskas tai liian herkkä**. Tähän OpenClawissa on olemassa tarkoituksella rajattu hätäventtiili, `localModelLean`.

Minun nyrkkisääntöni on tämä: **ota `localModelLean` käyttöön vasta sen jälkeen, kun olet todistanut että itse malli ja Gateway-reititys toimivat, mutta täysi agenttivuoro ei pysy kasassa**. Jos taas jo kevyet probe-ajot epäonnistuvat, lean-tila ei korjaa oikeaa ongelmaa.

## Mitä `localModelLean` oikeasti tekee

OpenClawin experimental features -dokumentaatio kuvaa `agents.defaults.experimental.localModelLean: true` -lipun paineenalennusventtiiliksi paikallisille malleille. Kun se kytketään päälle, OpenClaw pudottaa agentin oletustyökaluista kolme raskainta: `browser`, `cron` ja `message`. Tarkoitus ei ole muuttaa agentin logiikkaa salaa, vaan **lyhentää promptissa mukana kulkevaa työkaluskeemaa**, jotta pienempi tai tiukempi backend pysyy paremmin mukana.

Tämä on tärkeä erotus. Lean-tila ei tee heikosta mallista vahvaa, eikä se korjaa rikkinäistä provideria. Se vain pienentää työkalulistaa niin, että paikallinen malli saa helpomman työpöydän.

## Milloin tämä on todennäköisesti oikea testi

OpenClawin local models -ohje antaa tähän käytännössä hyvän etenemisjärjestyksen:

1. testaa että paikallinen malli vastaa ilman agenttikontekstia
2. testaa että Gateway osaa reitittää saman mallin
3. vasta sitten kokeile lean-tilaa, jos oikeat agenttivuorot yhä rikkoutuvat

Käytännössä `localModelLean` on järkevä kokeilu silloin, kun näet tällaisen ketjun:

- `openclaw infer model run --local` toimii
- `openclaw infer model run --gateway` toimii
- mutta tavallinen agenttiajo tuottaa rikkinäisiä tool calleja, liian suuria pyyntöjä tai alkaa sivuuttaa työkalut kokonaan

Juuri tässä kohtaa ongelma ei yleensä ole "OpenClaw ei löydä mallia", vaan "malli tai backend ei jaksa koko agentin normaalia työkalupintaa".

## Miksi tämä korostuu paikallisissa Ollama- ja OpenAI-yhteensopivissa backendeissa

Ollaman OpenAI-yhteensopivuusdokumentaatio on selvästi paremmassa kunnossa kuin vielä aiemmin, ja se tukee nykyään myös `v1/responses`-rajapintaa. Silti dokumentaatio muistuttaa samalla yhdestä rajasta: tuki on vain ei-tilallinen, eli `previous_response_id`- tai `conversation`-jatkuvuutta ei ole samalla tavalla kuin täysissä stateful-polussa. Tästä voi päätellä, että vaikka backend näyttäisi paperilla yhteensopivalta, **suurempi agenttikonteksti ja työkalut voivat silti paljastaa kapasiteetti- tai yhteensopivuusrajoja**, joita pieni testi ei vielä näytä.

Sama pätee muihin OpenAI-yhteensopiviin paikallisiin palvelimiin. Jos kevyt chat-pyyntö toimii mutta täysi agenttiprompti hajoaa, vika ei välttämättä ole yhdessä yksittäisessä asetuksessa vaan siinä, että koko yhdistelmä on liian tiukka normaalille työkaluskeemalle.

## Milloin `localModelLean` kannattaa jättää väliin

Lean-tila on väärä ensimmäinen liike ainakin näissä tapauksissa:

- paikallinen endpoint ei vastaa edes suoraan testikutsuun
- Gateway-probe epäonnistuu jo ilman täyttä agenttikontekstia
- malli toimii työkalujen kanssa, mutta kaatuu vasta pitkissä tehtävissä GPU-muistin, konteksti-ikkunan tai KV-cachen takia
- tarvitset juuri niitä työkaluja, jotka lean-tila poistaa käytöstä

OpenClawin local models -sivu sanoo myös suoraan, että jos ongelmat jatkuvat vielä lean-tilan ja `compat.supportsTools: false` -polun jälkeen, jäljelle jää yleensä upstream-mallin tai palvelimen kapasiteettiongelma: konteksti-ikkuna, GPU-muisti, KV-cachen häätö tai backend-bugi. Tämä on minusta olennainen muistutus, koska muuten lean-tilasta tulee helposti tapa peittää väärä juurisyy.

## Hyvä käytännön päätöspuu

Jos oma paikallinen OpenClaw-malli oireilee, etenisin näin:

1. varmista että backend vastaa suoraan
2. varmista että Gateway-reititys toimii samalla mallilla
3. kytke `localModelLean` päälle vain, jos nimenomaan täysi agenttivuoro hajoaa
4. tarkista `openclaw status --deep`, että `browser`, `cron` ja `message` todella putosivat työkalulistasta
5. jos ongelma jatkuu, lopeta promptin rukkaus ja tutki kapasiteettia tai backendin yhteensopivuutta

Tämä järjestys säästää aikaa siksi, että se erottaa kolme eri ongelmaluokkaa toisistaan:

- reachability- tai auth-ongelma
- liian raskas työkalupinta
- aito malli- tai palvelinkapasiteetin raja

## Oma johtopäätökseni

`localModelLean` kannattaa ottaa käyttöön silloin, kun tarvitset **diagnostisen kavennuksen**, et yleistä taikakytkintä. Se on hyvä testi, jos paikallinen malli on jo todistetusti olemassa ja vastaa, mutta normaali OpenClaw-agentti on sille liikaa. Se ei taas ole oikea korjaus silloin, kun backend ei jo valmiiksi selviä perusprobeista tai kun varsinainen ongelma on VRAMissa, konteksti-ikkunassa tai rikkonaisessa OpenAI-yhteensopivuudessa.

Lyhyin muistilappu on tämä: **ensin todista kuljetus, sitten kavenna työkalupintaa, ja vasta sen jälkeen syytä mallia tai promptia**.

## Lähteet

- https://docs.openclaw.ai/gateway/local-models
- https://docs.openclaw.ai/concepts/experimental-features
- https://docs.ollama.com/api/openai-compatibility
