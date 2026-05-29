---
title: "Paikallinen LLM käytännössä: miksi 8 Gt GPU ja paljon RAMia ei tunnu 24 Gt VRAMilta?"
date: "2026-05-12T10:15:00+03:00"
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
Moni yrittää venyttää paikallista LLM-konetta näin: koneessa on 8 Gt näytönohjainta, mutta keskusmuistia on paljon, joten ehkä iso malli saadaan jotenkin juoksemaan lähes saman tuntuisesti kuin oikeasti isossa VRAMissa. Tämä toimii osittain, mutta vain osittain. Käytännössä suuri RAM auttaa enemmän siinä, että ajo ylipäätään onnistuu, kuin siinä että kokemus tuntuisi samalta kuin 24 Gt VRAMin koneessa.

Lyhyt käytännön sääntö on tämä: jos malli tai sen työdata mahtuu kunnolla GPU:n omaan muistiin, saat yleensä paljon tasaisemman ja nopeamman ajon. Jos taas joudut jatkuvasti nojaamaan järjestelmämuistiin, voit saada mallin käyntiin, mutta nopeus, latenssi ja ennustettavuus alkavat kärsiä.

## Miksi tämä tuntuu paperilla houkuttelevammalta kuin käytännössä

Ajatus on ymmärrettävä. RAM on usein halvempaa kuin suuri VRAM. Lisäksi monet työkalut osaavat offloadata osan mallista GPU:lle ja jättää loput CPU:lle tai järjestelmämuistiin. Tästä tulee helposti vaikutelma, että pieni GPU ja iso RAM olisivat melkein sama asia kuin suuri GPU.

Todellisuudessa kyse on kahdesta eri asiasta:

- **kapasiteetti**: saadaanko malli ylipäätään mahtumaan johonkin
- **kaistanleveys ja sijainti**: missä muistissa data on juuri silloin, kun laskenta sitä tarvitsee

Juuri jälkimmäinen ratkaisee paljon enemmän kuin moni aluksi arvaa.

## GPU:n oma muisti on tärkeä siksi, että se on lähellä laskentaa

NVIDIAn CUDA-dokumentaatio sanoo asian aika suoraan: heterogeenisessa järjestelmässä CPU:lla on oma DRAM ja GPU:lla oma muistinsa, ja suorituskyky on parhaimmillaan silloin, kun data sijaitsee sen prosessorin muistissa, joka sitä käyttää. Tämä kuulostaa teoriapuheelta, mutta LLM-arjessa sillä on suora seuraus.

Kun mallin aktiivinen osa, välimuistit ja työdata pysyvät GPU:n omassa muistissa, GPU voi tehdä työnsä ilman jatkuvaa liikennettä järjestelmämuistin suuntaan. Kun taas osa datasta pitää hakea kauempaa RAMista, mukaan tulee lisää siirtoa, odottelua ja epätasaisuutta.

Käytännössä tämä näkyy niin, että:

- ensimmäinen token voi tulla hitaasti
- tokennopeus heittelee enemmän
- suurempi konteksti rankaisee aiempaa kovemmin
- pieni VRAM auttaa edelleen, mutta ei taianomaisesti muutu isoksi VRAMiksi

## Miksi suuri RAM silti auttaa

Iso RAM ei ole turha. Se auttaa useassa oikeassa tilanteessa:

- malli mahtuu ylipäätään ladattavaksi
- CPU-ajosta tulee mahdollinen vaihtoehto
- osa kerroksista voidaan offloadata GPU:lle
- kvantisoitu malli voidaan pitää muistissa ilman jatkuvaa levyliikennettä
- RAG, embeddingit ja muu oheistyö saavat enemmän tilaa

Tämä on tärkeä ero: suuri RAM nostaa katon sille, mitä voit yrittää ajaa. Suuri VRAM taas nostaa paljon useammin lattiaa sille, miltä käyttö oikeasti tuntuu.

## Missä kohtaa pullonkaula yleensä syntyy

llama.cpp-keskusteluissa tämä tulee vastaan hyvin käytännöllisesti. Jos esimerkiksi noin 24 Gt mallia yritetään pyörittää 8 Gt GPU:n kanssa niin, että osia joudutaan jatkuvasti pitämään järjestelmämuistissa, ongelma ei ole vain laskennassa vaan myös siinä, kuinka nopeasti data liikkuu GPU:n ja muun koneen välillä.

