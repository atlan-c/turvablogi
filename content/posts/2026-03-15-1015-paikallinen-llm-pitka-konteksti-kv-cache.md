---
title: "Paikallinen LLM pitkällä kontekstilla: milloin KV-cache kannattaa kvantisoida?"
date: "2026-03-15T10:15:00+02:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Agents"
  - "Local LLM"
  - "GPU"
  - "Hardware"
---
Moni harrastaja huomaa saman vasta käytännössä: 7B tai 14B -malli voi tuntua aivan kelvolliselta lyhyissä tehtävissä, mutta muuttuu raskaaksi heti kun keskustelu pitenee tai mukaan tuodaan paljon dokumentteja. Syy ei ole aina itse mallin painoissa, vaan siinä muistissa, jota **KV-cache** syö generoinnin aikana. Jos pitkä konteksti aiheuttaa OOM-virheitä tai pakottaa ajamaan mallia osittain CPU:lla, KV-cachen kvantisointi voi olla fiksumpi ensiaskel kuin uusi GPU.

## Mikä KV-cache oikeastaan on?

KV-cache tallentaa aiempien tokenien attention-laskennassa tarvittuja avain- ja arvoesityksiä, jotta mallin ei tarvitse laskea kaikkea uudelleen jokaisella uudella tokenilla. Tämä nopeuttaa generointia, mutta samalla välimuisti kasvaa keskustelun mukana. Hugging Facen dokumentaatio korostaa suoraan, että KV-cache voi muuttua pitkässä kontekstissa merkittäväksi muistipullonkaulaksi, ja siksi eri cache-strategioissa joudutaan vaihtamaan nopeuden ja muistinkulutuksen välillä.

Käytännön käännös kotilabraan on tämä: vaikka itse GGUF-malli mahtuisi VRAMiin, pitkä istunto ei välttämättä mahdu. Silloin oireena voi olla hidastuminen, epätasainen vaste tai se, että runtime alkaa siirtää osia CPU-muistiin.

## Mitä kvantisointi tekee välimuistille?

llama.cpp:n server-parametreissa KV-cachen datatyypit voi valita erikseen avaimille ja arvoille. Oletus on `f16`, mutta tarjolla on myös kevyempiä vaihtoehtoja kuten `q8_0`, `q4_0` ja `q4_1`. Idea on yksinkertainen: välimuisti tallennetaan pienempänä, jolloin sama laitteisto jaksaa pidemmän kontekstin tai useamman rinnakkaisen session.

Hinta ei ole nolla. Muistin säästö tulee yleensä pienenä laatutappiona ja joskus myös suorituskykykompromissina. Siksi tätä ei kannata ottaa käyttöön sokkona kaikissa tilanteissa. Mutta jos valinta on joko hieman kvantisoitu KV-cache tai jatkuvat muistiongelmat, kompromissi on usein arjessa erittäin järkevä.

## Milloin tämä kannattaa tehdä ensin?

KV-cachen kvantisointi on hyvä ensiliike erityisesti näissä tilanteissa:

- malli mahtuu muuten GPU:lle, mutta pitkä konteksti kaataa ajon
- käytät RAG-tyyppistä työnkulkua ja syötät paljon taustatekstiä
- haluat ajaa useampaa keskustelua rinnakkain samalla koneella
- olet jo todennut, että CPU-säikeet ja GPU-offload ovat kunnossa

Jos taas malli pyörii jo valmiiksi lähes kokonaan CPU:lla, tämä ei ole ensimmäinen vipu. Silloin tärkeämpää on varmistaa ensin, että GPU-offload todella toimii ja että säiemäärä ei saturoi prosessoria. llama.cpp:n suorituskykydokumentaatio muistuttaa, että väärä `--threads`-arvo voi tehdä generoinnista yllättävän hidasta, vaikka GPU olisi käytössäkin.

## Käytännön testitapa harrastajalle

Älä vaihda kaikkea kerralla. Tee yksi toistettava testi:

1. Valitse yksi oma pitkä prompti tai dokumenttisyöte.
2. Aja sama malli normaalilla cache-asetuksella.
3. Mittaa mahtuuko ajo muistiin ja miltä vaste tuntuu.
4. Kokeile kevyempää KV-cache-tyyppiä.
5. Vertaa kahta asiaa: mahtuuko pidempi konteksti ja heikkeneekö laatu oikeasti omassa käytössä.

Ollaman puolella hyvä reality check on katsoa `ollama ps`: jos malli ei pysy GPU:lla pitkän session aikana, syy voi olla juuri muistin kasvu. Ollaman FAQ muistuttaa myös, että oletuskonteksti on 4096 tokenia, ja suurempi `num_ctx` kasvattaa muistitarvetta nopeasti. Siksi kontekstin kasvattaminen ilman muuta säätöä on usein se hetki, jolloin ongelma vasta ilmestyy näkyviin.

## Oma peukalosääntö

Jos tavoite on sujuva paikallinen käyttö kotikoneella, etenisin tässä järjestyksessä:

1. varmista GPU-offload
2. säädä säikeet järkeviksi
3. pidä konteksti realistisena
4. kokeile KV-cachen kvantisointia
5. osta lisää VRAMia vasta jos nämä eivät riitä

Tämä järjestys säästää rahaa, koska moni muistiongelma ei johdu siitä, että kone olisi "liian heikko", vaan siitä, että pitkä konteksti kasvattaa välimuistin liian suureksi. KV-cachen kvantisointi ei ole taikatemppu, mutta se on yksi hyödyllisimmistä asetuksista juuri silloin, kun haluat puristaa nykyisestä raudasta vähän enemmän käyttökelpoista kontekstia ulos.

## Lähteet

- Hugging Face Transformers – Cache strategies: https://huggingface.co/docs/transformers/en/kv_cache
- llama.cpp server README (KV cache types and offload flags): https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- llama.cpp – Token generation performance troubleshooting: https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md
- Ollama FAQ (context size and GPU visibility): https://docs.ollama.com/faq
