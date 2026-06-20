---
title: "Paikallinen LLM käytännössä: miksi 128k konteksti ei ole ilmainen"
date: "2026-06-20T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "Paikallinen LLM käytännössä"
tags:
  - "Local LLM"
  - "Context Window"
  - "VRAM"
  - "Ollama"
  - "vLLM"
---
Pitkä konteksti kuulostaa paikallisissa malleissa lähes aina hyvältä idealta. Jos 8k on hyödyllinen, eikö 32k tai 128k olisi vielä parempi? Käytännössä vastaus on usein "vain joskus". **Oma nyrkkisääntöni on tämä: älä nosta paikallisen LLM:n konteksti-ikkunaa maksimiin vain siksi, että malli tai käyttöliittymä sallii sen. Pitkä konteksti maksaa muistia, voi tiputtaa mallin pois täys-GPU-ajosta ja tekee usein koko koneesta kalliimman ilman että arjen laatu paranee samassa suhteessa.**

Tämä on niitä valintoja, joissa paperilla iso luku näyttää houkuttelevalta, mutta kotilabrassa tärkeämpää on kysyä mitä kuorma oikeasti tarvitsee. Moni harrastaja ajaa samaa mallia yhdellä käyttäjällä, lyhyillä keskusteluilla, lyhyillä dokumenttipätkillä tai kohtuullisella koodikontekstilla. Silloin maksimiin väännetty konteksti on helposti muistibudjetin syöjä eikä suoranaisesti hyötyominaisuus.

## Mitä konteksti oikeasti tekee

Ollaman dokumentaatio kuvaa kontekstin yksinkertaisesti: se on enimmäismäärä tokeneita, joihin malli pääsee käsiksi muistissa. Sama sivu kertoo myös, että oletusarvot riippuvat VRAM-määrästä: alle 24 GiB:n koneilla oletus on 4k, 24-48 GiB:n koneilla 32k ja vähintään 48 GiB:n koneilla 256k.

Jo tämä yksin kertoo tärkeän asian. Kontekstin oletus ei ole mielivaltainen käyttöliittymävalinta, vaan se on sidottu siihen, paljonko muistia koneessa todennäköisesti on käytettävissä. Jos nostat kontekstia paljon yli oletuksen, et pyydä vain "enemmän historiaa", vaan pyydät samalla järjestelmää varaamaan enemmän muistia.

## Miksi pitkä konteksti syö muistia niin nopeasti

Ollaman `Context length` -sivu sanoo tämän suoraan: suurempi konteksti kasvattaa mallin muistitarvetta, joten VRAMia pitää olla riittävästi ennen kuin sitä kannattaa nostaa. vLLM:n dokumentaatio sanoo saman eri kulmasta: jos haluat säästää muistia, rajoita `max_model_len`- ja `max_num_seqs`-arvoja.

Käytännön seuraus on tärkeä:

- mallin painot eivät ole ainoa muistisyöppö
- myös KV-välimuisti kasvaa kontekstin mukana
- rinnakkaiset pyynnöt kasaavat tätä muistitarvetta lisää

Siksi 7B- tai 14B-malli voi tuntua "mahtuvan helposti" yhdellä asetuksella, mutta muuttua epävakaaksi tai osittain CPU:lle valuvaksi heti kun konteksti nostetaan kunnolla ylös.

## Yleinen virhe: pitkä konteksti päälle, mutta väärälle työkuormalle

Pitkä konteksti on järkevä silloin, kun todella tarvitset paljon promptihistoriaa kerralla: pitkää dokumenttityötä, agentteja, web-hakua, koodipohjan selausta tai RAG-virtaa, jossa suuri määrä lähdemateriaalia pitää syöttää samaan pyyntöön. Ollama mainitsee nimenomaan agentit, web-haun ja koodityökalut esimerkkeinä tehtävistä, joissa kannattaa tähdätä vähintään 64k:hon.

Mutta tästä ei seuraa, että jokainen paikallinen chat tai pieni automaatio hyötyisi 64k:sta tai 128k:sta. Jos tavallinen kuormasi on esimerkiksi:

- lyhyet kysymys-vastaus-chatit
- yksi dokumentti kerrallaan
- muutaman tiedoston koodiapu
- yksi käyttäjä ilman rinnakkaisuutta

niin maksimoitu konteksti voi olla puhdasta ylimitoitusta.

## Mikä hinta väärästä valinnasta tulee käytännössä

Väärä kontekstipäätös ei näy aina heti selvänä virheilmoituksena. Usein se näkyy näin:

- malli ei enää mahdu kokonaan GPU:lle
- ensimmäinen vastaus hidastuu
- `ollama ps` näyttää osittaista CPU/GPU-jakoa
- rinnakkaiset pyynnöt alkavat tökkiä
- kone vaatii isomman GPU:n tai lisää RAMia vain siksi, että konteksti nostettiin varmuuden vuoksi liian ylös