Sama keskustelu arvioi PCIe 4.0 x16 -siirron karkeasti noin 31,5 GB/s luokkaan. Paperilla luku näyttää suurelta. Silti se ei tee mallin osien edestakaisesta liikuttelusta ilmaista, varsinkaan jos tokenin generointi muutenkin elää sekunnin murto-osien tai sekuntien aikaskaalassa. Jos jokaisessa vaiheessa pitää odottaa datan siirtymistä takaisin oikeaan paikkaan, hyöty GPU:sta jää helposti pienemmäksi kuin harrastaja toivoi.

Tässä kohtaa moni pettymys syntyy: GPU kyllä näkyy käytössä, offload toimii ja VRAM mittareissa täyttyy, mutta tuntuma ei silti muutu "oikean ison GPU:n" kaltaiseksi.

## Miten tämä eroaa yhtenäismuistista

On hyvä erottaa kaksi eri tilannetta:

1. **Erillinen GPU + järjestelmämuisti PCIe:n takana**
2. **Yhtenäismuistia käyttävä järjestelmä, jossa CPU ja GPU jakavat muistialuetta eri tavalla**

Ensimmäisessä tapauksessa etäisyys laskennan ja datan välillä näkyy usein kovemmin. Toisessa tapauksessa malli voi mahtua mukavammin yhteen muistialtaaseen, mikä helpottaa käytettävyyttä. Silti perussääntö ei katoa: nopeinta on yleensä se, että aktiivisesti käytetty data on mahdollisimman lähellä sitä laskentayksikköä, joka tekee työn.

Siksi yhtenäismuistikin kannattaa nähdä ennen kaikkea tapana vähentää kovia kapasiteettirajoja, ei lupauksena siitä että jokainen suuri malli käyttäytyisi kuin se eläisi kokonaan leveässä erillisessä VRAMissa.

## Milloin 8 Gt GPU + paljon RAMia on silti järkevä ratkaisu

Tällainen kone voi olla erittäin hyvä, jos tavoitteesi on jokin näistä:

- ajaa 7B- tai 8B-luokan kvantisoituja malleja fiksusti
- käyttää GPU:ta osittaiseen offloadiin CPU-ajon tueksi
- opetella paikallisten mallien workflow't ilman kallista GPU-hankintaa
- hyväksyä, että kaikkein suurimmat mallit ovat enemmän kokeiluja kuin päivittäisiä työkaluja
- priorisoida hiljaisuus, hinta tai kokonaiskoneen monikäyttöisyys

Tämä on minusta usein parempi tapa ajatella asiaa kuin jahtaa "halpaa tapaa saada 24 Gt VRAM". Sellaista ei yleensä oikeasti synny vain lisäämällä RAMia.

## Milloin isompi VRAM on oikea ratkaisu

Suurempi GPU-muisti on yleensä oikea vastaus, jos jokin näistä toistuu jatkuvasti:

- joudut aggressiivisesti kvantisoimaan enemmän kuin haluaisit
- suurempi konteksti romahduttaa nopeuden
- mallinvaihto tai offload-sekoilu tekee ajosta epätasaista
- käytät konetta nimenomaan interaktiiviseen keskusteluun, et vain batch-ajoihin
- haluat vähemmän säätöä ja enemmän ennustettavuutta

Tässä kohtaa lisä-VRAM ei ole enää luksusta vaan suora käytettävyysparannus.

## Oma ostosääntöni harrastajalle

Jos mietin rahankäyttöä paikalliseen LLM-koneeseen, kysyisin nämä kolme kysymystä tässä järjestyksessä:

1. **Mitä mallikokoa oikeasti käytän arjessa?**
2. **Haluaanko mallin vain käyntiin vai myös tuntuvan sujuvalta?**
3. **Onko hitauteni tällä hetkellä kapasiteettiongelma vai muistiliikenteen ongelma?**

Jos vastaus kakkoseen on "haluan sujuvan tuntuman", isompi VRAM on hyvin usein arvokkaampi kuin pelkkä lisä-RAM. Jos taas tavoite on saada enemmän asioita edes mahdollisiksi pienellä budjetilla, suuri RAM voi olla erittäin järkevä ensimmäinen askel.

## Yhteenveto

Miksi 8 Gt GPU ja paljon RAMia ei tunnu 24 Gt VRAMilta? Koska muistimäärä ja muistipaikka eivät ole sama asia. Iso RAM voi auttaa mallin mahtumisessa ja pitää projektin liikkeessä, mutta se ei poista sitä, että GPU toimii parhaiten omalla lähellä olevalla muistillaan.

Lyhyt muistilappu on tämä: **RAM voi pelastaa yhteensopivuuden, mutta VRAM pelastaa usein käyttökokemuksen**.

## Lähteet

- https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html
- https://github.com/ggml-org/llama.cpp/discussions/6124
- https://en.wikipedia.org/wiki/PCI_Express
