---
title: "Paikallinen LLM käytännössä: miksi 24 Gt VRAM on usein parempi ostos kuin nopeampi 16 Gt kortti?"
date: "2026-07-15T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "GPU"
  - "VRAM"
  - "Ollama"
---
Jos paikallista LLM-konetta rakentava harrastaja epäröi nopean 16 gigatavun kortin ja vähän vanhemman tai kalliimman 24 gigatavun kortin välillä, valitsisin useimmiten jälkimmäisen. **Syy ei ole se, että laskentateho lakkaisi merkitsemästä, vaan se, että paikallisissa malleissa muistikatto pysäyttää työn kokonaan paljon useammin kuin raakasuorituskyky.**

Käytännön nyrkkisääntöni on tämä: **kun käyttötapa sisältää pidempää kontekstia, agentteja, koodityökaluja tai 20B-luokan malleja, 24 Gt VRAM tuntuu hyvin nopeasti eri luokalta kuin 16 Gt.** Vasta sen jälkeen kannattaa murehtia, onko toinen kortti hieman nopeampi paperilla.

## Miksi juuri VRAM ratkaisee ensin

Paikallisessa LLM-ajossa näytönohjaimen muisti ei kulu vain itse mallin painoihin. Sitä syövät myös konteksti, K/V-välimuisti, mahdollinen rinnakkaisuus ja osa runtimejen omista varauksista. Siksi monessa kotilabrassa ongelma ei ole "malli on hidas", vaan "malli ei mahdu sillä asetuksella jolla sitä oikeasti haluaisin käyttää".

Ollaman dokumentaatio tekee tästä yllättävän konkreettista. Sen oletuskäyttäytyminen vaihtuu VRAM-määrän mukaan näin:

- alle 24 GiB VRAMia: oletuksena 4k konteksti
- 24-48 GiB VRAMia: oletuksena 32k konteksti
- 48 GiB tai enemmän: oletuksena 256k konteksti

Pelkkä tuo kynnys kertoo paljon. 16 Gt kortti on usein hyvä "ajan mallia paikallisesti" -kortti, mutta 24 Gt alkaa olla "ajan mallia oikeilla työkaluilla ja pidemmällä muistilla" -kortti.

## 24 Gt ei ole vain enemmän muistia, vaan eri käyttöluokka

Moni katsoo näytönohjainta edelleen pelikäytön logiikalla: enemmän kaistaa, enemmän ytimiä, enemmän kellotaajuutta. Paikallisessa LLM-käytössä tämä ei aina ole ensimmäinen pullonkaula.

Jos 16 Gt kortti pakottaa sinut:

- pudottamaan kontekstin 4k-8k alueelle
- valitsemaan pienemmän mallin kuin oikeasti haluaisit
- siirtämään osan mallista tai välimuistista järjestelmämuistille
- välttämään rinnakkaisia pyyntöjä

... silloin nopeampi siru ei pelasta kokonaiskokemusta. Käyttö muuttuu tahmeaksi jo ennen kuin varsinainen laskentasuorituskyky ehtii ratkaista mitään.

Ollaman omissa integraatio-ohjeissa tämä näkyy myös mallisuosituksissa. Esimerkiksi Hermes-agentin paikallisissa suosituksissa `gemma4` on noin 16 Gt VRAM -luokan valinta, kun taas `qwen3.6` on noin 24 Gt VRAM -luokan valinta. Samoin Ollaman Anthropic-yhteensopivuusohjeessa `qwen3-coder`-mallista sanotaan suoraan, että sujuva ajo vaatii vähintään 24 Gt VRAMia, ja pidempi konteksti vaatii vielä enemmän.

Tämä on käytännössä tärkeämpää kuin moni ensiksi tajuaa: 24 Gt ei vain tee vanhaa mallia hieman mukavammaksi, vaan avaa kokonaan uuden mallijoukon ja pidemmät kontekstit ilman jatkuvaa kikkailua.

## Pitkä konteksti syö muistia nopeammin kuin aloittelija arvaa

Paikallisessa LLM-maailmassa moni budjetoi vain mallin koon, vaikka pitkä konteksti voi olla se asia joka lopulta kaataa suunnitelman.

Ollaman dokumentaatio suosittelee isoihin agentti- ja koodityökäyttöihin vähintään 64k kontekstia. Se on hyvä muistutus siitä, että "malli mahtuu 4k:lla" ei vielä tarkoita "setup on hyvä käytännössä". Jos ajat koodiapuria, dokumenttihakua, agenttia tai työkaluja käyttävää työnkulkua, konteksti ei ole koriste vaan osa käyttökokemusta.

Siksi 16 Gt kortti voi tuntua paperilla hyvältä, mutta päätyä arjessa kompromissikoneeksi:

- chat onnistuu
- lyhyet tehtävät onnistuvat
- pidempi repository- tai dokumenttityö alkaa kiristää muistia
- agenttimainen käyttö vaatii säätöä, pienemmän mallin tai matalamman kontekstin

