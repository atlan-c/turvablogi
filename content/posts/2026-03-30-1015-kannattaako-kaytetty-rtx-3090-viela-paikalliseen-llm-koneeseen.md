---
title: "Kannattaako käytetty RTX 3090 vielä paikalliseen LLM-koneeseen?"
date: "2026-03-30T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "GPU"
  - "Hardware"
  - "Troubleshooting"
  - "Homelab"
---
Paikallista LLM-konetta rakentaessa yksi houkuttelevimmista oikopoluista on edelleen käytetty **RTX 3090**. Syy on helppo ymmärtää: kortissa on 24 Gt VRAMia, CUDA-tuki on kypsä ja käytettyjen markkinassa hinta on usein paljon alempi kuin uudemmissa 24–32 Gt korteissa. Mutta kannattaako se oikeasti vielä vuonna 2026, vai onko kyse vain vanhan suosikin nostalgiasta?

Lyhyt vastaus on tämä: **kyllä, käytetty RTX 3090 on yhä erittäin järkevä ostos paikalliseen LLM-ajoon, jos tärkein tavoitteesi on saada paljon VRAMia kohtuullisella hinnalla.** Se ei kuitenkaan ole paras valinta, jos arvostat ennen kaikkea energiatehokkuutta, hiljaisuutta tai huoletonta takuuta.

## Miksi 3090 on edelleen kiinnostava juuri LLM-käytössä?

NVIDIAn omien speksien mukaan RTX 3090 tarjoaa **24 Gt GDDR6X-muistia** ja **384-bittisen muistiväylän**. Juuri nämä kaksi kohtaa tekevät siitä paikallisessa LLM-ajossa kiinnostavan vieläkin: kapasiteetti on monelle harrastajalle tärkeämpi kuin absoluuttinen huippunopeus.

Käytännössä 24 Gt VRAM tarkoittaa sitä, että paljon useampi malli mahtuu kokonaan GPU:lle kuin 12–16 Gt korteilla. Tämä näkyy arjessa kolmella tavalla:

- vähemmän tarvetta CPU-offloadille
- vähemmän säätöä kvantisoinnin ja konteksti-ikkunan kanssa
- tasaisempi käyttökokemus, kun malli ei elä aivan muistin rajalla

Juuri tämä on 3090:n ydinetu. Uudempi 16 Gt kortti voi olla monessa asiassa modernimpi, mutta jos tavoite on ajaa paikallisesti hieman isompia malleja ilman jatkuvaa kompromissijumppaa, 24 Gt on edelleen eri luokan mukavuusraja.

## Mitä 24 Gt oikeasti ostaa harrastajalle?

Aloittelija tekee tässä usein yhden virheen: katsotaan vain raakaa suorituskykyä ja unohdetaan muistibudjetti. Paikallisessa inferenssissä juuri VRAM loppuu usein ensin.

Jos käytössä on llama.cpp:n CUDA-backend tai vastaava GPU-kiihdytys, hyvä lopputulos tulee yleensä siitä, että saat mallin mahdollisimman pitkälle GPU:n omaan muistiin. llama.cpp:n dokumentaatio muistuttaa suoraan, että projekti tukee useita GPU-kiihdytettyjä backendeja ja CUDA-rakennusta nimenomaan tähän käyttöön. Käytännössä tämä tarkoittaa, että 24 Gt kortti antaa enemmän liikkumavaraa mallin koolle, kvantisoinnille ja kontekstille kuin 12 Gt tai 16 Gt luokka.

Arjen kielelle käännettynä 24 Gt auttaa erityisesti silloin, kun:

- ajat 7B–14B malleja mukavuusmarginaalilla etkä aivan veitsenterällä
- haluat kokeilla myös suurempia kvantisoituja malleja ilman jatkuvaa hybridiajoa
- pidät useamman tuhannen tokenin kontekstia realistisena oletuksena
- et halua käyttää jokaista iltaa siihen, että etsit juuri yhtä pykälää pienemmän kvantisoinnin

Toisin sanoen 3090 ei ole vain "vanha nopea kortti", vaan edelleen yksi halvimmista tavoista ostaa **aidosti käyttökelpoista VRAM-kapasiteettia**.

## Missä käytetty RTX 3090 voittaa uudemmat kuluttajakortit?

XDA:n kevään 2026 käytännön artikkeli tiivistää hyvin sen, miksi 3090 on pysynyt suosikkina paikallisessa AI-käytössä: **VRAM per euro** on edelleen poikkeuksellisen hyvä. Artikkelissa kortin käytetty hintahaarukka arvioitiin noin 600–800 dollariin, mikä on tärkeä muistutus siitä, että harrastajalle suurin arvo ei aina tule uusimmasta arkkitehtuurista vaan siitä, paljonko muistia saa samalla budjetilla.

Tässä kohtaa 3090 voittaa usein seuraavilla tavoilla:

- 24 Gt VRAM on edelleen harvinainen kuluttajaluokassa
- CUDA-ekosysteemi toimii paikallisten LLM-työkalujen kanssa yleensä kitkattomasti
- käytettyjen markkina on laaja, joten kortteja löytyy enemmän kuin niche-työasemamalleja

