---
title: "Paikallinen LLM käytännössä: lukitse chat-template ennen kuin vertailet malleja"
date: "2026-08-02T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "tokenizer"
  - "prompt"
  - "benchmark"
---
## Tiivistelmä
Yllättävän moni paikallisen LLM:n "mallivertailu" menee pieleen jo ennen ensimmäistä vastausta. Syy ei ole aina itse mallissa, vaan siinä että **chat-template tai tokenizer vaihtuu huomaamatta** työkalusta toiseen. Käytännössä tämä tarkoittaa, että sama testi voi antaa eri tuloksen Ollamassa, llama.cpp:ssä ja omassa skriptissäsi, vaikka GGUF tai painot näyttävät olevan samat.

Jos haluat arvioida mallia agenttikäyttöön, koodiapuun tai tavalliseen keskusteluun, tärkeä perussääntö on tämä: **lukitse template, tokenizer ja stop-säännöt ennen kuin vertailet mitään muuta**. Muuten saat helposti väärän käsityksen siitä, onko malli oikeasti huono vai syötitkö sille vain eri keskustelurakenteen.

## Miksi template ratkaisee näin paljon

Hugging Facen oma chat templating -dokumentaatio sanoo asian käytännössä suoraan: jokainen keskustelumalli odottaa tiettyä keskusteluformaattia, ja väärä template heikentää laatua tuntuvasti. Tämä on loogista, koska hienosäätö on tehty juuri tietyn roolirakenteen, erikoistokenien ja viestierottimien ympärille.

Paikallisessa käytössä ongelma syntyy helposti näin:

- lataat saman mallin kahteen eri ajoympäristöön
- toinen käyttää malliin tallennettua `tokenizer.chat_template`-metatietoa
- toinen käyttää oletustemplatea tai omaa Modelfile-rakennetta
- lopuksi vertailet vastauksia kuin kyse olisi puhtaasti mallin kyvykkyydestä

Tässä kohtaa et enää vertaile vain mallia. Vertailet mallia ja prompttiputkea yhdessä paketissa.

## Tokenizer-mismatch on hiljainen laatobugi

GGUF-dokumentaatio muistuttaa, että mallin mukana voi olla tokenizeriin liittyvää metadataa, mukaan lukien chat-template, mutta samalla se huomauttaa myös tokenisoinnin tarkkuuteen liittyvistä kompromisseista. Käytännön opetus harrastajalle on yksinkertainen: jos promptin pilkkominen tokeneiksi muuttuu ympäristöstä toiseen, myös kontekstin käyttö, stop-tokit ja vastauksen aloitus voivat muuttua.

Tämä näkyy usein kolmella tavalla:

- malli alkaa puhua väärällä roolilla
- ensimmäinen vastaus on tavallista lyhyempi tai katkeaa oudosti
- työkalukäytössä rakenne hajoaa, vaikka sama malli "toimii chatissa"

Erityisen petollista tämä on agenttikäytössä. Jos testaat työkalukutsua, JSON-rakennetta tai järjestelmäohjeen noudattamista, väärä template voi näyttää siltä kuin malli ei osaisi tehtävää lainkaan.

## Missä tämä osuu käytännössä juuri nyt

Ollaman Modelfile-dokumentaatio näyttää, että template on eksplisiittinen osa mallipakettia eikä mikään kosmeettinen lisä. Samasta syystä llama.cpp:n serveri- ja chat-template-tuki on tärkeä tarkistuskohta aina, kun vaihdat frontendiä, backendia tai GGUF-muunnosta.

Oma nyrkkisääntöni on tämä:

### 1. Vertaa ensin yhtä templatea, älä kahta runtimea

Jos vertailet kahta mallia, pidä prompttirakenne mahdollisimman vakiona. Jos vertailet kahta runtimea, pidä malli ja template täysin samoina. Älä sekoita näitä yhteen testiin.

### 2. Tarkista mistä template oikeasti tulee

Katso tuleeko keskustelurakenne:

- mallin metadatasta
- Ollaman Modelfilestä
- käyttöliittymän omasta oletuksesta
- omasta skriptistäsi

Jos et tiedä vastausta varmasti, et vielä tiedä mitä vertailit.

### 3. Lukitse myös stop-säännöt

Template ei elä yksin. Samat erikoistokenit vaikuttavat usein myös siihen, missä vastaus pysäytetään. Jos stop-säännöt vaihtuvat template-vaihdon mukana, malli voi näyttää joko ylipuhuvan tai liian niukan oloiselta ilman että sen varsinainen laatu muuttui.

### 4. Mittaa epäonnistumiset agenttitehtävällä, ei vain yhdellä chat-kysymyksellä

Yksittäinen "kerro vitsi" ei paljasta juuri mitään. Parempi testi on yksi pieni agenttityö:

- järjestelmäohje
- käyttäjän pyyntö
- vaadittu rakenne tai työkaluformaatti
- yksi tarkistettava onnistumisehto

Jos template on väärä, ongelma näkyy tällaisessa testissä nopeasti.

## Milloin epäilisin template-ongelmaa ennen malliongelmaa

Epäilisin prompttiputkea ensin, jos:

- sama malli käyttäytyy eri työkalussa täysin eri tavalla
- kvantisoinnin vaihto ei selitä eroa
- vastaus alkaa toistuvasti oudolla roolitunnisteella
- JSON tai tool calling hajoaa vain yhdessä runtime-ympäristössä
- kontekstipituus näyttää kuluvan odotettua nopeammin

Tällöin en vaihtaisi mallia ensimmäisenä. Varmistaisin ensin template- ja tokenizeriketjun päästä päähän.

## Johtopäätös

Paikallisessa LLM-käytössä chat-template ei ole pieni renderöintiyksityiskohta vaan osa itse mallin käyttöliittymää. Jos se vaihtuu huomaamatta, myös laatuvertailu, agenttitesti ja token-budjetti vääristyvät. Siksi käytännöllisin tapa säästää aikaa ei ole aloittaa uudesta benchmarkista, vaan lukita ensin template, tokenizer ja stop-säännöt. Vasta sen jälkeen mallien erot alkavat kertoa jotain hyödyllistä.

## Lähteet

- https://huggingface.co/docs/transformers/chat_templating
- https://github.com/ggml-org/ggml/blob/master/docs/gguf.md
- https://docs.ollama.com/modelfile
- https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md
