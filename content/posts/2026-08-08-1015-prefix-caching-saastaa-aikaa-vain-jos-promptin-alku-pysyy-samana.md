---
title: "Prefix caching säästää aikaa vain, jos promptin alku pysyy samana"
date: "2026-08-08T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "prefix-caching"
  - "kv-cache"
  - "vllm"
---
## Tiivistelmä
Prefix caching kuulostaa helposti samalta kuin tavallinen KV-välimuisti, mutta käytännössä se ratkaisee eri ongelman: **se säästää promptin alun uudelleenlaskennan useiden pyyntöjen välillä**. Harrastajan tärkein sääntö on tämä: prefix caching auttaa oikeasti vasta silloin, kun pyynnöissä toistuu pitkä ja lähes identtinen alku, kuten sama järjestelmäprompti, samat työkalumäärittelyt tai sama pitkä dokumenttikonteksti.

## Mitä prefix caching oikeasti tekee

vLLM:n dokumentaatio kuvaa asian suoraviivaisesti. Kun uusi kysely jakaa saman alun aiemman kyselyn kanssa, palvelin voi käyttää jo laskettua KV-välimuistia eikä joudu prefillaamaan samaa tekstiosuutta uudelleen. Käytännössä säästö kohdistuu siis ennen kaikkea **promptin käsittelyyn**, ei uuden vastauksen dekoodaukseen.

SGLangin dokumentaatio sanoo saman toisesta kulmasta: se etsii yhteisiä prefiksejä saapuvien pyyntöjen ja välimuistissa olevien sekvenssien välillä, käyttää vanhaa KV-tilaa uudelleen ja hävittää vanhoja merkintöjä vasta kun muisti käy ahtaaksi. Tämä on hyödyllistä erityisesti agenttikuormassa, jossa sama runkoprompti, työkalulista ja keskustelun alku toistuvat monta kertaa päivän aikana.

## Missä tilanteessa hyöty näkyy heti

Prefix cachingista on yleensä selvä hyöty, jos jokin näistä toteutuu:

- käytät samaa pitkää järjestelmäpromptia jokaisessa pyynnössä
- agentti lähettää joka kierroksella saman työkaluskeeman ja ohjeistuksen
- kysyt samasta pitkästä dokumentista monta eri jatkokysymystä
- monikierroksinen keskustelu rakentuu saman historian päälle

Juuri näitä tapauksia vLLM nostaa esiin omissa esimerkeissään: pitkä dokumenttikysely ja monikierroksinen keskustelu. Ne ovat myös kotipalvelimessa yleisimpiä syitä ihmetellä, miksi ensimmäinen vastaus on hidas mutta myöhemmät tuntuvat nopeammilta.

## Missä tilanteessa hyöty jää pieneksi

Tämä optimointi ei ole taikakytkin kaikkeen hitauteen. vLLM huomauttaa suoraan, että prefix caching auttaa vain prefilling-vaiheessa. Jos mallisi käyttää suurimman osan ajastaan pitkän vastauksen generointiin, prefix caching ei muuta arkea yhtä paljon kuin moni toivoo.

Sama pätee tilanteeseen, jossa promptit eivät oikeasti muistuta toisiaan tarpeeksi. Jos järjestelmäprompti elää joka pyynnössä, työkalujen järjestys vaihtuu, RAG-konteksti tulee eri palasina tai käyttäjän viesti työnnetään keskelle runkoa eri tavalla, välimuistin osumia tulee vähemmän kuin paperilla pitäisi.

Käytännössä tämä tarkoittaa, että prefix caching ei korvaa:

- liian pitkää vastausmaksimia
- liian suurta kontekstia suhteessa VRAMiin
- huonoa chat-templatea
- satunnaisesti muuttuvaa prompttirakennetta

## Llama.cpp:ssä sama idea on usein eksplisiittisempi

Llama.cpp:n server-dokumentaatio on hyvä muistutus siitä, ettei kaikki paikalliset palvelimet tee tätä samalla tavalla. `cache_prompt`-asetus vertaa uutta promptia aiempaan ja evaluoi vain aiemmin näkemättömän loppuosan. Toisin sanoen hyöty riippuu siitä, että uusi pyyntö todella jatkaa tai toistaa vanhaa rakennetta.

Llama.cpp:n completion-työkalun dokumentaatio taas erottaa tästä vielä tiedostopohjaisen prompt cache -idean, jolla mallin tila voidaan tallettaa pitkän alku-promptin jälkeen nopeampaa käynnistystä varten. Harrastajalle tärkeä johtopäätös on, että "prompt cache" voi eri pinoissa tarkoittaa hieman eri toteutusta, vaikka tavoite on sama: vähemmän turhaa prefill-laskentaa.

## Yleisin aloittelijan virhe: kaikki muuttuu vähän joka kierroksella

Moni rakentaa agentin niin, että perusrunko muuttuu huomaamatta joka pyynnössä:

- työkalut serialisoidaan eri järjestykseen
- aikaleima lisätään promptin alkuun
- muistilohkoja lisätään vaihtelevaan kohtaan
- chat-template vaihtuu mallista tai kirjastosta toiseen

Silloin prefix cachingin osumaprosentti romahtaa, vaikka "samasta tehtävästä" on ihmisen mielestä kyse. Välimuisti ei päättele semanttista samankaltaisuutta, vaan tarvitsee käytännössä saman tokenijonon alun.

## Käytännön sääntö kotilabraan

Jos haluat tietää kannattaako prefix caching omassa pinossasi, etenisin näin:

1. lukitse ensin chat-template, järjestelmäprompti ja työkalujen serialisointi
2. mittaa ensimmäisen tokenin viive kylmällä ajolla
3. toista lähes sama pyyntö vain lyhyellä loppumuutoksella
4. seuraa lyheneekö prefill tai ensimmäisen tokenin viive selvästi
5. varmista lopuksi, ettei hyöty katoa heti kun RAG-konteksti tai promptin alku muuttuu

Jos ero näkyy vain laboratoriotestissä mutta ei oikeassa agenttiajossa, ongelma ei välttämättä ole palvelin. Usein ongelma on siinä, että promptin vakaa yhteinen alku puuttuu.

## Johtopäätös

Prefix caching on yksi hyödyllisimmistä paikallisen LLM-palvelimen optimoinneista, mutta vain oikeassa kuormassa. Se ei tee pitkästä vastauksesta itsessään halpaa eikä pelasta kaoottista prompttirakennetta. Se toimii silloin, kun sama alku toistuu tarpeeksi muuttumattomana, että palvelin voi jättää kalliin prefillin väliin. Siksi paras kysymys ei ole "onko prefix caching päällä", vaan **toistanko minä oikeasti saman promptin alun tarpeeksi tarkasti**.

## Lähteet

- https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/
- https://sgl-project-sglang-93.mintlify.app/concepts/prefix-caching
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- https://github.com/ggml-org/llama.cpp/blob/master/tools/completion/README.md
