---
title: "Paikallinen agentti käytännössä: vaadi natiivi tool calling ennen benchmarkkeja"
date: "2026-07-25T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoaly ja agentit"
tags:
  - "agent"
  - "local-llm"
  - "tool-calling"
  - "ollama"
  - "llama.cpp"
---
## Tiivistelmä

Jos paikallista mallia aiotaan käyttää agentissa eikä vain chatissa, ensimmäinen käytännön kysymys ei ole "mikä voitti tämän viikon benchmarkin", vaan **osaako runtime ja malli tehdä työkalukutsun omalla natiivilla tavalla ilman jatkuvaa paikkaamista**. Minun sääntöni on yksinkertainen: jos rakennat paikallista agenttia oikeaan käyttöön, vaadi ensin kunnollinen tool calling -polku ja vertaile vasta sitten muuta.

## Miksi tämä kysymys ratkaisee enemmän kuin raakakyvykkyys

Paikallisessa agentissa mallin pitää tehdä muutakin kuin kuulostaa fiksulta. Sen pitää tunnistaa, milloin työ kuuluu työkalulle, palauttaa kutsu oikeassa muodossa ja jatkaa tuloksen jälkeen järkevästi. Juuri tässä moni paikallinen kokeilu alkaa hajota. Chat onnistuu, mutta ensimmäinen oikea työkalusilmukka muuttuu nopeasti epävakaaksi:

- malli kirjoittaa vapaan tekstin JSONin sijaan
- työkalun nimi on melkein oikein mutta ei aivan
- parseri joutuu arvaamaan, oliko kyse sisällöstä vai työkalukutsusta
- seuraava vaihe toistaa saman kutsun tai selittää sitä takaisin käyttäjälle

Siksi en pitäisi "tool support" -mainintaa enää mukavana lisänä. Agentille se on perusvaatimus.

## Mitä lähteet sanovat paikallisista runtimeista

Ollama julkaisi varsinaisen tool support -tuen 25. heinäkuuta 2024 ja kuvasi sen suoraan tapana antaa mallille lista käytettävissä olevista työkaluista `tools`-kentän kautta. Myöhemmin 28. toukokuuta 2025 Ollama lisäsi suoratoistetut työkalukutsut sekä uuden parserin, jonka tarkoitus on erottaa työkalukutsut tavallisesta sisällöstä aiempaa luotettavammin.

llama.cpp:n nykyinen function calling -dokumentaatio tekee vielä yhden tärkeän eron näkyväksi. Se sanoo, että function calling toimii kaikille malleille, mutta kahdella eri tavalla:

- mallille on natiivi handleri ja tunnettu työkalukutsun formaatti
- tai järjestelmä putoaa geneeriseen muotoon, kun templatea ei tunnisteta

Sama dokumentaatio varoittaa suoraan, että geneerinen tuki voi kuluttaa enemmän tokeneita ja olla tehottomampi kuin mallin oma natiivi formaatti. Tämä on minusta koko aiheen tärkein käytännön lause.

## Mitä "natiivi" oikeasti tarkoittaa

Natiivi tool calling ei tarkoita mitään mystistä laatuleimaa. Käytännössä se tarkoittaa, että runtime tuntee mallin tai sen chat-templaten odottaman työkalukutsun rakenteen eikä yritä väkisin tulkita kaikkea yleisen JSON-heuristiikan läpi.

Tällä on arjessa kolme hyötyä:

- työkalukutsu löytyy helpommin oikeasta kohdasta vastausta
- parserin ei tarvitse arpoa yhtä paljon
- koko työkalusilmukka polttaa vähemmän turhaa kontekstia

Jos taas malli ajetaan geneerisellä fallbackilla, setup voi silti toimia. Mutta silloin rakennat agenttia kompromissin päälle. Se on ihan hyväksyttävää testipenkissä, ei yhtä houkuttelevaa päivittäisessä automaatiossa.

## Missä geneerinen fallback on vielä täysin ok

En sanoisi, että geneerinen tool calling on aina huono valinta. Se on aivan käyttökelpoinen, jos teet vasta alkuvaiheen kartoitusta:

- testaat, osaako uusi avoin malli ylipäänsä kutsua työkalua
- rakennat yhtä pientä demoa
- käytät vain yhtä tai kahta yksinkertaista funktiota
- hyväksyt sen, että osa virheistä johtuu parserista eikä itse mallista

