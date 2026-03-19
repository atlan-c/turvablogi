---
title: "Kannattaako käytetty RTX 3090 vielä paikalliselle LLM-harrastajalle vuonna 2026?"
date: 2026-03-19T10:15:00+02:00
draft: false
---

Jos paikallista LLM-konetta rakentava harrastaja kysyy vuonna 2026, mikä käytetty näytönohjain kiinnostaa edelleen eniten, **RTX 3090 nousee yhä hyvin nopeasti listalle**. Syy ei ole mystinen: NVIDIA:n omien speksien mukaan kortissa on **24 Gt GDDR6X-muistia**, 384-bittinen muistiväylä ja PCIe Gen 4 -tuki. Juuri tuo 24 gigatavun VRAM on se kohta, joka tekee 3090:stä edelleen käytännöllisen AI-rautakortin eikä vain vanhan lippulaivan.

Lyhyt vastaus on tämä: **käytetty RTX 3090 voi olla edelleen erittäin järkevä ostos paikalliseen LLM-koneeseen, jos saat sen hyvään hintaan ja hyväksyt tehonkulutuksen, lämmön ja käytetyn raudan riskit**. Se ei ole automaattisesti paras ostos kaikille, mutta 24 Gt VRAMia on edelleen vaikea korvata halvalla.

## Miksi 24 Gt VRAM on edelleen koko keskustelun ydin?

Paikallisessa LLM-käytössä tärkein raja ei yleensä ole se, onko kortti "uusi", vaan se, **mahtuuko malli riittävän pitkälle GPU:lle**. Ollaman FAQ kuvaa tämän hyvin konkreettisesti: malli voi olla `100% GPU`, `100% CPU` tai osittain molemmissa. Harrastajan näkökulmasta ero on iso, koska täysin GPU:lla pysyvä ajo tuntuu yleensä paljon mukavammalta kuin tilanne, jossa osa mallista valuu järjestelmämuistin puolelle.

Siksi 24 Gt VRAM ei ole vain numero. Se on käytännössä se raja, jonka ansiosta voit:

- ajaa suurempia kvantisoituja malleja ilman välitöntä CPU-offloadia
- jättää enemmän tilaa kontekstille ja runtime-yläkuluille
- testata useampia malliperheitä ilman että jokainen kokeilu kaatuu kapasiteettiin
- rakentaa koneen, joka tuntuu työkalulta eikä jatkuvalta kompromissilta

Hugging Facen Llama 3.1 -kirjoitus muistuttaa hyvin, että muistitarve nousee nopeasti mallikoon mukana. Se tekee 24 gigasta edelleen houkuttelevan luokan: se ei tee mahdottomasta mahdollista, mutta se siirtää paljon harrastajalle relevantteja malleja pois "ehkä juuri ja juuri" -kategoriasta ja kohti oikeasti käyttökelpoista aluetta.

## Milloin käytetty 3090 on hyvä idea?

Käytetty 3090 on yleensä hyvä idea tällaiselle ostajalle:

- haluat nimenomaan **enemmän VRAMia**, et vain lisää pelisuorituskykyä
- ajat paikallisesti 7B–32B-luokan kvantisoituja malleja ja haluat pelivaraa
- haluat välttää tilanteita, joissa malli tippuu jatkuvasti osittain CPU:lle
- rakennat yhden tehokkaan työaseman etkä pientä ja hiljaista konetta
- hyväksyt sen, että käytetty huippukortti voi vaatia enemmän tarkistamista kuin uusi keskihintainen kortti

Tämä on tärkeä ero. Jos tavoite on nimenomaan paikallinen AI, 3090:n arvo tulee VRAMista paljon enemmän kuin siitä, että kortti olisi tuore arkkitehtuuri.

## Milloin 3090 ei ole hyvä ostos?

3090 ei ole hyvä oletusvalinta kaikille. Jättäisin sen väliin ainakin näissä tilanteissa:

- haluat mahdollisimman hiljaisen ja viileän koneen
- kotelon ilmanvaihto tai virtalähde on jo valmiiksi rajallinen
- et halua ostaa käytettyä rautaa lainkaan
- ajat enimmäkseen pieniä malleja, joihin riittäisi selvästi pienempikin VRAM
- löydät uudemman 24 Gt kortin vain vähän kalliimmalla ja arvostat takuuta tai energiatehokkuutta enemmän

Toisin sanoen: **3090 on edelleen hyvä AI-kortti, mutta ei erityisen elegantti AI-kortti**. Se on enemmän voimatyökalu kuin siro ratkaisu.

## Käytetyn 3090:n kolme todellista riskiä

### 1. Et osta vain VRAMia, vaan myös vanhaa lämpö- ja rasitushistoriaa

