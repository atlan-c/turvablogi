---
title: "AI-rauta kotilabrassa: paljonko vapaata VRAMia kannattaa jättää paikalliselle LLM:lle?"
date: "2026-06-30T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-rauta kotilabrassa"
tags:
  - "AI-rauta"
  - "VRAM"
  - "Ollama"
  - "Paikalliset LLM:t"
  - "GPU"
---
Paikallista LLM-konetta rakentaessa moni katsoo vain yhtä lukua: paljonko mallin tiedosto vie levyltä tai paljonko VRAMia kortissa lukee laatikossa. Käytännössä tärkeämpi kysymys on usein tämä: **paljonko vapaata VRAMia kannattaa jättää mallin ympärille, jotta ajo pysyy vakaana eikä valu huomaamatta CPU:n puolelle?** Oma nyrkkisääntöni on yksinkertainen: **älä tähtää siihen, että GPU-muisti menee paperilla aivan tappiin. Jätä mieluummin selvä käyttövara, etenkin jos käytät pitkää kontekstia, pidät mallia lämpimänä muistissa tai ajat useampaa pyyntöä kuin yhtä demo-promptia kerrallaan.**

Tähän ei ole yhtä maagista yleislukua, koska oikea vara riippuu mallista, kvantisoinnista, kontekstin pituudesta ja siitä, onko koneella samaan aikaan muitakin malleja. Mutta juuri siksi "16 Gt kortti riittää, koska malli on 15,6 Gt" on harrastajalle vaarallinen laskutapa. Se on liian optimistinen.

## Miksi koko VRAM ei ole oikeasti vapaa mallille

Ollaman `Context length` -dokumentaatio sanoo suoraan kaksi hyödyllistä asiaa. Ensinnäkin suurempi konteksti kasvattaa muistitarvetta. Toiseksi paras suorituskyky tulee siitä, että malli pysyy kokonaan GPU:lla eikä offloadaudu CPU:lle. Tämä on koko aiheen ydin: VRAM ei kulu vain mallin painoihin, vaan myös siihen työtilaan, jolla malli oikeasti toimii.

Siksi sama malli voi tuntua täysin ongelmattomalta yhdessä asetuksessa ja muuttua tahmeaksi toisessa, vaikka et vaihtaisi mallia lainkaan. Jos nostat kontekstia, avaat rinnakkaisia pyyntöjä tai pidät toista mallia samalla lämpimänä, muistibudjetti kiristyy heti.

## Mitkä asiat syövät headroomin käytännössä

Kun mietit paljonko vapaata VRAMia tarvitaan, tarkista ainakin nämä:

1. Mallin oma VRAM-kulutus.
2. Valittu konteksti-ikkuna.
3. Pidätkö mallia muistissa myös pyyntöjen välissä.
4. Haluatko ajaa yhtä aikaa useampaa mallia tai rinnakkaisia pyyntöjä.

Ollaman FAQ tekee tästä käytännöllisen muistutuksen. Jos järjestelmässä on tarpeeksi vapaata muistia, Ollama voi pitää useita malleja ladattuna yhtä aikaa ja sallia samalle mallille rinnakkaista pyyntöjen käsittelyä. Jos muistia ei ole tarpeeksi, uudet pyynnöt menevät jonoon ja vanhoja malleja puretaan pois tieltä. GPU-ajossa uusi malli pitää lisäksi mahtua kokonaan VRAMiin, jotta rinnakkainen mallilataus onnistuu.

Tämä tarkoittaa harrastajalle jotain hyvin konkreettista: jos rakennat koneen niin tiukalle, että yksi malli juuri ja juuri mahtuu sisään, olet samalla rakentanut koneen, jossa kaikki lisämukavuus kuluttaa heti viimeiset marginaalit. Toinen lämmin malli, pidempi konteksti tai yksi huonommin ajoitettu rinnakkainen pyyntö voi riittää muuttamaan kokemuksen.

## Oma käytännön sääntöni VRAM-varalle

Minä en käyttäisi koko VRAMia suunnittelulaskennassa koskaan. Käyttäisin tätä karkeaa päätöspolkua:

1. Jos ajat yhtä mallia, maltillisella kontekstilla ja yksi käyttäjä kerrallaan, jätä vähintään noin 10-15 % VRAM-varaa.
2. Jos käytät pitkää kontekstia, agenttimaisia työkaluja tai haluat välttää herkästi CPU-offloadin, tähtää mieluummin noin 15-25 % käyttövaraan.
3. Jos haluat pitää useita malleja lämpimänä tai sallia enemmän rinnakkaisuutta, ajattele kapasiteettia mieluummin mallien summana plus erillinen turvamarginaali, ei yhtenä tarkkana rajana.

Tämä ei ole valmistajan virallinen taulukko vaan käytännön synteesi siitä, mitä Ollaman dokumentaatio kertoo muistista, kontekstista ja rinnakkaisuudesta. Ajatus ei ole löytää täydellistä prosenttia vaan välttää väärä optimointi: **viimeisten satojen megojen käyttäminen paperilla hyvältä näyttävään mahtuvuuteen maksaa usein enemmän vakaudessa kuin tuo hyötyä kapasiteetissa.**

