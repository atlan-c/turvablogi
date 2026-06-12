---
title: "AI-rauta kotilabrassa: kannattaako GPU:n power limit säätää paikalliseen LLM-koneeseen?"
date: "2026-06-12T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "GPU"
  - "Power Limit"
  - "Thermals"
  - "Local LLM"
  - "NVIDIA"
---
Paikallisen LLM-koneen pullonkauloista puhutaan usein vain VRAMin, RAMin ja mallikoon kautta. Silti arjessa vastaan tulee toinenkin käytännön kysymys: **kannattaako GPU:n power limit säätää alemmaksi, jos kone käy pitkään, on äänekäs tai lämpenee liikaa?** Usein kannattaa ainakin testata, mutta vain oikeasta syystä. **Power limit on hyvä työkalu lämmön, melun ja kulutuksen hillintään. Se ei yleensä ole taikatemppu, joka korjaa liian pienen VRAMin, huonon kotelon ilmankierron tai väärin mitoitetun mallin.**

Juuri tämä ero on tärkeä. Jos yksi kortti käy jatkuvasti kuumana, tuulettimet huutavat ja suorituskyky heittelee pitkissä ajoissa, maltillinen tehonrajoitus voi tehdä koneesta miellyttävämmän ja tasaisemman. Jos taas ongelma on se, että malli ei mahdu kunnolla GPU:lle tai ajo karkaa CPU:n puolelle, power limit ei poista varsinaista syytä.

## Mitä power limit oikeasti tekee?

NVIDIAn `nvidia-smi`-dokumentaatio kuvaa power limitin GPU:n enimmäistehorajana. Työkalu näyttää myös kortin minimi- ja maksimiarvot, joiden sisällä rajaa saa muuttaa. Sama dokumentaatio kertoo lisäksi, että GPU säätää suorituskykytilaansa pysyäkseen annetun tehorajan sisällä.

Käytännössä tämä tarkoittaa:

- kortti saa yhä tehdä samaa työtä, mutta pienemmällä tehoikkunalla
- kellotaajuus ei aina pysy yhtä korkealla kuin täysin vapaana
- lämpö ja melu voivat laskea selvästi
- suorituskyky voi laskea vähän, joskus yllättävän vähän

Monessa kotilabrassa tämä on ihan hyvä vaihtokauppa. Jos 24/7-kone käy hieman hitaammin mutta samalla viileämmin, hiljaisemmin ja vakaammin, kokonaiskokemus voi parantua enemmän kuin raakanopeus antaa ymmärtää.

## Miksi tämä voi auttaa paikallisessa LLM-ajossa?

Paikallinen inferenssi ei ole monelle harrastajalle lyhyt benchmark, vaan pitkä käyttötila: malli pidetään muistissa, ajoa tulee pitkin päivää ja sama kone tekee ehkä muutakin. Tällaisessa käytössä ongelma ei aina ole "maksiminopeus ensimmäisen minuutin aikana", vaan:

- lämpeneekö kortti niin paljon, että tuulettimet muuttuvat ärsyttäviksi
- alkaako suorituskyky vaihdella pitkän kuorman aikana
- nouseeko kulutus ja huonelämpö turhan korkeaksi
- pysyykö kotelo järkevänä kesällä tai pienessä työhuoneessa

NVIDIAn kellotapahtumien dokumentaatio kertoo suoraan, että kellot voivat laskea sekä ohjelmallisen power capin että lämpörajojen takia. Tämä on tärkeä käytännön havainto: jos kortti törmää jo valmiiksi thermal slowdown'hun, pieni ja hallittu power limit voi joskus tehdä käytöksestä tasaisempaa kuin "anna mennä täysillä kunnes lämpö pakottaa alas".

Toisin sanoen: **maltillinen tehonrajoitus voi joskus vähentää sahaamista**, vaikka se ei nosta huippusuorituskykyä.

## Milloin power limit on minusta järkevä kokeilu?

Kokeilisin sitä ensimmäisten asioiden joukossa, jos useampi näistä osuu:

- kone on päällä pitkään eikä vain lyhyissä testeissä
- GPU on selvästi äänekäs jatkuvassa inferenssissä
- kotelo tai huone on lämmin ja lämpökuorma tuntuu arjessa
- suorituskyky ailahtelee pitkissä ajoissa enemmän kuin odotit
- tavoite on parempi wattia kohti saatava hyöty, ei absoluuttinen huippunopeus

Tämä on erityisen järkevä kotikoneessa, jossa yksi GPU joutuu elämään normaalissa huoneessa eikä datakeskuksen ilmavirrassa.

## Milloin power limit ei ole oikea ratkaisu?

En käyttäisi sitä ensisijaisena vastauksena näihin ongelmiin:

