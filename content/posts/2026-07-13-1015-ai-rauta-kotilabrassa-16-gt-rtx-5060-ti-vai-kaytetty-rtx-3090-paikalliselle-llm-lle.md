---
title: "AI-rauta kotilabrassa: 16 Gt RTX 5060 Ti vai käytetty RTX 3090 paikalliselle LLM:lle?"
date: "2026-07-13T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Paikalliset LLM:t"
  - "GPU"
  - "NVIDIA"
  - "RTX 5060 Ti"
  - "RTX 3090"
---
Jos paikallista LLM-konetta rakentava harrastaja katsoo NVIDIA-puolta vuonna 2026, vastaan tulee nopeasti kaksi hyvin erilaista mutta aidosti kiinnostavaa vaihtoehtoa: **uudempi 16 Gt RTX 5060 Ti** ja **käytetty 24 Gt RTX 3090**. Oma lyhyt vastaukseni on tämä: **jos tärkeintä on hiljainen, viileä ja helppo yhden GPU:n arkikone 7B-14B-luokan malleille, 16 Gt RTX 5060 Ti on usein järkevämpi. Jos taas tiedät jo valmiiksi tarvitsevasi 24 Gt muistiluokan liikkumavaraa, RTX 3090 on edelleen käytännössä eri luokan kortti.**

Tämä ei ole vain vanha vastaan uusi -vertailu. NVIDIAn omien speksien mukaan RTX 5060 Ti tuo 16 Gt GDDR7-muistia ja 180 W kokonaiskorttitehon, kun taas RTX 3090 tarjoaa 24 Gt GDDR6X-muistia, 384-bittisen muistiväylän ja 350 W grafiikkakortin tehon. Jo tästä näkee, että kortit ratkaisevat eri ongelmia. Toinen yrittää olla järkevä ja kevyt arjen AI-kortti. Toinen yrittää edelleen ostaa sinulle lisää muistipäätä hinnalla, jonka maksat sähkönkulutuksessa, lämmössä ja usein myös fyysisessä koossa.

## Missä RTX 5060 Ti 16 Gt näyttää hyvältä

RTX 5060 Ti:n vahvuus ei ole vain se, että se on uudempi. Sen vahvuus on yhdistelmä:

- 16 Gt VRAMia
- selvästi alempi 180 W tehonkulutusluokka
- Blackwell-sukupolven CUDA-tuki
- suora tuki Ollaman nykyisessä NVIDIA-listassa

Ollaman laitetukisivu listaa RTX 5060 Ti:n GeForce RTX 50xx -sarjan tuettuihin kortteihin, ja dokumentaatio vaatii käytännössä vain riittävän uuden NVIDIA-ajurin. Tämä on hyvä uutinen harrastajalle, joka ei halua rakentaa jokaista päivitystä puhtaasti epävirallisten ohjeiden varaan.

Käytännössä 16 Gt RTX 5060 Ti on minusta kiinnostava juuri näissä tilanteissa:

1. ajat pääosin 7B-14B-luokan kvantisoituja malleja
2. haluat yhden koneen, joka voi olla päällä pitkään ilman että huone lämpenee turhaan
3. kotelossa, virtalähteessä tai melubudjetissa ei ole paljon ylimääräistä varaa
4. haluat mieluummin modernin ja siistin peruskoneen kuin vanhan lippulaivan luonteenpiirteet

Tässä kohtaa teen tietoisen tulkinnan lähteistä: 16 Gt ei ole rajaton määrä muistia, mutta se on jo riittävän terve taso siihen, että moni paikallinen assistentti, koodiapu ja dokumenttien kysely toimii ilman jatkuvaa 8 Gt -luokan säätöä. Samalla 180 W tehonkulutusluokka on iso käytännön etu, jos kone toimii työpöydällä tai 24/7-taustapalvelimena.

## Missä RTX 3090 on edelleen vaikea sivuuttaa

RTX 3090:n koko tarina tiivistyy edelleen yhteen numeroon: **24 Gt**. Se ei ole uusi havainto, mutta se on yhä tärkeä. NVIDIAn virallisissa spekseissä RTX 3090:llä on 24 Gt GDDR6X-muistia, 384-bittinen muistiväylä ja 350 W grafiikkateho. Tämä kertoo heti, että kyse ei ole pienestä 16 Gt luokan kortista, joka yrittää pärjätä nätisti, vaan kortista, joka on rakennettu aivan eri kapasiteettitasolle.

Paikallisessa LLM-ajossa tämä näkyy käytännössä näin:

- suurempi malli mahtuu todennäköisemmin kokonaan tai pidemmälle GPU:lle
- pidempi konteksti kiristää muistia myöhemmin
- useampi rinnakkainen pyyntö tuntuu vähemmän nopeasti ahtaalta
- mallivalinnat eivät kaadu yhtä helposti siihen, että VRAM loppuu aivan juuri ennen maalia

