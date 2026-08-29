---
title: "Paikallinen LLM käytännössä: miksi JSON-schema pitää selittää myös promptissa"
date: "2026-08-29T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "structured-output"
  - "json-schema"
  - "agents"
---
## Tiivistelmä
Paikallisen LLM:n structured output kuulostaa usein siltä, että riittää kun annat mallille JSON-scheman ja kaikki muuttuu luotettavaksi. Käytännössä tärkein sääntö on tämä: **schema pakottaa muodon, mutta ei automaattisesti opeta mallille mitä kenttiin kuuluu kirjoittaa**. Siksi harrastajan kannattaa kuvata odotettu sisältö yhä myös promptissa, pitää schema melko yksinkertaisena ja testata oman backendin rajat ennen kuin syyttää itse mallia "huonoksi agentiksi".

## Mikä tässä menee käytännössä pieleen

Moni paikallista mallia ajava huomaa saman ilmiön: vastaus on kyllä validia JSONia, mutta arvot ovat epätarkkoja, tyhjiä, väärässä muodossa tai muuten sovellukselle hankalia. Tämä tuntuu ristiriidalta, koska juuri structured outputin piti ratkaista luotettavuusongelma.

Ongelma on siinä, että muotorajoitus ja sisällön ymmärtäminen ovat eri asioita. Jos pyydät mallia palauttamaan esimerkiksi tiketin luokittelun, prioriteetin ja toimintasuosituksen, schema voi pakottaa nuo kentät olemassa oleviksi. Se ei silti yksin kerro mallille, miten erottaa toisistaan "bugi", "käyttötuki" ja "turvapoikkeama", ellei prompti anna siihen selvää sääntöä.

## Llama.cpp näyttää eron kaikkein selvimmin

`llama.cpp`:n grammars-ohje sanoo asian yllättävän suoraan: JSON-schemaa käytetään vain rajaamaan ulostuloa, eikä sitä injektoida promptiin. Toisin sanoen malli ei automaattisesti "näe" koko skeemaa samalla tavalla kuin moni pilvi-API:n käyttäjä helposti olettaa.

Tämä on paikallisessa käytössä iso käytännön oppi. Jos rakennat extractorin, agentin tai työkalukutsun ympärille kevyen OpenAI-yhteensopivan rajapinnan `llama.cpp`:n päälle, **pelkkä schema ei riitä ohjaukseksi**. Promptissa pitää yhä kertoa ainakin:

- mitä jokainen kenttä tarkoittaa
- milloin kenttä jätetään tyhjäksi tai `null`-arvoksi
- mitä ei saa keksiä
- mikä on toivottu tarkkuustaso

Muuten saat helposti muodollisesti oikean mutta käytännössä käyttökelvottoman JSONin.

## Ollama ja LM Studio tekevät tämän helpommaksi, mutta eivät maagiseksi

Ollaman dokumentaatio kuvaa structured outputin keinona pakottaa vastaukset JSON-schemaan. Samalla ohjeessa on minusta tärkeä realismirivi: JSON-schema kannattaa myös välittää promptissa merkkijonona, jotta malli ankkuroituu paremmin odotettuun rakenteeseen.

LM Studio puolestaan toteaa, että paikallinen palvelin voi palauttaa `/v1/chat/completions`-rajapinnasta validia JSONia annetun `response_format`-skeeman mukaan. Tämä helpottaa integraatiota paljon, koska samaa OpenAI-tyylistä asiakaskoodia voi usein käyttää sellaisenaan. Mutta LM Studionkin dokumentaatiossa vastaus tulee normaalin viestikentän sisällä merkkijonona, joka pitää vielä parsia sovelluksessa. Käytännössä siis:

1. schema auttaa pakottamaan muodon
2. sovellus joutuu silti validoimaan ja parsimaa tuloksen
3. prompti ratkaisee edelleen suuren osan siitä, ovatko kenttien arvot hyödyllisiä

Tämä on hyvä muistutus siitä, että structured output ei korvaa sovelluslogiikkaa. Se vain siirtää ongelman epämääräisestä tekstistä tiukempaan mutta edelleen testattavaan rajapintaan.

## vLLM:n malli on joustava, mutta juuri siksi mittaaminen kannattaa