Jos vertailet käytettyä 3090:tä ja uutta 12–16 Gt pelikorttia, kysymys ei ole yleensä siitä kumpi on "uudempi", vaan siitä kumpi osuu paremmin paikallisen AI:n todelliseen pullonkaulaan.

## Missä kohtaa 3090 ei ole enää automaattinen suositus?

Tämä on tärkeä vastapaino. RTX 3090:ssä on myös selviä haittoja, eikä niitä kannata romantisoida.

Ensimmäinen on **virrankulutus ja lämpö**. TechPowerUpin tietokannan mukaan RTX 3090:n nimellinen maksimiteho on noin **350 W**, mikä on paljon kotilabran jatkuvassa ajossa. Jos kone on päällä pitkiä aikoja, sähkölasku, melu ja jäähdytyksen laatu alkavat oikeasti merkitä.

Toinen on **käytetyn kortin riski**. 3090 on ollut suosittu sekä pelaajilla että raskaassa työkuormassa, ja osa korteista on voinut elää kuuman tai pölyisen elämän. Käytetty ostos voi olla erinomainen löytö, mutta se voi olla myös kortti, jonka tuulettimet, lämpötyynyt tai yleinen kunto eivät enää vastaa sitä mitä paikallinen inferenssi päivästä toiseen vaatii.

Kolmas on **kokonaiskoneen vaatimus**. 350 W luokan GPU ei ole irrallinen komponentti, vaan se tarvitsee ympärilleen kunnollisen virtalähteen, hyvän ilmanvaihdon ja fyysisesti sopivan kotelon. Jos yrität tehdä hiljaista tai pientä AI-työasemaa, 3090 voi olla väärä suunta vaikka VRAM houkuttelisi.

## Kenelle käytetty 3090 on edelleen hyvä ostos?

Minusta 3090 on edelleen hyvä hankinta erityisesti tällaiselle käyttäjälle:

- haluat paikalliseen LLM-ajoon mahdollisimman paljon VRAMia rajallisella budjetilla
- hyväksyt käytetyn raudan kompromissit
- sinulla on jo tai olet valmis hankkimaan riittävän virtalähteen ja jäähdytyksen
- tärkein mittarisi on "mitä malleja saan järkevästi ajettua paikallisesti" eikä "mikä kortti on uusin"

Tällaisessa käytössä 3090 osuu edelleen todella hyvin maaliin. Se ei ehkä ole elegantti, mutta se on käytännöllinen.

## Kenelle suosittelisin jotain muuta?

Suosittelisin katsomaan muuta vaihtoehtoa, jos jokin näistä on sinulle tärkeämpi kuin VRAM per euro:

- haluat mahdollisimman energiatehokkaan koneen
- arvostat uuden kortin takuuta enemmän kuin käytetyn markkinan säästöä
- aiot käyttää konetta paljon myös hiljaisena työpöytäkoneena samassa huoneessa
- et halua säätää mahdollisten lämpö- tai huoltoasioiden kanssa

Silloin uudempi kortti pienemmällä VRAMilla voi olla kokonaisuutena miellyttävämpi, vaikka se olisi paikallisen LLM:n näkökulmasta paperilla rajoittuneempi.

## Oma käytännön johtopäätökseni

Jos tavoitteena on rakentaa **mahdollisimman järkevä paikallinen LLM-kone harrastajabudjetilla**, käytetty RTX 3090 on edelleen yksi vahvimmista vaihtoehdoista juuri siksi, että 24 Gt VRAM ratkaisee enemmän kuin moni ensin ymmärtää. Se ei ole uusin, viilein eikä hiljaisin kortti. Mutta se on edelleen yksi halvimmista tavoista päästä pois 12–16 Gt luokan jatkuvista muistirajoista.

Sanoisin asian näin: **3090 kannattaa edelleen, jos ostat ennen kaikkea muistia etkä statusta.** Jos taas ostat mielenrauhaa, energiatehokkuutta ja takuuta, uudempi vaihtoehto voi olla parempi vaikka LLM-käytön kapasiteetti jäisi pienemmäksi.

Paikallisen AI-raudan kohdalla oikea kysymys ei siis ole "onko 3090 vanha", vaan **onko 24 Gt VRAM sinulle juuri nyt arvokkaampi kuin uuden sukupolven mukavuudet**. Monelle harrastajalle vastaus on edelleen kyllä.

## Lähteet

- NVIDIA GeForce RTX 3090 / 3090 Ti specifications: https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3090-3090ti/
- ggml-org/llama.cpp build documentation (CUDA and GPU backends): https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md
- XDA: A used RTX 3090 is still the best GPU for local AI in 2026, and it's not even close on value: https://www.xda-developers.com/used-rtx-3090-still-best-for-local-ai-in-value/
- TechPowerUp GPU Database, NVIDIA GeForce RTX 3090 specs: https://www.techpowerup.com/gpu-specs/geforce-rtx-3090.c3622
