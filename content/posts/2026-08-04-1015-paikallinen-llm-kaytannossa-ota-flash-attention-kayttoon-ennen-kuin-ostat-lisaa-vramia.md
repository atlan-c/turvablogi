---
title: "Paikallinen LLM käytännössä: ota Flash Attention käyttöön ennen kuin ostat lisää VRAMia"
date: "2026-08-04T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "flash-attention"
  - "vram"
  - "ollama"
  - "llama-cpp"
---
## Tiivistelmä
Jos paikallinen LLM alkaa hyytyä pitkällä kontekstilla, moni harrastaja ajattelee ensimmäiseksi uutta GPU:ta tai pienempää mallia. Minun käytännön sääntöni on toinen: **katso ensin, onko Flash Attention käytössä**. Varsinkin agentti- ja RAG-työssä muistipaine kasvaa nopeasti kontekstin mukana, ja tässä kohtaa väärä johtopäätös voi tulla kalliiksi.

Ollaman FAQ sanoo suoraan, että Flash Attention voi pienentää muistinkäyttöä merkittävästi kontekstin kasvaessa. Siksi se ei ole mikään hienosäätövipu vaan aivan ensimmäinen tarkistus, ennen kuin alat ostaa lisää VRAMia tai leikata käyttöä rumasti.

## Miksi pitkä konteksti syö muistia nopeammin kuin moni arvioi

Lyhyessä chatissa moni paikallinen malli näyttää kevyeltä. Tilanne muuttuu, kun sama ympäristö alkaa tehdä oikeaa työtä:

- pitkä system-ohje
- työkalukutsut
- välivastaukset
- RAG-haun tuoma lisäteksti
- useita kierroksia saman pyynnön sisällä

Silloin ongelma ei ole vain mallin painot vaan myös KV-välimuisti. Juuri tätä kohtaa Ollama korostaa Flash Attention -ohjeessaan: muistihyöty kasvaa, kun konteksti kasvaa. Käytännössä tämä tarkoittaa, että 8k voi vielä tuntua harmittomalta, mutta 32k tai 64k alkaa jo paljastaa, onko runtime oikeasti säädetty agenttityöhön vai vain yksittäisiin chattivastauksiin.

## Mitä tekisin ennen rautakauppaa

Tekisin nämä tarkistukset tässä järjestyksessä.

### 1. Varmista, että Flash Attention on käytössä

Ollama käyttää Flash Attentionia automaattisesti silloin, kun valittu backend ja laitteet tukevat sitä. Tarvittaessa sen voi pakottaa päälle ympäristömuuttujalla `OLLAMA_FLASH_ATTENTION=1`.

Tässä on käytännön opetus: jos et tiedä onko ominaisuus käytössä, et vielä tiedä johtuuko muistiongelma oikeasti raudasta vai vain oletuspolusta.

### 2. Tarkista, oletko itse asiassa ajamassa mallia osittain CPU:lla

Ollaman FAQ muistuttaa, että `ollama ps` näyttää onko malli kokonaan GPU:ssa vai osittain CPU/GPU-jaolla. Tämä on tärkeää siksi, että "tarvitsen lisää VRAMia" voi todellisuudessa tarkoittaa vain sitä, että nykyinen ajotapa ei käytä muistia tehokkaasti pitkällä kontekstilla.

Jos näet osittaisen CPU/GPU-jaon jo ennen kuin kuorma on oikeasti iso, en ostaisi mitään ennen kuin tarkistan Flash Attentionin tilanteen.

### 3. Mieti KV-välimuistin tyyppi vasta tämän jälkeen

Ollaman dokumentaatio sanoo myös, että KV-cache voidaan kvantisoida, kun Flash Attention on käytössä. Vaihtoehdoista `q8_0` vie noin puolet `f16`:n muistista ja on heidän mukaansa yleensä hyvä kompromissi, kun taas `q4_0` säästää enemmän mutta voi näkyä laadussa herkemmin varsinkin suuremmilla konteksteilla.

Tämä on hyvä toinen vipu, mutta ei ensimmäinen. Jos Flash Attention puuttuu, hyppäät liian nopeasti toissijaiseen optimointiin.

## llama.cpp kertoo saman eri tasolla

llama.cpp:n CLI-dokumentaatio tekee tästä hyvin konkreettista. Siellä Flash Attention on oma asetus `--flash-attn on|off|auto`, ja KV-välimuistin tyypit ovat erikseen säädettävissä `--cache-type-k` ja `--cache-type-v` -optioilla. Tämä on käytännössä hyödyllinen muistutus siitä, että pitkäkontekstinen paikallinen ajo ei ole vain "valitse malli ja aja", vaan muistipolitiikka on osa suorituskykyä.

Toisin sanottuna:

- Flash Attention ratkaisee ensin sitä, miten huomio-operaatio käyttäytyy pitkällä kontekstilla
- KV-cache-tyyppi säätää sen jälkeen, paljonko muistia välimuisti vie
- lisä-VRAM ratkaisee vasta sen, mitä kaikkea haluat tämän jälkeen mahduttaa sisään yhtä aikaa

Moni tekee nämä päätökset täsmälleen väärässä järjestyksessä.

## Missä uusi GPU on oikea ratkaisu

En väitä, että Flash Attention poistaisi rautarajat. Se ei poista niitä. Uusi GPU tai suurempi VRAM on edelleen oikea liike, jos:

- malli ei mahdu järkevästi edes optimoidulla muistipolulla
- ajat useita malleja rinnakkain
- tarvitset niin pitkän kontekstin, että kapasiteettiraja tulee vastaan joka tapauksessa
- muu kuorma, kuten rinnakkaiset pyynnöt, kasvattaa muistitarvetta enemmän kuin yksi optimointi voi pelastaa

Mutta vasta tässä kohdassa ostaminen muuttuu perustelluksi. Sitä ennen riskinä on, että ostat lisää kapasiteettia paikkaamaan asiaa, jonka runtime olisi voinut hoitaa halvemmalla.

## Hyvä käytännön tarkistuslista

Jos paikallinen agentti alkaa kaatua tai valua CPU:lle pitkällä kontekstilla, käyn tämän listan läpi:

1. onko Flash Attention käytössä tai pakotettu päälle tuetulla backendilla
2. näyttääkö `ollama ps`, että malli pysyy kokonaan GPU:ssa
3. onko konteksti oikeasti tarpeellinen eikä vain liian löysä oletus
4. pitäisikö KV-cache vaihtaa `f16`:sta `q8_0`:aan
5. vasta tämän jälkeen: tarvitaanko lisää VRAMia tai toinen GPU

Tämä järjestys säästää yllättävän usein rahaa ja aikaa.

## Johtopäätös

Pitkän kontekstin paikallisessa LLM-ajossa ensimmäinen kysymys ei ole "mikä GPU ostan", vaan "käytänkö jo muistipolkua, joka on tarkoitettu tähän kuormaan". Ollaman tämänhetkinen dokumentaatio sanoo suoraan, että Flash Attention voi pienentää muistinkäyttöä merkittävästi kontekstin kasvaessa, ja llama.cpp antaa saman luokan säädön suoraan omassa CLI:ssään. Siksi pitäisin Flash Attentionia ensimmäisenä tarkistuksena jokaisessa paikallisessa agentti- tai RAG-ympäristössä ennen rautapäätöksiä.

## Lähteet

- https://docs.ollama.com/faq
- https://docs.ollama.com/development
- https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md
