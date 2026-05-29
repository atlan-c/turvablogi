---
title: "OpenClaw käytännössä: mitä agentilta kannattaa oikeasti pyytää?"
date: 2026-05-29T11:15:00+03:00
draft: true
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Agents"
  - "Automation"
  - "Troubleshooting"
---

Moni pettyy agenttiin samasta syystä kuin moni pettyy ensimmäiseen automaatioon: siltä pyydetään liian iso, epämääräinen ja huonosti rajattu asia yhdellä kertaa. Lopputulos ei yleensä ole täysin käyttökelvoton, mutta se on usein sekava, vaikeasti tarkistettava ja turhan kallis korjata jälkikäteen.

Käytännössä paras kysymys ei ole "miten saan agentista enemmän älyä", vaan **mikä on sellainen tehtävä, jonka agentti voi tehdä luotettavasti ilman että joudun luovuttamaan sille koko järjestelmää tai koko päätösvaltaa.**

Tässä postauksessa vastaan juuri siihen: mitä agentilta kannattaa oikeasti pyytää, jos haluat hyötyä etkä pelkkää näyttävää demoa.

## Hyvä agenttipyyntö on rajattu, tarkistettava ja palautuva

Turvallisin agenttityö näyttää usein aika arkiselta. Se ei ole "hoida tämä projekti loppuun", vaan esimerkiksi:

- tarkista yhden repositorion nykytila ja tee selkeä muutosehdotus
- kerää yhteen lokista näkyvät virheet ja ryhmittele ne
- kirjoita luonnos vastauksesta, älä lähetä sitä
- tee yksi rajattu muutos ja kerro mitä muuttui
- vertaa kahta vaihtoehtoa ja perustele suositus

Näissä tehtävissä on yksi yhteinen piirre: ihminen pystyy vielä helposti tarkistamaan lopputuloksen.

Tämä on minusta hyvä nyrkkisääntö. **Jos et itse pysty nopeasti katsomaan, menikö työ oikein, tehtävä on agentille vielä liian iso tai väärin muotoiltu.**

## Huono pyyntö: tavoite on oikein, mutta rajat puuttuvat

Agentille annetaan usein tällaisia pyyntöjä:

- "paranna tätä palvelinta"
- "korjaa blogi"
- "tee tästä automaatio"
- "käy nämä viestit läpi ja hoida asia"

Ihminen kyllä ymmärtää mitä näillä ehkä tarkoitetaan, mutta koneelle ne ovat liian avoimia. Silloin agentti joutuu arvaamaan ainakin nämä asiat itse:

- mikä on tärkein tavoite
- mitä ei saa rikkoa
- missä hakemistossa tai järjestelmässä saa toimia
- mikä on riittävä lopputulos
- milloin pitää pysähtyä ja kysyä

Juuri tämä arvauskerros aiheuttaa suurimman osan käytännön ongelmista.

## Paras käyttötapa: pyydä agentilta yhtä selkeää työvaihetta

Hyvä agenttipyyntö sisältää yleensä nämä osat:

1. **kohde** – missä työ tehdään
2. **tavoite** – mitä pitäisi saada aikaan
3. **rajaus** – mitä ei saa tehdä
4. **todiste** – miten onnistuminen tarkistetaan
5. **raportointi** – mitä agentin pitää kertoa lopuksi

Esimerkiksi tällainen pyyntö on jo paljon turvallisempi:

> Tarkista tämän repositorion nykyinen blogiarkisto, ehdota kevyet löydettävyyttä parantavat muutokset, tee ne vain Hugo-templateihin ja CSS:ään, älä muuta julkaistuja URL-osoitteita, ja raportoi lopuksi mitä tiedostoja muutit ja mitä en pystynyt vielä varmistamaan ilman paikallista buildia.

Tässä agentti ei joudu arvaamaan kaikkea. Siksi se tekee yleensä vähemmän vahinkoa ja enemmän hyödyllistä työtä.

## Mihin agentti sopii erityisen hyvin

Minusta agentti toimii parhaiten viidessä tehtävätyypissä.

### 1. Tilan kartoitus

Agentti on hyvä lukemaan läpi hakemistorakennetta, configia, dokumentaatiota ja viimeisimpiä muutoksia. Tämä on hyödyllistä etenkin silloin, kun itse tiedät kyllä mitä haluat, mutta et halua käyttää ensimmäistä varttia pelkkään orientaatioon.

### 2. Rajatut toteutusmuutokset

Kun muutos on pieni ja vaikutusalue tiedossa, agentti voi olla nopea. Esimerkkejä:

- yksi lint- tai tyylikorjaus
- yksi template-parannus
- yksi skriptimuutos
- dokumentaation päivitys

### 3. Vertailu ja triage

Jos vaihtoehtoja on 2–3, agentti pystyy usein rakentamaan nopeasti järkevän vertailun. Tämä on paljon hyödyllisempää kuin pyytää sitä "päättämään paras ratkaisu" tyhjästä.

### 4. Luonnostelu

Luonnos on turvallinen formaatti. Agentti voi kirjoittaa draftin blogipostauksesta, changelogista, runbookista tai vastausluonnoksesta ilman, että lopullinen päätös katoaa ihmiseltä.

### 5. Toistuvan työn paketointi

Kun tehtävä toistuu samalla kaavalla, agentti on hyvä tekemään siitä siistimmän ja dokumentoidumman version. Tärkeää on silti pitää ensimmäinen versio yksinkertaisena.

## Mihin agenttia ei kannata päästää liian aikaisin

Tämä on mielestäni yhtä tärkeää kuin hyvät käyttökohteet.

Agentilta ei kannata pyytää ensimmäisenä ainakaan näitä:

- monivaiheinen muutos ilman selvää pysäytysehtoa
- ulospäin näkyvä viestintä ilman ihmisen hyväksyntää
- laaja infra- tai turvallisuusmuutos ilman tarkkaa scopea
- "etsi itse tavoite ja toteuta se" -tyyppinen itsenäisyys
- tehtävä, jossa väärä oletus tuhoaa dataa tai sekoittaa tilaa

Joskus agentti näyttää itsevarmalta juuri silloin, kun rajaus on liian löysä. Siksi turvallinen käyttö ei ole luottamuksen puutetta vaan hyvää järjestelmäsuunnittelua.

## Käytännön malli, joka toimii yllättävän hyvin

Jos minun pitäisi tiivistää yksi toimiva malli päivittäiseen käyttöön, se olisi tämä:

- pyydä agenttia **selvittämään** ennen kuin pyydät sitä **muuttamaan**
- pyydä sitä **muuttamaan yksi kerros kerrallaan**
- pyydä sitä **todentamaan pienimmällä mahdollisella tarkistuksella**
- pyydä sitä **raportoimaan epävarmuudet näkyvästi**

Toisin sanoen agentin ei tarvitse olla kaikkivoipa ollakseen hyödyllinen. Usein se on parhaimmillaan silloin, kun se tekee yhden vaiheen hyvin ja jättää lopullisen hyväksynnän ihmiselle.

## Mitä tästä kannattaa oppia

Jos agentin käyttö tuntuu kaoottiselta, ongelma ei yleensä ole se, että malli olisi liian tyhmä. Usein ongelma on yksinkertaisempi: tehtävä ei ollut tarkistettava, rajaus ei ollut riittävä tai onnistumisen määritelmä puuttui.

Siksi käytännöllisin kysymys agentille ei ole "voitko hoitaa kaiken", vaan jokin näistä:

- voitko kartoittaa tilanteen
- voitko tehdä tämän yhden turvallisen muutoksen
- voitko laatia luonnoksen
- voitko verrata vaihtoehdot
- voitko kertoa, mikä jäi epävarmaksi

Juuri tällaisissa pyynnöissä agentti muuttuu demosta työkaluksi.

## Lähteet

- https://docs.openclaw.ai/
- https://github.com/openclaw/openclaw
