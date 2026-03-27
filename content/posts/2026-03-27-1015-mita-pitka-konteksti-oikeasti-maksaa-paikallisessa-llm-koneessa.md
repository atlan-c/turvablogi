---
title: "Mitä pitkä konteksti oikeasti maksaa paikallisessa LLM-koneessa?"
date: 2026-03-27T10:15:00+02:00
draft: false
---
Paikallista LLM:ää rakentaessa moni katsoo ensin vain mallin kokoa levyllä. Se on ymmärrettävää, koska GGUF-tiedoston koko näyttää konkreettiselta rajalta: jos tiedosto on 5–8 gigaa, ehkä se mahtuu 12–16 Gt VRAMille. Käytännössä tämä on kuitenkin vasta puolet tarinasta. Toinen puoli on **konteksti**, ja juuri siinä moni aloittelija arvioi raudan tarpeen pieleen.

Yksinkertainen nyrkkisääntö on tämä: **mitä pidemmän kontekstin pyydät, sitä enemmän muistia kuluu KV-välimuistiin, vaikka itse mallin koko ei muuttuisi lainkaan.** Siksi malli voi mahtua 4k-kontekstilla mutta kaatua 32k-kontekstilla samalla kvantisoinnilla ja samalla GPU:lla.

## Mikä kontekstissa oikeasti syö muistia?

llama.cpp:n käynnistyslokeissa tämä näkyy yleensä melko selvästi. Mallin painot latautuvat ensin, ja sen jälkeen ohjelma varaa erikseen **KV bufferin**. Käytännössä kyse on muistista, johon tallennetaan aiempien tokenien avain- ja arvoesityksiä, jotta malli voi käyttää aiempaa keskustelua jokaisella seuraavalla askeleella.

Tärkeä käytännön havainto on, että **KV-välimuistin koko kasvaa suunnilleen lineaarisesti kontekstin mukana**. Jos nostat kontekstin 4k:sta 8k:hon, et yleensä maksa vain pientä lisähintaa vaan merkittävän lisäsiivun muistia. Jos nostat sen 32k:hon tai 64k:hon, muistibudjetti voi karata nopeasti paljon suuremmaksi kuin aloittelija odotti.

Eräässä llama.cpp-keskustelussa Gemma 2 9B Q4_K_M -malli käytti noin 5,4 GiB CUDA-bufferia painoihin ja lisäksi noin 1,3 GiB KV-välimuistia jo 4096 tokenin kontekstilla. Tämä on hyvä muistutus siitä, että "malli mahtuu" ei yksin kerro vielä mitään koko ajon muistitarpeesta.

## Missä kohtaa harrastaja kompastuu?

Tyypillinen virhe menee näin:

- valitaan sopivan kokoinen kvantisoitu malli
- huomataan, että se mahtuu juuri ja juuri GPU:lle
- nostetaan konteksti varmuuden vuoksi isoksi
- ihmetellään, miksi ajo hidastuu tai kaatuu muistin loppumiseen

Ongelma ei silloin välttämättä ole väärä malli vaan väärä oletus siitä, että konteksti on lähes ilmainen asetus. Se ei ole. Jos koneessa on rajallisesti VRAMia, pitkä konteksti kilpailee samasta muistista kuin itse malli, laskentapuskurit ja mahdolliset muut prosessit.

## Mitä tämä tarkoittaa 12–16 Gt GPU-luokassa?

Juuri tässä hintaluokassa asia tuntuu eniten. 24 Gt kortilla on enemmän pelivaraa, mutta 12–16 Gt luokassa jokainen lisägiga on tärkeä. Käytännössä tämä tarkoittaa, että harrastajan kannattaa optimoida muistia tässä järjestyksessä:

