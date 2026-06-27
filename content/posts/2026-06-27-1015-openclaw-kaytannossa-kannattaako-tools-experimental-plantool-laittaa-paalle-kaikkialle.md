---
title: "OpenClaw käytännössä: kannattaako `tools.experimental.planTool` laittaa päälle kaikkialle?"
date: "2026-06-27T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Planning"
  - "Local Models"
  - "Configuration"
---
Moni säätää OpenClawin ensin toimimaan ja alkaa vasta myöhemmin miettiä, pitäisikö agentille antaa näkyvä suunnittelutyökalu jokaiseen vuoroon. `tools.experimental.planTool` kuulostaa helposti sellaiselta ominaisuudelta, joka tekee agentista automaattisesti järjestelmällisemmän. Oma käytännön johtopäätökseni on silti tämä: **en laittaisi `planTool`-asetusta päälle kaikkialle vain varmuuden vuoksi**. Ottaisin sen käyttöön silloin, kun agentti tekee oikeasti monivaiheista työtä vahvalla mallilla, mutta pitäisin sen pois erityisesti pienemmissä paikallisissa seteissä ja rutiininomaisissa keskusteluissa.

Syy ei ole se, että suunnittelu olisi huono asia. Syy on se, että OpenClawin dokumentaatio kuvaa `planTool`in nimenomaan kokeellisena pintana, jonka tarkoitus on tuoda **strukturoitu `update_plan`-työkalu non-trivial multi-step work tracking** -käyttöön. Se ei ole yleinen "tee kaikesta parempaa" -vipu.

## Mitä `planTool` oikeasti tekee

OpenClawin tools-konfiguraation dokumentaatio sanoo suoraan, että `tools.experimental.planTool` ottaa käyttöön strukturoidun `update_plan`-työkalun. Kun se on käytössä, system prompt lisää lisäksi ohjeen, jonka mukaan työkalua pitäisi käyttää vain merkittävään monivaiheiseen työhön, pitää korkeintaan yksi askel kerrallaan tilassa `in_progress` eikä toistaa koko suunnitelmaa joka päivityksessä.

Tämä on tärkeä yksityiskohta. `planTool` ei siis ole vain "näytä käyttäjälle lista". Se muuttaa myös sitä, miten runtime ohjaa mallia käyttämään kyseistä listaa. Jos agentti tekee paljon pieniä, suoria vastauksia, lisätyökalu ja lisäohjaus eivät välttämättä tuo hyötyä lainkaan.

## Miksi en käyttäisi sitä globaalina oletuksena

OpenClawin experimental features -sivu antaa hyvän yleissäännön kaikille kokeellisille lipuille: pidä ne pois päältä oletuksena, ellei dokumentaatio nimenomaan kehota kokeilemaan niitä, ja testaa pienessä ympäristössä ennen kuin leivot niistä yhteisen baseline-asetuksen. Minusta tämä sopii `planTool`iin täydellisesti.

Käytännössä globaali päällekytkentä voi olla huono idea ainakin kolmessa tilanteessa:

1. **Pieni tai tiukka paikallinen malli.** Jos backend on jo valmiiksi herkkä pitkälle promptille ja laajalle työkalupinnalle, lisätyökalu ei ole ilmainen.
2. **Enimmäkseen lyhyet tehtävät.** Jos agentin tavallinen työ on vastata, etsiä yksi tieto, ajaa yksi komento tai tehdä pieni editointi, näkyvä suunnitelmapolku voi olla pelkkää ylimääräistä seremoniaa.
3. **Laaja rollout usealle agentille.** Kokeellisen ominaisuuden levittäminen kaikkialle ennen käyttötapausten erottelua tekee vikojen tulkinnasta vaikeampaa.

Tässä kohtaa teen tietoisen tulkinnan dokumentaatiosta: jos OpenClaw itse sanoo kokeellisista ominaisuuksista "prefer the stable path first", minun oletukseni ei ole "laita kaikkialle päälle", vaan "ota käyttöön vain siellä, missä hyöty on helppo nähdä".

## Milloin laittaisin sen päälle

Laittaisin `planTool`in päälle erityisesti silloin, kun kaikki seuraavista pitävät suurin piirtein paikkansa:

1. tehtävät ovat aidosti monivaiheisia
2. käyttäjä hyötyy näkyvästä etenemisseurannasta
3. käytössä on vahva OpenAI- tai Codex-pohjainen GPT-5-luokan malli
4. agentti tekee enemmän koordinaatiota kuin pelkkää pika-Q&A:ta

OpenAI-providerin dokumentaatio kertoo, että `strict-agentic`-suoritussopimus voi GPT-5-perheen `openai/*`-ajoissa auto-enablettää `update_plan`in merkittävään työhön. Tämä on minusta hyvä vihje siitä, missä ympäristössä ominaisuus on luontevimmillaan: kun runtime, malli ja käyttöliittymä on jo viritetty agenttisempaan työskentelyyn.

