---
title: "AI-rauta kotilabrassa: pitääkö paikallisen LLM-koneen SSD-levyn olla nopea NVMe vai riittääkö SATA?"
date: "2026-05-20T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "GPU"
  - "Hardware"
  - "Homelab"
  - "Troubleshooting"
---
Paikallista LLM-konetta rakentaessa rahaa palaa helposti väärään paikkaan. Yksi yleinen kysymys on, pitääkö mallikoneeseen ostaa mahdollisimman nopea NVMe-levy, vai riittääkö tavallinen SATA-SSD. Käytännön vastaus on yllättävän rauhallinen: **SATA-SSD riittää monelle aivan hyvin, jos ajat yhtä tai muutamaa mallia ilman jatkuvaa kylmäkäynnistystä. Nopea NVMe tuntuu eniten silloin, kun lataat isoja malleja usein uudelleen, vaihdat niitä paljon tai elät muuten levyn ja RAMin välisen liikenteen varassa.**

Toisin sanoen levy vaikuttaa ennen kaikkea siihen, kuinka nopeasti pääset "malli levyltä käyttöön" -vaiheen läpi. Se ei yleensä ole ensimmäinen asia, joka määrää varsinaisen tokennopeuden.

## Missä SSD oikeasti näkyy paikallisessa LLM-ajossa

On hyödyllistä erottaa toisistaan kolme eri hetkeä:

- **mallin lataus** levyltä käyttöön
- **ensimmäiseen tokeniin kuluva aika**
- **varsinainen generointinopeus** eli tokenit sekunnissa

Nämä menevät helposti puheessa sekaisin, vaikka ne eivät ole sama ongelma. `llama.cpp`:n dokumentaatiossa on tästä hyvä vihje kahdesta suunnasta. Ensinnäkin työkalun argumenteissa todetaan suoraan, että jos memory mapping eli `mmap` otetaan pois käytöstä, mallin lataus hidastuu. Toiseksi tokennopeuden vianetsintäohjeet korostavat GPU-offloadia ja CPU-säikeiden määrää, eivät levyn nopeutta. Käytännön tulkinta on selvä: **levy vaikuttaa eniten lataukseen, mutta jatkuvan generoinnin aikana pullonkaulat ovat tavallisesti muualla.**

Tämä sopii hyvin myös yleiseen paikallisen inference-putken malliin: tiedosto luetaan levyltä, käyttöjärjestelmä mapittaa sivuja muistiin, osa painoista siirtyy RAMiin ja osa mahdollisesti VRAMiin, ja vasta sen jälkeen varsinainen ajo alkaa.

## Miksi NVMe silti voi tuntua paljon nopeammalta

Vaikka levy ei yleensä ratkaise tokennopeutta, nopea NVMe voi silti tehdä koneesta selvästi mukavamman käyttää. Syy on yksinkertainen: iso GGUF tai muu mallitiedosto on oikeasti iso. Kun niitä ladataan usein, kylmäkäynnistyksen kitka alkaa näkyä arjessa.

Jos käytät yhtä vakiomallia ja pidät sen prosessin lämpimänä pitkään, lataus maksetaan ehkä vain kerran. Silloin SATA-SSD:n hitaampi luku ei välttämättä haittaa juuri lainkaan. Mutta jos teet tällaista:

- vaihdat mallia monta kertaa päivässä
- testaat eri kvantisointeja rinnakkain
- käynnistelet palvelua uudelleen usein
- ajat useita eri agentteja tai prosesseja, jotka avaavat malleja erikseen
- käytät niin isoja malleja, että käyttöjärjestelmä joutuu tekemään enemmän sivutusta

... silloin nopeampi NVMe alkaa näkyä suoraan hermoissa säästyvänä aikana.

Minun mielestäni tässä kohtaa moni tekee pienen mutta tärkeän ajatusvirheen: ostetaan nopein mahdollinen levy siksi, että "AI tarvitsee nopeutta", vaikka todellinen ongelma voi olla se, että mallia ladataan huonon workflow'n takia jatkuvasti uudelleen. Jos malli pysyy muistissa ja käyttö on vakaata, levy ei ehdi enää näytellä pääroolia.

## `mmap` muuttaa ostojärjestystä enemmän kuin moni huomaa

`llama.cpp`:n rajapinnassa ja argumenteissa näkyy suoraan, että moottori tukee `mmap`- ja `mlock`-käyttöä. Se on käytännössä tärkeää siksi, että mallia ei aina tarvitse lukea levystä "kaikki heti RAMiin" -mallilla. Käyttöjärjestelmä voi mapittaa tiedoston muistiavaruuteen ja ladata sivuja tarpeen mukaan.

Tästä seuraa harrastajalle kaksi käytännön johtopäätöstä:

- **Nopea levy parantaa erityisesti kylmiä avauksia ja page-in-tilanteita**
- **Riittävä RAM ja järkevä VRAM-offload vähentävät sitä, kuinka usein levyn nopeus ehtii sattua**

