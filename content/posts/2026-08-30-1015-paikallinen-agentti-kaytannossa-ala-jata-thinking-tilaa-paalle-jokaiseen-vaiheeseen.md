---
title: "Paikallinen agentti käytännössä: älä jätä thinking-tilaa päälle jokaiseen vaiheeseen"
date: "2026-08-30T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "reasoning"
  - "agents"
  - "ollama"
---
## Tiivistelmä
Paikallisissa malleissa reasoning- tai thinking-tila näyttää helposti oletusarvoiselta parannukselta: enemmän ajattelua, parempi vastaus. Käytännössä kotilabrassa tärkein sääntö on usein päinvastainen. **Thinking kannattaa laittaa päälle vain niihin työvaiheisiin, joissa lisäpäättely oikeasti muuttaa lopputulosta.** Reititys, yksinkertainen luokittelu, tiukan JSON-rakenteen palautus ja monet työkalukutsujen välivaiheet ovat usein nopeampia ja vakaampia ilman pitkää ajatusjälkeä.

## Miksi tästä tulee paikallisesti isompi ongelma kuin pilvessä

Pilvipalvelussa lisäviive jää helposti piiloon, mutta omalla koneella jokainen turha reasoning-token näkyy suoraan vasteajassa, VRAM-paineessa ja rinnakkaisuuden heikkenemisenä. Jos sama malli tuottaa ensin pitkän ajatusketjun ja vasta sitten lyhyen hyötyvastauksen, agenttiputki tuntuu hitaalta vaikka varsinainen tehtävä olisi pieni.

Ongelma korostuu erityisesti silloin, kun yksi agenttikierros koostuu useasta halvasta osasta:

- pyynnön luokittelu
- sopivan työkalun valinta
- parametrien palautus JSONina
- lyhyt jatkokysymys tai vahvistus

Näissä vaiheissa et yleensä osta laatua, vaan lisäät vain odotusta.

## Qwen3 teki tästä ominaisuuden, ei sivuvaikutusta

Qwen3:n julkaisussa yksi keskeinen ajatus oli hybridinen thinking- ja non-thinking-tila. Virallinen blogi sanoo suoraan, että thinking sopii vaikeampiin ongelmiin ja non-thinking nopeisiin vastauksiin, joissa nopeus on tärkeämpi kuin syvä päättely. Tämä on hyvä muistutus harrastajalle: jos malliperhe itse tarjoaa kaksi tilaa, niitä kannattaa käyttää eri tehtäviin eikä jättää yhtä pysyvästi päälle.

Käytännössä tämä tarkoittaa, että sama paikallinen malli voi tehdä kahta eri työtä:

1. suunnitella tai ratkaista hankalamman ongelman reasoning päällä
2. hoitaa putken mekaaniset välivaiheet reasoning pois päältä

Jos kaikki ajetaan samalla "ajattele aina enemmän" -asetuksella, putki kallistuu väärään suuntaan: deterministiset apuvaiheet hidastuvat eniten.

## Ollama tekee eron näkyväksi rajapinnassa

Ollaman thinking-dokumentaatio tekee tämän käytännössä hyvin konkreettiseksi. Thinking-kykyiset mallit palauttavat erillisen `thinking`-kentän, ja `content` sisältää lopullisen vastauksen. Lisäksi dokumentaatio kertoo, että `think` voidaan asettaa pyynnössä päälle tai pois, ja joillekin malleille myös eri tasoille.

Tästä seuraa kotikäytössä tärkeä suunnittelusääntö: **thinking ei ole persoonallisuuspiirre vaan pyyntökohtainen asetus**. Älä siis päätä vain "käytän Qwen3:a" tai "käytän reasoning-mallia", vaan päätä myös missä putken kohdassa ajattelua oikeasti pyydetään.

Toinen käytännön oppi löytyy suoratoistosta. Ollaman streaming-ohje painottaa, että thinking-chunkit, tool callit ja lopullinen vastaus pitää kaikki säilyttää keskusteluhistoriaan oikein. Jos annat mallin ajatella pitkään jokaisessa välivaiheessa, historia paisuu nopeasti myös silloin kun hyötyä ei juuri tule.

## vLLM muistuttaa, ettei reasoning ole vain "enemmän tekstiä"

vLLM:n reasoning outputs -dokumentaatio näyttää, että reasoning-mallit palauttavat erillisen `reasoning`-kentän ja että eri malliperheillä thinking voi olla oletuksena päällä tai pois. Qwen3-sarjan kohdalla reasoning on dokumentaation mukaan oletuksena käytössä, ja sen poistaminen vaatii `enable_thinking=False`-asetuksen `chat_template_kwargs`-parametriin.

Tämä on tärkeä käytännön yksityiskohta. Jos vaihdat backendin mutta et tarkista oletuksia, voit kuvitella vertailevasi "samaa mallia" vaikka todellisuudessa toisessa pinossa reasoning juoksee koko ajan ja toisessa ei. Silloin mittaat yhtä aikaa mallia, backendiä ja asetuksia.

## Missä thinking kannattaa jättää pois ensimmäisenä

Jos paikallinen agentti tuntuu tahmealta, aloittaisin karsinnan näistä vaiheista:

- intentin tai viestin nopea luokittelu
- yksinkertainen työkalun valinta selkeällä skeemalla
- parametrien täyttö, jos kentät ovat pieniä ja tarkasti rajattuja
- RAG-putken päätös "haetaanko lisää vai ei", jos sääntö on yksinkertainen
- lyhyet vahvistus- ja formatointivastaukset

Ajatus on sama kuin tavallisessa ohjelmistossa: älä käytä raskainta algoritmia kohtaan, jossa kevyt if-lause riittäisi.

## Missä thinking yleensä maksaa itsensä takaisin

Reasoning-tila on silti hyödyllinen, kun työ todella vaatii välivaiheista päättelyä. Esimerkiksi:

- monivaiheinen suunnitelma ennen työkalusarjaa
- vaikea virheenjäljitys tai koodin syy-seurausanalyysi
- ristiriitaisen aineiston punninta ennen johtopäätöstä
- laajempi päätös siitä, pitääkö agentin ylipäätään toimia vai pyytää ihmiseltä vahvistus

Näissä tilanteissa lisätokenit voivat ostaa oikeasti parempaa päätöksentekoa. Mutta juuri siksi ne kannattaa kohdistaa niihin vaiheisiin eikä valuttaa jokaiseen pikkuaskelmaan.

## Näin tekisin tämän omassa kotilabrassa

Jos rakentaisin paikallista agenttia tänään, käyttäisin yksinkertaista kolmiportaista sääntöä:

1. Oletuksena thinking pois kaikista apuvaiheista.
2. Thinking päälle vain suunnittelu- tai ratkaisuvaiheeseen, jossa virheen hinta on oikeasti suurempi kuin lisäviive.
3. Mittaa erikseen koko putken läpimenoaika, ei vain yhden vastauksen laatua.

Tähän kannattaa lisätä vielä yksi käytännön testi. Aja sama tehtävä kahdesti:

- ensin reasoning päällä koko putkessa
- sitten reasoning päällä vain yhdessä valitussa kohdassa

Jos lopputulos pysyy lähes samana mutta vasteaika putoaa selvästi, löysit halvan optimoinnin ilman että vaihdoit mallia tai laitteistoa.

## Aloittelijan yleisin väärä oletus

Yleisin harha on ajatella, että thinking-tila tekee kaikesta "älykkäämpää". Paikallisessa agenttikäytössä se tekee usein vain osasta putkea puheliaamman. Malli kyllä tuottaa enemmän sisäistä päättelyä, mutta kaikki työvaiheet eivät hyödy siitä samalla tavalla.

Siksi parempi kysymys ei ole "tukeeko tämä malli reasoningia" vaan **mihin yhteen tai kahteen kohtaan reasoning kannattaa ottaa käyttöön**.

## Johtopäätös

Paikallisessa agentissa thinking kannattaa nähdä rajallisena budjettina, ei aina päällä olevana premium-tilana. Kun erotat raskaan päättelyn kevyistä välivaiheista, sama kone tuntuu nopeammalta ja agentti käyttäytyy tasaisemmin. Usein paras optimointi ei ole pienempi malli tai uusi GPU, vaan se että **lopetat ajattelun pyytämisen niissä kohdissa, joissa et oikeasti tarvitse sitä**.

## Lähteet

- Ollama thinking docs: https://docs.ollama.com/capabilities/thinking
- Ollama streaming docs: https://docs.ollama.com/capabilities/streaming
- Qwen3 announcement: https://qwenlm.github.io/blog/qwen3/
- vLLM reasoning outputs docs: https://docs.vllm.ai/en/latest/features/reasoning_outputs/
