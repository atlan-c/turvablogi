---
title: "AI-rauta kotilabrassa: milloin kaksi GPU:ta on järkevämpi kuin yksi iso paikalliselle LLM:lle?"
date: "2026-06-14T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "GPU"
  - "Multi-GPU"
  - "VRAM"
  - "Local LLM"
  - "Ollama"
---
Käytettyä rautaa katsellessa vastaan tulee usein houkutteleva ajatus: **entä jos ostaisin kaksi halvempaa GPU:ta yhden kalliin ison kortin sijaan?** Paikallisessa LLM-koneessa tämä voi joskus olla järkevää, mutta paljon harvemmin kuin ensiksi näyttää. **Oma nyrkkisääntöni on yksinkertainen: jos malli mahtuu yhdelle järkevän kokoiselle GPU:lle, yksi isompi kortti on yleensä parempi valinta. Kaksi korttia alkaa kannattaa vasta silloin, kun tarvitset enemmän VRAMia kuin yksi kortti antaa tai kun tiedät jo valmiiksi säätäväsi monen GPU:n työnkulkuja.**

Tämä johtuu siitä, että paikallisen inferenssin pullonkaula ei ole vain raakamuistin määrä. Kun malli ja sen välimuistit pitää jakaa useamman GPU:n välille, mukaan tulee myös korttien välinen liikenne, backend-kohtaiset rajoitukset ja enemmän tilaisuuksia sille, että ajo hidastuu tai muuttuu hankalammaksi ylläpitää.

## Miksi yksi isompi GPU voittaa usein käytännössä?

Ollaman FAQ sanoo tämän poikkeuksellisen suoraan: jos malli mahtuu kokonaan yhdelle GPU:lle, Ollama yrittää ladata sen yhdelle kortille, koska tämä antaa tyypillisesti parhaan suorituskyvyn ja vähentää PCIe-väylän yli siirtyvän datan määrää inferenssin aikana.

Tämä on kotilabrassa tärkeä perusperiaate. Yksi 24 Gt tai 32 Gt luokan kortti on usein käytännössä mukavampi kuin kaksi pienempää korttia, jos tavoite on:

- mahdollisimman yksinkertainen käyttöönotto
- vähemmän säätöä ajureiden, backendien ja laitevalinnan kanssa
- tasainen vasteaika chatissa, koodiavussa tai RAG-ajossa
- vähemmän riskiä sille, että osa ajosta valuu hitaasti CPU:n puolelle

Yhden kortin koneessa ongelmat ovat yleensä helpompia tulkita. Jos malli ei mahdu, tiedät heti että VRAM loppuu. Kahden kortin koneessa ongelma voi olla muistijaossa, split-modessa, interconnectissa tai siinä, että käytetty backend ei toteuta monen GPU:n tilaa samalla tavalla kuin odotit.

## Milloin kaksi GPU:ta oikeasti auttaa?

`llama.cpp`:n oma multi-GPU-ohje tiivistää käyttötilanteet hyvin. Monen GPU:n ratkaisuun kannattaa tarttua silloin, kun:

- malli ei mahdu yhden GPU:n VRAMiin ja haluat pitää sen silti kokonaan kiihdyttimillä
- tarvitset enemmän läpimenoa ja hyväksyt sen, että tulos riippuu split-modesta ja GPU:iden välisestä yhteydestä

Ensimmäinen kohta on selvästi tärkein harrastajalle. Jos yksittäinen kortti ei riitä ja vaihtoehto on CPU-offload hitaaseen järjestelmämuistiin, kaksi GPU:ta voi olla täysin perusteltu ratkaisu. Se ei tee koneesta automaattisesti eleganttia, mutta se voi tehdä aiemmin epärealistisesta mallista käyttökelpoisen.

Tässä tilanteessa kannattaa ajatella ostosta ennen kaikkea **VRAM-ratkaisuna**, ei ihmelääkkeenä nopeuteen.

## Missä moni pettyy kahden GPU:n koneeseen

Suurin harhaluulo on, että kaksi GPU:ta tarkoittaa automaattisesti lähes kaksinkertaista nopeutta. `llama.cpp`:n dokumentaatio ei lupaa tätä. Päinvastoin: sama ohje varoittaa suoraan, että multi-GPU voi olla single-GPU:ta hitaampi, jos suorituskyky törmää GPU:iden välisen yhteyden nopeuteen.

Käytännössä tämä näkyy näin:

- halpa toinen kortti lisää VRAMia, mutta ei tee tokeneista dramaattisesti nopeampia
- PCIe-kaistat ja emolevyn topologia alkavat vaikuttaa enemmän kuin yhden kortin koneessa
- kaikki split-modet eivät ole yhtä kypsiä tai tuettuja kaikille arkkitehtuureille
- kokeelliset asetukset voivat antaa enemmän säätöä kuin hyötyä

