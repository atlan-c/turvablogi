---
title: "Vaihdatko embedding-mallia? Älä kirjoita uusia vektoreita vanhan indeksin päälle"
date: "2026-09-01T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "rag"
  - "embeddings"
  - "qdrant"
---
## Tiivistelmä
Jos paikallisessa RAG-pinossa tuntuu siltä, että vanha embedding-malli on tullut tiensä päähän, vaihto ei yleensä ole pelkkä mallitiedoston päivitys. Yleisin virhe on tämä: uusi malli otetaan käyttöön, mutta vanhaan vektori-indeksiin kirjoitetaan lisää dokumentteja ikään kuin kaikki olisi yhä yhteismitallista. Lopputulos on helposti sekava haku, huonosti osuvia naapureita ja turhaa epäilyä siitä, että vika olisi LLM:ssä.

Käytännön nyrkkisääntö on yksinkertainen: **kun embedding-malli vaihtuu, käsittele sitä yleensä uutena vektoriavaruutena**. Jos et rakenna indeksiä uudelleen, tee vähintään rinnakkainen migraatio ja mittaa tulos ennen vanhan indeksin poistamista.

## Mikä tässä oikeasti menee rikki

Sentence Transformersin dokumentaatio muistuttaa kahdesta perusasiasta. Ensiksi embedding-malli tuottaa kiinteän kokoisen vektorin. Toiseksi sama kirjasto tukee myös erillistä `truncate_dim`-asetusta, jolla ulostulon dimensioita voidaan typistää.

Tämä houkuttelee vaaralliseen oikopolkuun: jos vanha indeksi odottaa vaikka 768-ulotteista vektoria ja uusi malli tuottaa 1024-ulotteisen, joku yrittää helposti pakottaa uuden mallin samaan kokoon typistyksellä tai muulla sovituksella. Teknisesti data voi silloin mahtua samaan laatikkoon, mutta se ei tarkoita, että vektorit eläisivät samassa semanttisessa avaruudessa.

Tämä viimeinen johtopäätös on osittain päätelmä, ei suora dokumenttilause: kiinteä ulottuvuus kertoo vain koosta, ei siitä, että eri mallien koordinaatit tarkoittaisivat samaa asiaa. Siksi saman pituinenkaan vektori ei automaattisesti tee vanhasta indeksistä yhteensopivaa uuden mallin kanssa.

## Mitä vektorikanta odottaa

Qdrantin dokumentaatiossa dense-vektorin koko määritellään kokoelman asetuksissa etukäteen. Samalla dokumentaatio sanoo suoraan, että muisti- ja levytila kasvavat lineaarisesti ulottuvuuden mukana. Käytännössä tämä tarkoittaa kahta asiaa:

1. Jos uusi embedding-malli tuottaa eri mittaisen vektorin, et voi vain jatkaa samaan dense-kokoelmaan ilman rakenteellista muutosta.
2. Vaikka mitta olisi sama, vanhan ja uuden mallin sekoittaminen samaan indeksiin kannattaa olettaa riskiksi, kunnes olet todistanut toisin omalla eval-setillä.

Moni huomaa vasta liian myöhään, että hakutulos heikkeni vähitellen. Syy ei ole aina siinä, että uusi malli olisi huono. Usein syy on se, että osa dokumenteista on indeksoitu yhdellä mallilla ja osa toisella, jolloin lähinaapurihaut eivät enää vertaile samanlaista signaalia keskenään.

## Turvallinen tapa vaihtaa mallia

Qdrant tukee nimettyjä vektoreita, eli samaan dataobjektiin voi tallentaa useita erikokoisia vektoreita. Tämä on käytännössä paras migraatiopolku harrastajalle ja pienelle tiimille.

Toimiva etenemisjärjestys on yleensä tämä:

1. Jätä vanha embedding-indeksi rauhaan.
2. Luo rinnalle uusi nimetty vektori tai kokonaan uusi kokoelma uudelle mallille.
3. Reindeksoi dokumentit taustalla uudella mallilla.
4. Aja sama kyselyjoukko vanhaa ja uutta indeksiä vasten.
5. Vaihda tuotantohaku vasta, kun uusi indeksi voittaa oikeissa kysymyksissä eikä vain yhdellä näyttävällä demolla.

Tämä tuntuu hitaammalta kuin "vaihdetaan malli ja katsotaan", mutta se on yleensä halvempi tie kuin viikon mittainen vikajahti agentin, chunkkauksen tai promptien ympärillä.

## Milloin täysi uudelleenindeksointi on pakollinen

Tekisin täyden uudelleenindeksoinnin heti, jos jokin näistä täyttyy:

- embedding-vektorin koko muuttuu
- vaihdat monikielisestä mallista englanninkieliseen tai toisin päin
- vaihdat dokumentti- ja kyselypromptteja ohjaavaan malliin
- vanha indeksi sisältää jo sekaisin eri mallisukupolvien dataa

Erityisesti viimeinen kohta kannattaa ottaa vakavasti. Kun indeksi on kerran "saastunut" usealla embedding-tulkinnalla, ongelma ei yleensä korjaannu pelkällä uusien dokumenttien uudelleenajolla. Silloin koko aineisto kannattaa rakentaa uudestaan hallitusti.

## Entä `truncate_dim`?

`truncate_dim` on hyödyllinen työkalu, jos haluat testata pienempää vektoria, säästää muistia tai sovittaa järjestelmää hallitusti pienempään dimensioon. En kuitenkaan käyttäisi sitä ensisijaisena keinona teeskennellä, että uusi embedding-malli on yhteensopiva vanhan indeksin kanssa.

Parempi ajattelutapa on tämä: typistys voi olla osa uuden indeksin suunnittelua, mutta se ei ole migraatio-oikotie. Jos haluat käyttää typistettyä vektoria tuotannossa, evaluoi se omana varianttinaan ja rakenna sille oma hakupolku.

## Oma käytännön sääntöni

Jos paikallisessa agentissa on päämalli, embeddings-malli ja reranker, epäilen ensin embeddings-kerrosta aina kun hakutulokset huononevat "mystisesti" mallipäivityksen jälkeen. LLM saa usein syyt niskoilleen, vaikka todellinen regressio syntyi jo siinä vaiheessa, kun dokumentit vietiin väärään vektoriavaruuteen.

Siksi pitäisin tämän säännön seinällä:

**uusi embedding-malli = uusi indeksi, kunnes toisin todistetaan**

Se säästää aikaa, hermoja ja yllättävän usein myös levyä, koska hallittu rinnakkaisajo on helpompi siivota kuin puoliksi rikottu tuotantoindeksi.

## Johtopäätös

Embedding-mallin vaihto on paikallisessa LLM- ja agenttipinossa enemmän tietomigraatio kuin pelkkä mallipäivitys. Jos kirjoitat uudet vektorit vanhan indeksin päälle, saat helposti tilanteen, jossa mikään yksittäinen osa ei näytä täysin rikkinäiseltä mutta koko haku toimii silti huonommin.

Turvallisin oletus on, että uusi malli ansaitsee oman indeksin, oman mittauksen ja oman cutover-päätöksen. Vasta sen jälkeen kannattaa poistaa vanha.

## Lähteet

- https://qdrant.tech/documentation/manage-data/collections/
- https://qdrant.tech/documentation/manage-data/vectors/
- https://www.sbert.net/docs/quickstart.html
- https://www.sbert.net/docs/package_reference/sentence_transformer/model.html