vLLM:n structured output -dokumentaatio on hyödyllinen siksi, että se näyttää kuinka monta eri rajausmallia käytännössä on olemassa: valmiit vaihtoehdot, regex, JSON-schema, varsinainen grammar ja jopa backendin valinta automaattisesti tai erikseen pakotettuna. Tämä on tehokasta, mutta myös muistutus siitä, ettei "structured output" ole yksi yhtenäinen ominaisuus vaan kokonainen joukko eri toteutustapoja.

Harrastajalle tästä seuraa yksi tärkeä sääntö: **jos vaihdat backendiä, testaa sama schema uudelleen äläkä oleta semantiikan pysyvän samana**. vLLM:n docs mainitsee myös, että regex-tuki riippuu valitusta backendistä. Jos yksi palvelin hyväksyy tietyn kuvion tai skeemapiirteen ja toinen ei, vika ei välttämättä ole mallissa vaan ohjauskerroksessa.

## Missä agenttityössä tämä näkyy ensimmäisenä

Structured output alkaa tuntua todella hyödylliseltä vasta silloin, kun malli tekee jotain muutakin kuin kirjoittaa vapaata tekstiä. Esimerkiksi:

- luokittelee saapuvia viestejä
- valitsee työkaluparametreja
- tekee RAG-haun jatkopäätöksiä
- palauttaa UI:lle täsmällisen tietorakenteen

Näissä tapauksissa suurin riski ei yleensä ole täysin rikkinäinen JSON, vaan hiljainen semanttinen virhe. Kenttä on olemassa, mutta arvo on huono. Siksi tärkein testikysymys ei ole "onko tämä validia JSONia" vaan **tekisikö sovellus tämän perusteella oikean päätöksen**.

## Näin tekisin tämän kotilabrassa

Jos rakentaisin paikallista agenttiketjua tänään, käyttäisin tätä yksinkertaista järjestystä:

1. Kirjoita ensin pieni schema, jossa on vain oikeasti tarvittavat kentät.
2. Selitä promptissa jokaisen kentän merkitys luonnollisella kielellä.
3. Aseta matala lämpötila, jos tavoite on deterministinen rakenne eikä luova vastaus.
4. Validoi vastaus aina vielä sovelluksessa, vaikka backend lupaisi validin JSONin.
5. Testaa erikseen virhesyötteet, puuttuvat tiedot ja rajatapaukset.

Erityisesti viimeinen kohta erottaa demon oikeasta työkalusta. Structured output toimii vakuuttavasti helpoissa esimerkeissä lähes aina. Arvo näkyy vasta silloin, kun syöte on sotkuinen, puutteellinen tai ristiriitainen.

## Milloin schemaa kannattaa yksinkertaistaa eikä laajentaa

Jos tulokset heittelevät, ensimmäinen korjaus ei yleensä ole monimutkaisempi schema. Usein parempi ratkaisu on:

- vähemmän kenttiä
- selkeämmät enum-arvot
- yksi päätös per kutsu
- pidempi ja konkreettisempi ohjeprompti

Tämä on erityisen totta paikallisissa 7B-14B-luokan malleissa, joita moni ajaa kotona. Pienempi malli hyötyy enemmän selkeästä rajauksesta kuin hienosta skeemakikkailusta.

## Johtopäätös

JSON-schema on paikallisen LLM:n kanssa erinomainen työkalu, mutta sitä ei kannata kuvitella automaattiseksi totuuskoneeksi. **Se pakottaa rakenteen, ei ymmärrystä.** Paras käytännön tulos tulee yleensä yhdistelmästä, jossa schema rajaa muodon, prompti selittää semantiikan ja sovellus validoi lopputuloksen vielä kerran. Jos tämän muistaa, structured outputista tulee oikeasti hyödyllinen osa paikallista agenttipinoa eikä vain siistiltä näyttävä demo.

## Lähteet

- llama.cpp grammars README: https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md
- llama.cpp server README: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- LM Studio structured output docs: https://lmstudio.ai/docs/developer/openai-compat/structured-output
- Ollama structured outputs docs: https://docs.ollama.com/capabilities/structured-outputs
- vLLM structured outputs docs: https://docs.vllm.ai/en/latest/features/structured_outputs/
