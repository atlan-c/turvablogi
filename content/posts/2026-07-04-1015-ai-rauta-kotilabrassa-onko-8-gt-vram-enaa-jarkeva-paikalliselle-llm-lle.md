---
title: "AI-rauta kotilabrassa: onko 8 Gt VRAM enää järkevä paikalliselle LLM:lle?"
date: "2026-07-04T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-rauta kotilabrassa"
tags:
  - "AI-rauta"
  - "VRAM"
  - "Ollama"
  - "GPU"
  - "Paikalliset LLM:t"
---
Jos olet ostamassa tai päivittämässä paikallista LLM-konetta vuonna 2026, yksi käytännön kysymys nousee yhä uudestaan esiin: **onko 8 Gt VRAM enää järkevä lähtötaso vai muuttuuko se nopeasti liian pieneksi heti kun käyttö kasvaa demosta oikeaksi työksi?** Oma lyhyt vastaukseni on tämä: **8 Gt voi vielä riittää pieneen ja kurinalaiseen käyttöön, mutta uutena ostoksena se on nyt useimmiten liian niukka, jos aiot ajaa paikallisia malleja säännöllisesti etkä vain testata että "kyllä tämä käynnistyy".**

Tärkein syy ei ole pelkkä mallin tiedostokoko. Käytännössä VRAMia syövät samaan aikaan mallin painot, konteksti ja mahdollinen rinnakkaisuus. Siksi 8 Gt näyttää paperilla siedettävältä pidempään kuin se tuntuu arjessa.

## Miksi 8 Gt ei ole sama asia kuin "8 gigaa mallille"

Ollaman dokumentaatio sanoo suoraan, että kontekstin pituus kasvattaa muistitarvetta. Samassa ohjeessa oletuskontekstit on sidottu VRAM-luokkiin: alle 24 GiB VRAMilla oletus on 4k, 24-48 GiB VRAMilla 32k ja siitä ylöspäin vielä enemmän. Tämä on harrastajalle hyödyllinen signaali, koska se kertoo kahdesta asiasta kerralla:

1. pieni VRAM ei rajoita vain mallin kokoa
2. pieni VRAM rajoittaa myös sitä, kuinka mukavasti voit kasvattaa kontekstia agentteihin, koodiapuun tai pidempiin dokumentteihin

Toinen käytännön kohta löytyy FAQ:sta. Ollama kertoo, että rinnakkaiset pyynnöt kasvattavat muistitarvetta, ja että GPU-ajossa uuden mallin pitää mahtua kokonaan VRAMiin, jotta useita malleja voidaan pitää ladattuina yhtä aikaa. Tämä on juuri se kohta, jossa 8 Gt alkaa kiristää nopeasti: yksi pieni malli voi vielä tuntua ihan käyttökelpoiselta, mutta toinen malli, pidempi konteksti tai pieni rinnakkaisuus syö viimeiset marginaalit heti.

## Mitä 8 Gt:lla voi vielä tehdä järkevästi

En pitäisi 8 Gt VRAMia täysin kuolleena luokkana. Sille on edelleen olemassa ihan oikea käyttö:

- yksi käyttäjä
- yksi pieni tai kohtuullisesti kvantisoitu malli kerrallaan
- lyhyt tai maltillinen konteksti
- ei tavoitetta pitää useita malleja lämpimänä muistissa

Ollaman mallin tuontiohje muistuttaa myös, että kvantisointi pienentää muistinkulutusta ja nopeuttaa ajoa, tosin tarkkuuden kustannuksella. Tämä on 8 Gt -luokan pelastuskeino. Jos olet valmis käyttämään pienempiä kvantisointeja ja hyväksymään sen, että kaikki mallit eivät ole "täyslaatuisia", saat 8 Gt koneesta vielä ihan käyttökelpoisen henkilökohtaisen apurin.

Toisin sanoen 8 Gt voi toimia, jos työ muistuttaa enemmän paikallista chattia, lyhyitä tiivistyksiä ja satunnaista koodiapua kuin jatkuvaa agenttityötä.

## Missä kohtaa 8 Gt muuttuu huonoksi ostokseksi