- malli ei mahdu kunnolla VRAMiin
- `ollama ps` tai vastaava näyttää, että ajo valuu CPU:n puolelle
- kone swappaa tai muuten kärsii muistipulasta
- kotelon ilmankierto on aidosti huono
- virtalähde tai kaapelointi on alimitoitettu

Näissä tilanteissa tehonrajoitus voi peittää oireita, mutta ei korjaa juurisyytä. Jos malli on väärän kokoinen koneelle, parempi ratkaisu on usein pienempi kvantisointi, alempi konteksti, enemmän VRAMia tai yksinkertaisesti realistisempi odotus suorituskyvystä.

## Käytännön tapa testata ilman arvailua

Jos käytössä on NVIDIA-kortti, turvallinen perusidea on tämä:

1. katso nykyinen tehoraja, minimi, maksimi ja lämpötila
2. aja sama paikallinen LLM-kuorma vakioasetuksilla
3. laske power limit maltillisesti, ei aggressiivisesti
4. toista sama kuorma
5. vertaa melua, lämpöä, vakautta ja vasteaikaa

Esimerkiksi:

```bash
nvidia-smi -q -d POWER,TEMPERATURE
sudo nvidia-smi -pl 250
```

Oleellinen kohta on "maltillisesti". Tavoite ei ole tehdä 350 W kortista 150 W ihmettä, vaan katsoa, katoaisiko turha lämpö- ja melupiikki pienellä suorituskykyhinnalla.

## Yksi tärkeä käytännön rajoitus: asetus ei ole pysyvä

NVIDIAn NVML-dokumentaatio sanoo suoraan, että power limitin muuttaminen vaatii root- tai admin-oikeudet, ja että asetus ei ole pysyvä uudelleenkäynnistyksen tai ajurin purun yli. Samassa dokumentaatiossa myös persistence mode kuvataan Linuxissa heti vaikuttavaksi mutta ei reboottien yli säilyväksi.

Tästä seuraa kaksi käytännön johtopäätöstä:

- jos testaat power limitin hyväksi, tarvitset tavan asettaa se uudelleen bootissa
- jos kone käyttäytyy oudosti suspend/resume-jakson jälkeen, tarkista ensin että GPU ylipäätään näkyy oikein

Ollaman GPU-dokumentaatio muistuttaa, että Linuxissa suspend/resume voi joskus pudottaa NVIDIA-GPU:n pois käytöstä niin, että ajo fallbackaa CPU:lle. Silloin ongelma ei ole power limit vaan ajuri- ja laitepolku.

## Mitä minä odottaisin tulokselta?

En odottaisi ihmettä, vaan tätä:

- hieman alempi huippunopeus
- vähemmän lämpöä ja melua
- tasaisempi pitkä kuorma
- parempi käyttömukavuus jatkuvassa käytössä

Jos taas mittaat kaiken ja huomaat, että suorituskyky putoaa paljon mutta lämpö tai ääni ei korjaannu tarpeeksi, kokeilu kertoi jotain hyödyllistä: ongelma on todennäköisesti muualla kuin liian korkeassa tehorajassa.

## Oma nyrkkisääntöni kotilabrassa

Power limit on minusta hyvä viimeistelysäätö, ei ensimmäinen ostopäätös. Menisin yleensä tässä järjestyksessä:

1. varmista, että malli ja kvantisointi sopivat kortin VRAMiin
2. varmista, että kotelon ilmankierto on oikeasti kunnossa
3. varmista, ettei ongelma ole RAM-, swap- tai CPU-offload-puolella
4. testaa vasta sitten maltillista power limit -säätöä

Kun perusasiat ovat kunnossa, tehonrajoitus voi olla yksi helpoimmista tavoista tehdä paikallisesta LLM-koneesta siedettävämpi jokapäiväiseen käyttöön.

## Tiivis johtopäätös

**GPU:n power limitin säätäminen kannattaa paikallisessa LLM-koneessa silloin, kun tavoitteena on vähemmän lämpöä, vähemmän melua ja tasaisempi pitkä kuorma.** Se ei yleensä ole oikea lääke liian suurelle mallille tai liian pienelle VRAMille, mutta se voi olla erinomainen käytännön hienosäätö 24/7-koneeseen.

Jos kone on jo muuten tasapainoinen, pieni tehonrajoitus voi olla yllättävän hyvä diili. Jos taas perusarkkitehtuuri on vinossa, power limit vain pehmentää oireita.

## Lähteet

- https://docs.nvidia.com/deploy/nvidia-smi/
- https://docs.nvidia.com/deploy/nvml-api/group__nvmlDeviceCommands.html
- https://docs.nvidia.com/deploy/nvml-api/group__nvmlClocksEventReasons.html
- https://docs.ollama.com/gpu
