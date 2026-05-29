---
title: "Paikallinen LLM vai pilvimalli: käytännön valintakriteerit"
date: "2026-05-29T11:45:00+03:00"
draft: true
topic_family: "llm-hardware"
series:
  - "Paikalliset LLM:t"
tags:
  - "Local LLM"
  - "Hardware"
  - "Security"
  - "Homelab"
  - "Troubleshooting"
---
Kysymys paikallisen LLM:n ja pilvimallin välillä esitetään usein väärin. Vastakkain asetetaan ideologiat, vaikka arjessa pitäisi vertailla työn luonnetta. Käytännössä tärkein kysymys ei ole "kumpi on parempi", vaan **mihin tehtävään tarvitset mallia, millä vasteajalla, millä kustannusmallilla ja millä tietoturvarajauksilla.**

Jos tämän jättää tekemättä, päätyy helposti kahteen huonoon lopputulokseen:

- rakennat kalliin paikallisen setupin tehtäville, joissa pilvi olisi ollut käytännöllisempi
- viet pilveen työn, joka olisi pitänyt pitää paikallisesti joko hinnan, luottamuksellisuuden tai toimintavarmuuden takia

## Ensimmäinen raja: missä data saa ylipäätään käydä

Minusta tämä on oikea aloituspiste. Jos aineisto sisältää jotain, mitä et halua tai saa siirtää ulos omasta ympäristöstäsi, vertailu lyhenee heti.

Tyypillisiä esimerkkejä ovat:

- sisäiset muistiinpanot
- asiakas- tai käyttäjädata
- keskeneräiset sopimus- tai henkilötiedot
- lokit, joissa on tunnisteita tai ympäristön yksityiskohtia
- sellainen yritys- tai kotilabradata, jonka et halua päätyvän ulkopuolisen palvelun läpi edes hetkellisesti

Näissä tapauksissa paikallinen malli voi olla heikompi paperilla, mutta silti oikea käytännön ratkaisu.

## Toinen raja: tarvitsetko laatua, nopeutta vai ennustettavuutta

Pilvimalli voittaa usein raakakyvykkyydessä, erityisesti jos tehtävä vaatii:

- vahvaa yleispäättelyä
- laajaa kielitaitoa
- pitkää kontekstia ilman suurta paikallista rautaa
- nopeaa pääsyä uusimpiin mallisukupolviin

Paikallinen malli taas voittaa eri kohdissa:

- vaste on ennustettava ilman ulkoista palveluriippuvuutta
- käyttö ei pysähdy verkkokatkoon tai palvelinongelmaan
- kustannus ei kasva jokaisesta pyynnöstä erikseen
- samaa ympäristöä voi säätää omaan työnkulkuun sopivaksi

Eli jos tärkein mittari on paras mahdollinen kertavastaus, pilvi voittaa usein. Jos tärkein mittari on hallittavuus ja jatkuva käyttö omassa ympäristössä, paikallinen malli alkaa näyttää paremmalta.

## Kolmas raja: kuinka toistuva tehtävä on

Tämä erottaa kokeilun tuotantokelpoisesta käytöstä.

Jos teet mallilla satunnaisesti:

- pari vaikeaa analyysia viikossa
- satunnaisia kirjoitus- tai ideointitehtäviä
- harvoin toistuvia selvityksiä

pilvi voi olla helpoin ratkaisu. Paikallisen setupin ylläpito voi olla enemmän vaivaa kuin siitä saatava hyöty.

Jos taas tehtävä toistuu päivittäin tai useita kertoja päivässä, paikallisen mallin edut kasvavat nopeasti. Esimerkkejä:

- samanmuotoinen loki- tai dokumenttitiivistys
- toistuva agenttityö omassa ympäristössä
- pieni sisäinen analyysiketju, joka hyötyy pienestä viiveestä
- automaatio, jossa haluat pitää koko putken omalla koneella

Toistuva työ suosii usein paikallista mallia, koska yhden kerran optimointi maksaa itsensä takaisin.

