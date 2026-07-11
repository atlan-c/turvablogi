---
title: "Kannattaako käytetty RTX 3080 10 Gt vai 12 Gt paikalliselle LLM:lle?"
date: "2026-07-11T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Paikalliset LLM:t"
  - "GPU"
  - "NVIDIA"
  - "RTX 3080"
  - "VRAM"
---
Käytettyä paikallisen LLM-koneen GPU:ta etsiessä vastaan tulee yhä sama kysymys: **jos tarjolla on RTX 3080 10 Gt ja 12 Gt, onko 12 gigan versio oikeasti selvästi parempi vai vain vähän eri speksilista?** Oma käytännön vastaukseni on tämä: **paikalliseen LLM-käyttöön ottaisin 12 Gt version lähes aina, jos hintaero ei karkaa typeräksi.** Syy ei ole ensisijaisesti se, että 12 Gt malli olisi valtavasti nopeampi laskennassa, vaan se että se antaa juuri sen verran lisää muistipäätä, että arki muuttuu useammin "toimii" kuin "melkein toimii".

Tämä ei silti tee 12 Gt RTX 3080:sta maagista AI-korttia. Se on yhä 12 Gt kortti. Se tarkoittaa, että se sopii paremmin kvantisoitujen pienten ja keskikokoisten mallien käyttöön kuin siihen, että ajat huolettomasti kaikkea mitä viikolla julkaistaan. Mutta jos vertailu on nimenomaan 10 Gt vastaan 12 Gt, lisämuisti on paikallisessa LLM-ajossa paljon hyödyllisempi ero kuin moni pelikäyttäjä ensi silmäyksellä arvaa.

## Mitä eroa korteissa oikeasti on

NVIDIAn omalla RTX 3080 -sivulla 12 Gt ja 10 Gt versiot näkyvät samassa taulukossa. 12 Gt mallissa on enemmän CUDA-ytimiä, enemmän muistia ja leveämpi muistiväylä kuin 10 Gt versiossa. Käytännön kannalta tärkeimmät rivit ovat kuitenkin nämä:

- 12 Gt vs 10 Gt muistia
- 384-bittinen vs 320-bittinen muistiväylä
- hieman enemmän laskentaresursseja 12 Gt mallissa

Pelikäytössä tästä voi syntyä "ihan mukava päivitys". Paikallisessa LLM-ajossa ero tuntuu usein rajummin, koska muistiraja on binäärinen: joko malli, konteksti ja välimuisti mahtuvat mukavasti yhdelle GPU:lle tai sitten eivät mahdu.

Juuri tässä kohtaa 2 Gt ei ole pieni kosmetiikka vaan noin 20 prosentin lisäys koko VRAM-budjettiin. Kun lähtötaso on vain 10 Gt, tuo lisätila voi ratkaista:

- mahtuuko malli kokonaan GPU:lle
- joudutko pienentämään kvantisointia enemmän kuin haluaisit
- paljonko kontekstia uskallat pitää päällä ennen kuin muisti kiristyy
- pysyykö ajo yhdellä GPU:lla vai valuuko se osittain järjestelmämuistin tai useamman kortin puolelle

## Miksi paikallisessa LLM-ajossa VRAM ratkaisee enemmän kuin pieni nopeusero

Ollaman FAQ sanoo tämän hyvin käytännöllisesti: jos malli mahtuu kokonaan yhdelle GPU:lle, se on tyypillisesti paras suorituskykypolku, koska PCIe-väylän yli siirrettävää dataa tulee vähemmän. Jos malli ei mahdu yhdelle kortille, se voidaan levittää useammalle GPU:lle, mutta yksittäisen harrastajan koneessa se on usein juuri se raja, jonka haluaisi välttää.

Siksi 10 Gt ja 12 Gt eivät ole paikallisessa LLM-käytössä "vain kaksi lähellä toisiaan olevaa vaihtoehtoa". Ne ovat usein:

- 10 Gt: tarkempi budjettikortti, jolla pitää ajatella kontekstia ja mallivalintaa tiukemmin
- 12 Gt: edelleen rajallinen, mutta paljon joustavampi käyttöluokka

Toinen tärkeä Ollaman huomio liittyy kontekstiin. Dokumentaatio sanoo suoraan, että Flash Attention voi pienentää muistinkulutusta kontekstin kasvaessa, ja että K/V-välimuistin kvantisointi voi tiputtaa välimuistin muistitarvetta noin puoleen tai jopa neljäsosaan oletus-`f16`-tilaan verrattuna. Tämä on hyödyllinen optimointi, mutta minä en käyttäisi sitä tekosyynä ostaa 10 Gt korttia, jos 12 Gt on saatavilla järkevällä lisähinnalla.

Syy on yksinkertainen: optimoinnit ovat parhaimmillaan joustovaraa, eivät korvike puuttuvalle peruskapasiteetille. On mukavampi käyttää Flash Attentionia ja KV-cache-kvantisointia lisätilan luomiseen kuin siihen, että muuten kone ei pysyisi pystyssä.

## Missä 10 Gt alkaa tuntua ahtaalta

10 Gt RTX 3080 ei ole hyödytön paikalliseen LLM-käyttöön. Se voi olla edelleen hyvä kortti, jos oma käyttö näyttää tältä:

