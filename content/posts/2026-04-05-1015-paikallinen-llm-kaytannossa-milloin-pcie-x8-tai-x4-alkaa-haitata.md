---
title: "Paikallinen LLM käytännössä: milloin PCIe x8 tai x4 alkaa oikeasti haitata?"
date: "2026-04-05T10:15:00+03:00"
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
Paikallista LLM-konetta rakentaessa moni käyttää käytettyä rautaa, riser-kortteja, toista PCIe-slottia tai emolevyä, jossa kaikki slotit eivät kulje täydellä x16-kaistalla. Siksi vastaan tulee nopeasti käytännön kysymys: **haittaako PCIe x8 tai jopa x4 paikallista LLM-ajoa oikeasti, vai onko tämä lähinnä paperilla iso mutta arjessa pieni ongelma?**

Lyhyt vastaus on tämä: **jos malli mahtuu hyvin GPU:n VRAMiin ja ajo pysyy siellä, PCIe-kaistojen kaventuminen ei yleensä ole ensimmäinen pullonkaula. Mutta jos nojaat paljon CPU+GPU-hybridiajoon, pitkään kontekstiin tai muuhun offloadiin, PCIe alkaa merkitä paljon enemmän.**

Toisin sanoen kysymys ei ole vain siitä, onko kortti x16-, x8- vai x4-slotissa. Oleellisempi kysymys on tämä:

**kuinka usein inferenssin aikana joudutaan liikuttelemaan tavaraa GPU:n ja muun muistin välillä?**

Jos vastaus on “vähän”, pienempi PCIe ei yleensä pilaa harrastelabraa. Jos vastaus on “jatkuvasti”, väylästä voi tulla yllättävän nopeasti juuri se osa, joka tekee koko koneesta tahmean.

## Miksi tästä kysytään nyt niin paljon?

Käytännön syy on yksinkertainen. Paikallisia LLM-koneita rakennetaan usein kompromisseilla:

- käytetty GPU tulee halvalla, mutta emolevyssä ei ole täyttä x16-paikkaa kaikille korteille
- kotipalvelimessa GPU päätyy toiseen slottiin, joka toimii sähköisesti x8- tai x4-tilassa
- bifurcation, riserit ja adapterit mahdollistavat enemmän laitteita, mutta eivät aina täydellä kaistalla
- osa malleista mahtuu VRAMiin vain osittain, jolloin CPU+GPU-hybridiajo alkaa kiinnostaa

Silloin aloittelija helposti ajattelee asian liian mustavalkoisesti:

- joko “aina pitää olla x16 tai kaikki on pilalla”
- tai “PCIe:llä ei ole mitään väliä, koska inferenssi on vain GPU-laskentaa”

Todellisuus on keskellä. **PCIe ei ole yleensä tärkein osa silloin, kun malli istuu nätisti VRAMissa, mutta siitä tulee nopeasti tärkeämpi, jos ajo vaatii jatkuvaa siirtoliikennettä.**

## Mitä llama.cpp ja Ollama kertovat käytännössä?

llama.cpp:n oma projektikuvaus korostaa kahta kohtaa, jotka ratkaisevat tämän kysymyksen melkein suoraan:

- projekti tukee kvantisointia, joka pienentää muistitarvetta
- projekti tukee **CPU+GPU-hybrid inference** -ajoa, jotta myös VRAMia suurempia malleja voidaan kiihdyttää osittain GPU:lla

Tämä on hyvä uutinen harrastajalle, koska kaikki ei kaadu siihen, ettei koko malli mahdu yhdelle näytönohjaimelle. Mutta samalla siitä seuraa tärkeä käytännön oivallus: **mitä enemmän nojaat hybridiajoon, sitä vähemmän voit teeskennellä, ettei väylällä ole merkitystä.**

Ollaman FAQ kuvaa saman asian vielä käytännöllisemmin. `ollama ps` näyttää, onko malli:

- `100% GPU`
- `100% CPU`
- tai osittain molemmissa, esimerkiksi `48%/52% CPU/GPU`

Tämä on hyödyllinen muistutus siitä, että paikallinen LLM-ajo ei ole binäärinen “GPU tai ei mitään” -tilanne. Kun malli tai sen työkuorma jakautuu GPU:n ja järjestelmämuistin välille, myös niiden välinen yhteys alkaa vaikuttaa enemmän käyttökokemukseen.

## Milloin PCIe x8 ei yleensä ole iso ongelma?

Useimmille harrastajille **x8 ei ole automaattisesti punainen lippu**. Se on usein täysin hyväksyttävä kompromissi, jos käyttö näyttää enimmäkseen tältä:

- ajat yhtä mallia kerrallaan
- valitset kvantisoinnin niin, että malli mahtuu hyvin GPU:lle
- et pyri jatkuvasti maksimoimaan konteksti-ikkunaa
- et tee raskasta monen käyttäjän palvelua tai jatkuvaa rinnakkaiskuormaa
- et käytä kokoonpanoa, jossa iso osa mallista tai välimuisteista elää jatkuvasti CPU-muistissa

Tällöin tärkein pullonkaula on usein edelleen jokin näistä ennen PCIe:tä:

- GPU:n laskentateho
- käytettävissä oleva VRAM
- muistibandwidth GPU:n sisällä
- mallin koko ja kvantisointitaso

Käytännössä tämä tarkoittaa, että jos ajat esimerkiksi kohtalaisen kokoista kvantisoitua mallia yhdellä GPU:lla ja pidät työn “VRAM-painotteisena”, siirtyminen x16:sta x8:aan ei välttämättä tunnu arjessa juuri missään.

## Milloin PCIe alkaa oikeasti näkyä?

PCIe alkaa kiinnostaa aivan eri tavalla, kun käyttö ei enää pysy siististi yhden GPU:n sisällä.

Tässä kohtaa ongelma ei yleensä ole pelkkä mallin alkuperäinen lataus levyllä, vaan **inferenssin aikainen siirtoliikenne**. Tuore tutkimus KV-offloadingista sanoo tämän aika suoraan: kun KV-välimuistia offloadataan CPU:n DRAMiin, **PCIe-kaistan rajoitukset voivat muodostua vakavaksi pullonkaulaksi**, ja heidän mittauksissaan valtaosa latenssista saattoi kulua siirtoihin eikä laskentaan.

Tämä näkyy käytännössä etenkin silloin, jos jokin näistä pitää paikkansa:

- malli ei mahdu kokonaan VRAMiin ja osa työstä asuu jatkuvasti järjestelmämuistissa
- käytät pitkää konteksti-ikkunaa, jolloin KV-cache kasvaa
- ajat useampaa raskasta pyyntöä rinnakkain
- yrität puristaa liian ison mallin liian pieneen GPU:hun “kyllä tämä jotenkin pyörii” -periaatteella
- käytössä on erityisen kapea slotti, kuten x4, eikä vain x8

Tässä tilanteessa pienempi PCIe ei ole enää vain teoreettinen speksi. Se voi näkyä konkreettisesti näin:

- ensimmäinen token tulee hitaammin
- vastaus etenee nykien
- GPU:n käyttöaste näyttää yllättävän matalalta
- kone tuntuu oudosti “jumittavalta”, vaikka GPU itsessään ei ole täydessä rasituksessa

Tämä on juuri se tilanne, jossa moni alkaa syyttää mallia, kvantisointia tai ohjelmaa, vaikka todellinen ongelma onkin se, että dataa siirtyy väärässä paikassa liian hitaasti.

## x8 vastaan x4: käytännön ero on isompi kuin x16 vastaan x8

Jos pitäisi antaa yksi käytännön nyrkkisääntö, se olisi tämä:

**x16 → x8 on usein siedettävä kompromissi, mutta x8 → x4 on jo paljon helpommin aidosti tuntuva riski.**

En sano tätä siksi, että x4 olisi aina käyttökelvoton. Kevyessä tai täysin VRAMiin mahtuvassa ajossa sekin voi toimia. Mutta jos suunnitelma perustuu siihen, että ajat vähän liian isoa mallia, pidät pitkää kontekstia ja hyväksyt hybridiajon, x4 jättää paljon vähemmän pelivaraa.

Siksi käytettyä serveriä tai työasemaa rakentaessa kannattaa tarkistaa kolme asiaa ennen ostoa:

- mikä on slotin **sähköinen** kaistamäärä, ei vain mekaaninen koko
- tippuuko pää-GPU x8-tilaan, jos toinen slotti tai NVMe-paikka on käytössä
- onko tarkoitus ajaa malleja, jotka mahtuvat aidosti VRAMiin, vai rakennatko koko setin offload-kompromissin päälle

Viimeinen kysymys ratkaisee yleensä koko asian.

## Yleinen väärinkäsitys: “malli on GPU:lla, joten PCIe ei enää merkitse mitään”

Tämä pitää vain osittain paikkansa.

