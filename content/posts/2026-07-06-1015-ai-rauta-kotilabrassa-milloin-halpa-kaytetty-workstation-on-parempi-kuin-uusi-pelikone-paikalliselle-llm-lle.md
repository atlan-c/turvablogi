---
title: "AI-rauta kotilabrassa: milloin halpa käytetty workstation on parempi kuin uusi pelikone paikalliselle LLM:lle?"
date: "2026-07-06T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-rauta kotilabrassa"
tags:
  - "AI-rauta"
  - "Workstation"
  - "GPU"
  - "Ollama"
  - "Paikalliset LLM:t"
---
Paikallista LLM-konetta kasaava harrastaja törmää ennemmin tai myöhemmin houkuttelevaan ajatukseen: **entä jos jättäisin uuden pelikoneen väliin ja ostaisin käytetyn workstationin, jossa on valmiiksi paljon PCIe-paikkoja, ECC-muistin tuki, järeä virtalähde ja yritysraudan runko?** Lyhyt käytännön vastaukseni on tämä: **halpa käytetty workstation on hyvä ostos silloin, kun tarvitset ennen kaikkea laajennettavuutta, paljon RAMia, monta levyä tai useamman raskaan lisäkortin ympärille rakennetun rungon. Jos taas tavoite on yksi moderni GPU, yksi paikallinen malli ja mahdollisimman vähän sivuongelmia, uusi tai uudehko pelikone on usein helpompi ja joskus myös nopeampi tie.**

Tärkein syy on aika arkinen. Käytetty workstation ostetaan yleensä alustan ominaisuuksien vuoksi, ei siksi että sen yksittäinen CPU-sukupolvi olisi väistämättä nopein paikalliseen inferenssiin. Jos et oikeasti tarvitse niitä workstationin etuja, saatat ostaa itsellesi ison, raskaan ja vanhemman rungon ilman että varsinainen LLM-kokemus paranee yhtä paljon kuin toivoit.

## Mikä käytetyssä workstationissa on oikeasti houkuttelevaa

Workstation-luokan koneet ovat kiinnostavia siksi, että ne on rakennettu aivan eri oletuksella kuin tavallinen pelikone. Niissä oletetaan, että käyttäjä tarvitsee paljon muistia, useita lisäkortteja, paljon tallennusta ja vakaata jatkuvaa käyttöä.

Dellin Precision 5820 on tästä hyvä esimerkki. Sen speksissä näkyy kaksi oikeaa PCIe x16 -paikkaa, yksi x16-paikka joka on sähköisesti x8, yksi x4-paikka sekä vaihtoehtona 425 W tai 950 W virtalähde. Samassa rungossa on myös useita tallennusvaihtoehtoja ja tuki useille NVMe-ratkaisuille. Lenovo ThinkStation P620 taas näyttää, miltä workstation-ajatus hieman uudemmalla alustalla näyttää: kuusi PCIe-paikkaa, joista neljä on PCIe 4.0 x16 ja kaksi x8, 1000 W virtalähde, ECC-muisti ja hyvin runsaat M.2- sekä levymahdollisuudet.

Harrastajalle tästä syntyy neljä konkreettista etua:

1. **Laajennettavuus on usein aidosti parempi.** Tilaa on useammalle GPU:lle, verkkokortille, HBA:lle tai M.2-adapterille ilman että koko alusta menee heti kompromissiksi.
2. **Muistikatto on korkeampi.** Jos tavoite on paljon järjestelmämuistia CPU-ajoon, hybridiin tai monen muun työkuorman rinnalle, workstation pääsee usein selvästi ylemmäs kuin tavallinen kuluttajakokoonpano.
3. **Virtalähde ja runko on mitoitettu raskaammalle käytölle.** Tämä ei tee koneesta automaattisesti hiljaista, mutta se tekee siitä usein uskottavamman pohjan isoille korteille kuin satunnainen halpa pelikotelopaketti.
4. **Yritysrauta on usein mekaanisesti käytännöllistä.** Huolto, levypaikat ja korttien vaihto ovat monessa mallissa suoraviivaisempia kuin näyttäväksi rakennetussa kuluttajakotelossa.

## Missä uusi pelikone voittaa yllättävän usein

Tämä on se kohta, jossa moni tekee väärän johtopäätöksen. Se, että workstationissa on enemmän kaikkea, ei tarkoita että se olisi automaattisesti paras paikalliseen LLM-käyttöön.

Ollaman dokumentaatio antaa tähän hyvän käytännön perussäännön kahdesta suunnasta. FAQ muistuttaa, että `ollama ps` näyttää suoraan, onko malli kokonaan GPU:ssa vai osittain CPU:n puolella. Context length -ohje taas sanoo suoraan, että parhaaseen suorituskykyyn kannattaa välttää mallin offloadausta CPU:lle. Tämä on tärkein ajatus koko vertailussa: **jos tavoitteesi on yksi moderni GPU ja malli, joka mahtuu sille kunnolla, workstationin ylimääräinen runsaus ei välttämättä tuo ratkaisevaa etua.**

Tällöin uusi tai uudehko pelikone voittaa usein näissä asioissa:

- saat uudemman alustan pienemmällä sähkön- ja lämmönkulutuksella
- saat usein helpomman BIOS-, ajuri- ja varaosapolun
- yksi tehokas kuluttaja-GPU mahtuu koneeseen ilman että koko rungon muu ikä alkaa näkyä
- kone on helpompi pitää hiljaisena työpöytä- tai kotilabrakäytössä

Jos siis käyttö näyttää tältä, kallistuisin useimmiten pelikoneeseen:

- yksi käyttäjä
- yksi pää-GPU
- yksi malli kerrallaan
- ei suunnitelmaa usealle lisäkortille
- ei tarvetta valtavalle RAM-määrälle tai suurelle levyarsenaalille

Tässä maailmassa tärkein asia ei ole se, montako fyysistä slottia rungossa on, vaan se että pää-GPU saa hyvän paikan, riittävästi VRAMia ja muun koneen pysymään pois tieltä.

## Milloin käytetty workstation on minusta selvästi järkevä ostos

Pidän halpaa käytettyä workstationia hyvänä ostona etenkin silloin, kun tiedät jo etukäteen että olet rakentamassa enemmän alustaa kuin vain "yksi näytönohjain ja Ollama".

### 1. Kun tarvitset paljon RAMia etkä vain vähän lisää FPS-ajattelua

Jos ajat mallia osittain CPU:lla, pidät samaan aikaan muuta raskasta kehitysympäristöä päällä tai haluat rakentaa koneen, jossa RAM ei lopu ensimmäiseen kunnianhimoiseen kokeiluun, workstation-alusta alkaa näyttää heti järkevämmältä. P620:n ECC-tuki ja suuri laajennettavuus ovat tässä oikeita etuja, eivät markkinointisanoja.

### 2. Kun tarvitset useita lisäkortteja tai paljon levyjä

Jos koneeseen tulee esimerkiksi 10 GbE -kortti, useita NVMe-adaptereita, toinen GPU tai muu erikoiskortti, workstationin kotelo ja kaistabudjetti ovat usein paljon helpompia hallita. Dellin 5820:n ja Lenovon P620:n kaltaiset rungot on suunniteltu juuri tällaiseen käyttöön.

### 3. Kun ostat käytettyä koko alustaa, et vain prosessoria

Tämä on tärkeä ero. Käytetty workstation voi olla erinomainen diili, jos saat samalla kertaa rungon, virtalähteen, emolevyn, paljon muistia ja hyvän laajennettavuuden. Jos taas ostat vanhan workstationin ja joudut heti vaihtamaan PSU:n, adapterit, kaapelit, jäähdytyksen ja puolet levyistä, "halpa löytö" alkaa muistuttaa kallista kiertotietä.

### 4. Kun hyväksyt sen, että työasemarauta on kompromissi myös arjessa

Moni yritysrunko on fyysisesti iso, painava ja tehty ennen kaikkea vakaaksi työjuhdaksi. Se voi olla täydellinen kotilabran nurkkaan, mutta huonompi olohuoneen hiljaiseksi yleiskoneeksi. Jos tämä ei haittaa, workstationista saa paljon enemmän iloa.

