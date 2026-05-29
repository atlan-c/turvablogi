---
title: "Kannattaako mini-PC:hen yksi 32 Gt RAM-kampa vai 2 x 16 Gt paikallista LLM:ää varten?"
date: "2026-05-16T10:15:00+03:00"
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
Moni yrittää parantaa pientä paikallista LLM-konetta ensimmäiseksi vaihtamalla mallia, säätämällä kvantisointia tai haaveilemalla isommasta GPU:sta. Yllättävän usein halvin oikea parannus on paljon arkisempi: yksi muistipalikka lisää, jotta kone siirtyy yksikanavaisesta muistista kaksikanavaiseen. Erityisesti mini-PC:issä, iGPU-koneissa ja CPU-painotteisessa `llama.cpp`-ajossa tämä voi tuntua enemmän kuin mikään pieni prosessoripäivitys.

Lyhyt käytännön sääntö on tämä: **jos paikallinen LLM-koneesi käyttää järjestelmämuistia mallin tai grafiikan työmuistina, varmista ensin että muisti toimii kahdella kanavalla ennen kuin käytät rahaa hienompiin optimointeihin**.

## Miksi juuri RAM-kanavat ratkaisevat näin paljon

Paikallinen LLM-inferenssi on usein muistipainotteista työtä. Johannes Gaesslerin `llama.cpp`-suorituskykykooste tiivistää tämän poikkeuksellisen suoraan: CPU-ajossa tärkein yksittäinen tekijä on muistien kaistanleveys, ja suorituskyky seuraa hyvin paljon muistitaajuutta ja käytettävissä olevaa muistiväylää. Samassa koosteessa todetaan myös, että jo muutama säie riittää syömään tavallisen dual-channel-muistin kaistan täyteen.

Tämä on käytännössä tärkeä havainto, koska se muuttaa ostojärjestyksen. Jos pullonkaula on muistikaista eikä raakaa laskentaa puutu ensimmäisenä, nopeampi CPU ei aina tunnu nopeammalta. Sen sijaan yksikanavaisen muistiasetuksen muuttaminen kaksikanavaiseksi voi nostaa mallin tokennopeutta ja ennen kaikkea tasoittaa ajoa.

## Mitä "dual channel" oikeasti tarkoittaa harrastajalle

Intel kuvaa oman muistiohjaimensa dokumentaatiossa, että kaksikanavainen symmetrinen tila antaa parhaan suorituskyvyn oikeissa sovelluksissa. Idea on yksinkertainen: kun molemmat muistikanavat ovat käytössä tasapainoisesti, muistipyyntöjä voidaan jakaa kanavien välillä eikä kaikki liikenne ruuhkaudu yhdelle reitille.

Käytännössä tämä tarkoittaa yleensä seuraavaa:

- yksi muistikampa = kone saattaa toimia vain single channel -tilassa
- kaksi saman kokoista kampaa oikeissa paikoissa = kone voi toimia aidosti dual channel -tilassa
- eripariset tai epäsymmetriset kampamäärät = osa muistista voi pudota hitaampaan tai sekamuotoiseen käyttöön

LLM-käytössä tämä ei ole pieni teoriadetalji. Jos ajat mallia CPU:lla tai integroidulla grafiikalla, sama järjestelmämuisti ruokkii suoraan sitä laskentaa, josta tokenit syntyvät.

## Mini-PC ja iGPU: tässä virhe näkyy kaikkein nopeimmin

Tornikoneessa, jossa on iso erillinen GPU omalla VRAMilla, huono RAM-kokoonpano ei välttämättä ole ensimmäinen asia jonka huomaat. Mini-PC:ssä tilanne on toinen. Kun kone nojaa integroidun grafiikan ja järjestelmämuistin yhdistelmään, käytettävä muistibudjetti ja muistikaista vaikuttavat samaan aikaan sekä mallin mahtumiseen että nopeuteen.

Siksi juuri pienissä koneissa yksi 32 Gt kampa voi olla huonompi valinta kuin kaksi 16 Gt kampaa, vaikka kokonaiskapasiteetti näyttäisi paperilla riittävältä. Kapasiteetti kyllä riittää paremmin, mutta muistikaista jää vajaaksi juuri siinä kohdassa, jossa LLM eniten sitä tarvitsee.

Minun mielestäni tämä on yksi yleisimmistä paikallisen AI-raudan ostovirheistä: ostetaan ensin "tarpeeksi gigatavuja" ja huomataan vasta myöhemmin, että käytännön vaste tuntuu silti tahmealta.

## Mistä tiedät että juuri tämä on pullonkaula

Tyypillisiä oireita ovat nämä:

