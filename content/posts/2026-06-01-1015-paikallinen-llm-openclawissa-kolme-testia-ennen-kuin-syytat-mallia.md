---
title: "Paikallinen LLM OpenClawissa: kolme testiä ennen kuin syytät mallia"
date: "2026-06-01T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Ollama"
  - "Local LLM"
  - "Troubleshooting"
---
Paikallisen mallin kanssa on OpenClawissa yksi toistuva ansa: heti kun agentti alkaa käyttäytyä oudosti, moni syyttää itse mallia liian aikaisin. Käytännössä vika voi olla ainakin kolmessa eri kohdassa: **paikallinen backend ei vastaa oikein, OpenClawin reititys ei osu oikein tai työkalupinta on paikalliselle mallille liian raskas**. Siksi hyödyllisin rutiini ei ole satunnainen säätö vaan kolme nopeaa testiä samassa järjestyksessä. Jos ne tekee rauhassa, erotat yleensä jo muutamassa minuutissa, onko ongelma oikeasti mallissa vai jossain sen ympärillä.

Minun nyrkkisääntöni on tämä: **älä vaihda mallia, promptia ja asetuksia yhtä aikaa. Testaa ensin kuljetus, sitten reititys, sitten agenttikuorma.** Se säästää aikaa paljon enemmän kuin yhden uuden kvantisoinnin tai "ehkä tämä toinen runtime toimii paremmin" -kierroksen aloittaminen.

## 1. Testaa ensin malli ilman agenttia

OpenClawin paikallismalliopas suosittelee aloittamaan kaikkein kapeimmasta testistä: aja malli paikallisesti ilman agenttikontekstia, työkaluja tai workspace-kuormaa. Ajatus on yksinkertainen. Jos itse paikallinen palvelin ei pysty vastaamaan vakaasti lyhyeen "pong"-tyyppiseen pyyntöön, ongelma ei vielä ole OpenClawissa vaan backendissä, mallissa tai konfiguraatiossa.

Käytännössä tämä tarkoittaa kysymystä: **osaako paikallinen palvelin vastata oikein yhdelle pienelle pyynnölle?**

Jos vastaus on ei, älä siirry vielä agentin diagnostiikkaan. Tarkista ennemmin nämä:

- onko oikea malli todella ladattu
- kuunteleeko palvelin oikeassa osoitteessa ja portissa
- vastaako runtime sillä API-tyylillä, jota aiot käyttää
- pysyykö malli muistissa vai kylmälataako se itsensä joka kerta

Ollaman oma API-dokumentaatio tukee tätä työjärjestystä hyvin, koska se näyttää paikallisen HTTP-rajapinnan olevan suoraan testattavissa ilman muuta sovellusta ympärillä. Tämä on tärkeää juuri siksi, että saat ensin varmistettua yhden asian: runtime elää.

## 2. Testaa sitten OpenClawin reititys erikseen

Toinen testi on minusta se, jonka moni ohittaa. Paikallinen backend voi vastata aivan siististi suoraan omasta API:staan, mutta sama malli voi silti takkuilla vasta siinä vaiheessa, kun pyyntö kulkee OpenClawin gatewayn, provider-valinnan ja mallireferenssien läpi.

OpenClawin dokumentaatio erottaa nämä tasot fiksusti. Ensin kannattaa varmistaa paikallinen malliajo, sitten sama peruspyyntö gatewayn kautta. Tämä kertoo heti, onko vika kuljetuksessa vai orkestroinnissa.

Tässä kohtaa kannattaa ajatella ongelmaa näin:

- jos suora paikallinen ajo epäonnistuu, korjaa backend ensin
- jos suora paikallinen ajo toimii mutta gateway-ajo ei, etsi vikaa provider- tai mallikytkennästä
- jos molemmat toimivat mutta oikea agenttivuoro ei, ongelma on todennäköisesti promptikuormassa, työkalukutsuissa tai yhteensopivuuden reunoissa

Tämä jako on käytännössä arvokas, koska muuten kaikki oireet näyttävät samalta: "paikallinen malli on huono". Oikeasti malli voi olla ihan kunnossa, mutta ympärillä oleva kytkentä väärä.

## 3. Testaa lopuksi, kestääkö malli oikean agenttikuorman

Vasta kolmannessa vaiheessa kannattaa kysyä, pärjääkö paikallinen malli aidossa agenttisilmukassa. Tässä kohtaa OpenClawin paikallismalliopas on poikkeuksellisen hyödyllinen, koska se sanoo suoraan jotain, minkä moni harrastaja huomaa vasta kantapään kautta: **pieni tai aggressiivisesti kvantisoitu paikallinen malli voi näyttää hyvältä yksittäisessä testissä mutta kompastua heti, kun mukaan tulee työkaluja, järjestelmäohjeita ja pidempi konteksti**.