Vuonna 2026 ongelma ei ole enää vain se, että 8 Gt on pieni. Ongelma on se, että monet uudemmat kortit tulevat muuten hyvin lähelle toisiaan, mutta tarjoavat eri VRAM-määrän. NVIDIA:n tuotesivujen mukaan esimerkiksi RTX 5060 Ti on saatavana sekä 16 Gt että 8 Gt GDDR7 -versiona, ja myös aiemman sukupolven RTX 4060 Ti:stä on sekä 16 Gt että 8 Gt versiot.

Kun muu kortin luonne on lähellä samaa, VRAM ei ole paikallisen LLM-käytön kannalta sivuseikka vaan käytännössä se ominaisuus, joka ratkaisee käyttöiän. Siksi pitäisin 8 Gt -versiota huonona uutena ostoksena ainakin näissä tilanteissa:

- haluat käyttää pidempiä konteksteja kuin peruschatissa
- haluat kokeilla agentteja, työkaluja tai web-haun kaltaisia työnkulkuja
- haluat pitää useita malleja valmiina muistissa
- haluat että kone kestää myös ensi vuoden mallit, ei vain tämän päivän pienimmät vaihtoehdot
- et halua elää jatkuvasti kompromissilla "käytän tätä pienempää kvantisointia, koska muuten ei mahdu"

Tässä mielessä 8 Gt on tänään enemmän demoluokka kuin mukava työluokka.

## Jos vaihtoehto on 8 Gt tai 16 Gt samasta korttiperheestä

Jos valitset kahden muuten lähellä toisiaan olevan kortin välillä, minun käytännön suositukseni on yksinkertainen: **ota 16 Gt, jos budjetti vain venyy siihen ilman että koko muu kone kärsii.** Perustelu ei ole vain "isompi on parempi", vaan tämä:

1. kontekstin kasvatus vaatii muistia
2. rinnakkaisuus vaatii muistia
3. toisen mallin pitäminen ladattuna vaatii muistia
4. isompi VRAM vähentää tarvetta aggressiiviselle kvantisoinnille

Paikallisessa LLM-käytössä tämä näkyy usein selvemmin kuin raakasuorituskyvyn pienet erot. Jos toinen kortti on vähän nopeampi mutta jää 8 Gt:hen, ja toinen tarjoaa selvästi enemmän muistia, ottaisin itse useimmiten muistia.

## Milloin ostaisin 8 Gt kortin silti

Ostaisin 8 Gt kortin vielä vain, jos jokin seuraavista pitää paikkansa:

- saat sen selvästi halvemmalla käytettynä
- tiedät ajavasi vain pieniä kvantisoituja malleja
- käyttö on satunnaista eikä kone ole tärkeä työväline
- muu budjetti menisi muuten rikki niin pahasti, että vaihtoehto olisi olla ostamatta mitään

Silloinkin ajattelisin sitä välivaiheen ratkaisuna, en "nyt tämä ongelma on ratkaistu vuosiksi" -ostoksena.

## Käytännön nyrkkisääntö vuonna 2026

Jos kysyt minulta onko 8 Gt VRAM enää järkevä paikalliselle LLM:lle, vastaan näin:

- kyllä, jos tarkoitus on opetella, kokeilla ja käyttää pieniä kvantisoituja malleja yksin
- ehkä, jos ostat käytettynä hyvin halvalla ja hyväksyt selvät rajat
- ei, jos ostat uuden kortin nimenomaan paikallista LLM-työtä varten

Minusta tämän hetken järkevin ajattelutapa on pitää 8 Gt VRAMia miniminä, jonka yli pyritään heti kun mahdollista. Se ei ole täysin käyttökelvoton, mutta se on nyt liian lähellä rajoja, jotta sitä voisi suositella turvallisena oletusostoksena.

## Tiivis johtopäätös

**8 Gt VRAM ei ole täysin kuollut paikallisessa LLM-käytössä, mutta se ei ole enää hyvä oletus uudelle ostokselle vuonna 2026.** Pienet kvantisoidut mallit ja kevyt käyttö toimivat yhä, mutta kontekstin kasvatus, useampi malli ja agenttimaisempi työ syövät marginaalin nopeasti. Jos valitset muuten samantasoisten korttien välillä, paikalliselle LLM:lle tärkein lisäominaisuus ei ole hienompi markkinointisana vaan suurempi VRAM.

## Lähteet

- https://docs.ollama.com/context-length
- https://docs.ollama.com/faq
- https://docs.ollama.com/import
- https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5060-family/
- https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4060-4060ti/