1. **Valitse ensin järkevä mallikoko omaan käyttöön.** Älä osta kontekstia mallin laadun kustannuksella, jos et oikeasti tarvitse pitkiä dokumentteja tai valtavia keskusteluhistorioita.
2. **Pidä oletuskonteksti maltillisena.** Monessa käytössä 4k–8k riittää hyvin. Jos workflow ei tarvitse 32k:ta, sitä ei kannata pitää päällä vain varmuuden vuoksi.
3. **Käytä KV-välimuistin kvantisointia, jos työkalu tukee sitä ja laatu pysyy riittävänä.** Tämä voi olla käytännössä helpoin tapa saada lisää liikkumavaraa rajallisella VRAMilla.
4. **Jätä turvamarginaali.** Jos laskelma sanoo, että kaikki juuri ja juuri mahtuu, todellinen käyttö voi silti kaatua puskureihin, taustaprosesseihin tai eri backendin käyttäytymiseen.

## Miksi pelkkä GGUF-tiedoston koko johtaa harhaan?

Oobaboogan laajassa mittauksessa testattiin lähes 20 000 eri yhdistelmää, joissa vaihdeltiin GPU-layereita, kontekstikokoa ja KV-välimuistin kvantisointia. Tuloksen käytännön opetus oli tärkeä: **VRAM-kulutus ei ole pelkkä tiedostokoko jaettuna kerroksilla plus pieni lisä**, vaan siihen vaikuttavat yhtä aikaa mallin rakenne, GPU:lle offloadattujen kerrosten määrä, konteksti ja cache-tyyppi.

Tämä on minusta harrastajalle hyödyllisempi johtopäätös kuin yksittäinen kaava. Jos arvioit konetta vain sillä perusteella, että "7 Gt malli mahtuu 12 Gt kortille", arvio on usein liian optimistinen. Oikea kysymys on: **millä kontekstilla, millä cache-tyypillä ja kuinka paljon muuta muistia sama ajo tarvitsee?**

## Milloin pitkä konteksti on oikeasti sen arvoinen?

Pitkä konteksti kannattaa maksaa silloin, kun käyttö todella hyötyy siitä:

- analysoit pitkiä dokumentteja paikallisesti
- pidät suurta keskusteluhistoriaa samassa sessiossa
- ajat RAG-työnkulkua, jossa syötetään paljon lähdemateriaalia kerralla
- et halua pilkkoa aineistoa aggressiivisesti pieniin osiin

Mutta jos käyttö on pääosin komentoriviä, koodiapua, lyhyitä luonnoksia tai yksittäisiä kysymyksiä, erittäin suuri konteksti voi olla enemmän muistisyöppö kuin hyödyllinen ominaisuus. Moni kotilabra toimii paremmin, kun konteksti pidetään realistisena ja säästynyt muisti käytetään hieman parempaan malliin tai vakaampaan ajokokemukseen.

## Oma käytännön sääntöni

Jos rakennat paikallista LLM-konetta harrastajabudjetilla, **suunnittele ensin muistibudjetti kontekstin mukaan ja vasta sitten romantisoi mallikokoa**. Pitkä konteksti on hyödyllinen ominaisuus, mutta se ei ole ilmainen eikä aina tärkein pullonkaula. Usein parempi lopputulos tulee siitä, että ajat hieman lyhyempää kontekstia vakaasti kuin siitä, että tavoittelet näyttävää 64k-lukua paperilla ja taistelet koko ajan VRAM-rajan kanssa.

Toisin sanoen: aloittelijan kannattaa kysyä vähemmän "mikä malli mahtuu?" ja enemmän "mikä kokonaisuus mahtuu oikeassa käytössä?" Se on paljon lähempänä todellista käyttökokemusta.

## Lähteet

- llama.cpp Discussion #9936, memory allocations and KV buffer example: https://github.com/ggml-org/llama.cpp/discussions/9936
- Oobabooga, A formula that predicts GGUF VRAM usage from GPU layers and context length: https://oobabooga.github.io/blog/posts/gguf-vram-formula/
- llama.cpp documentation, token generation performance tips: https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md
