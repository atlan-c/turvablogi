---
title: "Tarvitaanko PCIe 5.0 SSD paikalliseen LLM-koneeseen?"
date: "2026-04-03T10:15:00+03:00"
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
Paikallista LLM-konetta rakentaessa huomio menee yleensä ensin GPU:hun, sitten VRAMiin ja ehkä vasta sen jälkeen tallennustilaan. Silti juuri SSD on osa, josta moni kysyy nyt saman asian: **kannattaako paikalliseen AI-koneeseen ostaa kallis PCIe 5.0 NVMe-levy, vai riittääkö tavallinen PCIe 4.0 oikein hyvin?**

Lyhyt käytännön vastaus on tämä: **useimmille harrastajille ja kotilabran paikallisen LLM-ajon käyttäjille hyvä PCIe 4.0 NVMe riittää edelleen erinomaisesti.** PCIe 5.0 SSD voi nopeuttaa mallien siirtelyä, kylmäkäynnistyksiä ja suurten tiedostojen käsittelyä, mutta se ei yleensä ole se päivitys, joka näkyy selvimmin varsinaisessa tokennopeudessa. Jos budjetti on rajallinen, rahat kannattaa yleensä laittaa ensin VRAMiin, RAMiin, jäähdytykseen tai suurempaan levytilaan.

Oleellinen ero on yksinkertainen:

- **SSD vaikuttaa ennen kaikkea siihen, kuinka nopeasti malli saadaan levyltä käyttöön**
- **GPU, VRAM ja joskus CPU vaikuttavat enemmän siihen, kuinka nopeasti vastauksia oikeasti syntyy**

## Missä SSD oikeasti näkyy paikallisessa LLM-käytössä?

Aloittelija ajattelee helposti, että kaikki koneen nopeus kertautuu suoraan mallin käyttöön. Paikallisten LLM:ien kanssa näin ei kuitenkaan yleensä mene. Tallennus on tärkeä, mutta sen rooli on eri kuin GPU:n.

SSD näkyy arjessa erityisesti näissä tilanteissa:

- lataat uusia malleja verkosta koneelle
- avaat suuren GGUF-mallin ensimmäistä kertaa
- käynnistät palvelun tai työkalun uudelleen ja malli pitää ladata kylmästä tilasta
- säilytät useita kymmenien gigatavujen malleja samalla koneella
- siirrät malleja levyjen välillä tai pidät niitä ulkoisella tallennuksella

Sen sijaan **pitkän generoinnin aikana pullonkaula ei tavallisesti ole SSD**, vaan laskenta ja muistihierarkia. Kun malli on jo muistissä ja ajo pyörii GPU:lla tai CPU+GPU-hybridinä, nopeampi NVMe ei yleensä muuta käyttökokemusta yhtä paljon kuin moni toivoo.

## Miksi nopeampi levy ei yleensä tee tokeneista paljon nopeampia?

llama.cpp:n oma projektikuvaus kertoo suoraan kaksi asiaa, jotka auttavat hahmottamaan kokonaisuutta:

- projekti keskittyy paikalliseen inferenssiin laajalla laitekirjolla
- se tukee GPU-kiihdytystä ja myös **CPU+GPU-hybridiajoa**, kun malli on suurempi kuin käytettävissä oleva VRAM

Tämä on tärkeä vihje. Käytännön suorituskyky riippuu ennen kaikkea siitä, missä mallin painot ja laskenta elävät ajon aikana: GPU:ssa, CPU:ssa vai osittain molemmissa. SSD ei ole tässä ketjussa jatkuvasti töissä samalla tavalla kuin laskentapuoli.

Ollaman FAQ sanoo saman käytännönläheisemmin toisesta kulmasta. `ollama ps` näyttää, onko malli ladattu kokonaan GPU:lle, CPU:lle vai osittain molempiin. Toisin sanoen oleellinen kysymys ei ole pelkästään "kuinka nopea levy minulla on", vaan **päätyykö malli lopulta pyörimään GPU-muistissa, järjestelmämuistissa vai hybridinä**.

Kun malli on jo ladattu käyttöön, tokennopeutta määrää tavallisesti jokin näistä ennen SSD:tä:

- GPU:n laskentakyky
- käytettävissä oleva VRAM
- muistibandwidth GPU:n puolella
- CPU:n suorituskyky, jos ajetaan paljon prosessorilla
- konteksti-ikkunan koko ja kvantisointitaso

Siksi PCIe 5.0 SSD ei ole useimmille "LLM-nopeuspäivitys" vaan ennemmin **mukavuus- ja läpivirtausparannus**.

## Missä PCIe 5.0 SSD:stä on oikeasti hyötyä?

Tämä ei tarkoita, että Gen5-levy olisi turha. Sille on ihan järkeviä käyttötilanteita.

KIOXIAn PCIe 5.0 -materiaali muistuttaa perusfaktasta: PCIe 5.0 x4 -luokan SSD:t tähtäävät noin kaksinkertaiseen siirtokapasiteettiin PCIe 4.0:aan nähden. Käytännössä kuluttajalevyissä tämä näkyy usein niin, että hyvä PCIe 4.0 levy liikkuu karkeasti noin 7 GB/s luokassa, kun taas PCIe 5.0 levyt voivat yltää noin 10–14 GB/s lukemien maailmaan mallista riippuen.

Paikallisessa LLM-koneessa tästä on eniten hyötyä, jos jokin näistä pitää paikkansa:

- vaihtelet jatkuvasti isoja malleja edestakaisin
- boottaat tai käynnistelet mallipalvelun usein uudelleen
- rakennat konetta, jossa sama levy palvelee myös video-, data- tai muuta raskasta I/O-työtä
- pidät hyvin suurta mallikirjastoa ja arvostat nopeaa kopiointia, purkua ja siirtoa
- käytät useita rinnakkaisia työnkulkuja, joissa levyliikennettä tulee muutenkin paljon

Tällöin nopeampi levy voi tehdä koneesta "terävämmän" tuntuisen. Ero näkyy erityisesti silloin, kun siirretään tai avataan paljon kymmenien gigatavujen tiedostoja.

## Missä PCIe 4.0 on yleensä parempi valinta?

Useimmissa kotilabran LLM-koneissa parempi ostos on silti edelleen hyvä PCIe 4.0 NVMe. Siihen on viisi käytännön syytä:

- **hinta per teratavu on usein parempi**
- **lämmöntuotto on yleensä helpompi hallita**
- **emolevy- ja jäähdytysyhteensopivuus on mutkattomampi**
- **todellinen hyöty inferenssissä jää usein pieneksi**
- **isompi kapasiteetti voittaa usein huippunopeuden**

Tämä viimeinen kohta on harrastajalle tärkeä. Paikalliset mallit syövät levytilaa nopeasti. Yksi järkevä 2–4 teratavun PCIe 4.0 levy on usein hyödyllisempi kuin pienempi, kuumempi ja kalliimpi PCIe 5.0 levy, jos valinta pitää tehdä näiden välillä.

Käytännössä moni hyötyy enemmän tästä kuin Gen5:stä:

- enemmän tilaa useille GGUF-malleille
- enemmän tilaa embeddingeille, datasetille ja projektitiedostoille
- vähemmän tarvetta siivota malleja jatkuvasti pois
- tasaisempi lämpö- ja melukäytös pienessä kotelossa

## Entä kylmäkäynnistys, mallin vaihto ja mmap-tyylinen käyttö?

Juuri tässä SSD:n nopeus näkyy selkeimmin. Jos työnkulku on sellainen, että malli pitää saada levystä käyttöön usein, nopeampi NVMe voi lyhentää odottelua. Sama pätee silloin, jos kokeilet päivän aikana useita eri malleja tai kvantisointeja.

Mutta on hyvä erottaa kaksi eri tunnetta:

1. **"Malli tuli käyttöön nopeammin"**
2. **"Varsinainen generointi on nyt paljon nopeampaa"**

Ensimmäinen voi olla totta nopeammalla SSD:llä. Toinen ei useimmiten seuraa siitä automaattisesti.

Siksi ostospäätöstä kannattaa miettiä oman käytön kautta:

- jos ajat yleensä yhtä tai kahta mallia pitkissä sessioissa, Gen5-levyn hyöty jää helposti pieneksi
- jos taas hypit mallista toiseen, testaat paljon, rakennat benchmark- tai eval-ympäristöä tai pidät koneen yleisenä raskaan työn työasemana, Gen5 voi olla perusteltu

## Millainen tallennusratkaisu on järkevä paikalliseen AI-koneeseen juuri nyt?

Jos rakentaisin harrastajalle tai kotilabran käyttäjälle tasapainoisen paikallisen LLM-koneen, lähtisin tästä prioriteetista:

1. riittävästi VRAMia oikeaan malliluokkaan
2. riittävästi RAMia hybridiajoon ja muuhun työhön
3. kunnollinen jäähdytys ja virtapuoli
4. **vähintään hyvä PCIe 4.0 NVMe riittävällä kapasiteetilla**
5. vasta tämän jälkeen harkinta siitä, tuoko PCIe 5.0 oikeasti arvoa

Karkeana peukalosääntönä:

- **PCIe 4.0 2–4 TB** on useimmille paikallisen LLM-koneen sweet spot
- **PCIe 5.0** kannattaa, jos tiedät jo etukäteen että teet paljon raskasta levy-I/O:ta tai haluat muuten maksimoida kylmäkäynnistysten ja siirtojen nopeuden

## Yhteenveto

Jos kysymys kuuluu **"nopeuttaako PCIe 5.0 SSD paikallisen LLM:n vastaamista merkittävästi?"**, vastaus on yleensä: **ei siinä määrin kuin GPU-, VRAM- tai RAM-päivitys**.

Jos kysymys taas kuuluu **"tekeekö PCIe 5.0 SSD isojen mallien käsittelystä, kopioinnista ja kylmäkäynnistyksestä nopeampaa?"**, vastaus on: **kyllä, usein tekee**.

Siksi käytännöllinen ostosuositus on tylsä mutta hyödyllinen: **osta ensin riittävän suuri ja luotettava PCIe 4.0 NVMe, ja siirry PCIe 5.0:aan vasta jos tiedät hyötyväsi nimenomaan levy-I/O:sta.** Paikallisessa LLM-ajossa suurin pettymys syntyy usein siitä, että rahaa laitetaan väärään pullonkaulaan.

## Lähteet

- https://github.com/ggml-org/llama.cpp
- https://docs.ollama.com/faq
- https://americas.kioxia.com/en-us/business/news/2023/ssd-20231218-1.html
- https://apac.kioxia.com/en-apac/personal/news/2024/20241216-1.html