Käytetty 3090 on monella myyjällä ollut kovassa kuormassa. Se ei yksin tee kortista huonoa ostosta, mutta nostaa tarkistuslistan arvoa. Harrastajan kannattaa tarkistaa ainakin:

- onko korttia avattu tai huollettu
- pyörivätkö tuulettimet tasaisesti
- onko coil whine, lämpöjen karkaaminen tai muistien kuumeneminen selvä ongelma
- näkyykö kortissa pölyn, öljyn tai huolimattoman purkamisen merkkejä
- saako kortista testivideon tai vähintään kuvakaappaukset kuormituksesta

### 2. Tehonkulutus ja lämpö kuuluvat pakettiin

Vaikka käytetty hinta olisi hyvä, 3090 ei ole "halpa kokonaisuus", jos muu kone ei ole valmis sille. Tämän korttiluokan kanssa kannattaa ajatella aina koko järjestelmää: virtalähde, kotelon ilmankierto, melu ja huonelämpö. Jos rakennat pientä kotilabrapalvelinta nurkkaan, 3090 voi olla juuri väärä tapa säästää rahaa.

### 3. Pelkkä kortti ei ratkaise huonoa kokoonpanoa

llama.cpp:n suorituskykyvinkit ovat tässä hyödyllinen muistutus. Dokumentaatio painottaa, että GPU-offload pitää tarkistaa oikeasti eikä vain olettaa sen toimivan, ja että väärä thread-asetus voi tehdä tokenituotannosta yllättävän hidasta. Käytännössä tämä tarkoittaa, että jos paikallinen LLM tuntuu tahmealta, syy ei aina ole kortin puute vaan esimerkiksi:

- malli ei oikeasti offloadaudu kunnolla GPU:lle
- säiemäärä on pielessä
- järjestelmämuisti tai tallennuspuoli ahdistaa
- konteksti on nostettu liian korkeaksi suhteessa rautaan

3090 auttaa kapasiteettiin. Se ei korjaa automaattisesti huonoa säätöä.

## Mitä tarkistaisin ennen ostopäätöstä?

Jos harkitsisin käytettyä RTX 3090:tä tänään nimenomaan paikallisiin LLM-ajohin, kävisin läpi tämän listan:

1. **Hinta suhteessa 24 Gt vaihtoehtoihin** – ostatko aidosti VRAM-etua vai vain vanhaa huippukorttia?
2. **Kotelon ja virtalähteen valmius** – mahtuuko kortti ja kestääkö muu kokoonpano sen järkevästi?
3. **Näyttö myyjän testeistä** – idle-lämpö, kuormalämpö, fanit, mahdolliset artifactit.
4. **Tavoitemallit** – mitä malleja oikeasti aiot ajaa ja hyötyvätkö ne 24 gigasta selvästi?
5. **Käyttöprofiili** – tuleeko kone työpöydälle, palvelimeksi vai satunnaiseen testiin?

Tämä viimeinen kohta on yllättävän tärkeä. Jos kone on joka päivä käytössä, energiatehokkuus, melu ja huollettavuus painavat enemmän kuin jos kyseessä on satunnainen kokeiluloota.

## Oma käytännön johtopäätös

Minusta käytetty RTX 3090 on vuonna 2026 edelleen **aidosti järkevä paikallisen LLM-harrastajan ostos**, jos prioriteetti on mahdollisimman paljon VRAMia mahdollisimman kohtuullisella rahalla. Se on erityisen kiinnostava silloin, kun haluat ajaa paikallisia malleja mukavammin ilman että jokainen askel päätyy CPU/GPU-sekoitukseen.

En kuitenkaan suosittelisi sitä sokkona. Jos haluat hiljaisen, viileän, uuden ja huolettoman koneen, 3090 ei ole kovin romanttinen ratkaisu. Mutta jos katsot rautaa käytännön kautta ja ymmärrät mitä 24 Gt VRAM sinulle ostaa, se on edelleen vaikea sivuuttaa.

Yksi hyvä nyrkkisääntö on tämä: **jos koko projektin tarkoitus on ajaa paikallisia LLM:iä, osta VRAM edellä — mutta osta käytetty 3090 vain, jos muu kone ja oma riskinsietosi sopivat sen luonteeseen**.

## Lähteet

- NVIDIA GeForce RTX 3090 / 3090 Ti specs: https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3090-3090ti/
- Ollama FAQ (`ollama ps`, CPU/GPU-jako, konteksti): https://docs.ollama.com/faq
- llama.cpp – Token generation performance tips: https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md
- Hugging Face – Llama 3.1 inference and memory overview: https://huggingface.co/blog/llama31#inference-memory-requirements
