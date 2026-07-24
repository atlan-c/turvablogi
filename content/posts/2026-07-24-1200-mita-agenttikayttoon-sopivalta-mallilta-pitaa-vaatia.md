---
title: "Mitä agenttikäyttöön sopivalta mallilta pitää vaatia?"
date: "2026-07-24T12:00:00+03:00"
draft: false
phase: "new-era"
allow_same_day: true
topic_family: "ai-models"
series:
  - "Tekoaly ja agentit"
tags:
  - "agent"
  - "structured-output"
  - "tool-use"
  - "evaluation"
---
## Tiivistelmä
Jos mallia aiotaan käyttää agentissa eikä pelkkänä chat-ikkunana, ensimmäinen kysymys ei ole "kuinka fiksulta se kuulostaa", vaan **kuinka luotettavasti se pysyy osana järjestelmää**. Minun listani alkaa neljästä asiasta: työkalukutsut, rakenteinen ulostulo, virheen tunnistaminen ja ennustettava käytös pidemmässä työnkulussa.

## Älä aloita benchmarkista

Moni valitsee mallin liian aikaisin yleisistä ranking-listoista. Se on ymmärrettävää, mutta agenttityössä ongelma näkyy heti: korkea yleisälykkyys ei vielä tarkoita, että malli osaa palauttaa oikean skeeman, valita oikean työkalun tai pysähtyä silloin kun tieto puuttuu.

Jos rakennat agentin, mallilta pitäisi vaatia vähintään nämä:

- se osaa kutsua työkaluja rajatulla sopimuksella
- se pysyy sovitussa rakenteessa ilman jatkuvaa jälkikorjausta
- se erottaa puuttuvan tiedon arvauksesta
- se ei romahda heti, kun tehtävässä on useampi vaihe

## Työkalukutsu on enemmän kuin lisäominaisuus

OpenAI kuvaa function callingin keinona liittää malli ulkoisiin järjestelmiin ja sovelluksen tarjoamiin toimintoihin. Anthropic puhuu samasta asiasta tool use -mallina: malli valitsee työkalun, palauttaa rakenteisen kutsun ja varsinainen sovellus tekee oikean työn. Käytännössä tämä tarkoittaa, että agenttimallin pitää osata **pyytää toimintaa oikealla muodolla**, ei vain ehdottaa sitä luonnollisella kielellä.

Jos malli ei tee tätä vakaasti, loppu arkkitehtuuri alkaa täyttyä regex-paikkauksista, fallback-haaroista ja "jos malli sattuu kirjoittamaan oikein" -logiikasta.

## Rakenteinen ulostulo on usein tärkeämpi kuin nokkela selitys

Structured output -tuki on agentissa aliarvostettu ominaisuus. OpenAI:n docs korostaa JSON-skeemaan sidottua structured outputs -mallia juuri siksi, että downstream-koodi voi luottaa vastauksen muotoon paremmin kuin vapaaseen tekstiin tai kevyeen JSON-toiveeseen.

Tämä on arjessa iso ero. Agentti, joka antaa kauniin kappalevastauksen mutta rikkoo joka kolmannen skeeman, on huonompi kuin malli, joka on hieman tylsempi mutta palauttaa kelvollisen rakenteen joka kerta.

## Hyvä malli osaa myös sanoa "en tiedä"

Toinen käytännön vaatimus on epävarmuuden käsittely. Agenttiympäristössä hallusinaatio ei näy vain vääränä lauseena. Se voi näkyä vääränä parametrina, vääränä työkaluna tai täysin keksittynä resurssina. Siksi mallin pitää tunnistaa puuttuva tieto ja pyytää täydennystä tai lisähakua ennen kuin se jatkaa.

## Pieni tarkistuslista ennen kuin sitoudut malliin

Ennen kuin rakennat mitään mallin varaan, testaa ainakin nämä:

1. Palauttaako malli pyydetyn skeeman ilman korjauslenkkejä?
2. Valitseeko se oikean työkalun kahden tai kolmen vaihtoehdon joukosta?
3. Mitä se tekee, kun yksi vaadittu arvo puuttuu?
4. Pysyykö laatu samana myös pidemmässä monivaiheisessa promptissa?

## Johtopäätös

Agenttikäyttöön sopiva malli ei ole vain "paras yleismalli". Se on malli, joka toimii luotettavana komponenttina. Jos työkalukutsut ja structured output eivät pysy kasassa, muu järjestelmä joutuu maksamaan erotuksen käsityönä.

## Lähteet

- https://developers.openai.com/api/docs/guides/function-calling
- https://developers.openai.com/api/docs/guides/structured-outputs
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview
