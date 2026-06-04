---
title: "Miksi `ollama ps` näyttää `CPU/GPU`-jakoa, ja mitä se tarkoittaa paikallisessa LLM-koneessa?"
date: "2026-06-04T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "Paikallinen LLM käytännössä"
tags:
  - "Local LLM"
  - "Ollama"
  - "VRAM"
  - "GPU"
  - "Troubleshooting"
---
Kun `ollama ps` näyttää mallin kohdalla esimerkiksi `48%/52% CPU/GPU`, ensimmäinen reaktio on usein väärä: moni tulkitsee sen suoraksi todisteeksi siitä, että "nyt tarvitaan heti isompi näytönohjain". Käytännössä tuo näkymä kertoo vain yhden asian varmasti: **malli ei juuri nyt elä kokonaan GPU-muistissa**, vaan osa työstä tai mallista on valunut myös järjestelmämuistin puolelle. Se voi johtua aidosta VRAM-pulasta, mutta yhtä usein syy on liian aggressiivinen konteksti, rinnakkaisuus tai se, että koneessa on jo valmiiksi muita malleja ladattuna.

Minun käytännön sääntöni on tämä: **älä tee ostospäätöstä pelkän `CPU/GPU`-jaon perusteella ennen kuin tarkistat samalla kontekstin, rinnakkaisuuden ja montako mallia Ollama yrittää pitää muistissa.** Vasta sen jälkeen tiedät, onko ongelma raudassa vai asetuksissa.

## Mitä `ollama ps` oikeastaan kertoo

Ollaman FAQ dokumentoi tämän suoraan: `PROCESSOR`-sarake kertoo, onko malli ladattu kokonaan GPU:lle, kokonaan CPU:lle vai osittain molempiin. Lisäksi `api/ps`-rajapinta näyttää koneellisesti luettavassa muodossa ainakin mallin koon, `size_vram`-arvon ja käytössä olevan `context_length`-asetuksen.

Tämä on tärkeä ero. `ollama ps` ei ole vain "mukava statusnäkymä", vaan nopein tapa nähdä kolme käytännön kysymystä kerralla:

1. mahtuuko malli kokonaan GPU:lle
2. paljonko VRAMia on oikeasti varattu
3. millä kontekstilla ajo tapahtuu juuri nyt

Jos siis näet sekalaisen `CPU/GPU`-jaon, aloittaisin aina tästä:

```bash
ollama ps
curl http://127.0.0.1:11434/api/ps
```

CLI on nopeampi ihmisen silmälle. API taas on hyödyllinen, jos haluat vertailla useita ajoja tai lokittaa tilanteen talteen.

## Yleisin syy ei ole "huono GPU", vaan muistibudjetti joka karkasi sivuun

Ollaman kontekstidokumentaatio sanoo kaksi asiaa, jotka kuuluvat lukea yhdessä:

- suurempi konteksti kasvattaa muistitarvetta
- paras suorituskyky syntyy, kun malli pysyy kokonaan GPU:ssa eikä offloadaa CPU:lle

Sama dokumentaatio kertoo myös oletuksista: alle 24 GiB VRAM -koneissa lähtökohta on 4k-konteksti, 24-48 GiB VRAM -luokassa 32k ja siitä ylöspäin 256k. Tämä on hyödyllinen nyrkkisääntö, mutta se ei tarkoita, että jokainen malli jaksaa käytännössä saman kontekstin samalla tavalla. Jos nostat `OLLAMA_CONTEXT_LENGTH`-arvon korkeaksi, muistitarve nousee heti, vaikka itse mallitiedosto ei muuttuisi.

Käytännössä tämä näkyy usein näin:

- pieni tai keskikokoinen malli mahtuu GPU:lle 4k- tai 8k-kontekstilla
- sama malli alkaa valua osittain CPU:lle, kun konteksti nostetaan paljon suuremmaksi
- käyttäjä luulee ostaneensa "liian pienen GPU:n", vaikka todellinen ongelma on muistia syövä käyttötapa

Jos et oikeasti tarvitse pitkää kontekstia agentteihin, koodityöhön tai laajoihin dokumentteihin, ensimmäinen testi ei ole uuden kortin ostaminen vaan kontekstin laskeminen.

## Rinnakkaisuus kasvattaa muistitarvetta yllättävän nopeasti

Ollaman FAQ korostaa myös toista helposti unohtuvaa asiaa: rinnakkaiset pyynnöt kasvattavat muistitarvetta käytännössä `OLLAMA_NUM_PARALLEL * OLLAMA_CONTEXT_LENGTH` -suunnassa. Dokumentaation oma esimerkki on 2k-konteksti neljällä rinnakkaisella pyynnöllä, joka muuttuu käytännössä 8k:n muistikulutukseksi.

Tämä on mielestäni yksi yleisimmistä syistä siihen, miksi kotilabran LLM-kone käyttäytyy "epävakaasti":

- yksi testi komentoriviltä näyttää hyvältä
- myöhemmin sama malli onkin agenttien, automaatioiden tai usean rinnakkaisen pyynnön alla
- `ollama ps` alkaa näyttää osittaista CPU/GPU-jakoa
- käyttäjä syyttää mallia tai rautaa, vaikka oikea muutos tapahtuikin kuormaprofiilissa