## Miten tarkistat tilanteen oikeasti

Paras tapa lopettaa arvailu on katsoa mitä järjestelmä tekee oikeasti. Ollaman `ps`-rajapinta ja `ollama ps` näyttävät sekä `size_vram`-arvon että käytössä olevan kontekstin. `Context length` -sivu neuvoo myös katsomaan `PROCESSOR`-saraketta, jotta näet pysyykö ajo kokonaan GPU:lla vai valuuko se osittain CPU:lle.

Tämä on minusta tärkein käytännön mittari koko aiheessa:

- jos `PROCESSOR` pysyy `100% GPU`:ssa, olet yleensä turvallisemmalla puolella
- jos sama malli siirtyy osittaiseksi CPU/GPU-ajoksi heti kun konteksti kasvaa, VRAM-headroom loppui käytännössä jo
- jos toinen malli pakottaa ensimmäisen ulos muistista koko ajan, et suunnitellut kapasiteettia käyttöä vaan yksittäistä demoa varten

Eli älä kysy vain "mahtuuko tämä malli". Kysy mieluummin:

1. mahtuuko se edelleen, kun oikea konteksti on päällä
2. mahtuuko se edelleen, kun malli pidetään lämpimänä
3. mahtuuko se edelleen, jos koneelle tulee toinen pyyntö tai toinen malli

Jos vastaus muuttuu nopeasti ei:ksi, ostos tehtiin liian tiukalle.

## Milloin pieni headroom riittää

Pieni käyttövara voi riittää, jos koko käyttö on hyvin ennustettavaa:

- yksi malli
- lyhyt tai kohtalainen konteksti
- yksi käyttäjä
- ei tarvetta pitää useita malleja yhtä aikaa muistissa

Tässä maailmassa on ihan mahdollista elää lähempänä kapasiteetin rajaa, koska kuorma ei heilu paljon. Esimerkiksi yksittäinen paikallinen chat-käyttö tai kevyt apu koodiin voi toimia aivan hyvin ilman suurta marginaalia, jos tiedät tarkalleen mitä ajat.

## Milloin jättäisin varaa selvästi enemmän

Jättäisin VRAMia reilummin vapaaksi lähes aina, jos jokin näistä osuu:

- käytät 64k+ kontekstia tai muuten pitkiä syötteitä
- ajat OpenClawin, agenttien tai työkalukäytön kaltaista kuormaa
- haluat pitää useita malleja valmiina
- koneella tehdään muutakin kuin yhden mallin yhtäaikaista generointia
- testaat eri kvantisointeja tai vaihtelet malleja päivän aikana

Silloin liian tiukka VRAM-suunnittelu näkyy yleensä ensin epämääräisenä tahmeutena, jonoutumisena tai jatkuvana mallien purkamisena ja lataamisena, ei välttämättä nätisti yhtenä virheilmoituksena.

## Käytännön ostopäätös: älä osta korttia vain yhdelle numerolle

Jos vertailisin kahta GPU:ta paikalliseen LLM-käyttöön, en vertaisi vain sitä mahtuuko tavoitemalli toiseen juuri ja juuri ja toiseen selvästi. Vertaisin ennemmin tätä:

1. jääkö pienemmän kortin jälkeen mitään käyttövaraa oikealle kontekstille
2. pysyykö ajo kokonaan GPU:lla myös arjen kuormassa
3. voinko pitää mallin lämpimänä ilman että muu käyttö kärsii

Jos vastaus on "ei juuri", suurempi VRAM-kortti ei osta vain isompaa mallia vaan myös rauhallisempaa käyttöä. Tässä mielessä 24 Gt VRAM ei ole vain kapasiteettiluku. Se on usein headroom-luku.

## Tiivis johtopäätös

**Paikalliselle LLM:lle ei kannata jättää VRAMia vapaaksi siksi, että prosentti näyttää nätimmältä, vaan siksi että todellinen käyttö ei ole sama asia kuin mallitiedoston koko.** Konteksti, lämpimänä pidetyt mallit ja rinnakkaisuus syövät kaikki samaa muistibudjettia.

Jos haluat turvallisen nyrkkisäännön, tähtäisin itse vähintään noin 10-15 prosentin käyttövaraan yksinkertaisessa käytössä ja mieluummin 15-25 prosenttiin heti kun konteksti, työkalut tai rinnakkaisuus kasvavat. Kun mittaat tilanteen `ollama ps`:llä ja katsot pysyykö malli oikeasti 100 % GPU:ssa, pääset paljon lähemmäs totuutta kuin yhdelläkään "malli on tämän kokoinen levyllä" -oletuksella.

## Lähteet

- https://docs.ollama.com/context-length
- https://docs.ollama.com/faq
- https://docs.ollama.com/api/ps
