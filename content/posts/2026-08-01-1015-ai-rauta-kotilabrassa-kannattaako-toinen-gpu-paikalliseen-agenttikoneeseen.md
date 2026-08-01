---
title: "AI-rauta kotilabrassa: kannattaako toinen GPU paikalliseen agenttikoneeseen?"
date: "2026-08-01T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "gpu"
  - "llama-cpp"
  - "agent"
  - "vram"
---
## Tiivistelmä
Jos paikallinen agentti ei enää mahdu yhdelle GPU:lle, toinen näytönohjain voi olla järkevä päivitys. Mutta käytännön sääntöni on tämä: **osta toinen GPU ensisijaisesti kapasiteetin takia, älä siksi että odotat automaattista nopeusihmettä**. Paikallisessa agenttikäytössä lisä-GPU auttaa ennen kaikkea pitämään mallin ja kontekstin kiihdytettynä, mutta nopeushyöty riippuu paljon siitä, miten kuorma jaetaan ja millainen yhteys korttien välillä on.

Tämä on tärkeä ero, koska moni harrastaja katsoo vain toisen kortin VRAM-määrää. Se on kyllä oikea ensimmäinen tarkistus, mutta ei ainoa. Kun agentti käyttää pitkiä ohjeita, työkaluja ja web-hakua, pullonkaula ei ole aina sama kuin kuvageneroinnissa tai pelikäytössä.

## Milloin toisesta GPU:sta on eniten hyötyä

llama.cpp:n oma multi-GPU-ohje sanoo asian suoraan: useampaa GPU:ta kannattaa käyttää etenkin silloin, kun malli ei mahdu yhden kortin VRAMiin tai kun halutaan lisää throughputia. Käytännössä ensimmäinen syy on kotilabrassa paljon tärkeämpi kuin toinen.

Jos yksi GPU ei riitä, osa mallista tai muistista valuu helposti järjestelmämuistiin. Ollaman context length -dokumentaatio muistuttaa samalla, että agentit, web-haku ja koodityökalut hyötyvät vähintään noin 64k kontekstista ja että suurempi konteksti kasvattaa muistitarvetta. Siksi toinen GPU voi olla hyvä ostos juuri silloin, kun tavoite ei ole "enemmän FPS:ää", vaan se että:

- koko malli pysyy kiihdytettynä
- pidempi konteksti mahtuu mukaan ilman aggressiivista kompromissia
- CPU-offloadia tarvitsee käyttää vähemmän

Toisin sanottuna lisäkortti ostaa sinulle ennen kaikkea työrauhaa muistibudjettiin.

## Miksi lisäkortti ei aina tunnu nopealta

Tässä moni pettyy. llama.cpp:n dokumentaatio kertoo, että multi-GPU voi parantaa prefilliä ja tokenointinopeutta, mutta tulos riippuu split-modesta sekä korttien välisen yhteyden nopeudesta. Se on varoitus siitä, ettei "kaksi GPU:ta" yksin vielä kerro suorituskyvystä tarpeeksi.

NVIDIAn CUDA-dokumentaatio kuvaa saman ilmiön alemmalla tasolla: jos GPU joutuu käsittelemään dataa järjestelmämuistin kautta PCIe-yhteydellä, viive on suurempi ja kaista pienempi kuin GPU:n omassa muistissa. Käytännön tulkintani tästä on yksinkertainen: jos kahden kortin yhteistyö nojaa huonosti optimoituun siirtelyyn tai fallbackiin järjestelmämuistiin, lisä-GPU voi ratkaista mahtumisongelman mutta jättää nopeushyödyn yllättävän vaatimattomaksi.

Siksi halpa toinen kortti ei ole automaattisesti huono idea, mutta sille pitää antaa oikea rooli. Se on usein kapasiteettipäivitys ensin ja nopeuspäivitys vasta mahdollisesti sen jälkeen.

## Mitä tarkistaisin ennen ostoa

Jos harkitsisin tänään toista GPU:ta paikalliseen agenttikoneeseen, kävisin läpi nämä kysymykset:

### 1. Ratkaisetko mahtumisen vai haetko puhdasta nopeutta?

Jos malli ei mahdu yhdelle kortille, toinen GPU voi olla juuri oikea liike. Jos taas malli mahtuu jo hyvin ja haluat vain selvästi nopeammat vastaukset, lopputulos on epävarmempi.

### 2. Onko korteilla järkevä työnjako?

llama.cpp tukee useita split-tapoja, ja oletus on kerrospohjainen jako. Se on hyvä yleisvalinta, mutta ei poista sitä tosiasiaa, että hitaampi kortti voi myös hidastaa kokonaisuutta. Epäsymmetrinen yhdistelmä voi silti olla täysin järkevä, jos tavoite on saada suuri malli kokonaan pois CPU:lta.

### 3. Onko peer-to-peer oikeasti käytettävissä?

llama.cpp:n build-ohjeissa `GGML_CUDA_P2P` mahdollistaa suoran GPU:iden välisen siirron, mutta sama ohje varoittaa että tuki riippuu ajureista ja on usein käytännössä workstation- tai datacenter-puolen etu. Harrastajalle tämä tarkoittaa, ettei kahden kuluttajakortin yhdistelmän varaan kannata laskea liikaa "suoraa väylätaikaa" ennen kuin testaat asian omassa koneessa.

### 4. Riittäisikö yksi isompi GPU sittenkin paremmin?

Jos budjetti sallii, yksi riittävän iso GPU on yleensä yksinkertaisin ratkaisu. Kaksi korttia voittaa sen, kun:

- sinulla on jo yksi sopiva kortti valmiina
- käytetty lisäkortti on selvästi halvempi kuin koko alustan uusiminen
- päätavoite on saada suurempi malli tai pidempi konteksti käyttöön nyt

## Milloin ostaisin toisen GPU:n hyvillä mielin

Ostaisin toisen GPU:n ilman suurempaa draamaa, jos tilanne olisi tämä:

- nykyinen agenttikäyttö kaatuu VRAM-rajaan eikä niinkään raakanopeuteen
- haluan pitää pidemmän kontekstin käytössä paikallisesti
- hyväksyn, että hyöty näkyy ensin mahtumisessa ja vakaudessa
- voin käyttää olemassa olevaa konetta ilman koko alustan uusimista

Tällöin toinen GPU on käytännöllinen tapa pidentää nykyisen koneen elinkaarta.

## Milloin en ostaisi

Jättäisin ostamatta, jos odotus on että kaksi satunnaista korttia muuttaa paikallisen agentin suorituskyvyn lineaarisesti kaksinkertaiseksi. En myöskään ostaisi toista korttia ensimmäisenä liikkeenä, jos ongelma johtuu oikeasti liian pitkästä kontekstista, turhasta CPU-offloadista tai huonosti valitusta mallikoosta. Ne kannattaa korjata ennen rautakauppaa.

## Johtopäätös

Toinen GPU kannattaa paikalliseen agenttikoneeseen ennen kaikkea silloin, kun tarvitset lisää käyttökelpoista VRAM-tilaa mallille ja kontekstille. Se voi parantaa myös nopeutta, mutta sitä ei pidä olettaa automaattisesti. Harrastajalle tärkein kysymys ei ole "montako GPU:ta saan koneeseen", vaan "saanko mallin pysymään kiihdytettynä ilman että agentin konteksti romahtaa". Jos vastaus vaatii toisen kortin, päivitys voi olla hyvin perusteltu.

## Lähteet

- https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md
- https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md
- https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html
- https://docs.ollama.com/context-length