Jos oma käyttösi on jo valmiiksi siinä luokassa, jossa 16 Gt tuntuu paperilla "ehkä riittävältä", 24 Gt voi olla paljon helpompi arki. Tämä on erityisen totta silloin, jos ajat muutakin kuin yhtä pientä keskustelumallia: esimerkiksi suurempia koodimalleja, pidempää kontekstia tai useampaa erää samassa koneessa.

## Käytännön ero ei ole vain VRAMissa vaan koko koneessa

Tärkein virhe tässä vertailussa on katsoa vain muistia. Korttien mukana tulee aivan eri luokan konevaatimus.

RTX 5060 Ti:

- 180 W kokonaiskorttiteho
- 600 W suositeltu järjestelmäteho
- yksi 8-pin tai Gen 5 -virtakaapeli

RTX 3090:

- 350 W grafiikkateho
- 750 W suositeltu järjestelmäteho
- fyysisesti iso 3-slotin kortti Founders Edition -mitoissa

Tämä tarkoittaa, että 3090 ei ole vain "enemmän VRAMia". Se on myös:

- enemmän lämpöä poistettavaksi
- enemmän melua, jos jäähdytys tai kotelo ei ole kunnossa
- enemmän painetta virtalähteelle
- suurempi riski siihen, että käytetty kortti on elänyt raskasta elämää

Siksi 3090 on parhaimmillaan silloin, kun ostat tietoisesti kapasiteettia etkä vain "hyvän diilin". Jos koko muu kone on kevyt, hiljainen tai kompakti, 3090 voi helposti muuttaa tasapainoisen rakennelman kuumaksi kompromissiksi.

## Milloin ottaisin 16 Gt RTX 5060 Ti:n

Ottaisin 16 Gt RTX 5060 Ti:n paikalliseen LLM-koneeseen mieluummin kuin käytetyn 3090:n, jos nämä pitävät enimmäkseen paikkansa:

- käyttö on pääosin yhden käyttäjän paikallista avustajaa, koodiapua tai kevyttä RAGia
- tavoite on hyvä arkinen käyttökokemus, ei maksimaalinen mallikoko yhdellä GPU:lla
- arvostat matalampaa virrankulutusta enemmän kuin viimeisiä lisägigatavuja VRAMia
- haluat rakentaa koneen, joka mahtuu tavalliseen koteloon ilman erikoisjärjestelyä

Toisin sanoen 5060 Ti on järkevä valinta silloin, kun haluat paikallisen AI-koneen tuntuvan enemmän hyvältä työkalulta kuin projektilta.

## Milloin ottaisin käytetyn RTX 3090:n

Ottaisin käytetyn RTX 3090:n edelleen vakavaan harkintaan, jos jokin näistä on totta:

1. tiedät jo nyt, että 16 Gt tulee vastaan liian nopeasti
2. haluat minimoida CPU-offloadin ja hybridiajon määrää
3. ajat pidempiä konteksteja tai isompia kvantisointeja säännöllisesti
4. koneen sähkönkulutus, melu ja koko eivät ole tärkein rajoite

Tässä tapauksessa 3090:n 24 Gt ei ole vain mukava lisä. Se on syy, miksi kortti yhä elää paikallisten LLM-koneiden keskusteluissa. Vaikka arkkitehtuuri on vanhempi, muistiluokka on edelleen se kohta, joka ratkaisee paljon enemmän kuin moni haluaisi myöntää.

## Oma käytännön sääntöni

Jos joutuisin antamaan tästä yhden yksinkertaisen ostosäännön, se olisi tämä:

**osta 16 Gt RTX 5060 Ti, jos haluat tehokkaan mutta järkevän yhden käyttäjän paikallisen LLM-koneen; osta käytetty RTX 3090 vain silloin, kun tiedät tarvitsevasi nimenomaan 24 Gt VRAMin tuomaa liikkumavaraa enemmän kuin matalampaa virrankulutusta ja helpompaa kotelointia.**

Tämä on tarkoituksella epähypeinen suositus. 5060 Ti ei ole maaginen AI-kortti vain siksi, että se on uudempi. 3090 ei taas ole automaattisesti paras vain siksi, että sillä on 24 Gt muistia. Oikea valinta riippuu siitä, rakennatko **mukavaa päivittäistä työkonetta** vai **mahdollisimman paljon muistipäätä yhdelle GPU:lle**.

Jos oma käyttösi on vielä epäselvä, valitsisin useimmiten 16 Gt RTX 5060 Ti:n kaltaisen siistimmän peruskoneen. Jos taas tiedät jo etukäteen, että sinua alkaa nopeasti ärsyttää jokainen VRAM-kompromissi, silloin käytetty 3090 on edelleen niitä harvoja vanhoja kortteja, joille löytyy oikea, konkreettinen peruste.

## Lähteet

- https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5060-family/
- https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3090-3090ti/
- https://docs.ollama.com/gpu
