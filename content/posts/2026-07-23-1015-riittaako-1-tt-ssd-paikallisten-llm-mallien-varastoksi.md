---
title: "Riittääkö 1 Tt SSD paikallisten LLM-mallien varastoksi?"
date: "2026-07-23T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Paikalliset LLM:t"
  - "SSD"
  - "Tallennus"
  - "Ollama"
---
Paikallista LLM-konetta suunnitellessa huomio karkaa helposti GPU:hun, VRAMiin ja RAMiin. Se on ymmärrettävää, koska ne vaikuttavat suoraan siihen mitä malleja voi ajaa. Silti yllättävän moni tekee tallennuksen kanssa saman virheen: ostaa koneeseen pienen mutta nopean SSD:n ja huomaa vasta myöhemmin, että **levy ei loppunut siksi että yksi malli olisi valtava, vaan siksi että paikallinen käyttö kerää nopeasti monta mallia, kvantisointia ja versiota rinnakkain**. Jos kysymys kuuluu, riittääkö 1 teratavun SSD paikallisten mallien varastoksi, käytännön vastaukseni on tämä: **riittää usein yhdelle käyttäjälle ja hallitulle mallivalikoimalle, mutta 2 Tt on paljon turvallisempi taso, jos vertailet aktiivisesti eri kokoja, koodimalleja tai 70B-luokkaa.**

## Miksi levytila loppuu helpommin kuin moni arvaa

Ollaman dokumentaatio sanoo tämän suoraan: itse asennus vie vain muutamia gigatavuja, mutta mallit voivat viedä kymmeniä tai satoja gigatavuja. Tämä on tärkeä lähtökohta, koska paikallinen LLM-kone ei yleensä pysähdy yhteen malliin. Käytännössä levylle kertyy nopeasti ainakin näitä:

- yleismalli chattiin
- koodimalli erikseen
- yksi tai kaksi isompaa mallia testiin
- eri kvantisointitasoja samasta mallista
- vanhoja versioita, joita ei tullutkaan poistettua

Siksi levytilan suunnittelussa kannattaa ajatella mallikirjastoa, ei yksittäistä suosikkimallia.

## Lähteet näyttävät jo kokoluokan

llama.cpp:n kvantisointiohje antaa erittäin hyödyllisen mittapuun. Sen esimerkissä Llama 3.1 8B pienenee Q4_K_M-kvantisoinnilla noin 32,1 gigatavusta noin 4,9 gigatavuun. Sama dokumentti näyttää myös, että 70B-malli voi olla kvantisoitunakin noin 43,1 gigatavua ja 405B-luokka noin 249,1 gigatavua.

Ollaman kirjastosivut näyttävät saman ilmiön toisesta kulmasta. `qwen2.5-coder:0.5b` on vain 398 Mt, mutta saman perheen `latest`-malli on 4,7 Gt. `llama3.1:8b` on 4,9 Gt, `llama3.1:70b` 43 Gt ja `llama3.1:405b` 243 Gt. Tästä seuraa aika arkinen mutta tärkeä havainto: **levytilaa ei syö yksi “LLM”, vaan malliperheiden leveys ja se, että kiinnostavat vaihtoehdot ovat usein eri kokoluokissa.**

## Mitä 1 Tt käytännössä tarkoittaa

Paperilla 1 Tt kuulostaa suurelta. Käytännössä kaikki siitä ei ole paikallisille malleille vapaata:

- käyttöjärjestelmä vie osansa
- työkalut, editorit ja muut projektit vievät osansa
- välimuistit, checkpointit ja lataukset paisuvat ajan myötä
- turvallinen vapaa tila kannattaa jättää erikseen

Siksi “1 Tt SSD” ei tarkoita “1 Tt malleille”. Käytännöllinen ajattelutapa on varata vain osa levystä mallikirjastolle, ei koko levyä.

Minun nyrkkisääntöni olisi tällainen:

- `512 Gt`: riittää lähinnä yhdelle kevyelle paikalliskoneelle, jos käytät pääasiassa 7B-14B-luokan malleja ja poistat vanhat aktiivisesti
- `1 Tt`: hyvä perustaso, jos käytät muutamaa mallia tarkoituksella etkä kerää isoja 70B-kokeiluja monta rinnakkain
- `2 Tt`: paljon huolettomampi taso, jos ajat koodimalleja, vertailet kvantisointeja tai pidät 32B-70B-luokan malleja oikeasti saatavilla