Jos sinulla on pieni tai keskikokoinen GPU, testaisin aina ainakin kerran näin:

1. `OLLAMA_NUM_PARALLEL=1`
2. konservatiivinen `OLLAMA_CONTEXT_LENGTH`
3. vain yksi aktiivinen malli kerrallaan

Jos malli mahtuu tällä profiililla kokonaan GPU:lle, ongelma ei ollut puhtaasti "väärä GPU", vaan kapasiteetin jakaminen liian moneen asiaan yhtä aikaa.

## Useampi ladattu malli voi pilata muuten järkevän kokoonpanon

FAQ:n mukaan Ollama voi pitää useita malleja ladattuna samanaikaisesti, jos muistia riittää. Se on kätevä ominaisuus, mutta samalla klassinen ansa. Käytännössä yksi järkevä malli ja yksi taustalla hengailenut vanha malli voivat yhdessä viedä juuri sen verran VRAMia, että uusi pyyntö tipahtaa osittain CPU:n puolelle.

Tämän takia en katsoisi vain yhtä malliriviä erillään, vaan koko `ollama ps`-listaa. Jos siellä näkyy enemmän kuin yksi ladattu malli, kannattaa kysyä:

- pitääkö näiden oikeasti olla samaan aikaan muistissa
- onko `OLLAMA_MAX_LOADED_MODELS` liian antelias juuri tälle koneelle
- olisiko yksi aktiivinen malli käytännössä nopeampi kuin kaksi puoliksi mahtuvaa

Pienessä kotikoneessa "vähemmän yhtä aikaa" voittaa usein paperilla hienomman moniajon.

## Jos GPU putoaa kokonaan pois, syy voi olla ajurissa eikä mallissa

Kaikki `CPU/GPU`-ongelmat eivät ole muistibudjettiongelmia. Ollaman hardware support -sivu muistuttaa, että tuettu GPU, oikea ajuritaso ja backend-tuki ratkaisevat sen, voiko GPU:ta käyttää lainkaan. Dokumentaatio mainitsee esimerkiksi Linuxin suspend/resume-tilanteen, jossa NVIDIA-GPU voi kadota Ollamalta ja ajo fallbackaa CPU:lle. AMD:n puolella taas tuettu ROCm/HIP-polku ratkaisee paljon enemmän kuin pelkkä kortin nimi.

Tästä vedän yhden käytännön johtopäätöksen: jos `ollama ps` näyttää yhtäkkiä `100% CPU`, älä hyppää heti kvantisoinnin tai kontekstin kimppuun. Tarkista ensin:

- tunnistaako Ollama GPU:n ylipäänsä
- onko ajuri tuettu
- onko kone käynyt sleepissä tai resume-tilassa
- onko käytössä backend, jota tämä kortti oikeasti tukee

Tässä kohtaa ostoskorin avaaminen on usein aivan väärä ensimmäinen liike.

## Näin erottaisin asetuspulman oikeasta rautapulasta

Jos haluaisin päättää, onko kone todella alitehoinen vai vain väärin säädetty, tekisin kolme testiä tässä järjestyksessä:

1. Ajan mallin yhdellä rinnakkaisella pyynnöllä ja maltillisella kontekstilla.
2. Varmistan, ettei muita malleja ole turhaan ladattuna.
3. Katson vasta sitten, jääkö `PROCESSOR` edelleen osittain CPU:n puolelle.

Jos malli pysyy näillä ehdoilla `100% GPU`-tilassa, et todennäköisesti tarvitse uutta korttia saman tien. Silloin sinun pitää vain päättää, mikä on tärkeämpää:

- pidempi konteksti
- useampi rinnakkainen pyyntö
- useampi malli muistissa yhtä aikaa

Et voi yleensä maksimoida kaikkia kolmea halvassa harrastajakoneessa.

Jos taas malli valuu CPU:lle jo konservatiivisilla asetuksilla, laitteistoraja on todennäköisesti oikea. Silloin uusi GPU, pienempi kvantisointi tai pienempi malli ovat oikeita vaihtoehtoja.

## Oma peukalosääntö ennen GPU-päivitystä

Minun käytännön neuvo on tämä: **jos `ollama ps` näyttää sekajakoa, tee ensin yksi "rehellinen minimiprofiili" ennen kuin päätät että kone on liian pieni**. Se tarkoittaa:

- yksi malli
- yksi pyyntö kerrallaan
- realistinen, ei ylimitoitettu konteksti
- varmistettu GPU-tuki ja ajurit

Vasta jos tämäkin profiili jää osittain CPU:lle, pidän GPU-päivitystä aidosti perusteltuna. Muuten päivität helposti rautaa, vaikka todellinen ongelma olisi vain liian optimistinen käyttöprofiili.

Yksinkertaisesti sanottuna: `CPU/GPU`-jako ei ole ostokäsky. Se on diagnostiikkasignaali.

## Lähteet

- https://docs.ollama.com/faq
- https://docs.ollama.com/context-length
- https://docs.ollama.com/api/ps
- https://docs.ollama.com/gpu