## Neljäs raja: pystytkö oikeasti ylläpitämään paikallista ratkaisua

Tämä on kohta, jossa moni innostuu liikaa. Paikallinen malli ei ole vain yksi binääri ja yksi GGUF-tiedosto. Käytännössä mukana tulee usein myös:

- ajurit
- runtime
- levytila
- varmuus siitä, mikä kvantisointi toimii milläkin raudalla
- päivitysrutiini
- loki- ja vianrajauspolku

Jos et oikeasti halua ylläpitää tätä pinoa, pilvipalvelu voi olla rehellisesti parempi työkalu. Paikallisuus on hyödyllistä vasta, kun sen mukana tuleva operointi on sinulle hyväksyttävä kustannus.

## Viides raja: onko latenssi vai riippumattomuus tärkeämpi

Pilvi on joskus nopeampi, joskus hitaampi. Se riippuu mallista, kuormasta ja käyttötavasta. Mutta yksi ero pysyy: paikallisen mallin käyttäytyminen on yleensä helpompi ankkuroida omaan ympäristöön.

Tämä voi olla tärkeää esimerkiksi silloin, kun:

- automaatio täytyy saada toimimaan myös ilman internetiä
- haluat välttää ulkoisen palvelun hetkelliset katkot
- haluat rajata vasteajan ja kapasiteetin omalla laitteella
- haluat pitää koko työnkulun yhdellä koneella auditoinnin vuoksi

Pilvi taas on usein parempi silloin, kun tarvitset nopeasti enemmän kapasiteettia ilman uutta laitteistoa.

## Käytännön päätöspuu

Jos minun pitäisi tehdä karkea valintapuu, käyttäisin tätä:

### Valitse paikallinen malli, jos:

- dataa ei haluta siirtää ulos
- tehtävä toistuu usein
- sinulla on jo sopiva rauta tai realistinen suunnitelma sille
- haluat oman ympäristön hallinnan ja audit-polun
- hieman heikompi yleinen suoritus ei kaada koko käyttötapausta

### Valitse pilvimalli, jos:

- tarvitset parasta mahdollista yleislaatua heti
- tehtävä on satunnainen eikä jatkuvaa käyttöä ole paljon
- et halua ylläpitää paikallista mallipinoa
- konteksti- tai laatutarve ylittää nykyisen paikallisen raudan realistiset rajat
- ulkoinen palveluriippuvuus on hyväksyttävä

### Käytä molempia, jos:

- kevyt ja toistuva työ kannattaa pitää paikallisesti
- vaikeat tai harvinaiset tehtävät kannattaa lähettää pilveen
- haluat erottaa luottamuksellisen työn yleisemmästä ideoinnista

Tämä hybridimalli on usein käytännössä paras, vaikka se ei olekaan ideologisesti puhdas.

## Yleisin virhe: päätät työkalun ennen käyttötapausta

Moni sanoo ensin "haluan kaiken paikalliseksi" tai "pilvi on aina parempi", ja vasta sitten miettii tehtäviä. Minusta järjestys kannattaa kääntää toisin päin.

Listaa ensin kolme todellista tehtävää:

1. mitä analysoit
2. kuinka usein
3. mitä haittaa väärästä tietoturva- tai kustannuspäätöksestä olisi

Sen jälkeen valinta on yleensä paljon helpompi.

## Yhteenveto

Paikallinen LLM vai pilvimalli? **Valinta pitäisi tehdä datan rajausten, toistuvuuden, ylläpitokyvyn ja vastevaatimusten perusteella, ei identiteettikysymyksenä.**

Paikallinen malli on vahvoilla, kun hallinta, yksityisyys ja toistuva käyttö ovat tärkeimpiä. Pilvimalli on vahvoilla, kun tarvitset parasta laatua nopeasti etkä halua ylläpitää omaa mallipinoa. Ja yllättävän usein järkevin ratkaisu on käyttää molempia eri töihin.

## Lähteet

- https://github.com/ggml-org/llama.cpp
- https://ollama.com/