24 Gt taas antaa enemmän tilaa hengittää ennen kuin ensimmäinen käytännön seinä tulee vastaan.

## Entä jos 16 Gt kortti on muuten selvästi nopeampi?

Silloin kysyisin vain yhden asian: **mahtuuko oma oikea työnkulku varmasti siihen ilman että joudut alentamaan mallia tai kontekstia?**

Jos vastaus on kyllä, nopeampi 16 Gt kortti voi olla erinomainen ostos. Tämä pätee erityisesti silloin, jos käytät pääosin:

- 7B-8B malleja
- kohtalaisia kvantisointeja
- lyhyttä tai keskipitkää kontekstia
- yhtä käyttäjää kerrallaan

Mutta jos tavoite on ostaa kortti kahdeksi tai kolmeksi vuodeksi eteenpäin, minä en laskisi vain tämän päivän 7B-käyttöä. Paikallisten mallien käytännön suunta on ollut jo pitkään sama: enemmän kontekstia, enemmän työkaluja, enemmän muistisyöppöjä työnkulkuja. Siinä maailmassa 24 Gt on paljon turvallisempi katto kuin 16 Gt.

## Muistikaistaa tärkeämpi kysymys: vältätkö jaetun kuorman

Ollaman FAQ muistuttaa myös yhdestä käytännön asiasta: jos malli mahtuu kokonaan yhdelle GPU:lle, se on yleensä paras suorituspolku, koska PCIe-siirtoa syntyy vähemmän. Tämä on hyvä syy suosia suurempaa yksittäistä VRAM-määrää silloin, kun vaihtoehtona olisi jatkuva tasapainottelu yhden GPU:n ja järjestelmämuistin tai usean kortin välillä.

Toisin sanoen isompi muistikatto voi tuoda suorituskykyhyödyn myös epäsuorasti. Vaikka itse kortti olisi hieman hitaampi, yhden laitteen sisälle mahtuva malli voi käyttäytyä kokonaisuutena paremmin kuin nopeampi mutta ahtaampi vaihtoehto.

## Milloin 16 Gt on edelleen täysin järkevä

En väitä, että 16 Gt olisi huono luokka. Se on monelle edelleen paras hinta-suorituskykyalue, jos käyttö on realistista.

16 Gt on minusta hyvä valinta, jos:

- ajat pääosin 7B-14B luokan kvantisoituja malleja
- et tarvitse jatkuvasti 32k-64k kontekstia
- käyttö on enemmän paikallista chattia kuin agenttipohjaista työnkulkua
- olet valmis säätämään K/V-välimuistin kvantisointia ja kontekstia tilanteen mukaan

Ollaman FAQ:ssa on tähän myös käytännön pelastuskeino: K/V-välimuistin kvantisointi. `q8_0` pudottaa muistitarpeen noin puoleen `f16`:een verrattuna ja `q4_0` noin neljäsosaan, tosin laadullisilla kompromisseilla. Tämä on hyödyllinen vipu 16 Gt korteille, mutta minusta sitä kannattaa ajatella optimointina, ei tekosyynä liian pienen muistimäärän ostolle.

## Milloin maksaisin mieluummin 24 Gt:sta

Maksaisin 24 Gt kortista mieluummin enemmän, jos yksikin näistä on totta:

- haluat käyttää paikallista koodiapuria tai agenttia pidemmällä kontekstilla
- haluat pitää koneen käyttökelpoisena myös ensi vuoden mallisukupolville
- et halua viettää aikaa jatkuvasti VRAM-rajan kanssa neuvotellen
- sinulle on tärkeää, että yksi GPU riittää mahdollisimman moneen tehtävään

Tässä kohtaa 24 Gt ei ole luksusta vaan käytännön joustovaraa.

## Yhteenveto

Jos budjettisi sallii valinnan nopeamman 16 Gt kortin ja riittävän 24 Gt kortin välillä, pitäisin paikallisia LLM:iä varten useimmiten 24 Gt vaihtoehtoa parempana ostoksena. **Syynä ei ole markkinointihype vaan se, että muistiraja määrää ensin mitä voit ajaa, millä kontekstilla ja kuinka paljon säätöä arki vaatii.**

16 Gt on yhä hyvä luokka kevyempään paikalliseen käyttöön. Mutta jos tähtäät pidempään kontekstiin, koodi- ja agenttityöhön tai haluat enemmän käyttöikää yhdelle ostokselle, 24 Gt on usein se raja jonka jälkeen kone alkaa tuntua vähemmän demolta ja enemmän oikealta työkalulta.

## Lähteet

- https://docs.ollama.com/context-length
- https://docs.ollama.com/faq
- https://docs.ollama.com/integrations/hermes
- https://docs.ollama.com/api/anthropic-compatibility
