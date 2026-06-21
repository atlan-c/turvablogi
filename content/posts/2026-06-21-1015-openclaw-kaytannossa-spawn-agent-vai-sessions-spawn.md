---
title: "OpenClaw käytännössä: `spawn_agent` vai `sessions_spawn`?"
date: "2026-06-21T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Codex"
  - "Subagents"
  - "Automation"
---
OpenClawia ja Codexia yhdessä käyttäessä yksi käytännön kysymys toistuu nopeasti: **milloin riittää, että pyydät Codexia spawnamaan oman subagentin, ja milloin kannattaa käyttää nimenomaan OpenClawin `sessions_spawn`-työkalua?** Oma nyrkkisääntöni on tämä: jos haluat Codexin hoitavan rinnakkaisen työn saman tehtävän sisällä ja palauttavan tulokset yhteen vastaukseen, aloita `spawn_agent`-tasolta. Jos taas haluat OpenClawiin näkyvän erillisen taustarunin, lapsisession, `runId`:n ja session-orkestroinnin omilla työkaluillaan, käytä `sessions_spawn`ia.

Tämä ei ole pieni terminologinen ero. Se vaikuttaa siihen, kuka omistaa työn elinkaaren, missä tuloksia seurataan ja millä tasolla delegointi näkyy myöhemmin debugatessa.

## Mikä ero näillä oikeasti on

OpenClawin Codex-harnessin dokumentaatio sanoo suoraan, että `sessions_spawn` pidetään searchable-työkaluna siksi, että **Codexin natiivi `spawn_agent` on ensisijainen subagenttipinta**. Toisin sanoen oletuspolku Codex-ajattelussa ei ole "etsi aina OpenClawin spawn-työkalu", vaan "käytä Codexin omaa agenttidelegointia, kun haluat Codexin orkestroivan rinnakkaisen työn".

OpenAI:n Codex-dokumentaatio täydentää kuvan: Codex spawnaa subagentteja vain, kun pyydät sitä erikseen, ja se myös odottaa ne takaisin osaksi samaa työnkulkua. Tämä sopii hyvin tilanteisiin, joissa haluat esimerkiksi:

- yhden agentin tutkimaan dokumentaatiota
- toisen tarkistamaan koodia
- kolmannen kokoamaan löydökset

...ja haluat lopuksi yhden koontivastauksen samaan pääsäikeeseen.

`sessions_spawn` on eri muotoinen työkalu. Session tools -dokumentaation mukaan se tekee oletuksena **eristetyn, ei-blokkaavan subagenttisession taustatyötä varten** ja palauttaa heti `runId`:n sekä `childSessionKey`:n. Tämä on enemmän "avaa uusi OpenClaw-run omalla elinkaarella" kuin "tee yksi rinnakkainen Codex-apuagentti tämän vastauksen sisällä".

## Milloin `spawn_agent` on parempi oletus

Valitsisin Codexin natiivin `spawn_agent`-mallin ensin, jos työ näyttää tältä:

- haluat rinnakkaistaa saman tehtävän osia
- haluat lopputuloksen takaisin yhden vastauksen sisällä
- et tarvitse erillistä OpenClaw-session avainta tai myöhempää sessionhallintaa
- et halua rakentaa näkyvää taustatyöputkea `subagents`- tai `sessions_*`-työkalujen ympärille

Käytännössä tämä on oikea malli silloin, kun delegointi on osa ajattelua, ei erillinen automaatioprosessi. Codexin omat subagentit ovat tähän luonnollisia, koska Codex myös kerää tulokset takaisin samaan työnkulkuun.

## Milloin `sessions_spawn` on oikea työkalu

`sessions_spawn` kannattaa ottaa esiin silloin, kun tarvitset nimenomaan OpenClawin sessionhallintaa etkä vain Codexin sisäistä rinnakkaistusta.

Tyypillisiä tilanteita ovat nämä:

- haluat erillisen taustarunin, jota voi seurata `subagents`-työkalulla
- tarvitset `childSessionKey`-avaimen myöhempää triagea tai jatkoviestejä varten
- haluat käyttää `sessions_yield`-mallia, jossa vanhempi ajo loppuu ja jatko tulee myöhemmin takaisin
- haluat eksplisiittisesti OpenClawin `runtime`-, `sandbox`-, `thread`- tai `context`-valinnat spawn-kutsuun
- rakennat orkestrointia, jossa sessiot ovat itsessään osa arkkitehtuuria

Tässä kohtaa kannattaa ajatella näin: **`spawn_agent` pilkkoo työn, `sessions_spawn` rakentaa uuden session.** Ne voivat näyttää päällepäin samansuuntaisilta, mutta käytännössä ne ratkaisevat eri ongelmaa.

## Yleinen kompastuskivi: väärä tool profile

Moni luulee delegoinnin olevan rikki, vaikka todellinen syy on paljon arkisempi. OpenClawin session tools- ja config-dokumentaatio muistuttaa, että `tools.profile: "messaging"` sisältää kyllä `sessions_list`-, `sessions_history`- ja `sessions_send`-työkalut, mutta **ei `sessions_spawn`ia**. `coding`-profiili taas sisältää koko session-orkestrointijoukon, ja `messaging`-profiilia voi täydentää `alsoAllow`-listalla.

Tämä on käytännössä tärkeä raja. Jos agentin pitää vain lukea sessioita ja lähettää viestejä, `messaging` voi olla hyvä ja kapea profiili. Mutta jos odotat siltä varsinaista delegointia OpenClaw-sessiona, väärä profiili estää työn ennen kuin itse orkestrointilogiikka edes alkaa.

## Hyvä nopea päätöspuu

Kysyn itseltäni yleensä nämä neljä kysymystä:

1. Haluanko yhden koontivastauksen samaan Codex-tehtävään?
2. Tarvitsenko näkyvän OpenClaw-lapsisession omalla avaimellaan?
3. Pitääkö työn jatkua ei-blokkaavana taustalla ja palata myöhemmin?
4. Onko käytössä profiili, joka edes sallii `sessions_spawn`in?

Jos vastaukset ovat:

- kyllä
- en
- en
- ei väliä

...aloitan `spawn_agent`-tyylillä.

Jos taas vastaukset ovat:

- ei välttämättä
- kyllä
- kyllä
- kyllä

...käytän `sessions_spawn`ia.

## Oma käytännön sääntöni

Jos rakennan yhden keskusteluvuoron sisäistä rinnakkaistyötä, pysyn Codexin omassa subagenttimallissa niin pitkään kuin voin. Se pitää arkkitehtuurin yksinkertaisempana. Kun taas tarvitsen OpenClawin näkyvän sessionelinkaaren, taustarunin tilaseurannan tai session-avaimiin perustuvaa jatko-orkestrointia, siirryn tietoisesti `sessions_spawn`-malliin.

Ytimekkäin muistilappu on tämä: **Codexin `spawn_agent` on työn sisäinen delegointi, OpenClawin `sessions_spawn` on sessionhallittu taustadelegointi**. Kun tämän eron pitää kirkkaana, sekä promptit että myöhempi debuggaus selkiytyvät huomattavasti.

## Lähteet

- https://docs.openclaw.ai/plugins/codex-harness
- https://docs.openclaw.ai/concepts/session-tool
- https://docs.openclaw.ai/tools/subagents
- https://docs.openclaw.ai/gateway/config-tools
- https://developers.openai.com/codex/subagents