Toisin sanoen en lähtisi ensimmäisenä ruuvaamaan `planTool`ia mini-PC:n paikalliseen pikkumalliin, vaan käyttäisin sitä siellä missä agentti oikeasti tekee projektinomaista työtä ja jaksaa myös noudattaa työkalun kurinalaista käyttöä.

## Milloin pitäisin sen pois

Pitäisin `planTool`in oletuksena pois näissä tilanteissa:

- paikallinen OpenAI-yhteensopiva backend oireilee jo muutenkin työkalujen kanssa
- agentin tärkein tehtävä on nopeat vastaukset, tarkistukset tai yksittäiset komennot
- yrität pienentää promptin kokoa etkä kasvattaa sitä
- et oikeasti tarvitse näkyvää askel-seurantaa käyttäjälle

Tämä liittyy samaan käytännön ajatteluun kuin `localModelLean`-tila: pienempi tai tiukempi backend kärsii yleensä ensin työkalupinnan paisumisesta, ei siitä että siltä puuttuisi yksi uusi strukturoitu meta-ominaisuus. Jos agentti jo kamppailee työkalujen, skeemojen tai kontekstibudjetin kanssa, lisäisin mieluummin kuria tehtävänantoon kuin yhden uuden yleisluontoisen työkalun.

## Codex-käytössä asia on vielä hienovaraisempi

Codex harness -referenssi sanoo, että Codex-dynaamiset työkalut latautuvat oletuksena `searchable`-mallilla ja että OpenClaw ei exposeaa sellaisia dynaamisia työkaluja, jotka duplikoivat Codexin omia workspace-operaatioita. Luettelossa on mukana myös `update_plan`.

Minun käytännön tulkintani tästä on seuraava: **jos ajat jo Codex-pohjaisella vahvalla mallilla, sinun ei yleensä kannata ajatella `planTool`ia irrallisena "pakko lisätä tämäkin" -kytkimenä**. Osa suunnittelulogiiikasta voi jo istua siihen runtime-polkuun, jota Codex/OpenAI GPT-5 -ajot muutenkin käyttävät. Tällöin parempi ensimmäinen kysymys ei ole "miten saan enemmän plania", vaan "tarvitseeko tämä agentti näkyvää suunnitelmaseurantaa juuri tässä työnkulussa".

## Oma nyrkkisääntö

Jos joutuisin kirjoittamaan tästä yhden lyhyen politiikan omaan OpenClaw-konfigiini, se olisi tämä:

1. pidä `tools.experimental.planTool` pois päältä oletuksena
2. anna `strict-agentic`-GPT-5/Codex-polun hoitaa auto-enable siellä missä se on luontevaa
3. pakota `planTool: true` vain niille agenteille tai ympäristöille, joissa tehdään oikeasti monivaiheista koordinaatiotyötä
4. jos ajat pientä paikallista mallia, optimoi ensin työkalupinta ja tehtävänannot ennen kuin lisäät näkyvää suunnittelutyökalua

Minusta tämä on parempi kuin kaksi huonoa ääripäätä:

- "aina päälle, koska suunnittelu kuulostaa hyvältä"
- "ei koskaan päälle, koska kokeellinen tarkoittaa turhaa"

Oikea vastaus on arkisempi. `planTool` kannattaa ottaa käyttöön silloin, kun siitä syntyy käyttäjälle tai operaattorille oikea havaittava hyöty. Muulloin se on helposti vain yksi lisäkerros, jonka vaikutus näkyy promptissa ja käytöksessä enemmän kuin lopputuloksen laadussa.

## Käytännön päätös vuodelle 2026

Jos rakennat OpenClawia omaan käyttöön tai pieneen kotilabraan, lähtisin liikkeelle ilman `planTool`-globaalikytkentää. Seuraa ensin, missä tilanteissa agentti oikeasti hukkaa monivaiheisen työn rakenteen. Jos ongelma on toistuva juuri vahvalla mallilla ja näkyvä eteneminen helpottaa yhteistyötä, kytke ominaisuus päälle rajatusti. Jos taas ongelma on paikallisen mallin haparointi, työkalutulva tai pieni konteksti-ikkuna, ratkaisu on todennäköisesti jossain muualla kuin yhdessä uudessa experimental-työkalussa.

## Lähteet

- https://docs.openclaw.ai/concepts/experimental-features
- https://docs.openclaw.ai/gateway/config-tools
- https://docs.openclaw.ai/concepts/system-prompt
- https://docs.openclaw.ai/providers/openai
- https://docs.openclaw.ai/plugins/codex-harness-reference