Ollaman FAQ neuvoo tarkistamaan `ollama ps`-komennolla, latautuiko malli täysin GPU:lle vai osittain CPU:lle. Tämä on erinomainen käytännön testi. Jos kasvatit kontekstia ja sama malli siirtyi 100 % GPU-tilasta osittain CPU/GPU-tilaan, olet todennäköisesti ostanut pidemmän historian hinnalla hitaamman kokonaiskokemuksen.

## Rinnakkaisuus tekee asiasta vielä kalliimman

Pelkkä pitkä konteksti ei ole ainoa ansa. vLLM:n ohje korostaa erikseen myös batch-kokoa ja rinnakkaisten sekvenssien määrää. Se on hyvä muistutus siitä, että muistia kuluttavat samaan aikaan sekä "kuinka pitkä yksi pyyntö on" että "kuinka monta pyyntöä on elossa".

Tämä on juuri se kohta, jossa kotilabrassa tehdään usein väärä johtopäätös. Ajatellaan, että:

1. yksi käyttäjä tarvitsee joskus pitkän kontekstin
2. siis palvelimelle kannattaa asettaa pitkä konteksti aina
3. ja samalla sallitaan useita rinnakkaisia pyyntöjä

Yhdistelmä voi olla tarpeeton ja kallis. Usein parempi ratkaisu on valita ensisijaisesti jompikumpi:

- pitkä konteksti harvalle pyynnölle
- lyhyempi konteksti useammalle yhtäaikaiselle pyynnölle

Harva harrastajakone jaksaa molempia loputtomasti ilman kompromisseja.

## Milloin 128k tai enemmän on oikeasti perusteltu

Minun mielestäni pitkä konteksti on perusteltu vain, jos osaat nimetä selvästi mitä sillä ostat. Esimerkiksi:

- ajat paikallista agenttia, joka käsittelee paljon työkalu- ja hakuhistoriaa
- syötät säännöllisesti isoja dokumentteja samaan pyyntöön
- teet koodityötä, jossa samaan sessioon pitää mahduttaa paljon lähdetiedostoja
- tiedät jo testanneesi, että lyhyempi konteksti katkaisee oikeita käyttötapauksia

Jos et pysty kuvaamaan tällaista todellista käyttöä, valitsisin itse mieluummin konservatiivisemman asetuksen ja pitäisin mallin varmasti GPU:ssa.

## Milloin pienempi konteksti on järkevämpi valinta

Pienempi konteksti on yleensä parempi, jos tavoitteena on:

- halpa ja vakaa kotipalvelin
- nopea vaste yhdelle tai muutamalle käyttäjälle
- mahdollisimman hyvä token/s suhteessa rautaan
- useiden mallien testaus samalla koneella
- se, että malli mahtuu varmasti ilman CPU-offloadia

Tässä maailmassa 8k, 16k tai 32k voi olla paljon terveempi oletus kuin 64k tai 128k. Se ei kuulosta yhtä näyttävältä, mutta tuottaa usein paremman oikean käyttökokemuksen.

## Oma käytännön päätöspolku

Jos miettisin oman paikallisen mallin kontekstia, kysyisin nämä neljä asiaa tässä järjestyksessä:

1. tarvitaanko oikeasti pitkää historiaa, vai onko käyttö enimmäkseen lyhyttä
2. pysyykö malli täysin GPU:ssa valitulla asetuksella
3. tuleeko koneelle rinnakkaisia pyyntöjä tai useita sessioita
4. olisiko pienempi konteksti parempi kuin GPU-offloadin menettäminen

Jos kolmanteen tai neljänteen kohtaan tulee epävarmuutta, pienentäisin kontekstia ennen kuin alkaisin ostaa lisää rautaa.

## Tiivis johtopäätös

**Pitkä konteksti ei ole ilmainen mukavuusvalinta vaan muistibudjettipäätös.** Paikallisessa LLM-koneessa liian suuri konteksti voi syödä juuri sen kapasiteetin, jonka tarvitsisit mallin pitämiseen kokonaan GPU:ssa tai useamman pyynnön palvelemiseen vakaasti.

Jos käyttötapauksesi on aidosti agenttimainen, dokumenttipainotteinen tai muuten pitkäkontekstinen, 64k tai 128k voi olla täysin perusteltu. Mutta jos tavoite on vain hyvä ja nopea yleiskäyttöinen paikallinen malli, järkevin ratkaisu on usein pienempi konteksti, vakaampi muistibudjetti ja vähemmän turhaa numerokilpailua.

## Lähteet

- https://docs.ollama.com/context-length
- https://docs.ollama.com/faq
- https://docs.vllm.ai/en/latest/configuration/conserving_memory/
