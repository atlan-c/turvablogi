---
title: "Paikallinen LLM käytännössä: kannattaako konteksti nostaa heti 32K:hon?"
date: "2026-05-22T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "Paikalliset LLM:t"
tags:
  - "Local LLM"
  - "GPU"
  - "Hardware"
  - "Troubleshooting"
---
Paikallista LLM:ää viritellessä yksi yleisimmistä "no laitetaan tämäkin isoksi" -asetuksista on konteksti-ikkuna. Moni nostaa sen heti 16K:hon, 32K:hon tai vielä pidemmälle, koska pidempi konteksti kuulostaa automaattisesti paremmalta. Käytännössä näin ei aina ole. **Useimmille harrastajille fiksu oletus on pitää konteksti aluksi maltillisena ja nostaa sitä vasta, kun oma käyttö oikeasti tarvitsee sitä, koska pidempi konteksti syö muistia ja voi lisätä hitautta yllättävän paljon jo ennen kuin mallin painot vaihtuvat isommiksi.**

Tämä ei tarkoita, että pitkä konteksti olisi huono asia. Se tarkoittaa vain sitä, että se ei ole ilmainen.

## Mitä konteksti oikeasti tekee

Konteksti-ikkuna kertoo, kuinka paljon tokeneita malli pystyy pitämään mukana aktiivisessa työmuistissaan. Sinne menevät esimerkiksi:

- järjestelmäohje
- keskusteluhistoria
- pitkä dokumentti tai koodinpätkä
- mallin juuri tuottamat aiemmat tokenit

Jos ajat paikallista mallia vaikka Ollamalla, oletuskonteksti on dokumentaation mukaan 4096 tokenia. Sitä voi kasvattaa `OLLAMA_CONTEXT_LENGTH`-muuttujalla tai per-ajon `num_ctx`-asetuksella. Se on hyödyllinen säätö, mutta samalla juuri se kohta, jossa moni vahingossa kasvattaa muistijalanjälkeä enemmän kuin ymmärtää.

## Miksi pidempi konteksti syö muistia

Mallin painot eivät ole koko tarina. Pitkän kontekstin kanssa rinnalle kasvaa myös niin sanottu KV-välimuisti eli key-value cache. Se on käytännössä muistia, johon tallennetaan aiempien tokenien attention-laskennan tuloksia, jotta niitä ei tarvitse laskea joka askeleella uudelleen.

Hugging Facen tekninen kirjoitus selittää tämän hyvin: KV-cache voi muuttua pitkässä ajossa omaksi muistipullonkaulakseen, vaikka itse malli olisi jo kvantisoitu järkevän kokoiseksi. Samassa kirjoituksessa annetaan myös käytännön mittakaava: 7B-luokan mallilla 10 000 tokenin KV-cache voi viedä noin 5 gigatavua muistia jo yksinään, jos käytössä on fp16-tarkkuus.

Tämä on juuri se kohta, joka yllättää aloittelijan. Hän katsoo vaikka 8 Gt tai 12 Gt VRAM-korttia ja ajattelee, että "malli mahtuu, siis olen turvassa". Mutta jos konteksti nostetaan korkeaksi, osa muistista kuluukin nopeasti muuhun kuin itse painoihin.

## Käytännön esimerkki: miksi 4K voi toimia, mutta 8K tai 16K kaataa tunnelman

`llama.cpp`-keskusteluissa näkyy tästä hyvin konkreettisia lukuja. Esimerkiksi Gemma 2 9B -mallin ajossa 4096 tokenin kontekstilla loki näyttää noin 1344 MiB:n kokoisen KV-bufferin. Se on paljon muistia pelkästä kontekstista, eikä mukana ole vielä kaikki muu, kuten mallin painot ja muut compute-bufferit.

Oleellinen opetus ei ole yksi tarkka numero, koska se vaihtelee mallin rakenteen mukaan. Oleellinen opetus on tämä: **kontekstin kasvattaminen ei ole vain pieni metatietoasetus, vaan oikea muistipäätös**.

Jos koneesi toimii juuri ja juuri 4K-kontekstilla, ei ole mikään yllätys, jos 8K tai 16K tekee jostakin näistä:

- malli ei enää mahdu siististi VRAMiin
- osa ajosta valuu CPU:lle ja nopeus putoaa
- ensimmäinen tokeni tulee paljon myöhemmin
- koko prosessi kaatuu muistivirheeseen

Tämä tuntuu käyttäjästä usein siltä, että "malli meni rikki", vaikka oikeasti rikkoutui vain muistibudjetti.

## Pitkä konteksti ei auta, jos tehtävä ei tarvitse sitä

Minusta tässä on hyvä pysähtyä yhteen arkiseen kysymykseen: **mitä olet oikeasti tekemässä?**

