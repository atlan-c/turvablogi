---
title: "AI-rauta kotilabrassa: milloin 64 Gt RAM kannattaa päivittää ennen uutta GPU:ta?"
date: "2026-06-06T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "RAM"
  - "VRAM"
  - "Ollama"
  - "Hardware"
---
Paikallista LLM-konetta päivittäessä katse osuu yleensä ensimmäisenä näytönohjaimeen. Se on ymmärrettävää, koska VRAM ratkaisee paljon. Silti yllättävän monessa kotilabrassa seuraava oikea päivitys ei olekaan uusi GPU vaan **lisää järjestelmämuistia**. Käytännön kysymys kuuluu näin: **milloin 64 Gt RAM parantaa arkea enemmän kuin seuraava GPU-ostoshaave?**

Minun nyrkkisääntöni on tämä: **päivitä RAM ennen GPU:ta silloin, kun malli valuu osittain CPU:n puolelle, ajat pitkiä konteksteja tai sama kone hoitaa useita agentti- ja automaatioprosesseja yhtä aikaa.** Jos taas tärkein ongelma on se, että haluamasi malli ei yksinkertaisesti mahdu kokonaan GPU:lle, lisä-RAM ei korvaa VRAMia. Se helpottaa selviytymistä, mutta ei poista varsinaista pullonkaulaa.

## Aloita tästä: onko mallisi oikeasti kokonaan GPU:lla?

Ollaman dokumentaatio antaa tähän hyvän käytännön testin: tarkista `ollama ps` ja katso `PROCESSOR`-sarake. Jos siinä näkyy `100% GPU`, malli on kokonaan näytönohjaimen muistissa. Jos taas näet muodon `48%/52% CPU/GPU`, osa mallista tai ajosta elää jo järjestelmämuistin puolella.

Tämä on tärkein ensimmäinen haarautumispiste:

1. Jos malli on `100% GPU`, lisä-RAM ei yleensä tee ihmeitä raakanopeudelle.
2. Jos malli on osittain `CPU/GPU`, lisä-RAM voi tehdä koneesta vakaamman ja käyttökelpoisemman.
3. Jos malli on `100% CPU`, olet käytännössä jo RAM- ja CPU-maailmassa, et VRAM-maailmassa.

Tässä kohtaa on hyvä erottaa kaksi asiaa toisistaan: **toimiiko ajo ylipäätään** ja **toimiiko se nopeasti**. Järjestelmämuisti auttaa usein ensimmäiseen. GPU auttaa useammin toiseen.

## Miksi RAM alkaa ratkaista heti, kun ajo ei enää mahdu siististi VRAMiin

`llama.cpp` kuvaa tämän suoraan: se tukee CPU+GPU-hybridi-inferenssiä, jolla voidaan osittain kiihdyttää malleja, jotka ovat suurempia kuin kokonais-VRAM. Toisin sanoen kone voi kyllä jatkaa ajoa, vaikka kaikki ei mahtuisi näytönohjaimelle. Mutta sana "hybridi" ei tarkoita samaa kuin "yhtä nopea". Se tarkoittaa ennemmin: **ajo onnistuu kompromissilla**.

Ollaman FAQ täydentää tätä käytännön näkökulmasta. Sen mukaan paras suorituskyky saadaan yleensä silloin, kun uusi malli mahtuu kokonaan yhdelle GPU:lle, koska silloin PCIe-väylän yli ei tarvitse siirtää dataa samalla tavalla kesken inferenssin. Tästä voi päätellä turvallisesti yhden harrastajalle hyödyllisen säännön: **jos ajo vuotaa CPU:n puolelle, RAM-päivitys voi estää muistipulan, mutta se ei tee hybridirakenteesta yhtä nopeaa kuin täysi GPU-ajo.**

Siksi 64 Gt RAM on usein järkevä "selviytymispäivitys", ei taikatemppu.

## Kolme tilannetta, joissa 64 Gt RAM on usein parempi seuraava ostos

### 1. Käytät tarkoituksella osittaista CPU/GPU-ajoa

Jos ajat kvantisoituja malleja, jotka mahtuvat juuri ja juuri lähelle GPU:n rajoja, lisä-RAM voi olla halpa tapa pitää kone ylipäätään käyttökelpoisena. Tällöin et ehkä tavoittele maksiminopeutta vaan sitä, että:

- malli käynnistyy luotettavasti
- käyttöjärjestelmä ei ala swapata liian aikaisin
- samalla koneella voi olla muutakin kuin yksi ainoa inference-prosessi

Tässä tilanteessa 32 Gt on usein se kohta, jossa kaikki toimii vielä "jotenkin", ja 64 Gt on se kohta, jossa kone lakkaa tuntumasta jatkuvalta kompromissilta.

### 2. Nostit kontekstin pitkäksi agentti- tai koodityössä

