---
title: "AI-rauta kotilabrassa: milloin jäähdytys on tärkeämpi päivitys kuin seuraava prosessori?"
date: 2026-04-28T10:15:00+03:00
draft: false
topic_family: "llm-hardware"
---

Paikallista LLM-konetta rakentaessa seuraava päivityshaave on usein uusi prosessori. Se kuulostaa järkevältä, mutta käytännössä monessa koneessa parempi seuraava sijoitus olisi ensin jäähdytys. Jos lämpö karkaa, kellot laskevat, melu nousee ja koko koneen käytös muuttuu epävakaammaksi. Silloin kalliimpi CPU ei välttämättä tuo sitä hyötyä, jota odotit.

Lyhyt käytännön sääntö on tämä: jos nykyinen kone throttlaa, puhaltaa jatkuvasti kovaa tai käy kuumana pitkissä ajoissa, jäähdytys voi olla tärkeämpi päivitys kuin seuraava prosessori.

## Miksi jäähdytys vaikuttaa niin paljon

Tietokoneen jäähdytyksen tehtävä on poistaa komponenttien tuottama hukkalämpö niin, että ne pysyvät sallituissa lämpötiloissa. Wikipedia tiivistää asian suoraan: CPU:t, GPU:t, piirisarjat, levyt ja muut osat voivat ylikuumentuessaan joko toimia väliaikaisesti huonosti tai vaurioitua pysyvämmin. Modernit prosessorit myös suojaavat itseään hidastamalla kellojaan tai sammuttamalla itsensä, jos lämpötila karkaa liian korkeaksi.

Paikallisessa LLM-käytössä tämä on erityisen tärkeää, koska kuorma ei ole aina lyhyt piikki vaan usein pitkäkestoista laskentaa. Jos kone käy tunnin, kaksi tai pidempään kovassa rasituksessa, huono jäähdytys ei näy vain hetkellisenä epämukavuutena vaan jatkuvana suorituskyvyn menetyksenä.

## Miksi TDP ei ole koko totuus

Thermal design power eli TDP kertoo, minkä verran lämpöä jäähdytysratkaisun pitäisi pystyä poistamaan normaalissa käytössä. Mutta kuten TDP-artikkeli muistuttaa, todellinen hetkellinen tai raskaan kuorman tehonkulutus voi ylittää tämän. Erityisesti turbokäyttäytyminen ja käytännön kuormat voivat nostaa lämmön korkeammaksi kuin pelkkä numero paperilla antaa ymmärtää.

Tästä syntyy tuttu kotilabran ansa: katsotaan että "cooleri tukee tämän prosessorin TDP:tä", mutta todellisessa pitkässä AI-kuormassa lämpötilat nousevat silti liikaa. Paperi ja arki eivät aina ole sama asia.

## Milloin jäähdytys on todennäköisesti parempi päivitys

Jäähdytys kannattaa nostaa seuraavaksi investoinniksi erityisesti silloin, kun huomaat jotain näistä:

- tuulettimet huutavat pitkissä ajoissa
- CPU tai GPU throttlaa raskaassa kuormassa
- koteloon kertyy selvästi kuumaa ilmaa
- pöly, huono ilmankierto tai heikko cooleri pitävät lämmöt korkealla
- suorituskyky putoaa pidemmässä ajossa verrattuna lyhyeen testiin

Tällöin uusi prosessori voi jopa pahentaa ongelmaa, koska se tuo lisää lämpöä samaan jo valmiiksi rajalliseen koteloon.

## Missä jäähdytyksen parannus näkyy käytännössä

Hyvä jäähdytys ei ole vain pienempi lämpölukema ruudulla. Se näkyy käytännössä näin:

- kellot pysyvät tasaisempina pitkissä ajoissa
- melu vähenee
- komponentit eivät elä jatkuvasti lämpörajoilla
- koko koneen vakaus ja käyttömukavuus paranevat
- tuleville päivityksille jää enemmän pelivaraa

Toisin sanoen jäähdytys ei vain suojele rautaa, vaan tekee suorituskyvystä tasaisempaa. Tämä on paikallisissa LLM-ajoissa usein arvokkaampaa kuin lyhyt piikki benchmarkissa.

## Oma käytännön nyrkkisääntö

Minun käytännön sääntöni olisi tämä:

1. jos kone on jo lämpörajalla, älä päivitä heti tehokkaampaan prosessoriin
2. tarkista ensin coolerin taso, kotelon ilmankierto, pöly ja tuulettimien suunta
3. paranna jäähdytystä ennen CPU-päivitystä, jos nykyinen suorituskyky ei pysy vakaana pitkissä ajoissa
4. päivitä prosessori vasta, kun tiedät että lämpöbudjetti oikeasti kestää sen

Tämä tuntuu vähemmän hauskalta kuin uuden prosessorin ostaminen, mutta usein juuri tässä kohtaa säästyy rahaa ja hermoja.

## Yhteenveto

Milloin jäähdytys on tärkeämpi päivitys kuin seuraava prosessori? Silloin, kun nykyinen kone ei pysty pitämään suorituskykyään vakaana lämmön vuoksi.

Paikallisessa LLM-käytössä hyvä jäähdytys ei ole vain mukavuuslisä. Se voi olla se ero, joka ratkaisee pysyykö kone oikeasti nopeana koko ajon ajan vai vain ensimmäiset minuutit.

## Lähteet

- https://en.wikipedia.org/wiki/Computer_cooling
- https://en.wikipedia.org/wiki/Thermal_design_power
