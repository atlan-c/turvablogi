---
title: "Kuinka monta rinnakkaista agenttipyyntöä paikallinen LLM oikeasti kestää?"
date: "2026-07-29T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoaly ja agentit"
tags:
  - "local-llm"
  - "agent"
  - "ollama"
  - "llama.cpp"
  - "context"
---
## Tiivistelmä
Tyypillinen kotilabran tilanne näyttää tältä: yksi agentti toimii vielä hyvin, mutta heti kun avaat toisen saman mallin työn, kone alkaa yskiä. Tokenit tulevat epätasaisesti, VRAM ei tunnu enää riittävän ja palvelin käyttäytyy kuin rauta olisi yhtäkkiä huonontunut. Ongelma ei useinkaan ole rikki mennyt malli vaan se, että pitkä konteksti ja rinnakkaisuus osuvat samaan muistibudjettiin. Siksi käytännön vastaus otsikon kysymykseen on tavallista varovaisempi: **useimmilla yhden käyttäjän paikallisilla asetuksilla kannattaa aloittaa yhdestä rinnakkaisesta pyynnöstä per malli ja nostaa sitä vasta sitten, kun tiedät paljonko valittu konteksti oikeasti maksaa**.

## Miksi tämä menee pieleen juuri agenteilla

Tavallisessa chatissa yksi malli vastaa yleensä yhteen asiaan kerrallaan. Agentti taas tekee helposti useita pieniä työvaiheita:

- haku tai dokumentin luku
- tool-kutsu
- tarkentava jatkokysymys
- uusi pyyntö saman session sisällä

Tästä syntyy houkutus ajatella, että enemmän rinnakkaisuutta on automaattisesti parempi. Se ei pidä paikallisessa ajossa aina paikkaansa, koska agentit tarvitsevat usein myös pitkää kontekstia. Ollaman nykyinen kontekstidokumentaatio sanoo suoraan, että alle 24 GiB VRAMilla oletus on 4k, 24-48 GiB luokassa 32k ja 48 GiB tai enemmän nostaa oletuksen 256k:hon. Sama sivu lisää, että web-hakuun, agentteihin ja koodityökaluihin kannattaa asettaa vähintään 64 000 tokenia.

Juuri tässä kohtaa moni kompastuu. Kun agentille annetaan reilu konteksti, jokainen lisärinnakkaisuus ei ole vain "yksi pyyntö lisää" vaan myös lisää muistia.

## Ollama kertoo ongelman suoraan

Ollaman FAQ on tässä harvinaisen selkeä. Dokumentaation mukaan rinnakkainen käsittely kasvattaa kontekstikokoa rinnakkaisten pyyntöjen määrällä. Esimerkki on yksinkertainen: 2k konteksti neljällä rinnakkaisella pyynnöllä muuttuu 8k kontekstiksi ja vaatii lisää muistia. Samassa kohdassa sanotaan vielä suoremmin, että `OLLAMA_NUM_PARALLEL`-asetuksen vaatima RAM skaalautuu kaavalla:

`OLLAMA_NUM_PARALLEL * OLLAMA_CONTEXT_LENGTH`

Tästä ei pidä tehdä liian tarkkaa laboratoriokaavaa, koska todellinen muistinkäyttö riippuu myös mallista, kvantisoinnista ja siitä, ollaanko GPU- vai CPU-ajossa. Mutta käytännön johtopäätös on selvä: **jos nostat sekä kontekstin että rinnakkaisuuden samaan aikaan, muistitarve kasvaa nopeasti kahdesta suunnasta**.

Esimerkiksi harrastajan koneessa:

- `64k` konteksti ja `1` rinnakkainen pyyntö on yksi asia
- `64k` konteksti ja `4` rinnakkaista pyyntöä on aivan eri muistiluokan päätös

Siksi moni "malli hidastui yllättäen" -tilanne ei johdu itse mallista vaan siitä, että palvelimen asetuksista tuli vahingossa paljon raskaammat kuin käyttäjä ymmärsi.

## Miksi yksi lämmin pyyntö voittaa usein neljä kylmää

llama.cpp:n server-dokumentaatio antaa hyvän vastaparin tälle ajattelulle. Se kertoo kaksi käytännössä tärkeää asiaa:

- palvelin tukee rinnakkaista dekoodausta ja monen käyttäjän käyttöä
- `cache_prompt` on oletuksena käytössä, jolloin yhteinen prefiksi voidaan käyttää uudelleen eikä kaikkea tarvitse prosessoida aina alusta

Tästä seuraa tärkeä käytännön tulkinta. Jos käyttö on oikeasti yhden ihmisen tai yhden agentin toistuvaa työtä samalla mallilla, yhden vakaan pyynnön lämpimänä pitäminen voi olla parempi optimointi kuin rinnakkaisuuden aggressiivinen nosto. Yhteinen alku, system-prompt ja työkalumäärittelyt hyötyvät silloin välimuistista paremmin.

Toisin sanottuna kaikki jonotus ei ole paha asia. Jos vaihtoehto on:

- yksi lämmin malli, joka hyödyntää yhteistä prefiksiä
- tai monta rinnakkaista pyyntöä, jotka syövät muistibudjetin ja pakottavat kompromisseihin

valitsisin kotilabrassa hyvin usein ensimmäisen.

## Milloin rinnakkaisuutta kannattaa oikeasti nostaa

Rinnakkaisuuden nosto on perusteltu, jos ongelma on aidosti se, että useampi itsenäinen tehtävä odottaa vuoroaan eikä kone ole vielä muistirajalla. Esimerkiksi nämä tilanteet puoltavat sitä:

- samalla mallilla on useita käyttäjiä
- agentilla on erillisiä taustatöitä, jotka oikeasti hyötyvät samanaikaisuudesta
- käytössä on tarpeeksi VRAMia tai järjestelmämuistia eikä malli valu osittain CPU:lle

Ollaman FAQ muistuttaa samalla, että GPU-ajossa uuden mallin täytyy mahtua kokonaan VRAMiin, jotta useita malleja voidaan pitää ladattuna samaan aikaan. Tämä on hyvä muistutus erityisesti kotikoneille: pelkkä "GPU on käytössä" ei vielä tarkoita, että rinnakkaisuudelle olisi oikeasti tilaa.

## Oma nyrkkisääntöni

Jos rakennat paikallista agenttia yhdelle käyttäjälle, etenisin tässä järjestyksessä:

1. Valitse konteksti, jota työ oikeasti tarvitsee.
2. Jätä rinnakkaisuus ensin arvoon `1`.
3. Varmista, että malli pysyy muistissa ja samaa prefiksiä voidaan hyödyntää.
4. Nosta rinnakkaisuutta vasta, jos näet oikeaa jonotusta etkä vain yleistä hitautta.

Tämä säästää usein enemmän aikaa kuin se, että lähdet heti "avaamaan hanaa" rinnakkaisilla pyynnöillä.

## Entä llama.cpp:n `--ctx-size`

llama.cpp:n palvelimessa `--ctx-size` määrittää promptikontekstin koon. Se ei yksinään kerro koko muistitarinaa, mutta muistuttaa yhdestä tärkeästä asiasta: konteksti on tietoinen kapasiteettipäätös, ei ilmainen vipu. Kun samaan palvelimeen yhdistetään rinnakkaista käyttöä, jokainen liian optimistinen kontekstiarvo alkaa maksaa nopeasti.

Siksi en pitäisi 64k:ta tai 128k:ta oletuksena vain siksi, että malli "ehkä joskus tarvitsee sitä". Paikallisessa agenttikäytössä parempi periaate on: **anna niin paljon kontekstia kuin työnkulku vaatii, mutta älä oleta että sama määrä on halpa myös rinnakkaisena**.

## Johtopäätös

Paikallinen agentti ei yleensä kaadu ensimmäisenä siihen, että malli olisi liian heikko. Se kaatuu siihen, että muistibudjetti syödään huomaamatta loppuun yhdistämällä pitkä konteksti ja liian innokas rinnakkaisuus.

Siksi paras oletus harrastajalle on edelleen tylsä mutta toimiva:

- yksi malli lämpimänä
- yksi rinnakkainen pyyntö alkuun
- konteksti tarpeen mukaan, ei varmuuden vuoksi maksimiin

Kun tämä toimii, rinnakkaisuutta voi nostaa hallitusti. Jos tämä ei vielä toimi, ongelma ei yleensä ratkea sillä, että lisäät vielä yhden samanaikaisen pyynnön.

## Lähteet

- https://docs.ollama.com/faq
- https://docs.ollama.com/context-length
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