Tässä vaiheessa fallback on hyödyllinen juuri siksi, että se madaltaa kokeilun kynnystä. Ongelmia alkaa tulla vasta, kun demosta yritetään tehdä tuotantomainen työnkulku ilman että perustaa vaihdetaan.

## Milloin vaatisin natiivin tuen heti

Vaatisin natiivin tool calling -polun heti, jos yksikin näistä pitää paikkansa:

- agentti saa käyttää useita työkaluja
- työnkulku on monivaiheinen eikä yksi kertakutsu
- mallin pitää palauttaa myös rakenteista sisältöä luotettavasti
- virheellinen työkalunimi tai väärä argumentti maksaa oikeaa aikaa
- aiot vaihtaa malleja usein ja haluat erottaa mallivirheen runtime-virheestä

Juuri näissä tilanteissa paikallisen agentin pahin vihollinen ei ole yleensä "liian pieni benchmark-piste", vaan epäselvä rajapinta mallin ja työkalusilmukan välillä.

## Ollama vs. llama.cpp tästä kulmasta

Tämä ei ole uskonsota, vaan valinta siitä missä haluat monimutkaisuuden elää.

Ollama on tässä mielessä lähempänä tuotetta. Se tarjoaa yhden selkeän `tools`-kentän, OpenAI-yhteensopivan polun ja nykyään myös suoratoistetut työkalukutsut. Jos tavoitteena on päästä nopeasti hyödylliseen paikalliseen agenttiin, tämä on vahva etu.

llama.cpp taas näyttää rajan näkyvämmin. Sen dokumentaatio kertoo suoraan, milloin käytössä on natiivi formaatti ja milloin `Chat format: Generic`. Minusta tämä on tehokäyttäjälle arvokasta, koska näet heti rakennatko siistin polun vai nojaatko fallbackiin.

Käytännön valinta menee usein näin:

- jos haluat nopean ja siistin paikallisen agenttikokeilun, aloita sellaisella mallilla ja runtime-polulla, joilla työkaluformaatti on tunnettu
- jos haluat ymmärtää tarkasti missä kohtaa stacki vuotaa, llama.cpp antaa siihen paremman näkyvyyden

## Älä testaa vain "toimiiko", testaa miten se hajoaa

Hyvä paikallinen agenttimalli ei erotu vain onnistuneissa demoissa. Se erotu siinä, miten se epäonnistuu. Testaisin jokaisen ehdokkaan ainakin näin:

1. Kutsu yksi yksinkertainen työkalu ja tarkista, tuleeko kutsu puhtaasti ilman selittävää ylimääräistä tekstiä.
2. Anna kaksi työkalua ja katso, valitseeko malli oikean eikä vain ensimmäistä listassa.
3. Poista yksi pakollinen argumentti ja katso, pyytääkö malli täydennystä vai arvaako.
4. Aja sama koe pidemmällä kontekstilla, koska Ollama itsekin huomauttaa, että 32k tai suurempi konteksti voi parantaa tool callingin toimivuutta MCP-työssä, mutta kasvattaa muistinkäyttöä.

Tämä viimeinen kohta on tärkeä erityisesti paikallisessa ajossa. Jos agentti toimii vain silloin kun konteksti nostetaan korkeaksi, kyse ei ole enää vain mallivalinnasta vaan myös muistibudjetista.

## Oma käytännön johtopäätökseni

Jos rakentaisin tänään paikallista agenttia harrastajan tai pienen kotilabran käyttöön, tekisin valinnan tässä järjestyksessä:

1. valitse runtime, jossa työkalukutsun polku on jo kunnolla tuettu
2. valitse malli, jolla on tunnettu natiivi tool calling -formaatti
3. vasta sen jälkeen vertaile benchmarkeja, nopeutta ja hintaa

Syy on yksinkertainen. Agentissa paras malli ei ole se, joka näyttää yksittäisessä testissä älykkäimmältä, vaan se joka pysyy luotettavasti osana työkaluketjua. Paikallisessa käytössä tämä ero tuntuu heti, koska jokainen ylimääräinen korjauslenkki syö samaa rajallista kontekstia, aikaa ja muistia.

## Lähteet

- https://ollama.com/blog/tool-support
- https://ollama.com/blog/streaming-tool
- https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md
