---
title: "JSON vai vapaa teksti? Structured outputin paikka paikallisessa LLM:ssä"
date: "2026-08-09T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "structured-output"
  - "json-schema"
  - "llama-cpp"
---
## Tiivistelmä
Structured output kuulostaa helposti ominaisuudelta, joka kannattaa laittaa aina päälle, jos paikallinen LLM on osa ohjelmaa tai agenttia. Käytännössä tärkein sääntö on yksinkertaisempi: **pakota rakenne vain silloin, kun vastauksen on oikeasti mentävä koneellisesti eteenpäin ilman käsityötä**. Jos seuraava askel odottaa kelvollista JSONia, tarkkaa valintaa tai tiettyä muotoa, rajoitettu generointi säästää aikaa. Jos taas haluat mallilta vapaan selityksen, ideointia tai luonnollista keskustelua, liian tiukka rakenne voi tehdä vastauksesta tarpeettoman kömpelön.

## Mitä structured output paikallisessa pinossa oikeasti tarkoittaa

Perusidea on sama eri toteutuksissa: mallin ei anneta tuottaa mitä tahansa tekstiä, vaan generointia rajataan ennalta määritellyllä muodolla.

Llama.cpp:n GBNF-opas kuvaa tämän suoraan. Grammarin avulla voidaan pakottaa malli tuottamaan esimerkiksi validia JSONia tai muuta tarkasti rajattua rakennetta. Samassa dokumentissa muistutetaan myös, että `llama.cpp` osaa muuntaa osan JSON Schemasta grammatiksi.

vLLM:n structured outputs -dokumentaatio taas näyttää käytännön rajapinnan: pyynnössä voi rajoittaa vastauksen valintalistaan, regexiin, JSON-skeemaan tai kielioppiin. SGLangin dokumentaatio sanoo saman vielä eksplisiittisemmin: yhdelle pyynnölle voi antaa JSON-skeeman, regexin tai EBNF:n, ja ulostulo noudattaa annettua rajoitetta.

Käytännössä tämä ei siis ole "parempi prompti", vaan **dekoodauksen aikana tehtävä aitaus**, joka ohjaa mitä tokeneita malli saa seuraavaksi valita.

## Milloin rakenne kannattaa pakottaa

Structured output on yleensä hyvä idea, jos jokin näistä pitää paikkansa:

- vastaus parsitaan heti ohjelmallisesti seuraavaan vaiheeseen
- agentin pitää valita tarkasti yksi toiminto, tila tai luokka
- haluat JSONin, jonka kentät tarkistetaan suoraan koodissa
- epäonnistunut muoto aiheuttaa helposti ketjureaktion työkalukutsussa

Tyypillinen kotilabran esimerkki on pieni agentti, joka palauttaa vain tämänkaltaisen rungon:

```json
{
  "action": "search_docs",
  "reason": "user asked about install flags",
  "needs_clarification": false
}
```

Tässä tilanteessa vapaa tekstivastaus on usein huonompi kuin tarkasti rajattu rakenne. Jos seuraava ohjelman vaihe odottaa kenttiä `action` ja `needs_clarification`, rikkoutunut muoto on oikea virhe eikä vain esteettinen haitta.

## Milloin sitä ei kannata käyttää ensimmäisenä ratkaisuna

Structured output ei korjaa kaikkea. Jos ongelma on se, että malli ei ymmärrä tehtävää, rajoitettu formaatti ei tee siitä yhtäkkiä viisaampaa. Se voi kyllä pakottaa vastauksen oikeaan kuoreen, mutta sisällön laatu voi silti olla väärä.

Jättäisin rakenteen usein pois ainakin näissä tapauksissa:

- haluat pitkän luonnollisen selityksen ihmiselle
- tehtävä on luova tai vaihtoehtoisia vastauksia on monta hyvää
- schema on niin monimutkainen, että sen ylläpito maksaa enemmän kuin säästö
- mallin pitää ensin ajatella laajasti ja vasta lopuksi tiivistää tulos

Hyvä nyrkkisääntö on tämä: jos tarkistat tuloksen joka tapauksessa käsin ennen käyttöä, täysin pakotettu rakenne ei aina tuo suurinta hyötyä.

## Aloittelijan yleinen virhe: luotetaan pelkkään skeemaan