- ajat enimmäkseen 7B- tai kevyitä 8B-luokan kvantisoituja malleja
- pidät kontekstin maltillisena
- käytät yhtä mallia kerrallaan
- hyväksyt sen, että kaikkea ei saa mahtumaan mukavasti GPU:lle

Ongelma alkaa, kun käyttötapa liukuu vähänkään kunnianhimoisemmaksi. Esimerkiksi nämä syövät muistipäätä nopeasti:

- pidempi konteksti
- useampi rinnakkainen pyyntö
- suurempi malli tai vähemmän aggressiivinen kvantisointi
- se, että haluat jättää VRAMiin vähän pelivaraa etkä aja aivan rajalla

Tässä maailmassa 10 Gt tuntuu usein kortilta, jossa jokainen lisätoive täytyy maksaa jollakin kompromissilla. 12 Gt ei poista kompromisseja, mutta se siirtää kipurajaa juuri sen verran, että käyttö on paljon rauhallisempaa.

## Missä 12 Gt on oikeasti parempi, eikä vain paperilla parempi

Pidän 12 Gt RTX 3080:aa järkevämpänä vaihtoehtona erityisesti silloin, jos tavoitteena on yksi näistä:

1. ajaa kvantisoituja 7B-14B-luokan malleja ilman että jokainen kontekstin nosto tuntuu heti muistipaniikkina
2. pitää yksi kortti käytössä pidempään ilman että se tuntuu heti vanhentuneelta
3. välttää tilanne, jossa hyvin pieni lisähinta säästettiin väärässä kohdassa

Tässä on mielestäni koko ostosäännön ydin: **jos kaksi muuten läheistä korttia eroavat toisistaan juuri VRAMissa, paikalliselle LLM-harrastajalle VRAM on yleensä se rivi, josta kannattaa maksaa ensin.**

12 Gt mallin leveämpi muistiväylä ja hieman suurempi ydinmäärä ovat tervetulleita plussia, mutta en tekisi ostopäätöstä niiden perusteella yksin. Tekisin sen sen perusteella, että 12 Gt on paikallisessa AI-ajossa terveempi minimiraja kuin 10 Gt.

## Milloin 10 Gt voi silti olla oikea ostos

Ottaisin 10 Gt mallin edelleen vakavaan harkintaan, jos kaikki nämä pitävät paikkansa:

- hintaero 12 Gt versioon on iso
- käyttö on selvästi kevyt ja rajattu
- tiedät jo valmiiksi, että seuraava päivitys tulee myöhemmin isompaan 16-24 Gt luokkaan
- haluat väliaikaisen CUDA-kortin etkä pääkorttia useaksi vuodeksi

Toisin sanoen 10 Gt voi olla hyvä "pääsen liikkeelle nyt" -kortti. En vain rakentaisi sen ympärille liian kunnianhimoista tarinaa. Se ei ole huono, mutta se on muistibudjetiltaan helpommin nurkkaan ajettava.

## Milloin 12 Gt:stä ei silti kannata maksaa mitä tahansa

Tässäkin kohtaa pitää varoa yliyksinkertaistusta. **12 Gt RTX 3080 ei ole automaattisesti parempi ostos kuin mikä tahansa muu vaihtoehto samalla rahalla.** Jos 12 Gt version hinta nousee lähelle käytettyä 16 Gt korttia tai selvästi järkevämpää uudemman sukupolven vaihtoehtoa, tilanne muuttuu.

Sanoisin tämän näin:

- maksa pieni tai kohtuullinen lisä 12 Gt:stä mieluummin kuin jää 10 Gt:hen
- älä maksa niin paljon lisää, että ohitat kokonaan seuraavan muistiluokan

Paikallisessa LLM-raudassa tärkein yksittäinen kysymys ei ole "kumpi 3080 on tehokkaampi", vaan **kummalla pääset vähemmällä muistisäädöllä siihen käyttöön, jota oikeasti aiot ajaa**.

## Oma käytännön suositukseni

Jos joku kysyisi minulta vain yhden lauseen vastauksen, sanoisin näin: **osta käytetyistä RTX 3080 -vaihtoehdoista 12 Gt versio aina kun lisähinta on järkevä, koska paikallisessa LLM-käytössä 2 Gt lisä-VRAM on usein arvokkaampi kuin sen pieni numerolta näyttävä ero antaa ymmärtää.**

Jos taas 12 Gt versio on selvästi kalliimpi, silloin pysähtyisin hetkeksi enkä juoksisi automaattisesti 10 Gt korttiin. Kysyisin ennemmin, pitäisikö koko ostos nostaa seuraavaan muistiluokkaan.

Käytännössä:

- **10 Gt RTX 3080** on kelvollinen budjettiratkaisu tarkasti rajattuun käyttöön
- **12 Gt RTX 3080** on parempi paikallisen LLM:n arkeen lähes kaikissa muissa tapauksissa

Se ei ole siksi, että 12 Gt olisi dramaattisesti nopeampi benchmarkeissa. Se on siksi, että paikallisessa AI-koneessa muistipää ratkaisee usein enemmän kuin pieni ero raakasuorituskyvyssä.

## Lähteet

- https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3080-3080ti/
- https://github.com/ollama/ollama/blob/main/docs/faq.mdx
- https://github.com/ollama/ollama/blob/main/docs/gpu.mdx
