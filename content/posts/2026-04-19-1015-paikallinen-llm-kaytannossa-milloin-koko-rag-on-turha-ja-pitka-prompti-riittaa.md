---
title: "Paikallinen LLM käytännössä: milloin koko RAG on turha ja pitkä prompti riittää?"
date: 2026-04-19T10:15:00+03:00
draft: false
topic_family: "llm-hardware"
---

Paikallisia malleja rakentaessa yksi yleinen harha on tämä: heti kun puhutaan omista dokumenteista, pitää rakentaa täysi RAG-pino. Käytännössä näin ei aina ole. Jos aineisto on riittävän pieni, selkeä ja usein käytetty, pitkä prompti voi olla yksinkertaisempi, halvempi ja luotettavampi ratkaisu kuin erillinen chunkkaus, embedding-haku ja rerankkaus.

Tämä on hyvä uutinen erityisesti kotilabroihin, joissa tavoite ei ole rakentaa näyttävää arkkitehtuuria vaan saada hyödyllinen paikallinen assistentti toimimaan mahdollisimman vähällä liikkuvien osien määrällä.

## Milloin pitkä prompti oikeasti riittää

Yksinkertainen sääntö on tämä: jos koko tietopohja mahtuu käytännöllisesti mallin kontekstiin, testaa ensin suora prompti ennen kuin rakennat RAG-järjestelmän. Anthropicin käytännön ohje on vielä suorempi: jos tietopohja on alle noin 200 000 tokenia, koko aineiston sisällyttäminen promptiin voi olla täysin järkevä ratkaisu.

Kotikäytössä tämä kattaa yllättävän monta tapausta:

- yhden projektin dokumentaatio
- oma runbook tai huolto-ohjeet
- pienen yhdistyksen tai tiimin sisäinen wiki
- pari kymmentä usein käytettyä markdown-tiedostoa
- yhden asiakkaan rajattu aineisto testikäytössä

Jos kysymykset kohdistuvat samaan pieneen aineistoon toistuvasti, pitkä prompti voi olla paitsi helpompi myös luotettavampi. Tällöin vältät yhden koko RAG-maailman hankalimman kohdan: väärän chunkin löytymisen.

## Miksi RAG epäonnistuu yllättävän helposti

RAG kuulostaa elegantilta, mutta käytännössä se hajottaa tiedon pieniksi paloiksi. Tämä on samalla sen vahvuus ja heikkous. Kun dokumentit pilkotaan, yksittäinen chunk voi menettää juuri sen taustan, joka tekisi siitä haettavan ja ymmärrettävän.

Anthropic kuvaa tätä hyvin esimerkillä, jossa lause kertoo liikevaihdon kasvaneen 3 prosenttia, mutta chunkista ei enää selviä minkä yrityksen tai aikajakson kohdalla näin tapahtui. Haku voi siis löytää semanttisesti "samantyyppistä" tietoa mutta silti väärän kohdan.

Tämän takia RAG-järjestelmät lisäävät helposti uusia kerroksia:

- parempi chunkkaus
- embeddings-haku
- BM25 tai muu sanahaku
- tulosten yhdistäminen
- rerankkaus

Tämä voi olla oikein tarpeellista suurissa aineistoissa. Pienissä aineistoissa se voi myös olla aivan turhaa koneistoa, joka lisää vikapisteitä ilman että lopputulos paranee.

## Missä BM25 ja muu haku silti auttavat

BM25 on hyvä muistutus siitä, ettei kaikki tieto ole puhdasta "merkityksen hakua". Joissain kyselyissä tarvitaan tarkkaa merkkijonon osumaa, esimerkiksi virhekoodia, mallinumeroa tai dokumentin täsmällistä termiä. BM25:n vahvuus on juuri siinä: se etsii sanoja ja fraaseja dokumenteista ilman että kaiken pitää kulkea semanttisen upotteen kautta.

Jos rakennat paikallista RAG:ia esimerkiksi tekniseen dokumentaatioon, logeihin tai koodivarastoon, tällainen tarkka haku voi olla erittäin hyödyllinen. Mutta taas sama nyrkkisääntö pätee: jos aineisto on pieni, voi olla helpompaa antaa koko aineisto mallille ja välttää se vaihe, jossa ensin täytyy arvata mikä pieni osa siitä pitäisi nostaa esiin.

## Milloin RAG kannattaa oikeasti rakentaa

RAG alkaa olla perusteltu, kun jokin näistä pitää paikkansa:

- aineisto ei enää mahdu järkevään kontekstiin
- aineisto muuttuu usein ja sitä on paljon
- vasteajan pitää pysyä kurissa isossa tietopohjassa
- kyselyt osuvat vain pieneen osaan koko materiaalista
- haluat skaalata useisiin tietolähteisiin ilman että jokainen pyyntö paisuu valtavaksi

Tällöin retrieval tuo aitoa hyötyä. Mutta vasta silloin. Liian moni rakentaa RAG:in heti, vaikka todellinen tarve olisi vain syöttää mallille muutama tärkeä tiedosto siististi.

## Oma käytännön etenemisjärjestys

Jos rakentaisin paikallista dokumenttiassistenttia kotilabraan tänään, etenisin näin:

1. aloita yhdellä mallilla ja yhdellä pienellä tietopohjalla
2. testaa ensin koko aineiston syöttö promptiin
3. mittaa vastausten laatu ja viive
4. siirry RAG:iin vasta, jos konteksti käy oikeasti liian suureksi tai tarkkuus alkaa kärsiä
5. lisää ensin yksinkertainen retrieval, ja vasta myöhemmin monimutkaisempi yhdistelmä kuten embeddings + BM25 + rerankkaus

Tämä säästää aikaa, rahaa ja hermoja. Se myös opettaa paremmin, missä todellinen pullonkaula on. Joskus se on retrieval. Yllättävän usein se on vain liian innokas arkkitehtuuripäätös liian aikaisin.

## Yhteenveto

Milloin koko RAG on turha ja pitkä prompti riittää? Silloin, kun aineisto on rajattu, mahtuu kontekstiin ja haluat maksimoida yksinkertaisuuden sekä minimoida väärien hakutulosten riskin.

RAG ei ole väärä ratkaisu. Se on vain usein liian aikainen ratkaisu. Paikallisissa LLM-projekteissa kannattaa aloittaa helpoimmasta toimivasta versiosta ja lisätä retrieval vasta, kun siihen on selvä tekninen syy.

## Lähteet

- https://www.anthropic.com/engineering/contextual-retrieval
- https://en.wikipedia.org/wiki/Okapi_BM25