Ollaman context length -ohje sanoo asian suoraan: suurempi konteksti kasvattaa mallin vaatimaa muistia. Samassa dokumentaatiossa sanotaan myös, että parhaan suorituskyvyn takia mallin CPU-offloadia kannattaa välttää ja jako kannattaa tarkistaa `ollama ps`:stä.

Tämä on käytännössä tärkeää juuri siksi, että moni paikallinen LLM-kone ei enää aja pelkkää lyhyttä chattia. Kun samaa konetta käytetään:

- agenttityöhön
- koodiavustukseen
- RAG-hakuun
- pitkiin keskusteluihin

konteksti karkaa helposti paljon suuremmaksi kuin "vain kokeilen tätä mallia" -vaiheessa. Jos VRAM ei riitä koko asetelmaan siististi, lisä-RAM antaa lisää pelivaraa. Se ei poista sitä, että suuri konteksti maksaa, mutta se vähentää tilannetta jossa koko kone muuttuu epävakaaksi.

### 3. Samalla koneella on useita rinnakkaisia pyyntöjä tai useampi malli

Tämä on minusta yleisin aliarvioitu syy. Ollaman FAQ sanoo, että rinnakkaisuus kasvattaa muistitarvetta suoraan: tarvittava RAM skaalautuu `OLLAMA_NUM_PARALLEL * OLLAMA_CONTEXT_LENGTH` -logiikalla. Lisäksi useita malleja voidaan pitää muistissa vain, jos muistia on aidosti saatavilla.

Tämä tarkoittaa käytännössä sitä, että 32 Gt voi riittää yhdelle käyttäjälle ja yhdelle lyhyelle pyynnölle, mutta sama kone alkaa yskiä heti kun siihen lisätään:

- toinen agentti
- pidempi konteksti
- embedding-malli taustalle
- editori, selaimet, vektoritietokanta ja muu normaali työpöytäkuorma

Jos kone tekee muutakin kuin yhtä yksittäistä `ollama run` -komentoa, 64 Gt on paljon helpompi perustella kuin moni ensin ajattelee.

## Milloin RAM-päivitys ei ole oikea seuraava liike

On myös tilanteita, joissa lisä-RAM on vain laastari.

Älä odota 64 Gt RAM:lta liikaa, jos ongelma on oikeasti tämä:

- haluamasi malli ei mahdu millään järkevällä kvantisoinnilla kokonaan GPU:lle
- tavoite on selvästi parempi tokeninopeus, ei vain vakaus
- ajat kuvamalleja tai muita kuormia, joissa GPU on selvästi pääraja
- nykyinen kone on jo `100% GPU`, mutta haluat isomman mallin tai pidemmän kontekstin ilman offloadia

Näissä tapauksissa lisäjärjestelmämuisti voi kyllä auttaa taustalla, mutta varsinainen ratkaisu on yleensä enemmän VRAMia, toinen GPU tai pienempi malli. Käytännössä: **RAM auttaa silloin, kun yrität venyttää rajaa hallitusti. VRAM auttaa silloin, kun haluat siirtää itse rajaa.**

## Oma päätöspuu harrastajalle

Jos miettisin päivitystä tänään, käyttäisin tätä yksinkertaista järjestystä:

1. Aja malli ja tarkista `ollama ps`.
2. Jos näkyy `100% GPU`, kysy itseltäsi kärsitkö oikeasti muistipulasta vai haluatko vain enemmän suorituskykyä.
3. Jos näkyy osittainen `CPU/GPU`, tarkista myös paljonko kontekstia ja rinnakkaisuutta oikeasti käytät.
4. Jos kone toimii agentti- tai automaatiopalvelimena, laske mukaan koko muu kuorma, ei vain yhtä inferenssiä.
5. Jos 32 Gt tuntuu jatkuvalta tasapainoilulta, 64 Gt on usein järkevä ja suhteellisen edullinen vakautuspäivitys.
6. Jos tavoite on saada malli kokonaan GPU:lle, säästä ennemmin kohti suurempaa VRAM-budjettia.

## Tiivis johtopäätös

Paikallisessa LLM-koneessa 64 Gt RAM kannattaa usein päivittää ennen uutta GPU:ta silloin, kun kone toimii **sekä mallipalvelimena että yleisenä työ- tai agenttikoneena**, ja kun osa ajosta vuotaa jo CPU:n puolelle. Se tekee järjestelmästä anteeksiantavamman, vähentää muistipaineen aiheuttamaa säätöä ja auttaa etenkin pitkissä konteksteissa sekä rinnakkaisessa käytössä.

Mutta jos tavoite on päästä pois hybridi-ajosta kokonaan, lisä-RAM ei ole varsinainen ratkaisu. Se antaa tilaa kompromissille. **Varsinainen suorituskykypäivitys on yhä se, että malli mahtuu kokonaan GPU:lle.**

## Lähteet

- https://docs.ollama.com/faq
- https://docs.ollama.com/context-length
- https://github.com/ggml-org/llama.cpp
