---
title: "Paikallinen RAG käytännössä: rerankeri auttaa vasta kun top-k on ensin kunnossa"
date: "2026-09-02T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "rag"
  - "reranking"
  - "agents"
---
## Tiivistelmä
Rerankeri kuulostaa helposti seuraavalta pakolliselta päivitykseltä paikalliseen RAG-pinoon. Käytännössä tärkein sääntö on tylsempi: **rerankeri auttaa vasta sitten, kun ensimmäinen haku tuo oikeat dokumentit jo ehdokasjoukkoon**. Jos relevantti kappale ei päädy edes top-k-listalle, rerankeri ei voi pelastaa mitään. Silloin ongelma on ensin chunkkauksessa, embedding-mallissa, hybridihakujen painotuksessa tai liian pienessä candidate depthissä.

Tämä on hyvä uutinen harrastajalle, koska säästyt turhalta lisämonimutkaisuudelta. Ennen kuin lisäät uutta mallia, uutta latenssia ja uuden vikapaikan putkeen, kannattaa mitata mitä ensimmäinen haku oikeasti palauttaa.

## Mitä rerankeri tekee ja mitä se ei tee

Sentence Transformersin dokumentaatio tiivistää asian hyvin. Bi-encoder tekee nopean ensimmäisen haun, ja Cross-Encoderia käytetään sitten top-k-tulosten uudelleenjärjestämiseen. Cross-Encoder saa queryn ja dokumentin yhdessä sisään ja palauttaa niiden välille relevanssipisteen.

Tästä seuraa yksi käytännön totuus, jota moni ei sano ääneen tarpeeksi usein: **rerankeri ei hae mitään uutta**. Se vain vaihtaa jo löydettyjen ehdokkaiden järjestystä. Jos oikea dokumentti on kokonaan listan ulkopuolella, rerankerin lisääminen ei nosta sitä tyhjästä näkyviin.

## Qdrantin hyödyllinen kysymys: onko oikea vastaus jo ehdokkaissa?

Qdrantin 23. elokuuta 2026 julkaistu artikkeli antaa tähän erinomaisen käytännön testin. Ennen kuin säädät rerankeria, mittaa ero nykyisen rankingin ja "täydellisesti järjestettyjen" nykyisten ehdokkaiden välillä. Artikkelin mukaan juuri tämä erotus kertoo, kuinka paljon parempi järjestys voisi parhaimmillaan vielä pelastaa.

Sama artikkeli sanoo asian vielä suoremmin: **rerankeri järjestää vain sen, mitä se saa vastaanottaa**. Jos relevantit dokumentit puuttuvat candidate listasta, vika on retrievalissä tai candidate depthissä, ei ranking-vaiheessa.

Tämä on paikallisen RAG:n ehkä tärkein sääntö. Moni yrittää korjata heikon haun lisäämällä "älykkäämmän" toisen vaiheen, vaikka ensimmäinen vaihe ei vielä tuo oikeita kappaleita pöydälle.

## Missä rerankeri yleensä kannattaa

Rerankeri on usein hyvä lisä silloin, kun huomaat tällaisen kuvion:

- oikea dokumentti näkyy usein top-20 tai top-50-joukossa
- mutta se jää liian alas, jolloin väärä kappale päätyy LLM:n kontekstiin
- ja haku toimii jo melko hyvin, mutta järjestys on epätasainen

Tällöin ongelma ei ole löydettävyys vaan järjestys. Juuri siihen Cross-Encoder-tyylinen rerankeri sopii.

Sentence Transformersin docs muistuttaa samalla kompromissista: Cross-Encoder on yleensä tarkempi kuin bi-encoder, mutta hitaampi, koska laskenta tehdään jokaiselle parille erikseen. Qdrantin FastEmbed-ohje sanoo saman käytännönläheisesti: rerankerit ovat raskaampia ja niitä kannattaa käyttää vain rajatulle dokumenttijoukolle.

Kotilabrassa tämä tarkoittaa yleensä sitä, että rerankeri on järkevä vasta kun voit pitää sen työn pienenä. Jos lähetät sille 200 pitkää chunkia joka kyselyllä, lisälaatu voi tulla liian kalliiksi vasteajan kannalta.