Tämä jaottelu on oma käytännön tulkintani lähteiden kokoluokista, ei mikään valmistajien virallinen taulukko. Mutta juuri siksi se on harrastajalle hyödyllinen: se auttaa arvioimaan käyttötapaa, ei vain yksittäistä speksiä.

## Missä 1 Tt alkaa tuntua ahtaalta

1 Tt SSD alkaa kiristyä nopeasti, jos yksikin näistä pitää paikkansa:

- pidät samasta mallista useita kvantisointeja vertailussa
- käytät erikseen chat-, koodi- ja reasoning-malleja
- haluat säilyttää ainakin yhden 70B-luokan mallin valmiina
- lataat uusia malleja uteliaisuudesta mutta siivoat harvoin
- käytät samaa levyä myös peleille, kuville, virtuaalikoneille tai isoille repoille

Tässä kohtaa ongelma ei yleensä näy heti. Se näkyy kuukausien aikana pienenä kitkana: malli pitää poistaa ennen seuraavaa testiä, levy alkaa olla jatkuvasti yli 80-prosenttisesti täynnä, ja uusi kokeilu tuntuu aina vähän “siivousoperaatiolta”.

## Missä 1 Tt on edelleen täysin järkevä valinta

En pitäisi 1 Tt levyä huonona ostoksena, jos käyttö on rajattu ja kurinalainen. Se on aivan järkevä valinta esimerkiksi silloin, kun:

- ajat pääosin yhtä tai kahta päivittäistä mallia
- käytät enimmäkseen 7B-14B-luokkaa
- poistat vanhat vedot etkä säilytä kaikkea varmuuden vuoksi
- voit tarvittaessa siirtää mallihakemiston toiselle levylle

Tässä kohtaa Ollaman `OLLAMA_MODELS`-ympäristömuuttuja on käytännöllinen yksityiskohta. Jos nopea järjestelmälevy on pieni mutta koneessa on toinen suurempi SSD, mallikirjaston voi siirtää erikseen. Tämä on usein fiksumpi ratkaisu kuin väkisin tunkea koko mallivarasto samalle levylle kuin käyttöjärjestelmä.

## Milloin ostaisin suoraan 2 Tt

Ostaisin suoraan 2 Tt SSD:n, jos koneen tarkoitus ei ole vain “ajaa yhtä paikallista mallia” vaan toimia oikeana LLM-työasemana. Varsinkin nämä tilanteet puoltavat isompaa levyä:

- vertailet malleja aktiivisesti
- käytät sekä Ollamaa että llama.cpp-pohjaisia tiedostoja
- haluat säilyttää suurempia malleja ilman jatkuvaa poistamista
- rakennat koodi- tai agenttikäyttöä, jossa mallivalikoima elää

Tässä tapauksessa lisäkapasiteetti ei ole luksusta vaan tapa ostaa pois jatkuvaa levytilan mikromanageerausta.

## Oma suositukseni

Jos kysymys on “toimiiko 1 Tt paikallisten LLM-mallien kanssa”, vastaus on kyllä. Jos kysymys on “onko 1 Tt huoleton pitkäikäinen koko aktiiviselle mallikirjastolle”, vastaus on paljon varovaisempi.

Sanoisin sen näin:

- `1 Tt` on hyvä peruslähtö yhdelle käyttäjälle ja hallitulle mallimäärälle
- `2 Tt` on parempi oletus, jos tiedät jo valmiiksi että kokeilet paljon tai käytät myös isompia malleja

Paikallisessa AI-koneessa levytilan ongelma ei yleensä ala siitä, että yksi malli on liian iso. Se alkaa siitä, että **paikallinen työ muuttuu oikeaksi harrastukseksi tai työkaluksi, ja samalla yhdestä mallista tulee nopeasti kuusi**.

## Lähteet

- https://docs.ollama.com/windows
- https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/quantize/README.md
- https://ollama.com/library/qwen2.5-coder
- https://ollama.com/library/llama3.1
