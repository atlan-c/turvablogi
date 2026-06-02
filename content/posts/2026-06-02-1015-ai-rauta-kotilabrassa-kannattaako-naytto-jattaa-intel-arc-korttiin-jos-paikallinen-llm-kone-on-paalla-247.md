---
title: "AI-rauta kotilabrassa: kannattaako näyttö jättää Intel Arc -korttiin, jos paikallinen LLM-kone on päällä 24/7?"
date: "2026-06-02T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "GPU"
  - "Intel Arc"
  - "Power"
  - "Hardware"
---
Paikallisen LLM-koneen sähkölasku ei synny vain tokenien laskennasta. Yllättävän usein rahaa ja lämpöä kuluu siihen, että kone **odottaa** seuraavaa tehtävää väärällä tavalla. Tämä korostuu erityisesti Intel Arc -korteilla, koska niissä tyhjäkäynnin kulutus riippuu poikkeuksellisen paljon siitä, **montako näyttöä korttiin on kytketty, millä resoluutiolla ja millä virkistystaajuudella**. Siksi käytännön kysymys ei ole vain "toimiiko Arc paikallisessa LLM-ajossa", vaan myös: **kannattaako näyttö pitää kiinni juuri siinä GPU:ssa, joka pyörittää 24/7 paikallista AI-konetta?**

Minun lyhyt vastaukseni on tämä: **ei yleensä kannata, jos koneen tärkein rooli on olla aina päällä oleva paikallinen LLM-palvelin.** Jos voit ajaa näyttöä integroidulla grafiikalla, toisella koneella tai pitää AI-laatikon kokonaan headlessinä, se on Arc-koneessa usein fiksumpi ratkaisu kuin jättää korkean virkistystaajuuden näyttö suoraan AI-GPU:hun.

## Miksi tällä on juuri Arc-koneessa väliä

Intel sanoo tästä yllättävän suoraan omissa ohjeissaan. Arc-korttien tyhjäkäyntikulutus riippuu olennaisesti kytkettyjen näyttöjen määrästä sekä niiden resoluutiosta ja virkistystaajuudesta. Intelin tukisivun mukaan Arc A -sarja pääsee tyhjäkäynnin matalaan tehotilaan yhdellä näytöllä korkeintaan 4K 60 Hz -tasolla ja kahdella näytöllä korkeintaan 1080p 60 Hz -tasolla. Kolmella tai neljällä näytöllä matalaa idle-tilaa ei tuon ohjeen mukaan enää saavuteta.

Tämä on paikallisen LLM-harrastajan kannalta paljon tärkeämpää kuin miltä se ensin kuulostaa. Moni kotilabran AI-kone tekee päivän aikana lyhyitä inference-pyrähdyksiä, mutta muuten se seisoo valmiustilassa:

- odottaa seuraavaa agenttitehtävää
- toimii taustapalveluna Ollamalle tai `llama-serverille`
- pyörittää satunnaisia tiivistyksiä, hakuja tai automaatioita

Jos GPU ei koskaan laskeudu kunnolla lepotilaan, maksat siitä jokaisena tuntina, et vain silloin kun malli oikeasti vastaa.

## Käytännön peukalosääntö: erottele laskenta-GPU ja näyttö-GPU, jos voit

Jos Arc-kortti on ostettu ennen kaikkea paikalliseen malliajoon, pitäisin nyrkkisääntönä tätä:

1. Jos kone voi olla kokonaan ilman näyttöä, tee siitä headless-palvelin.
2. Jos paikallinen näyttö tarvitaan vain hallintaan, käytä mieluummin emolevyn iGPU:ta, jos sellainen on käytettävissä.
3. Jos näyttö on pakko kytkeä Arc-korttiin, pidä kokoonpano mahdollisimman konservatiivisena: yksi näyttö ja mieluiten 60 Hz.

Tämä ei ole pelkkää teoretisointia. Intelin mukaan jo yli 60 Hz virkistystaajuus voi pakottaa GPU:n ajamaan korkeammilla kelloilla myös tyhjäkäynnissä, koska kortin on ylläpidettävä suurempaa pikseliläpivirtausta. Käytännössä siis "mukava 144 Hz työpöytä" ja "hiljainen 24/7 AI-laatikko" voivat vetää eri suuntiin.

## Entä jos kortti näyttää silti oudolta idlessä

Arc-koneessa kannattaa erottaa kaksi asiaa toisistaan:

- korkea todellinen tyhjäkäyntikulutus
- korkea muistitaajuus ilman suurta tehonkulutusta

