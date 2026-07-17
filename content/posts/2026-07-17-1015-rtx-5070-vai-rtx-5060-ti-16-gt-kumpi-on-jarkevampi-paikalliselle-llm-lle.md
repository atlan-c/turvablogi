---
title: "RTX 5070 vai RTX 5060 Ti 16 Gt: kumpi on järkevämpi paikalliselle LLM:lle?"
date: "2026-07-17T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "GPU"
  - "VRAM"
  - "Ollama"
---
Jos budjetti osuu NVIDIA:n keskiluokan yläpäähän, yksi tämän hetken hankalimmista paikallisen LLM-koneen kysymyksistä on yllättävän yksinkertainen: **ostatko 12 gigatavun RTX 5070:n vai 16 gigatavun RTX 5060 Ti:n?** Pelaajalle vastaus voi kallistua helposti 5070:n suuntaan. Paikallisessa LLM-ajossa valitsisin silti usein 5060 Ti 16 Gt:n, jos tarkoitus on ajaa malleja oikeasti omalla koneella eikä vain testata niitä lyhyissä demoissa.

Tämä ei tarkoita, että RTX 5070 olisi huono kortti. Päinvastoin: NVIDIA:n omien speksien mukaan siinä on enemmän CUDA-ytimiä, leveämpi muistiväylä ja korkeampi kokonaisteholuokka kuin RTX 5060 Ti:ssä. Mutta paikallisessa LLM-käytössä ensimmäinen kysymys ei yleensä ole "kumpi on paperilla nopeampi", vaan **kumpi välttää muistirajan useammin omassa oikeassa työnkulussa**.

## Mitä speksit oikeasti kertovat

NVIDIA:n virallisten sivujen perusteella vertailu näyttää tältä:

- RTX 5060 Ti: 16 Gt GDDR7, 128-bittinen muistiväylä, 180 W TGP
- RTX 5070: 12 Gt GDDR7, 192-bittinen muistiväylä, 250 W TGP

Toisin sanoen RTX 5070 antaa enemmän raakaa GPU:ta, mutta RTX 5060 Ti antaa 4 gigatavua lisää muistikattoa ja pienemmän tehonkulutuksen. Paikalliseen LLM-koneeseen juuri tuo lisämuisti ratkaisee hämmästyttävän usein enemmän kuin nopeampi siru.

## Miksi 4 gigatavua lisää voi olla tärkeämpi kuin nopeampi kortti

Ollaman nykyinen dokumentaatio tekee muistirajan hyvin konkreettiseksi. Sen oletuskonteksti vaihtuu VRAM-määrän mukaan näin:

- alle 24 GiB VRAMia: 4k konteksti
- 24-48 GiB VRAMia: 32k konteksti
- 48 GiB tai enemmän: 256k konteksti

Lisäksi sama dokumentaatio sanoo suoraan, että web search, agentit ja koodityökalut kannattaa asettaa vähintään 64k kontekstiin. Tästä tulee paikalliselle harrastajalle tärkeä käytännön johtopäätös: **jos olet jo valmiiksi niukassa VRAM-luokassa, jokainen lisägigatavu vaikuttaa siihen, kuinka paljon joudut säätämään mallia, kontekstia ja offloadia.**

12 Gt on usein riittävä kevyelle 7B-8B käytölle ja lyhyelle kontekstille. 16 Gt ei ole maaginen raja, mutta se antaa enemmän tilaa seuraaville asioille samaan aikaan:

- mallin painot
- pidempi konteksti
- K/V-välimuisti
- runtimejen omat puskurit

Tämä näkyy arjessa niin, että 12 Gt kortti osuu herkemmin tilanteeseen, jossa osa mallista tai ajosta päätyy CPU:n puolelle. Silloin koko käyttökokemus muuttuu: vastaus voi edelleen tulla, mutta latenssi, promptin käsittely ja käyttömukavuus romahtavat.

## 5070 on parempi, jos malli mahtuu varmasti

Tästä pitää sanoa rehellisesti myös toinen puoli. Jos oma käyttö on tarkasti rajattu ja tiedät jo nyt ajavasi pääosin pieniä tai keskikokoisia kvantisoituja malleja, RTX 5070 voi olla järkevämpi ostos.