Jos paikallinen LLM toimii tällaisissa tehtävissä:

- lyhyet kysymys–vastaus-ajot
- pienet koodimuokkaukset
- lokirivien tai virheilmoitusten tulkinta
- muutaman kappaleen tekstin tiivistys

... et usein hyödy heti massiivisesta kontekstista. Silloin 4K tai 8K voi olla täysin riittävä ja samalla huomattavasti kevyempi ajaa.

Sen sijaan pitkä konteksti alkaa oikeasti ansaita paikkansa, jos teet tällaista:

- syötät kokonaisia pitkiä dokumentteja yhdellä kertaa
- pidät hyvin pitkää keskustelusäiettä ilman tiivistystä
- ajat RAG- tai agenttityönkulkua, jossa mallille annetaan paljon taustaa kerralla
- käsittelet isoja kooditiedostoja tai useita tiedostoja yhtä aikaa

Eli pitkä konteksti on hyvä renki, mutta huono oletusarvo vain siksi, että numero näyttää hienolta.

## Missä pitkä konteksti tuntuu suorituskyvyssä

Muistinkulutus on ensimmäinen ongelma, mutta ei ainoa. Hugging Face muistuttaa myös, että pitkä konteksti rasittaa erityisesti promptin alkuvaiheen käsittelyä eli prefill-vaihetta. Se on se kohta, jossa malli "syö sisään" koko promptin ennen varsinaista generointia.

Käytännössä tämä näkyy käyttäjälle näin:

- pitkä prompti alkaa hitaammin
- ensimmäiseen tokeniin kuluva aika kasvaa
- pitkän kontekstin hyöty voi tuntua huonolta vaihtokaupalta, jos tehtävä oli oikeasti lyhyt

Tämä on tärkeä erotus. Joskus malli näyttää paperilla kykenevän 32K- tai 64K-kontekstiin, mutta kotilabrassa käyttökokemus muuttuu silti huonommaksi, koska muistia ja kaistaa ei ole tarpeeksi mukavaan ajoon.

## Parempi käytännön tapa säätää

Jos rakentaisin paikallista LLM-konetta rajallisella budjetilla, etenisin kontekstin kanssa näin:

1. aloita maltillisesta oletuksesta, esimerkiksi 4K
2. mittaa, riittääkö se oikeisiin tehtäviin
3. nosta 8K:hon vasta, jos historia tai dokumentit oikeasti katkeavat liian aikaisin
4. siirry 16K+:hon vasta, kun tiedät myös muistibudjetin kestävän sen

Tämä kuulostaa ehkä varovaiselta, mutta minusta se on paljon järkevämpää kuin ostaa tai säätää koko kone sen ympärille, että joskus voisi ehkä käyttää pitkää kontekstia.

Jos tarvitset lisää tilaa, yleensä vaihtoehtoja on kolme:

- lyhennä promptia tai tiivistä historiaa
- käytä pienempää tai aggressiivisemmin kvantisoitua mallia
- kasvata muistia oikeasti, eli enemmän VRAMia tai yhtenäistä muistia

Nämä ovat usein terveempiä ratkaisuja kuin se, että vain pakotat `num_ctx`-arvon isommaksi ja toivot parasta.

## Milloin nostaisin kontekstia hyvillä mielin

Nostaisin kontekstia ilman suurempaa epäröintiä, jos kaikki nämä pitävät suunnilleen paikkansa:

- tiedän, että tehtävä tarvitsee pitkää muistia
- olen jo nähnyt nykyisen rajan tulevan vastaan käytännössä
- koneessa on muistia enemmän kuin vain juuri ja juuri mallin painoihin
- olen valmis hyväksymään pidemmän prefill-ajan

Silloin pitkä konteksti ei ole turha luksus vaan osa oikeaa käyttötarvetta.

## Yhteenveto

Kannattaako paikallisen LLM:n konteksti nostaa heti 32K:hon? Useimmiten ei. **Pitkä konteksti kuluttaa muistia yllättävän paljon, voi hidastaa etenkin pitkän promptin alkua ja ratkaisee vain ongelman, joka pitää oikeasti olla olemassa ennen kuin se kannattaa maksaa.**

Minun nyrkkisääntöni on tämä: säädä ensin malli vakaaksi ja nopeaksi pienemmällä kontekstilla, ja nosta rajaa vasta sitten, kun oma käyttö todistaa että tarvitset lisää. Paikallisessa ajossa paras asetus ei ole suurin mahdollinen, vaan se, joka mahtuu koneeseen ilman että koko käyttötuntuma hajoaa.

## Lähteet

- https://docs.ollama.com/faq#how-can-i-specify-the-context-window-size
- https://github.com/ggml-org/llama.cpp/discussions/9936
- https://huggingface.co/blog/kv-cache-quantization