Jos koneessa on vähän RAMia, paljon rinnakkaista kuormaa tai liian iso malli, käyttöjärjestelmä voi joutua nojaamaan levyyn enemmän kuin olisi mukavaa. Silloin nopea NVMe ei ratkaise kaikkea, mutta se pehmentää huonoa tilannetta. Jos taas malli mahtuu järkevästi ja prosessi pysyy vakaana, SATA-SSD voi tuntua yllättävän riittävältä.

## Missä tilanteessa SATA-SSD on täysin järkevä valinta

Valitsisin hyvillä mielin SATA-SSD:n paikalliseen LLM-koneeseen, jos suurin osa näistä pitää paikkansa:

- ajat enimmäkseen yhtä tai kahta mallia
- palvelu pysyy päällä eikä mallia avata jatkuvasti uudelleen
- tavoite on edullinen harrastekone, ei jatkuva benchmarkkaus
- pullonkaula on selvästi VRAM, RAM tai CPU eikä mallin avaaminen levyltä
- käytössä on jo kunnollinen SSD eikä vaihtoehto ole mekaaninen levy

Tärkeä huomio: **SATA-SSD on eri asia kuin HDD**. Minusta juuri tässä menee paljon keskustelua pieleen. Tavallinen SSD on edelleen valtava hyppäys pyörivästä levystä, ja monelle kotikäyttäjälle juuri se on olennaisin raja. Jos vaihtoehto on vanha HDD, en miettisi pitkään: siirtyisin SSD:hen heti. Varsinainen SATA vs NVMe -harkinta tulee vasta sen jälkeen.

## Milloin maksaisin NVMe:stä mielelläni enemmän

Maksaisin nopeasta NVMe-levystä tavallista mieluummin, jos jokin näistä osuu omaan käyttöön:

- käsittelet 20–70+ gigatavun malleja usein
- vaihdat kvantisointien ja malliversioiden välillä päivittäin
- ajat lokaalisti useita eri palveluita tai kontteja samalla koneella
- käytät RAG-setupia, jossa mallien lisäksi myös vektoridata ja muut indeksit liikkuvat samalla levyllä
- koneessa on muutenkin jo riittävästi RAMia ja GPU:ta, eli levy on oikeasti seuraava havaittava kitkan lähde

Silloin NVMe ei ole enää turhaa "spec-sheet-kiiltoa", vaan osa käytännön responsiivisuutta.

## Mikä on huono ostovirhe tässä aiheessa

Huonoin yleinen ostovirhe ei minun mielestäni ole "ostin SATA-SSD:n NVMe:n sijaan". Huonompi virhe on yleensä jompikumpi näistä:

- ostetaan huippunopea NVMe, vaikka koneessa on edelleen liian vähän RAMia tai VRAMia
- kuvitellaan, että NVMe korjaa hitaan tokennopeuden, vaikka ongelma on CPU-säikeissä, offloadissa tai muistikaistassa

`llama.cpp`:n suorituskykyohje on tästä melko suora: generointinopeuteen vaikuttavat näkyvästi esimerkiksi GPU-offload ja se, ettei CPU:ta ylikuormiteta väärällä säiemäärällä. Levy ei ole listan kärjessä. Tämä on hyvä muistutus ostojärjestyksestä.

Jos siis budjetti on tiukka, etenisin yleensä näin:

1. varmista että käytössä on **mikä tahansa kunnollinen SSD**, ei HDD
2. korjaa ensin **RAM-, VRAM- ja offload-pullonkaulat**
3. osta nopea NVMe vasta sitten, kun oikea kipu on mallien lataus ja kylmäkäynnistys

## Käytännön nyrkkisääntö

Jos haluat lyhyen version, käyttäisin tätä:

- **HDD → ei hyvä paikalliselle LLM-koneelle**
- **SATA-SSD → täysin kelvollinen monelle harrastajalle**
- **NVMe → paras silloin, kun avaat isoja malleja usein tai haluat minimoida käynnistyskitkan**

Eli ei, paikallisen LLM-koneen ei tarvitse aina saada kaikkein nopeinta NVMe-levyä ollakseen hyvä. **Jos koneessa on jo SSD ja malli pysyy lämpimänä muistissa, hyöty seuraavasta eurosta tulee usein ennemmin RAMista, VRAMista tai paremmasta workflow'sta kuin vielä nopeammasta levystä.**

## Lähteet

- https://raw.githubusercontent.com/ggml-org/llama.cpp/master/common/arg.cpp
- https://raw.githubusercontent.com/ggml-org/llama.cpp/master/include/llama.h
- https://raw.githubusercontent.com/ggml-org/llama.cpp/refs/heads/master/docs/development/token_generation_performance_tips.md
- https://www.runyard.dev/blog/how-local-llm-inference-actually-works