Llama.cpp:n dokumentaatio nostaa esiin yhden käytännössä tärkeän yksityiskohdan: JSON-skeemaa käytetään vain ulostulon rajaamiseen, eikä sitä automaattisesti syötetä mallille ymmärrettäväksi tehtävänannoksi. Dokumentti sanoo tämän suoraan. Jos haluat mallin ymmärtävän, millaista rakennetta odotat ja mitä kentät tarkoittavat, asia kannattaa kertoa myös promptissa.

SGLang antaa saman suuntaisen neuvon: paremman laadun vuoksi pyynnössä on hyvä sanoa eksplisiittisesti, että vastaus pitää tuottaa pyydetyssä muodossa.

Tämä on tärkeä harrastajalle, koska muuten syntyy helppo harha:

- muoto on oikein
- kenttien nimet ovat oikein
- mutta sisältö on silti väärä tai vajaa

Structured output takaa muodon paljon luotettavammin kuin merkityksen.

## Käytännön valinta: JSON schema, regex vai grammar

Jos joutuisin valitsemaan nopeasti, etenisin näin:

1. käytä `choice`- tai enum-tyyppistä rajausta, kun vaihtoehtoja on vain muutama
2. käytä regexiä, kun muoto on lyhyt ja yksinkertainen, kuten tunnus tai sähköposti
3. käytä JSON Schemaa, kun vastaus menee suoraan sovelluslogiikkaan
4. käytä grammar- tai EBNF-rajausta, kun tarvitset tarkempaa rakennetta kuin pelkkä JSON antaa

vLLM:n dokumentaatio tukee tätä ajattelutapaa hyvin, koska se tarjoaa erikseen `choice`-, `regex`-, `json`- ja `grammar`-tyypit. SGLangin dokumentaatio taas muistuttaa, että yhdessä pyynnössä käytetään vain yhtä rajoitetyyppiä kerrallaan, mikä helpottaa päätöstä: valitse yksinkertaisin väline, joka riittää.

## Missä paikallisessa LLM-ajossa kompromissi näkyy

Rakennerajoitus ei ole ilmainen lisäkerros. Llama.cpp:n GBNF-opas varoittaa suorituskykyyn liittyvistä sudenkuopista, ja erityisesti tehottomasti kirjoitetut toistot voivat hidastaa samplausta paljon. Tämä on hyvä muistutus siitä, että grammar ei ole vain tuotosmuotoa kuvaava tiedosto, vaan se vaikuttaa myös generoinnin työnkulkuun.

Kotipalvelimessa tämä näkyy yleensä näin:

- yksinkertainen JSON-skeema on usein halpa ja hyödyllinen
- monimutkainen grammar voi lisätä viivettä enemmän kuin odotit
- liian tiukka rajaus voi johtaa siihen, että malli jumittaa huonoon mutta muodollisesti sallittuun ratkaisuun

Siksi aloittaisin pienestä. Jos JSON schema riittää, en kirjoittaisi omaa laajaa grammar-tiedostoa vain periaatteesta.

## Käytännön sääntö kotilabraan

Jos mietit tänään kannattaako structured output ottaa käyttöön paikallisessa mallipalvelimessa, käyttäisin tätä tarkistuslistaa:

1. kysy meneekö vastaus suoraan koneen luettavaksi vai ihmiselle
2. jos kone lukee sen, määritä pienin mahdollinen sallittu rakenne
3. kerro promptissa silti selvästi mitä kentät tarkoittavat
4. validoi vastaus myös sovelluksessa, vaikka malli olisi rajattu
5. mittaa lopuksi, nostaako rakenne viivettä liikaa omassa kuormassasi

Tämä on yleensä turvallisempi tie kuin toivoa, että malli "varmaan palauttaa siistiä JSONia" vapaalla tekstillä.

## Johtopäätös

Structured output kannattaa paikallisessa LLM:ssä silloin, kun virheellinen muoto rikkoo seuraavan vaiheen. Silloin siitä tulee käytännön luotettavuusominaisuus, ei vain siisti demotemppu. Jos taas tuotat ennen kaikkea ihmiselle tarkoitettua tekstiä, rakenne kannattaa pitää niin kevyenä kuin mahdollista. Paras kysymys ei siis ole "tukeeko tämä pino JSON-skeemaa", vaan **menettääkö työnkulku jotain olennaista, jos malli saa vastata vapaasti**.

## Lähteet

- https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md
- https://docs.vllm.ai/en/latest/features/structured_outputs/
- https://docs.sglang.io/docs/advanced_features/structured_outputs