Syy on yksinkertainen: kun malli mahtuu kokonaan GPU:lle, enemmän laskentatehoa ja muistikaistaa voi näkyä parempana promptin läpimenona ja tokennopeutena. NVIDIA:n omat speksitkin kertovat, että RTX 5070 on selvästi ylemmän luokan kortti kuin RTX 5060 Ti.

Mutta tämä hyöty toteutuu vain silloin, kun työkuorma todella mahtuu. Jos joudut 12 Gt kortilla jatkuvasti pienentämään kontekstia tai vaihtamaan pienempään malliin, paperilla nopeampi kortti alkaa hävitä juuri siinä käytössä, johon se oli tarkoitus ostaa.

## Ollama sanoo asian suoraan: vältä CPU-offloadia

Ollaman context length -sivu neuvoo tarkistamaan `ollama ps` -näkymästä, onko malli kokonaan GPU:lla, ja suosittelee parhaan suorituskyvyn vuoksi välttämään mallin offloadia CPU:lle. FAQ puolestaan näyttää, miten `PROCESSOR`-sarakkeesta näkee, onko ajo `100% GPU`, `100% CPU` vai jaettu `CPU/GPU`.

Tämä on koko valinnan ydin. Paikallisessa LLM-koneessa nopein hyöty ei aina tule siitä, että GPU on hieman vahvempi, vaan siitä, että ajo pysyy kokonaan GPU:ssa. Jos 16 Gt muisti tekee tästä todennäköisempää kuin 12 Gt, se voi olla käytännössä suurempi suorituskykyparannus kuin 5070:n parempi paperispeksi.

## Missä 5060 Ti 16 Gt tuntuu paremmalta valinnalta

Valitsisin RTX 5060 Ti 16 Gt:n herkemmin, jos yksikin näistä pitää paikkansa:

- haluat käyttää paikallista koodiapuria tai agenttityötä
- ajat pitkiä dokumentteja tai reposisältöä vasten
- et halua säätää joka kerta kontekstia alas
- arvostat alempaa tehonkulutusta ja hiljaisempaa kotilabrakonetta
- haluat budjettiluokan kortin, joka sietää paremmin ensi vuoden suurempia malleja

Ollaman syyskuun 23. päivän 2025 päivitys mallien ajastukseen tukee tätä käytännön havaintoa. Sen mukaan tarkempi muistinhallinta pyrkii käyttämään enemmän GPU-muistia, vähentää out-of-memory-virheitä ja parantaa nopeutta silloin, kun enemmän kerroksia mahtuu näytönohjaimelle. Tämä ei tee 12 Gt:sta huonoa, mutta se muistuttaa siitä, että VRAM-katto ei ole sivuseikka vaan suoraan suorituskykyyn vaikuttava muuttuja.

## Missä 5070 on oikea valinta

Valitsisin RTX 5070:n, jos tiedät jo valmiiksi nämä asiat:

- käytät pääosin malleja, jotka mahtuvat hyvin 12 Gt luokkaan
- haluat samalla kortilla pelata tai tehdä muutakin GPU-raskasta työtä
- et rakenna koneesta ensisijaisesti agentti- tai koodiapuria
- hyväksyt sen, että LLM-käytössä muistikatto tulee vastaan aiemmin kuin 16 Gt vaihtoehdossa

Silloin 5070:n parempi yleis-GPU-luonne voi olla juuri oikea kompromissi.

## Oma nyrkkisääntöni

Jos koneen päärooli on paikallinen LLM, ottaisin näistä kahdesta useammin RTX 5060 Ti 16 Gt:n. Jos koneen päärooli on yleinen tehokone, jossa LLM on vain yksi käyttötapa muiden joukossa, RTX 5070 alkaa näyttää houkuttelevammalta.

Lyhyesti:

- `RTX 5060 Ti 16 Gt`: parempi valinta muistirajan takia, jos LLM on pääasia
- `RTX 5070 12 Gt`: parempi valinta, jos tiedät mallien mahtuvan ja arvostat muuta GPU-tehoa enemmän

Paikallisessa LLM-ajossa pahin ostovirhe ei yleensä ole "kortti oli liian hidas". Se on se, että **kortti oli juuri sen verran liian ahdas, että kaikki kiinnostava onnistuu vain kompromisseilla**.

## Lähteet

- https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5060-family/
- https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5070-family/
- https://docs.ollama.com/context-length
- https://docs.ollama.com/faq
- https://ollama.com/blog/new-model-scheduling
