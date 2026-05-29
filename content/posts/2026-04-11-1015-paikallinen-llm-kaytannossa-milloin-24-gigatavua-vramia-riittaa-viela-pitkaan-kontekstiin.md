---
title: "Paikallinen LLM käytännössä: milloin 24 gigatavua VRAMia riittää vielä pitkään kontekstiin?"
date: "2026-04-11T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "GPU"
  - "Hardware"
  - "Troubleshooting"
  - "Homelab"
---
24 gigatavua VRAMia on harrastajan paikallisessa LLM-koneessa vähän kuin vanha luottotyökalu: ei enää automaattisesti huippuluokkaa, mutta silti monessa oikeassa käytössä yllättävän järkevä. Ongelmia alkaa tulla vasta silloin, kun samassa paketissa halutaan sekä isohko malli että pitkä konteksti ilman kompromisseja.

Siksi oikea kysymys ei yleensä ole "onko 24 gigaa vielä tarpeeksi", vaan "mihin asti 24 gigaa riittää ennen kuin pitkä konteksti alkaa syödä liikaa suorituskykyä tai mallivalintaa".

Lyhyt vastaus: 24 gigatavua riittää edelleen pitkään kontekstiin silloin, kun mallikoko ja käyttötapa ovat järkeviä, mutta se ei ole enää mukava budjetti, jos tavoitteena on ajaa suuria malleja ja samaan aikaan nostaa konteksti aggressiivisesti ylöspäin.

## Miksi juuri 24 gigatavua on kiinnostava raja?

24 GB on käytännössä se luokka, jossa moni harrastaja siirtyy pois "ihan pienistä" kokeiluista kohti oikeasti käyttökelpoista paikallista ajamista. Samalla se on myös raja, jossa pitkän kontekstin hinta alkaa näkyä kunnolla.

Ollaman dokumentaatio käyttää VRAM-perustaista oletusta, jossa 24–48 GiB koneille asetetaan oletuksena 32k konteksti. Tämä on hyvä vihje siitä, että 24 GB on edelleen aivan oikea alue pitkälle kontekstille, mutta ei loputon muistibudjetti.

Tärkeä käytännön huomio on tämä: sama 32k voi olla yhdelle mallille kevyt ja toiselle jo liian kallis. Kontekstia ei voi arvioida ilman mallin kokoa.

## Milloin 24 GB toimii vielä hyvin?

24 GB toimii yhä varsin hyvin, kun jokin seuraavista pitää paikkansa:

- käytät pientä tai keskikokoista kvantisoitua mallia
- et vaadi joka tehtävään maksimaalista kontekstia
- pidät mallin kunnolla GPU:lla etkä anna ajon valua CPU:lle
- arvostat tasapainoa enemmän kuin absoluuttista maksimia

Monessa oikeassa harrastajakäytössä tämä riittää pitkälle. Jos työnkulku on esimerkiksi dokumenttien lukemista, koodiapua, RAG-hakuja tai pitkiä mutta ei äärettömiä keskusteluja, 24 GB voi olla edelleen erittäin käyttökelpoinen taso.

## Milloin 24 GB alkaa tuntua ahtaalta?

Ahtaus alkaa yleensä näkyä kolmessa tilanteessa.

### 1. Haluat ison mallin ja pitkän kontekstin yhtä aikaa

Jos tavoitteena on ajaa jo valmiiksi raskasta mallia ja samalla nostaa konteksti 32k:sta kohti 64k:ta tai pidemmälle, 24 GB muuttuu nopeasti kompromissibudjetiksi. Tässä kohtaa joudut usein valitsemaan:

- pienempi malli
- aggressiivisempi kvantisointi
- hitaampi ajo
- enemmän CPU-offloadia

Mikään näistä ei ole automaattisesti väärä ratkaisu, mutta ne ovat silti kompromisseja.

### 2. GPU-offload ei enää pysy siistinä

Ollaman ohje korostaa, että paras suorituskyky syntyy silloin, kun malli pysyy GPU:lla eikä valu CPU:n puolelle. Jos `ollama ps` ei enää näytä kunnollista GPU-ajon jakautumaa tai suorituskyky putoaa pitkän kontekstin takia, 24 GB:n muistibudjetti on käytännössä tullut vastaan.

### 3. Tokennopeus alkaa romahtaa

llama.cpp:n suorituskykyohjeista näkee hyvin sen perusidean, että pelkkä "käynnistyy" ei riitä. Jos asetukset tekevät tokennopeudesta epämukavan tai CPU alkaa ylikuormittua, kontekstin kasvatus on mennyt liian pitkälle suhteessa koneeseen.

Tässä kohtaa isoin virhe on pitää hidasta ajoa hyväksyttävänä vain siksi, että numerot paperilla näyttävät hienoilta.

## Mitä 24 GB:n omistajan kannattaa tehdä käytännössä?

Hyvä strategia ei ole maksimoida kaikkea, vaan rakentaa tasapainoinen profiili.

### Aloita tästä järjestyksestä

1. valitse malli, joka toimii jo mukavasti peruskontekstilla
2. tarkista, pysyykö ajo aidosti GPU:lla
3. nosta kontekstia vaiheittain
4. lopeta siihen kohtaan, jossa hyöty ei enää kasva samaa tahtia kuin hitaus

Tämä kuulostaa itsestään selvältä, mutta juuri näin moni välttää turhat laiteostokset. Jos 24 GB riittää 16k tai 32k kontekstiin sillä mallilla, jota oikeasti käytät päivittäin, isompi kortti ei välttämättä vielä ratkaise mitään tärkeintä ongelmaa.

## Milloin päivitys alkaa olla oikeasti perusteltu?

Päivitys isompaan VRAM-luokkaan alkaa olla järkevä, kun:

- tarvitset toistuvasti 64k tai enemmän käytännön työnkulussa
- et halua pienentää mallia pitkän kontekstin vuoksi
- nykyinen ajo valuu jatkuvasti CPU:lle
- vasteaika on jo selvästi liian hidas oikeaan käyttöön

Tällöin kyse ei enää ole vain mukavuudesta vaan siitä, että työnkulku osuu koneen fyysiseen rajaan.

## Entä jos et halua päivittää vielä?

Se on usein ihan järkevä päätös. 24 GB:n koneen elämää voi pidentää yllättävän paljon, jos:

- pidät kontekstin realistisena etkä aina maksimissa
- käytät RAGia silloin, kun kaikkea historiaa ei tarvitse pitää mukana
- valitset mallin koon käyttötarpeen mukaan etkä pelkän hype-arvon perusteella
- tarkkailet suorituskykyä oikeassa käytössä etkä vain benchmark-numeroita

Moni harrastaja hyötyy enemmän tästä ajattelutavasta kuin suorasta GPU-päivityksestä.

## Mitä tästä kannattaa muistaa?

24 gigatavua VRAMia riittää vielä pitkään kontekstiin silloin, kun koneelta ei vaadita kaikkea samaan aikaan. Se on edelleen vahva taso monelle käytännön työnkululle, mutta ei enää sellainen muistibudjetti, jossa mallin koko ja konteksti voi unohtaa kokonaan.

Paras kysymys ei siis ole "riittääkö 24 GB teoriassa", vaan "riittääkö se minun oikeaan työnkulkuuni ilman että joudun sietämään liikaa hitautta tai huonoja kompromisseja".

Monessa kotilabrassa vastaus on yhä: kyllä, kunhan asetukset pysyvät järkevinä.

## Lähteet

- https://docs.ollama.com/context-length
- https://docs.ollama.com/gpu
- https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md
