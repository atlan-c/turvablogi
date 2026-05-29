---
title: "Kannattaako PCIe 4.0 paikalliselle LLM-koneelle, jos GPU toimii vain x4- tai x8-nopeudella?"
date: "2026-03-23T10:15:00+02:00"
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
Paikallista LLM-konetta rakentaessa huomio menee helposti VRAMiin, mallikokoon ja kvantisointiin. Samaan aikaan moni harrastaja miettii, pilaako hidas PCIe-yhteys koko projektin: entä jos näytönohjain toimii vain x8-nopeudella, vanhemmalla PCIe 3.0 -alustalla tai pahimmillaan x4-adapterin kautta? Käytännön vastaus on lohdullinen: **täysin VRAMiin mahtuvassa ajossa PCIe ei yleensä ole ensimmäinen pullonkaula, mutta osittaisessa offloadissa, eGPU-ratkaisuissa ja mallia jatkuvasti siirtelevissä työnkuluissa se alkaa näkyä nopeasti**.

Toisin sanoen PCIe-kaistoihin kannattaa suhtautua samalla tavalla kuin moneen muuhunkin AI-raudan yksityiskohtaan: ne eivät yksin ratkaise kaikkea, mutta väärässä paikassa ne voivat tehdä muuten hyvästä kokoonpanosta turhauttavan.

## Mitä PCIe x4, x8 ja x16 oikeasti tarkoittavat?

PCIe on yhteys emolevyn ja lisäkortin välillä. Kaistat eli lanes määrittävät, kuinka paljon dataa linkki voi siirtää. Wikipedia ja PCI-SIG-pohjaiset yhteenvetotaulukot kertovat saman perusasian: PCIe 3.0 x16 tarjoaa noin 16 GB/s yksisuuntaista kaistaa, PCIe 4.0 x16 noin 32 GB/s, PCIe 3.0 x8 noin 8 GB/s ja PCIe 3.0 x4 noin 4 GB/s. PCIe 4.0 kaksinkertaistaa kaistan samaan kaistamäärään verrattuna.

Käytännössä siis nämä kaksi asiaa vaikuttavat samaan aikaan:

- **sukupolvi**: PCIe 3.0, 4.0, 5.0
- **linkin leveys**: x4, x8, x16

Siksi PCIe 4.0 x4 ja PCIe 3.0 x8 ovat käytännössä samassa suuruusluokassa. Tämä on tärkeä huomio, jos käytössä on esimerkiksi M.2–PCIe-adapteri, bifurkaatio, pieni kotipalvelinrunko tai emolevy, jossa toinen pitkä fyysinen slotti ei oikeasti tarjoa täyttä x16-linkkiä.

## Miksi PCIe ei aina hidasta tokennopeutta niin paljon kuin luulisi?

Paikallisen LLM:n ajossa raskain osa tapahtuu yleensä GPU:n omassa muistissa ja laskentayksiköissä, jos malli mahtuu sinne kunnolla. Kun mallin painot ovat jo VRAMissa ja generointi pyörii pääosin GPU:lla, PCIe-linkkiä ei välttämättä käytetä jatkuvasti niin paljon, että x16 → x8 olisi heti katastrofi.

Siksi moni harrastaja yllättyy siitä, ettei pelkkä "vanha PCIe 3.0 -alusta" automaattisesti tee kokoonpanosta huonoa. Jos ajat yhtä mallia paikallisesti, pidät sen muistissa ja kaikki olennaiset tensorit mahtuvat näytönohjaimelle, **VRAMin määrä, mallin kvantisointi ja jäähdytys vaikuttavat usein enemmän kuin se, onko linkki juuri 3.0 vai 4.0**.

## Missä hitaampi PCIe-yhteys sitten sattuu oikeasti?

Hitaampi PCIe näkyy käytännössä etenkin kolmessa tilanteessa.

### 1. Osa mallista jää RAMiin tai CPU:lle

llama.cpp-yhteisön käytännön keskusteluissa toistuu sama havainto: jos kaikkia kerroksia ei offloadata GPU:lle, loput jäävät CPU:n ja RAMin puolelle. Se ei tarkoita vain suurempaa RAM-kulutusta, vaan myös sitä, että työ ei pysy siististi yhdellä muistialueella. Tällöin hitaampi linkki voi alkaa näkyä enemmän, koska dataa ja työn vaiheita joudutaan jakamaan kahden maailman välillä.

Tämä on tärkeä ero aloittelijalle. Pullonkaula ei synny välttämättä siksi, että "PCIe on hidas", vaan siksi että **kokoonpano pakottaa mallin osittaiseen kompromissiin**. Jos malli ei mahdu kunnolla GPU:lle, hitaampi linkki vain pahentaa jo valmiiksi epätäydellistä tilannetta.

### 2. Promptin syöttö ja mallin lataus tuntuvat hitaammilta kuin itse generointi

Moni katsoo vain loppupään tokeneita sekunnissa. Se on virhe. Käytännön käyttökokemus muodostuu myös siitä, kuinka nopeasti malli käynnistyy, kuinka nopeasti pitkä prompti tai dokumentti menee sisään ja kuinka paljon työ tuntuu "odottelulta" ennen ensimmäistä tokenia.

