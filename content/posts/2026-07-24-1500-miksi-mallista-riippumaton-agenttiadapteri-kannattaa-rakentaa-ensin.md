---
title: "Miksi mallista riippumaton agenttiadapteri kannattaa rakentaa ensin"
date: "2026-07-24T15:00:00+03:00"
draft: false
phase: "new-era"
allow_same_day: true
topic_family: "ai-models"
series:
  - "Tekoaly ja agentit"
tags:
  - "agent"
  - "adapter"
  - "mcp"
  - "architecture"
  - "tooling"
---
## Tiivistelmä
Jos rakennat agentin suoraan yhden mallitarjoajan erikoisuuksien päälle, vertailu näyttää aluksi nopealta mutta vaihtaminen muuttuu myöhemmin kalliiksi. Siksi suosin mallista riippumatonta adapterikerrosta jo ennen ensimmäistä kunnollista mallivertailua.

## Mikä adapterissa oikeastaan on ideana

Ajatus on yksinkertainen: oma sovelluksesi ei puhu suoraan jokaisen mallin omalla murteella, vaan yhden sisäisen sopimuksen kautta. Käytännössä sovelluksella voi olla esimerkiksi kolme vakaata rajaa:

- pyydä vastaus
- pyydä rakenteinen vastaus
- aja työkalusilmukka

Näiden alla voi sitten olla yksi tai useampi provider.

## Providerin vaihtaminen on helpompaa paperilla kuin tuotannossa

OpenAI:n Agents SDK -dokumentaatio puhuu malleista, providereista ja transport-strategiasta erillisinä valintoina. Se on hyvä ajattelutapa laajemminkin: mallin ominaisuudet, provider-polku ja kuljetuskerros eivät ole sama asia. Kun ne sekoitetaan yhteen, myös debuggaus sekoittuu.

Tyypillinen virhe näyttää tältä:

- promptit kirjoitetaan yhden providerin omituisuuksille
- työkalumäärittelyt vuotavat läpi suoraan sovelluskoodiin
- tuloksen jäsentäminen nojaa yhden API:n sivuvaikutuksiin

Sitten kun haluat kokeilla toista mallia, et vaihdakaan vain mallia. Vaihdat samalla suuren kasan oletuksia.

## MCP tekee tämän rajan näkyväksi

OpenAI:n MCP- ja connector-docs sekä itse MCP-arkkitehtuurikuvaus korostavat yhteistä työkalupintaa: malli näkee yhtenäisen työkalurekisterin, vaikka taustalla olisi monta eri järjestelmää. Sama idea kannattaa pitää myös mallikerroksessa. Kun työkalut ja mallit sidotaan selkeisiin sopimuksiin, koko agentti pysyy vaihdettavana.

Tämä ei tarkoita, että kaikki mallit olisivat samanlaisia. Päinvastoin. Se tarkoittaa, että erot rajataan sinne missä niiden kuuluu näkyä: adapteriin, ei koko sovelluksen jokaiseen tiedostoon.

## Mitä adapteriin kannattaa oikeasti laittaa

Hyvä ensimmäinen versio on yllättävän pieni:

1. yksi yhtenäinen tapa välittää viestit ja järjestelmäohje
2. yksi tapa kuvata työkalut ja niiden skeemat
3. yksi tapa pyytää structured output
4. yksi paikka provider-kohtaisille retry-, timeout- ja logging-säännöille

Kun nämä ovat yhdessä kerroksessa, mallivertailu muuttuu oikeasti vertailuksi eikä arkkitehtuurin uudelleenkirjoitukseksi.

## Johtopäätös

Mallivertailu kannattaa aloittaa arkkitehtuurista, ei pelkästä rankingista. Jos rakennat ensin ohuen adapterin, voit myöhemmin testata uusia malleja, vaihtaa providereita ja säätää tool loopia ilman että koko agentti menee uusiksi.

## Lähteet

- https://developers.openai.com/api/docs/guides/agents/models
- https://developers.openai.com/api/docs/guides/tools-connectors-mcp
- https://modelcontextprotocol.io/docs/learn/architecture