## Missä rerankeri lisätään liian aikaisin

Lisäisin epäilylistan kärkeen nämä tilanteet:

- top-k on niin pieni, ettei oikea osuma mahdu listalle
- chunkit ovat liian pitkiä tai liian sekalaisia
- embedding-malli ei sovi kieleen tai aineistoon
- hybridihakua ei ole säädetty, vaikka dense ja sparse täydentäisivät toisiaan

Jos jokin näistä on pielessä, rerankeri voi näyttää pienessä demossa hyödylliseltä mutta peittää vain varsinaisen ongelman. Saat ehkä hieman parempia tuloksia yhdellä kyselyllä, mutta et korjaa peruslaatua.

## Käytännön mittaus, jonka tekisin ensin

Jos rakentaisin paikallista RAG-järjestelmää tänään, tekisin ennen rerankeria tämän testin:

1. Valitse 20-50 oikeaa käyttäjäkysymystä.
2. Tarkista, löytyykö relevantti chunk jo top-5-, top-10-, top-20- tai top-50-listoilta.
3. Jos oikea osuma ei näy tarpeeksi usein edes top-20:ssa, korjaa retrieval ensin.
4. Jos oikea osuma näkyy usein mutta liian alhaalla, rerankeri on todennäköisesti oikea seuraava kokeilu.

Tämä on käytännössä sama ajatus kuin Qdrantin candidate depth -mittauksessa, mutta harrastajalle kevyemmin tehtynä. Et tarvitse heti täydellistä arviointiputkea nähdäksesi, onko ongelma "ei löydy" vai "löytyy mutta väärässä järjestyksessä".

## Paikallisessa käytössä latenssi ratkaisee nopeasti

Qdrantin dokumentaatio muistuttaa, että rerankeri analysoi queryn ja dokumentin tokenit syvällisemmin juuri siksi, että se on tarkempi. Se on samalla syy siihen, miksi se on kalliimpi vaihe. Tästä vedän yhden käytännön johtopäätöksen: **paikallisessa pinossa rerankerin pitää ansaita paikkansa jokaisella lisäforward-passilla**.

Jos käytössäsi on pieni kotipalvelin tai CPU-painotteinen kone, ero näkyy helposti. Hidas toinen vaihe voi tehdä agentista tahmean, vaikka itse LLM olisi muuten täysin riittävä. Siksi pitäisin candidate listan pienenä ja mittaisin erikseen:

- retrieval-vaiheen osumatarkkuuden
- rerankerin lisäämän viiveen
- sen, paraneeko lopullinen vastaus oikeasti eikä vain välivaiheen ranking

Viimeinen kohta on tärkeä. Jos rerankeri nostaa mittaria vähän mutta ei muuta loppuvastausta, lisäpalikka ei välttämättä ole vaivan arvoinen.

## Oma nyrkkisääntöni

Pidän tästä yksinkertaisesta päätöspuusta:

1. Jos oikea tieto ei päädy edes top-k-joukkoon, korjaa retrieval.
2. Jos oikea tieto on top-k:ssa mutta väärässä järjestyksessä, kokeile rerankeria.
3. Jos rerankeri parantaa laatua vain vähän mutta lisää paljon viivettä, jätä se pois ja pidä pino yksinkertaisena.

Tämä sääntö säästää paljon aikaa, koska se estää optimointia väärässä kerroksessa.

## Johtopäätös

Rerankeri ei ole paikallisen RAG:n oletuspäivitys vaan täsmätyökalu. Se toimii hyvin vasta silloin, kun ensimmäinen haku on jo melkein oikea. Siksi kysy ennen uuden mallin lisäämistä yksi kysymys: **näkeekö järjestelmä oikean vastauksen jo ehdokaslistalla?** Jos ei näe, rerankeri on liian aikainen korjaus. Jos näkee, se voi olla juuri oikea seuraava askel.

## Lähteet

- https://qdrant.tech/articles/when-a-reranker-is-worth-it/
- https://qdrant.tech/documentation/fastembed/fastembed-rerankers/
- https://www.sbert.net/docs/quickstart.html
- https://www.sbert.net/examples/cross_encoder/applications/README.html