Tämä on hyvä muistaa erityisesti silloin, jos vertaat vaihtoehtoja kuten:

- yksi käytetty 24 Gt kortti
- kaksi 12 Gt korttia

Pelkkä yhteenlaskettu VRAM ei kerro koko totuutta. Kahden 12 Gt kortin kone ei käyttäydy samalla tavalla kuin yksi 24 Gt kortti.

## Split-mode ratkaisee paljon enemmän kuin moni odottaa

`llama.cpp`:n ohjeessa oletus on `layer`-tila, jossa kerrokset ja KV-välimuisti jaetaan GPU:iden kesken putkitetusti. Dokumentaatio kuvaa sitä oletus- ja yhteensopivimpana valintana silloin, kun tarvitset enemmän muistia kuin yksi GPU tarjoaa ja siedät hitaampia yhteyksiä korttien välillä.

Samassa ohjeessa `tensor`-tila esitellään kokeellisena. Se voi parantaa suorituskykyä tietyissä tilanteissa, mutta mukana tulee ehtoja:

- Flash Attention pitää olla käytössä
- KV-cache ei voi olla kvantisoitu
- kaikkia arkkitehtuureja ei tueta
- ilman NCCL:ää monen GPU:n suorituskyky jää heikommaksi

Tämä on juuri se käytännön syy, miksi en suosittelisi kahden GPU:n strategiaa aloittelijalle vain siksi, että käytettyjen korttien hinnat näyttävät houkuttelevilta. Toimiva multi-GPU on enemmän kuin kaksi korttia samassa kotelossa.

## Hyvä käytännön kysymys ennen ostoa

Kysy itseltäsi tämä ennen kuin ostat toisen GPU:n:

**Yritänkö ratkaista muistiongelmaa vai nopeusongelmaa?**

Jos ongelma on muistissa, kaksi GPU:ta voi olla oikein hyvä vastaus. Jos ongelma on siinä, että haluat saman mallin vastaavan nopeammin, yksi nopeampi tai isompi kortti on usein turvallisempi sijoitus.

Ollaman konteksti-ikkunaa koskeva dokumentaatio muistuttaa myös, että suurempi konteksti kasvattaa muistitarvetta, ja parhaan suorituskyvyn vuoksi mallin CPU-offloadia pitäisi välttää. Tämä vahvistaa saman käytännön opetuksen: jos tavoitteena on pitkä konteksti tai agenttityökalut, VRAM-kapasiteetti ratkaisee ensin. Vasta sen jälkeen kannattaa miettiä, tuleeko kapasiteetti yhdestä vai kahdesta kortista.

## Milloin minä ostaisin kaksi GPU:ta?

Pitäisin kahden GPU:n ratkaisua järkevänä lähinnä tällaisissa tilanteissa:

1. haluan ajaa mallia, joka ei mahdu järkevästi yhdelle kortille ilman raskasta CPU-offloadia
2. minulla on jo yksi sopiva GPU ja toinen yhteensopiva kortti on saatavilla selvästi halvemmalla kuin iso päivitys
3. hyväksyn sen, että käyttöönotto, viritys ja vianetsintä vievät enemmän aikaa
4. käytän työkalua, jonka multi-GPU-käytös on minulle ennestään tuttu, kuten `llama.cpp`

Jos taas rakentaisin ensimmäistä paikallista LLM-konettani, menisin lähes aina näin:

1. osta ensin yksi mahdollisimman hyvä yksittäinen GPU budjettiin sopivassa VRAM-luokassa
2. säädä kvantisointi ja konteksti kuntoon
3. lisää toinen GPU vasta kun tiedät täsmälleen, mikä raja yhdessä kortissa tuli vastaan

## Tiivis johtopäätös

**Kaksi GPU:ta on paikallisessa LLM-koneessa järkevämpi kuin yksi iso vasta silloin, kun ratkaiset ennen kaikkea VRAM-rajaa etkä oleta automaattista nopeusihmettä.** Jos malli mahtuu yhdelle kortille, yksi isompi GPU on yleensä helpompi, vakaampi ja usein myös nopeampi ratkaisu. Jos malli ei mahdu, multi-GPU voi avata oven muuten liian isolle mallille, mutta hinta maksetaan monimutkaisuutena.

Siksi oma oletusvalintani on edelleen yksi mahdollisimman hyvä kortti. Toinen GPU on laajennusliike, ei lähtökohta.

## Lähteet

- https://docs.ollama.com/faq
- https://docs.ollama.com/context-length
- https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md
