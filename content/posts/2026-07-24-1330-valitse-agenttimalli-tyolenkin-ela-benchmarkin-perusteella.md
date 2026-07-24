---
title: "Valitse agenttimalli työlenkin, älä benchmarkin perusteella"
date: "2026-07-24T13:30:00+03:00"
draft: false
phase: "new-era"
allow_same_day: true
topic_family: "ai-models"
series:
  - "Tekoaly ja agentit"
tags:
  - "agent"
  - "model-selection"
  - "latency"
  - "cost"
---
## Tiivistelmä
Agenttia varten mallia ei kannata valita yhdestä voittajalistasta, vaan siitä työnkulusta, jonka haluat oikeasti automatisoida. Usein ratkaisevin kolmio on paljon tylsempi kuin somekeskustelu antaa ymmärtää: **tarkkuus, viive ja hinta**.

## Miksi yksi "paras malli" on huono lähtökohta

OpenAI:n mallinvalintaopas painottaa samaa asiaa kuin käytännön tuotantotyö: mallin valinta on tasapainoa suorituskyvyn, viiveen ja kustannuksen välillä. Anthropicin työkaludocs sanoo saman käytännön kielellä: monimutkaisiin ja epäselviin työkalutehtäviin tarvitaan vahvempi malli, mutta suoraviivaisiin työkalukutsuihin kevyempi malli voi olla aivan riittävä.

Tämä on hyvä muistutus, koska agentit harvoin tekevät vain yhtä asiaa.

## Ajattele agentti työlenkkinä

Minusta hyödyllisin tapa on jakaa työ kolmeen rooliin:

- portinvartija: tunnistaa mitä käyttäjä haluaa ja tarvitseeko ylipäänsä raskasta mallia
- tekijä: tekee vaikeimman päättelyn, koodin tai suunnitelman
- viimeistelijä: muotoilee tuloksen skeemaan, tiivistää tai tarkistaa sen

Jos laitat saman raskaan mallin tekemään kaiken, saat kyllä näyttävän ratkaisun, mutta usein myös tarpeettoman kalliin ja hitaan.

## Missä kevyt malli riittää

Kevyt malli riittää usein hyvin, kun tehtävä on:

- luokitella pyyntö muutamaan tunnettuun luokkaan
- valita tunnettu työkalu selvässä tilanteessa
- purkaa teksti valmiiseen kenttärakenteeseen
- tehdä karkea triage ennen kuin vaikeampi malli kutsutaan mukaan

Juuri tässä kohtaa benchmark-voittaja on usein väärä oletus. Et tarvitse äärimmäistä päättelykykyä jokaiseen vaiheeseen, vaan riittävän vakaata käytöstä oikeassa kohdassa.

## Missä raskas malli maksaa itsensä takaisin

Vahvempi malli kannattaa säästää niihin kohtiin, joissa tehtävä on aidosti epäselvä tai monivaiheinen:

- ristiriitaisten lähteiden punninta
- pidemmän suunnitelman rakentaminen
- usean työkalutuloksen yhdistäminen
- vaikea koodimuutos tai virheen syyn päättely

Jos nämä kaikki sysätään pienelle mallille, agentti alkaa usein kompensoida virheitä lisäkutsuilla. Silloin halpa malli ei enää olekaan halpa, koska järjestelmä maksaa epävarmuuden uusintoina.

## Pidä provider-polku yksinkertaisena alussa

OpenAI:n Agents SDK -dokumentaatio suosittelee pitämään mallin ja transportin aluksi suoraviivaisina: valitse malli eksplisiittisesti ja siirry provider-overrideihin vasta kun workflow oikeasti tarvitsee sitä. Tämä on hyvä operatiivinen sääntö myös ilman kyseistä SDK:ta. Ensin yksi selkeä työlenkki, sitten vasta monimutkaisempi reititys.

## Johtopäätös

Paras agenttimalli ei ole yleinen mestari vaan oikeaan vaiheeseen sopiva työkalu. Jos työlenkki on kirkas, myös mallinvalinta kirkastuu: pieni malli tekee portinvartijan työn, vahvempi malli ratkaisee vaikean kohdan, ja koko järjestelmä pysyy halpana sekä nopeampana kuin yksi iso vasara kaikkeen.

## Lähteet

- https://developers.openai.com/api/docs/guides/model-selection
- https://developers.openai.com/api/docs/guides/agents/models
- https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use
