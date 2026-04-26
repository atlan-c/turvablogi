---
title: "AI-rauta kotilabrassa: milloin virtalähde on paikallisen LLM-koneen hiljainen pullonkaula?"
date: 2026-04-26T10:15:00+03:00
draft: false
topic_family: "llm-hardware"
---

Virtalähde on yksi niistä komponenteista, joita paikallista LLM-konetta rakentaessa aliarvioidaan jatkuvasti. Moni valitsee ensin GPU:n, RAMin ja levyt, ja ottaa PSU:n vasta lopuksi "jotain riittävää" -mentaliteetilla. Se toimii joskus, mutta juuri AI-koneissa virtalähde on yllättävän usein hiljainen pullonkaula, joka ei näy benchmarkissa vaan käytöksenä: satunnaisena epävakautena, meluna, kuumuutena tai huonona päivitettävyytensä.

Lyhyt käytännön sääntö on tämä: jos rakennat paikallista LLM-konetta yhdelläkin tehokkaalla GPU:lla, virtalähde ei ole paikka jossa kannattaa säästää viimeiseen asti. Sen ei tarvitse olla ylellinen, mutta sen pitää olla oikeasti sopiva kuormalle.

## Mitä virtalähde oikeastaan tekee

Tietokoneen virtalähde muuntaa verkkovirran matalajännitteiseksi tasavirraksi koneen sisäisille komponenteille. Wikipedia kuvaa tämän suoraan: PSU syöttää emolevylle, prosessorille ja oheislaitteille useita säänneltyjä jännitelinjoja. Käytännössä tämä tarkoittaa, että koko koneen vakaus lepää sen varassa, miten hyvin virtalähde hoitaa kuorman, piikit ja lämpenemisen.

Paikallisissa LLM-koneissa kuorma ei ole aina tasaista. GPU voi nousta nopeasti korkeaan kulutukseen, CPU saattaa samalla tehdä omaa osuuttaan, ja levyt sekä tuulettimet lisäävät oman osansa. Jos PSU on mitoitettu liian tiukasti tai laadultaan heikko, ongelma ei aina näy heti. Se näkyy vasta silloin kun kone on pitkään rasituksessa tai siirtyy äkisti kevyestä kuormasta raskaaseen.

## Milloin virtalähde muuttuu oikeaksi ongelmaksi

Virtalähde alkaa olla todellinen pullonkaula yleensä silloin, kun jokin näistä täyttyy:

1. GPU on teholtaan raskas ja kulutuspiikit ovat korkeita
2. koneessa on useita lisälaitteita, kuten useita levyjä tai toinen GPU
3. kotelo on lämmin ja PSU joutuu toimimaan jatkuvasti kovalla kuormalla
4. koneen halutaan olevan hiljainen mutta virtalähde joutuu koko ajan äänekkäälle alueelle
5. tulevia päivityksiä ei ole huomioitu lainkaan

Tällöin ongelma ei ole vain wattimäärä. Myös laatu, hyötysuhde, jäähdytys ja kaapelointi alkavat vaikuttaa käytännössä paljon.

## Miksi 80 Plus ei yksin ratkaise mitään

80 Plus -sertifiointi kertoo ennen kaikkea hyötysuhteesta tietyillä kuormatasoilla. Se on hyödyllinen signaali, mutta ei yksin takaa että virtalähde olisi juuri sinun AI-koneeseesi hyvä. Se kertoo, että vähemmän energiaa menee lämmöksi ja enemmän päätyy hyödylliseksi sähköksi, mutta se ei yksin kerro kaikkea transienttikäytöksestä, melusta, komponenteista tai kokonaislaadusta.

Siksi pelkkä "Gold riittää" tai "Platinum on pakko olla" on liian karkea sääntö. Tärkeämpää on, että virtalähde toimii järkevällä kuorma-alueella eikä jatkuvasti aivan rajalla.

## Oma käytännön nyrkkisääntö

Minun käytännön sääntöni olisi tämä:

- älä mitoita PSU:ta vain nimelliskulutuksen mukaan
- jätä järkevä pelivara GPU:n ja koko koneen kuormapiikeille
- suosi mallia, joka toimii normaalissa käytössä selvästi alle maksimin
- jos haluat hiljaisuutta ja päivitettävyyttä, ota mieluummin hieman väljempi kuin liian tiukka virtalähde

Tämä ei tarkoita, että kaikkeen pitäisi ostaa valtava overkill-PSU. Se tarkoittaa vain, että paikallisessa LLM-koneessa virtalähde kannattaa nähdä vakaus- ja käyttömukavuuskomponenttina, ei vain pakollisena laatikkona.

## Missä säästämisen hinta näkyy

Halpa tai liian pieni PSU kostautuu usein epäsuorasti:

- kone voi sammua tai käyttäytyä oudosti raskaassa kuormassa
- tuulettimen ääni nousee ikäväksi pitkissä ajoissa
- lämpökuorma kasvaa kotelossa
- tulevat GPU-päivitykset muuttuvat hankaliksi
- vianhaku vaikeutuu, koska oireet näyttävät helposti muistilta, emolevyltä tai ajureilta

Tämä on juuri sellainen komponentti, jonka arvo ymmärretään usein vasta sitten kun joku menee ärsyttävän epämääräisesti pieleen.

## Yhteenveto

Milloin virtalähde on paikallisen LLM-koneen hiljainen pullonkaula? Silloin, kun koneessa on paljon kuormaa, kulutuspiikkejä, lämpöä tai kasvunvaraa, mutta PSU on valittu liian optimistisesti.

Hyvä käytännön ajatus on tämä: paikallisen AI-koneen virtalähde ei tuo lisää tokeneita sekunnissa, mutta se voi ratkaista kuinka vakaa, hiljainen ja päivitettävä koko kone oikeasti on.

## Lähteet

- https://en.wikipedia.org/wiki/Power_supply_unit_(computer)
- https://en.wikipedia.org/wiki/80_Plus