Intelillä on tästä erillinen B580-ohje. Sen mukaan VRAM voi näkyä täydellä kellolla tyhjäkäynnissä, vaikka GPU itse idlaa alle 10 watin kulutuksessa oikein konfiguroituna. Toisin sanoen yksittäinen mittari ei vielä kerro koko totuutta. Jos siis seuraat vain muistitaajuutta, voit päätellä tilanteen turhan pessimistisesti.

Minusta tästä tulee hyvä käytännön toimintamalli:

- katso todellista seinästä tai ajurista näkyvää idle-tehoa
- tarkista montako näyttöä on kiinni ja millä taajuuksilla
- tarkista vasta sitten kellotaajuuslukemat

Muuten on helppo lähteä säätämään väärää asiaa.

## BIOS ja virransäästöasetukset eivät ole lisäbonus vaan osa kokoonpanoa

Intel ei jätä asiaa pelkkään "näin vain on" -tasoon, vaan suosittelee erikseen ASPM-asetusten kytkemistä päälle BIOSissa sekä PCIe Link State Power Managementin asettamista säästötilaan Windowsissa. Lisäksi Intelin uudempi Arc-työpöytäohje toistaa saman pääviestin: tyhjäkäyntikulutus riippuu yhä näyttökokoonpanosta, ja BIOSin ASPM/L1-substate-asetukset ovat oleellinen osa optimaalista idle-käytöstä.

Tämä on minusta hyödyllinen muistutus siitä, että paikallinen LLM-kone ei ole vain "GPU + malli". Se on kokonaisuus, jossa emolevyn BIOS-valinnat, näyttökaapelit ja käyttötapa voivat ratkaista yllättävän paljon enemmän kuin yksi pieni suorituskykyero benchmarkissa.

## Milloin näyttö Arc-kortissa on silti ihan järkevä

Näytön jättäminen Arc-korttiin voi olla aivan hyväksyttävä kompromissi, jos jokin näistä pitää paikkansa:

- kone ei ole päällä ympäri vuorokauden
- käytät sitä yhtä aikaa työasemana ja AI-koneena
- haluat mieluummin yksinkertaisen yhden koneen setupin kuin viimeiset watit takaisin
- näyttöjä on yksi ja virkistystaajuus maltillinen

Silloin kyse ei ole virheestä vaan tietoisesta kompromissista. Ongelmia alkaa tulla enemmän silloin, kun AI-koneen pitäisi olla hiljainen ja taloudellinen taustapalvelin, mutta siihen on jätetty kiinni yksi tai useampi korkean taajuuden näyttö vanhasta tottumuksesta.

## Oma johtopäätökseni harrastajalle

Jos rakentaisin Intel Arc -pohjaista paikallisen LLM:n kotipalvelinta tänään, yrittäisin pitää laskenta-GPU:n irti jatkuvasta näyttöajosta aina kun se on realistista. Käyttäisin hallintaan joko:

- SSH:ta
- selaimen kautta avattua käyttöliittymää
- integroitua grafiikkaa
- toista kevyttä hallintakonetta

Syy on yksinkertainen: **kun inference-kone idlaa suuren osan vuorokaudesta, jokainen turha wattikin toistuu koko ajan.** Silloin paras optimointi ei välttämättä ole uusi malli, uusi kvantisointi tai uusi ajuri, vaan se että sama GPU saa oikeasti levätä.

## Yhteenveto

Kannattaako näyttö jättää Intel Arc -korttiin, jos paikallinen LLM-kone on päällä 24/7? **Useimmiten ei, jos tavoite on hiljainen ja taloudellinen AI-palvelin.** Arc-korteilla näyttöjen määrä, resoluutio ja virkistystaajuus vaikuttavat suoraan siihen, pääseekö kortti kunnolla alhaiseen idle-tilaan. Siksi paras käytännön ratkaisu on usein pitää AI-GPU mahdollisimman puhtaasti laskentakäytössä ja siirtää näyttötoiminta muualle.

Jos näyttö pitää jättää Arc-korttiin, tee siitä tarkoituksella kevyt kompromissi: yksi näyttö, maltillinen taajuus, ASPM kuntoon. Muuten pieni käyttömukavuus voi muuttua hiljaiseksi 24/7 sähkörasitteeksi.

## Lähteet

- https://www.intel.com/content/www/us/en/support/articles/000092564/graphics.html
- https://www.intel.com/content/www/us/en/support/articles/000091128/graphics/intel-arc-dedicated-graphics-family.html
- https://www.intel.com/content/www/us/en/support/articles/000101330/graphics.html