Juuri tässä hitaampi PCIe voi näkyä enemmän kuin lyhyessä chat-vastauksessa. Jos työnkulussa:

- vaihdat malleja usein
- syötät pitkiä konteksteja
- ajat dokumentteja tai RAG-putkia sarjassa
- käytät osittaista GPU-offloadia

niin x4-linkki tai vanha alusta voi tuntua selvästi kankeammalta, vaikka puhdas generointinopeus ei romahtaisi yhtä dramaattisesti.

### 3. eGPU-, adapteri- ja kotipalvelinviritykset

Kotilabrassa yleisiä kompromisseja ovat OCuLink-, M.2- ja muut adapteriratkaisut, joissa fyysisesti suuri GPU ei saakaan käyttöön täyttä x16-linkkiä. Näissä kokoonpanoissa voi silti rakentaa toimivan paikallisen LLM-koneen, mutta silloin pitää ymmärtää mitä ostaa.

Jos tavoitteena on yksi selvästi VRAMiin mahtuva malli ja satunnainen oma käyttö, tällainen viritys voi olla täysin järkevä. Jos taas tavoitteena on maksimoida vasteaika, ajaa paljon pitkiä prompteja tai käyttää rautaa monen käyttäjän palveluna, linkkirajoitus alkaa tuntua paljon selvemmin.

## Milloin PCIe 4.0 on oikeasti rahan arvoinen?

PCIe 4.0:sta on eniten hyötyä silloin, kun se poistaa selkeän kompromissin:

- GPU toimii muuten vain x4-linkillä ja 4.0 nostaa käytännön kaistan siedettäväksi
- käytät NVMe-levyjä ja GPU:ta samalla alustalla niin, että kaistajako on muutenkin tiukka
- ajat osittaista offloadia, jossa liike RAMin ja GPU:n välillä on todellinen osa työkuormaa
- rakennat pidempään käyttöön jäävää konetta, johon voi tulla myöhemmin tehokkaampi GPU

Sen sijaan PCIe 4.0 ei ole automaattisesti tärkein päivitys, jos:

- nykyinen suurin ongelma on liian pieni VRAM
- käytät jo yhtä mallia, joka mahtuu hyvin GPU:lle
- valinta on "enemmän VRAMia PCIe 3.0 -alustalla" vastaan "vähemmän VRAMia mutta uudempi PCIe"

Useimmiten harrastajan kannattaa ottaa ensin enemmän käyttökelpoista muistia kuin paperilla hienompi väylä.

## Käytännön osto-ohje harrastajalle

Jos mietit PCIe:n merkitystä paikallisessa LLM-koneessa, etenisin näin:

1. **Tarkista ensin todellinen linkki, ei vain slotin pituus.** Pitkä fyysinen slotti voi olla sähköisesti x4 tai x8.
2. **Selvitä mahtuuko tavoitemalli oikeasti VRAMiin.** Jos ei mahdu, ongelma ei ratkea pelkällä PCIe-päivityksellä.
3. **Arvioi käyttötyyppi.** Yksi oma chat-malli sietää kompromisseja paremmin kuin pitkä promptinkäsittely tai palvelinkäyttö.
4. **Suhtaudu x8-linkkiin rauhallisesti.** Se ei yksin tee kokoonpanosta huonoa.
5. **Suhtaudu x4-linkkiin varauksella, jos malli ei mahdu kokonaan GPU:lle.** Tällöin kokonaiskäytettävyys voi kärsiä enemmän kuin pelkkä FPS- tai token-luku antaa ymmärtää.

## Käytännön johtopäätös

Kannattaako PCIe 4.0 paikalliseen LLM-koneeseen? **Kyllä, jos sen avulla vältät liian kapean x4-linkin, osittaisen offloadin tuskan tai muuten ahtaaksi menevän kaistajaon. Ei välttämättä, jos vaihtoehtona olisi menettää VRAMia tai muuta tärkeämpää kapasiteettia.**

Hyvä nyrkkisääntö on tämä: paikallisessa LLM-koneessa PCIe on harvoin ensimmäinen asia, joka kannattaa maksaa kuntoon, mutta liian hidas linkki voi tehdä kompromissikoneesta paljon huonomman käyttää. Siksi harrastajan kannattaa kysyä vähemmän "onko minulla PCIe 4.0" ja enemmän "mitä kautta data oikeasti liikkuu minun kokoonpanossani".

## Lähteet

- Wikipedia: PCI Express, kaistat, linkkileveydet ja perustopologia: https://en.wikipedia.org/wiki/PCI_Express
- Trenton Systems: PCIe Gen 4 vs. Gen 3 Slots, Speeds, sukupolvien ja kaistojen käytännön kaistataulukko: https://www.trentonsystems.com/en-us/resource-hub/blog/pcie-gen4-vs-gen3-slots-speeds
- llama.cpp Discussion #3111, käytännön huomioita osittaisesta GPU-offloadista ja RAM/VRAM-jaosta: https://github.com/ggml-org/llama.cpp/discussions/3111