Juuri siksi dokumentaatio ehdottaa `localModelLean`-tilaa ja tarvittaessa mallikohtaisesti jopa työkalupinnan kaventamista. Tämä on hyvä käytännön ajatus. Jos malli toimii pienessä ajossa mutta epäonnistuu täydessä agenttivuorossa, ensimmäinen järkevä liike ei ole aina uuden mallin lataus. Usein parempi liike on pienentää kuormaa ja katsoa, muuttuuko käytös heti.

Minä käyttäisin tätä kolmatta testiä näin:

1. Aja yksi oikea, pieni agenttitehtävä.
2. Jos tulos on epäluotettava, kokeile kevyempää työkalupintaa.
3. Jos ongelma katoaa heti, syy ei ollut "paikallisuus" vaan liiallinen agenttikuorma juuri tälle mallille.

Tämä on paljon hyödyllisempi tieto kuin pelkkä tunne siitä, että "Ollama on epävakaa" tai "OpenClaw ei toimi paikallisen mallin kanssa". Usein totuus on kapeampi: juuri tämä malli, tällä kontekstilla, tällä työkalupinnalla ei riitä tähän tehtävään.

## Missä kohtaa Ollaman OpenAI-yhteensopivuus auttaa

Ollaman OpenAI-yhteensopivuus on tässä hyödyllinen mutta sitä ei pidä romantisoida. Se madaltaa liityntäkynnystä, koska olemassa oleva OpenAI-tyylinen asiakas voidaan suunnata paikalliseen endpointtiin melko pienellä muutoksella. Se ei kuitenkaan yksin takaa, että koko agenttikäytös olisi samanlainen kuin vahvemmalla pilvimallilla.

Käytännössä tämä tarkoittaa, että yhteensopivuus kannattaa lukea näin:

- **hyvä uutinen:** paikallinen backend on helppo liittää testiin
- **varoittava uutinen:** helppo liitäntä ei vielä todista työkalukäytön, pitkän kontekstin tai monivaiheisen työn laatua

Tästä syystä pidän kolmen testin järjestystä niin tärkeänä. Yhteensopiva API kertoo, että putki voidaan kytkeä. Se ei vielä kerro, että siitä kannattaa ajaa kaikkea.

## Milloin lopputulos kertoo oikeasti mallin olevan väärä

Jos kaikki kolme testiä on tehty ja ongelma pysyy, vasta silloin sanoisin rauhassa, että malli tai rauta ei ehkä sovi tähän käyttöön. Erityisen vahva signaali on tämä yhdistelmä:

- suora paikallinen ajo toimii
- gateway-ajo toimii
- mutta oikea agenttivuoro hajoaa toistuvasti, vaikka työkalupintaa on jo kevennetty

Silloin ongelma on usein käytännön kapasiteetissa: konteksti-ikkuna, työkalukäytös, latenssi tai yksinkertaisesti mallin kyky pysyä kasassa OpenClawin oikeassa tehtävämuodossa.

Tässä kohtaa minä en ensimmäisenä virittäisi lisää. Tekisin arkipäiväisemmän päätöksen:

- pidä malli rajatussa erikoisroolissa
- käytä sitä pieniin paikallisiin töihin
- jätä laajempi agenttityö vahvemmalle mallille tai järeämmälle raudalle

Se on paljon terveempi ratkaisu kuin pakottaa paikallinen malli tekemään väkisin työ, johon se ei vielä oikeasti sovi.

## Käytännön johtopäätös

Paikallisen LLM:n kanssa OpenClawissa tärkein taito ei ole nopea mallin vaihto vaan siisti vianrajaus. **Ensin malli yksin, sitten sama reitti gatewayn kautta, vasta lopuksi täysi agenttikuorma.** Kun tämän rutiinin tekee aina samassa järjestyksessä, epäonnistuminen muuttuu hyödylliseksi tiedoksi eikä vain sekavaksi säätökierteeksi.

Jos siis paikallinen setup alkaa tänään oireilla, kysy nämä kolme kysymystä tässä järjestyksessä:

1. Vastaako runtime itse ilman agenttia?
2. Vastaako sama malli OpenClawin gatewayn kautta?
3. Vastaako se vielä, kun mukana on oikea agenttikuorma ja työkalut?

Jos et tiedä, missä näistä kolmesta kohdasta vika syntyy, et vielä tiedä mitä kannattaa korjata. Kun tiedät, korjaus on yleensä paljon pienempi kuin aluksi luulit.

## Lähteet

- https://docs.openclaw.ai/gateway/local-models
- https://docs.ollama.com/api
- https://docs.ollama.com/openai
