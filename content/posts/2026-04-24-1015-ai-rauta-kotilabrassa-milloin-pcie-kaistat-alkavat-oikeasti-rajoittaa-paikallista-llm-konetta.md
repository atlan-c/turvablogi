---
title: "AI-rauta kotilabrassa: milloin PCIe-kaistat alkavat oikeasti rajoittaa paikallista LLM-konetta?"
date: "2026-04-24T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "GPU"
  - "Hardware"
  - "Homelab"
  - "Troubleshooting"
---
Paikallista LLM-konetta rakentaessa moni jumittuu tuijottamaan vain GPU:n nimeä ja VRAM-määrää. Se on ymmärrettävää, mutta samalla yksi käytännön pullonkaula jää helposti taka-alalle: PCIe-kaistat. Ne eivät yleensä ole ensimmäinen ongelma, mutta tietyssä pisteessä niistä tulee hyvin konkreettinen syy siihen, miksi laitteisto ei käyttäydy niin hyvin kuin speksitaulukko lupaisi.

Lyhyt käytännön vastaus on tämä: yhden GPU:n harrastekoneessa PCIe-kaistat eivät yleensä ole ensimmäinen LLM-pullonkaula. Kun alat käyttää useita kortteja, NVMe-levyjä, lisäkortteja tai kapeammaksi pudotettuja slotteja, asia muuttuu nopeasti tärkeäksi.

## Mitä PCIe-kaistat oikeastaan ovat

PCI Express on sisäinen nopea väylästandardi, jolla tietokoneen laitteet kuten GPU:t, verkkokortit ja SSD:t keskustelevat keskenään. Wikipedia tiivistää olennaisen hyvin: yhteys rakentuu laneista eli kaistoista, ja laite voi käyttää yhtä tai useampaa kaistaa tarpeensa mukaan. Kaistojen määrä ei siis ole koriste, vaan suora osa sitä kuinka leveä yhteys laitteen ja muun järjestelmän välillä on.

Käytännössä juuri tästä syntyy klassinen kotilabran yllätys: emolevyssä voi olla fyysisesti pitkä x16-paikka, mutta sähköisesti se voikin toimia vain x4-tilassa. Paperilla GPU on "asennettu x16-slottiin", mutta todellinen väylä on paljon kapeampi.

## Milloin tämä ei yleensä haittaa paljon

Jos ajat yhtä paikallista mallia yhdellä GPU:lla ja malli mahtuu hyvin VRAMiin, PCIe ei yleensä ole suurin huoli. Silloin raskain työ tapahtuu kortin sisällä, eikä dataa tarvitse jatkuvasti siirtää edestakaisin järjestelmämuistin ja GPU:n välillä.

Tällaisessa koneessa tärkeämpiä asioita ovat usein:

- riittävä VRAM
- tarpeeksi järjestelmä-RAMia
- nopea SSD mallien lataukseen
- hyvä jäähdytys ja vakaa virtapuoli

Siksi on helppo kuulla neuvo "PCIe ei juuri vaikuta LLM:iin". Se on usein riittävän totta, mutta vain tässä rajatussa tapauksessa.

## Milloin PCIe-kaistat alkavat oikeasti sattua

Ongelmat alkavat näkyä, kun data liikkuu paljon enemmän kuin yhden kortin tavallisessa inferenssissä. Tyypillisiä tilanteita ovat:

1. käytössä on useita GPU-kortteja
2. osa mallista tai KV-cachesta valuu järjestelmämuistiin
3. koneessa on useita nopeita NVMe-levyjä samalla kaistabudjetilla
4. emolevy tai CPU jakaa kaistoja niin, että GPU putoaa x16:sta x8:aan tai x4:ään
5. samaa konetta käytetään sekä AI-ajoihin että muihin I/O-raskaisiin tehtäviin

Tällöin pullonkaula ei ole enää vain laskenta vaan myös datan kulkeminen. Jos GPU joutuu odottamaan syötettä tai järjestelmä jonglööraa kaistoja SSD:n, verkon ja useiden lisäkorttien välillä, käytännön suorituskyky kärsii vaikka itse komponentit näyttäisivät vahvoilta.

## Miksi tämä näkyy erityisesti "säästeliäissä" rakennelmissa

Kotilabroissa houkutus on usein suuri rakentaa yksi monikäyttöinen kone, johon tungetaan:

- yksi tai kaksi GPU:ta
- useita NVMe-levyjä
- 10 GbE -verkkokortti
- ehkä vielä jokin HBA tai capture-kortti

Tässä vaiheessa kaistoista tulee budjetti. Kaikkea ei saa täydellä leveydellä yhtä aikaa, ellei alusta oikeasti tue sitä. Jos pohjana on kuluttajatason prosessori ja emolevy, kompromissit alkavat näkyä nopeammin kuin moni odottaa.

Siksi hyvä kysymys ei ole vain "paljonko VRAMia saan", vaan myös "mikä jakaa kaistat ja kuinka pahasti".

## Oma käytännön nyrkkisääntö

Minun käytännön sääntöni olisi tämä:

- jos rakennat yhden GPU:n LLM-koneen, älä stressaa PCIe:tä ensimmäisenä
- jos rakennat kahden GPU:n tai monen nopean lisälaitteen konetta, tarkista kaistajako ennen ostoksia
- jos emolevy tarjoaa fyysisen x16-slotin, varmista myös sen sähköinen toteutus
- jos tarkoitus on ajaa paljon offloadia tai monikorttisia kokeiluja, kaistojen merkitys kasvaa nopeasti

Tämä ei ole kaikkein seksikkäin osa laitevalintaa, mutta juuri tästä syntyy paljon "miksi tämä ei tunnu niin nopealta kuin piti" -tyyppisiä pettymyksiä.

## Yhteenveto

Milloin PCIe-kaistat alkavat oikeasti rajoittaa paikallista LLM-konetta? Yhden GPU:n peruskäytössä usein vasta myöhään. Monikorttisissa, I/O-raskaissa tai kompromissiemolevyyn rakennetuissa koneissa paljon aiemmin kuin moni arvaa.

Jos siis rakennat yksinkertaista inferenssikonetta, priorisoi ensin VRAM, RAM ja vakaus. Jos taas suunnittelet laajenevaa AI-työasemaa tai kotipalvelinta, PCIe-kaistat kannattaa lukea osaksi budjettia samalla vakavuudella kuin watit ja gigatavut.

## Lähteet

- https://en.wikipedia.org/wiki/PCI_Express
- https://en.wikipedia.org/wiki/Memory-mapped_I/O_and_port-mapped_I/O