- CPU tai iGPU näyttää kuormittuvan, mutta tokennopeus jää silti vaatimattomaksi
- mallin vaihto pienempään auttaa vain vähän
- promptin käsittely tuntuu erityisen hitaalta suhteessa koneen muuhun käyttöön
- koneessa on yksi iso SO-DIMM tai yksi pöytäkoneen DIMM, koska toinen paikka jätettiin "myöhempää varten"

Jos tämä osuu omaan setupiin, tarkistaisin ennen muuta kahta asiaa:

1. onko muistia fyysisesti yhdessä vai kahdessa kammassa
2. näkyykö BIOSissa tai käyttöjärjestelmässä dual-channel / interleaved / symmetric -tila

Linuxissa jo pelkkä `dmidecode`, emolevyn manuaali ja BIOSin muistinäyttö kertovat usein tarpeeksi. Tähän ei tarvitse arvailla.

## Kaikki kahden kamman kokoonpanot eivät ole yhtä hyviä

Tässä kohtaa tulee toinen käytännön ansa. Intelin tukiohje muistuttaa, että muistinopeus voi laskea, jos käytössä on useita DIMM-moduleita per kanava. Toisin sanoen enemmän kampoja ei automaattisesti tarkoita enemmän suorituskykyä, vaikka kanavia saataisiinkin täyteen.

Siksi hyvä perussääntö paikalliseen LLM-koneeseen on tämä:

- täytä ensin kaksi kanavaa siististi
- suosi kahta samanlaista kampaa neljän sekalaisen sijaan, jos alusta on kuluttajaluokan kone
- tarkista, ettei lisäkapasiteetti pudota muistitaajuutta tarpeettomasti

Monelle tämä tarkoittaa käytännössä sitä, että **2 x 16 Gt on parempi lähtökohta kuin 1 x 32 Gt**, ja **2 x 32 Gt on usein järkevämpi kuin 4 x 16 Gt**, jos tavoitteena on sekä kapasiteetti että hyvä taajuus eikä aivan maksimaalinen gigatavumäärä halvimmalla tavalla.

## Milloin kapasiteetti silti voittaa kaistan

On yksi tärkeä poikkeus: jos malli ei mahdu muuten lainkaan, lisäkapasiteetti voi olla tärkeämpi kuin optimaalinen kanava-asetelma. Käytännössä siis huonompikin muistiasettelu voi olla perusteltu, jos vaihtoehto on ettei ajo käynnisty ollenkaan.

Silti tämäkin kannattaa nähdä välivaiheena eikä ihannetilana. Paikallisen LLM-koneen mukavuus syntyy yleensä kahden ehdon yhdistelmästä:

- malli mahtuu järkevällä kvantisoinnilla
- muistikaistaa on tarpeeksi, ettei jokainen token odota muistia

Jos vain ensimmäinen toteutuu, kone kyllä "toimii", mutta käyttökokemus jää helposti sellaiseksi että harrastus alkaa tuntua raudan kanssa painimiselta.

## Mitä ostaisin käytännössä juuri nyt

Jos lähtisin korjaamaan hidasta mini-PC:tä tai pientä kotipalvelinta paikallisia LLM:iä varten, etenisin tässä järjestyksessä:

1. tarkista nykyinen muistikanavatila
2. jos kone on single channel, korjaa se ensin
3. vasta sen jälkeen arvioi riittääkö kapasiteetti nykyisille malleille
4. vasta viimeisenä mieti prosessori- tai alustapäivitystä

Tämä ei ole yhtä näyttävä päivitys kuin uusi GPU, mutta usein selvästi halvempi ja yllättävän tehokas. Juuri siksi se on hyvä ensimmäinen liike: se poistaa yhden kaikkein tavallisimmista itse aiheutetuista pullonkauloista ennen kuin alat optimoida mitään hienompaa.

## Yhteenveto

Jos paikallinen LLM-koneesi on pieni, integroidulla grafiikalla varustettu tai muuten järjestelmämuistiin nojaava, kaksi oikein asennettua RAM-kampaa voi olla tärkeämpi päivitys kuin seuraava prosessorisukupolvi. LLM ei välitä vain siitä paljonko muistia on, vaan siitä kuinka nopeasti sitä muistia voidaan syöttää laskennalle.

Siksi sanoisin tämän aika suoraan: **älä osta paikalliseen LLM-mini-PC:hen yhtä isoa kampaa vain siksi, että toinen paikka jää joskus myöhemmin käyttöön.** Monessa oikeassa kokoonpanossa maksat sillä päätöksellä suorituskykyä joka päivä.

## Lähteet

- https://johannesgaessler.github.io/llamacpp_performance
- https://edc.intel.com/content/www/us/en/design/products/platforms/details/raptor-lake-s/13th-generation-core-processors-datasheet-volume-1-of-2/003/system-memory-controller-organization-mode-ddr4-5-only/
- https://www.intel.com/content/www/us/en/support/articles/000095111/processors/intel-core-processors.html