Jos malli on todella käytännössä kokonaan GPU:lla ja työkuorma pysyy siellä, väite on usein riittävän tosi. Mutta heti kun puhutaan osittaisesta CPU/GPU-jaosta, pitkästä kontekstista tai cache-offloadista, ajon aikana tapahtuu muutakin kuin yksi mallin lataus alkuun.

Silloin PCIe ei ole enää vain “käynnistysvaiheen putki”, vaan osa järjestelmän jatkuvaa muistihierarkiaa.

Tämän takia sama kone voi käyttäytyä kahdella mallilla aivan eri tavoin:

- pienempi malli tuntuu nopealta ja sulavalta myös x8-slotissa
- vähän liian iso malli tuntuu tahmealta, vaikka GPU on paperilla hyvä

Moni tulkitsee tämän niin, että “isompi malli on vain raskaampi”. Sekin on totta, mutta usein samalla **ajotapa muuttuu laskentapainotteisesta siirtopainotteiseksi**. Juuri siinä PCIe alkaa näkyä.

## Mitä tämä tarkoittaa ostopäätöksessä?

Jos rakennat paikallista LLM-konetta käytännön budjetilla, etenisin näin.

### x8 riittää yleensä hyvin, jos

- tavoittelet malleja, jotka mahtuvat järkevästi GPU:n VRAMiin
- käytät kvantisoituja malleja etkä väkisin liian suuria
- haluat yhden hyvän paikallisen avustajan tai koodiapurin
- rakennat käytetystä raudasta ja tarvitset kompromissin, joka ei oikeasti pilaa arkea

### x4 voi olla ok, jos

- käyttö on kevyehköä
- mallit ovat pieniä tai hyvin kvantisoituja
- ymmärrät jo etukäteen, että et optimoi kaikkein raskainta hybridiajoa varten
- kyse on enemmän kokeilu- tai sivukoneesta kuin pääasiallisesta AI-työasemasta

### täysi x16 tai muuten väljempi alusta kannattaa priorisoida, jos

- haluat kasvattaa mallikokoa myöhemmin
- tiedät jo nyt tarvitsevasi hybridiajoa
- ajat pitkiä konteksteja tai useampia töitä rinnakkain
- rakennat koneesta oikeaa päivittäistä työvälinettä etkä pelkkää testipenkkiä

Käytännössä tämä on sama neuvo kuin monessa muussakin AI-raudassa: **älä optimoi vain siihen, mikä juuri ja juuri toimii tänään, jos tiedät käyttötavan kasvavan pian.**

## Yksinkertainen testi omalle koneelle

Jos et halua arvailla, helpoin tapa arvioida omaa setupia on tämä:

1. aja yksi malli, joka mahtuu selvästi GPU:lle
2. aja toinen, joka menee osittain CPU/GPU-jaolle
3. vertaa sekä tuntumaa että mittareita

Ollaman `ollama ps` auttaa näkemään, muuttuuko ajotapa oikeasti CPU/GPU-sekoitukseksi. Jos suorituskyky romahtaa juuri siinä kohdassa, ongelma ei todennäköisesti ole vain “malli on isompi”, vaan myös se, että nyt väylä ja muu muistihierarkia joutuvat töihin aivan eri tavalla.

Tämä on hyödyllisempi testi kuin pelkkä speksitaulukon tuijotus.

## Oma käytännön johtopäätökseni

Jos joku kysyy minulta yksinkertaista ostosuositusta, sanoisin näin:

- **älä hylkää muuten hyvää paikallista LLM-konetta vain siksi, että GPU toimii x8-tilassa**
- **ole paljon varovaisempi, jos suunnitelma nojaa x4-kaistaan ja osittaiseen offloadiin**
- **priorisoi ensin VRAM, järkevä mallikoko ja hyvä kokonaisbalanssi ennen kuin alat jahdata täydellistä PCIe-speksiä**

Toisin sanoen **x8 on usein kompromissi, x4 on paljon useammin varoitusmerkki**.

Jos työ pysyy pääosin GPU:ssa, et todennäköisesti huomaa x8-ratkaisua juuri lainkaan. Jos taas rakennat koneen sen varaan, että iso osa työstä vuotaa jatkuvasti CPU-muistiin, PCIe-kaistoista tulee paljon tärkeämpiä kuin moni toivoisi.

## Lähteet

- https://github.com/ggml-org/llama.cpp
- https://docs.ollama.com/faq
- https://arxiv.org/abs/2601.19910
