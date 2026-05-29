---
title: "Milloin kannattaa käyttää `sessions_send`-työkalua uuden subagentin sijaan?"
date: "2026-05-19T10:15:00+03:00"
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
OpenClawia orkestroidessa on helppo mennä vähän liiankin innokkaasti samaan ratkaisuun: aina kun jokin työ pitää siirtää sivuun, spawnataan uusi subagentti. Se on usein hyvä oletus, mutta ei aina paras. **Jos työ kuuluu jo olemassa olevaan sessioon tai tietylle agentille, `sessions_send` voi olla käytännössä siistimpi, halvempi ja turvallisempi vaihtoehto kuin uuden lapsiajon avaaminen.**

Tämä säästää erityisesti silloin, kun et oikeasti tarvitse uutta eristettyä taustarunia vaan haluat vain jatkaa jonkin tunnetun session työtä.

## Mitä ero oikeasti tarkoittaa

`sessions_spawn` tekee uuden erillisen subagenttisession. Se on oletuksena eristetty, ei blokkaa vanhempaa ajoa ja sopii taustatyöhön, tutkimiseen ja hitaiden työkalujen käyttöön. `sessions_send` taas lähettää viestin **jo olemassa olevaan näkyvään sessioon** ja voi halutessasi odottaa vastauksen takaisin.

Käytännössä kysymys on siis tämä:

- tarvitsetko **uuden työtilan** vai
- haluatko **jatkaa olemassa olevaa työtilaa**?

Jos vastaus on jälkimmäinen, spawn on usein turhan raskas liike.

## Milloin `sessions_send` on parempi valinta

Käyttäisin `sessions_send`-työkalua erityisesti näissä tilanteissa:

- sinulla on jo olemassa oleva sessio, joka tuntee aiheen tai aiemman työn
- haluat pyytää toiselta sessiolta yhden täsmäjatkon ilman uutta orkestrointikerrosta
- haluat pitää saman keskustelu- tai projektikontekstin koossa yhdessä paikassa
- tarvitset vastauksen nopeasti etkä erillistä taustakäsittelyn elinkaarta

Hyvä käytännön esimerkki on dokumentointi- tai tarkistussessio, jota käytetään toistuvasti saman projektin ympärillä. Jos sama agentti on jo auki ja sillä on oikea työtila, uuden lapsiajon spawn ei tuo lisäarvoa. Se vain lisää yhden session lisää hallittavaksi.

## Milloin spawn on silti oikea ratkaisu

Uusi subagentti kannattaa edelleen spawnata, kun haluat jonkin näistä:

- selvästi eristetyn tehtävän
- pitkän tai hitaan työn, jota ei kannata pitää pääajon tiellä
- eri mallin tai thinking-tason kyseistä tehtävää varten
- puhtaan kontekstin ilman vanhan session painolastia
- mahdollisuuden ohjata, tappaa tai tarkistaa lasta erikseen `subagents`-työkalulla

Minusta hyvä nyrkkisääntö on tämä: **spawn on uusi työntekijä, `sessions_send` on viesti olemassa olevalle työntekijälle**.

## Käytännön hyöty: vähemmän sotkua transcriptiin

`sessions_spawn` on tarkoituksella ei-blokkaava, ja sen kanssa oikea kuvio on yleensä spawnata työ ja lopettaa oma vuoro `sessions_yield`-kutsulla, jotta valmistuminen tulee myöhemmin push-pohjaisesti takaisin. Se on erinomainen malli silloin, kun lapsi tekee itsenäistä taustatyötä.

Mutta jos tarvitset vain lyhyen jatkopyynnön valmiille sessiolle, tämä voi olla turhaa seremoniaa. `sessions_send` pitää transcriptin usein selkeämpänä, koska et luo uutta lasta, uutta announce-vaihetta ja uutta hallittavaa runia vain yhden viestin vuoksi.

## Yksi tärkeä raja: thread-sessioita ei voi käyttää miten tahansa

OpenClawin session tools -dokumentaatio nostaa esiin käytännön rajoituksen, joka on helppo unohtaa: thread-scoped chat-session avaimet eivät kelpaa `sessions_send`-kohteiksi. Jos kohde on esimerkiksi Slack- tai Discord-thread, viesti pitää ohjata sen **parent channel** -session kautta, jotta työkalureititetty liikenne ei ilmesty sotkemaan aktiivista ihmisketjua.

Tämä on hyvä esimerkki siitä, miksi `sessions_send` ei ole vain "spawn kevyempänä", vaan oma erillinen työkalunsa omine rajoineen.

## Käytännön päätöspuu

Jos mietit kumpaa käyttäisit, kysy nämä kolme kysymystä:

1. Onko olemassa jo sessio, jossa tämä työ luontevasti asuu?
2. Tarvitsenko uuden eristetyn ajon vai vain jatkoviestin?
3. Hyötyisinkö lapsiajon omasta mallista, omasta elinkaaresta tai omasta puhtaasta kontekstista?

Jos vastaukset ovat **kyllä, ei, en juuri**, valitsisin yleensä `sessions_send`-työkalun.

Jos taas vastaukset ovat **ei, kyllä, kyllä**, spawn on todennäköisesti oikea ratkaisu.

## Yhteenveto

OpenClawissa ei kannata spawnata uutta subagenttia vain tavan vuoksi. **Kun työ kuuluu jo olemassa olevaan sessioon, `sessions_send` on usein yksinkertaisempi ja halvempi tapa jatkaa työtä.**

Spawn kannattaa säästää niihin tilanteisiin, joissa oikeasti haluat uuden erillisen ajon, oman kontekstin tai taustalla valmistuvan työn. Tämä pieni ero tekee orkestroinnista yllättävän paljon siistimpää, kun sessioita alkaa olla enemmän kuin yksi tai kaksi.

## Lähteet

- https://docs.openclaw.ai/concepts/session-tool
- https://docs.openclaw.ai/tools/subagents