## Milloin käytetty workstation on huonompi idea kuin ensi silmäyksellä näyttää

Käytetty workstation muuttuu huonoksi ostokseksi yleensä silloin, kun ostaja kuvittelee saavansa samalla hinnalla sekä halvan rungon että modernin yhden GPU:n huippukoneen ilman sivuvaikutuksia.

Pidän sitä varoitusmerkkinä, jos jokin näistä toteutuu:

- ostat vanhan rungon mutta tavoite on silti yksi moderni suuri kuluttaja-GPU mahdollisimman vähällä säädöllä
- et oikeasti tarvitse ECC:tä, lisäslotteja tai suurta RAM-kattoa
- et tiedä etukäteen slotin sähköistä toteutusta, PSU-versiota tai GPU-virtakaapelien saatavuutta
- koneesta tulee päivittäinen työpöytäkone, jossa melu, koko ja idle-kulutus oikeasti haittaavat

Dellin 5820 on tässä hyvä muistutus. Se on aivan käyttökelpoinen runko, mutta sen dokumentaatio kertoo myös suoraan, että kaikki slotit eivät ole samanarvoisia: mukana on x8-, x4- ja x1-toteutuksia sekä eri PSU-vaihtoehtoja. Tämä ei tee koneesta huonoa. Se tarkoittaa vain, että käytetty workstation pitää ostaa speksitaulukko kädessä eikä pelkän "näyttää järeältä" -vaikutelman perusteella.

## Oma käytännön nyrkkisääntöni

Jos minulla olisi kaksi polkua paikallista LLM-konetta varten, valitsisin näin:

**Valitsisin käytetyn workstationin**, jos

- tarvitsen paljon RAMia tai ECC:tä
- suunnittelen useita lisäkortteja, levyjä tai myöhempää laajennusta
- hyväksyn vanhemman rungon koon, painon ja mahdollisen lisämelun
- saan paketin oikeasti hyvällä hinnalla kokonaisuutena

**Valitsisin uuden tai uudehkon pelikoneen**, jos

- haluan yhden mahdollisimman hyvän GPU:n ympärille yksinkertaisen paikallisen LLM-koneen
- tavoite on pitää malli kokonaan GPU:ssa
- arvostan helpompaa huollettavuutta, pienempää virrankulutusta ja vähemmän yllätyksiä
- en aio rakentaa korttifarmia vaan hyvän yhden käyttäjän työaseman

Toisin sanoen: **workstation on alustaongelman ratkaisu, pelikone on usein yhden GPU:n käyttökokemusongelman ratkaisu**.

## Tiivis johtopäätös

**Halpa käytetty workstation on parempi kuin uusi pelikone silloin, kun tarvitset ennen kaikkea laajennettavuutta, muistikattoa, useita kortteja tai paljon tallennusta.** Se ei ole automaattisesti paras valinta silloin, kun oikea tavoite on vain ajaa yksi paikallinen malli yhdellä modernilla GPU:lla mahdollisimman vaivattomasti. Siinä tehtävässä uusi tai uudehko pelikone osuu usein suoremmin maaliin.

Jos joutuisin antamaan vain yhden osto-ohjeen, se olisi tämä: **osta käytetty workstation vain, jos osaat nimetä vähintään kaksi sen alustatason etua, joita oikeasti tarvitset heti tai pian.** Jos et osaa, olet luultavasti ostamassa runkoa ominaisuuksilla, joista et saa paikallisessa LLM-ajossa tarpeeksi vastinetta.

## Lähteet

- https://docs.ollama.com/faq
- https://docs.ollama.com/context-length
- https://www.dell.com/support/manuals/en-us/oth-xlt5820/precision_5820_om_pub/card-slots?guid=guid-641b07b1-358e-40d2-a8c2-60ab826d654e&lang=en-us
- https://i.dell.com/sites/csdocuments/Shared-Content_data-Sheets_Documents/en/us/Precision-5820-Tower-Spec-Sheet.pdf
- https://psref.lenovo.com/syspool/Sys/PDF/ThinkStation/ThinkStation_P620/ThinkStation_P620_Spec.pdf
