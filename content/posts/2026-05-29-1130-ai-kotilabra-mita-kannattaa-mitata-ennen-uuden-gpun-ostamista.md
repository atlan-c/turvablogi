---
title: "AI-kotilabra: mitä kannattaa mitata ennen uuden GPU:n ostamista?"
date: 2026-05-29T11:30:00+03:00
draft: true
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

Uutta GPU:ta harkitseva paikallisen LLM:n harrastaja tekee usein saman virheen kuin moni kotilabran rakentaja muutenkin: ostos päätetään ennen kuin nykyisen koneen pullonkaula on mitattu. Se tuntuu loogiselta, koska GPU on näkyvin komponentti ja VRAM on juuri nyt koko keskustelun kovin valuutta. Silti käytännössä iso osa vääristä ostoista johtuu siitä, että **et tiedä, onko ongelma oikeasti GPU, järjestelmämuisti, levy, lämpö, virrankulutus vai vain huono ajoprofiili.**

Tässä postauksessa käyn läpi, mitä mittaisin ennen kuin ostaisin uuden näytönohjaimen paikalliseen LLM-koneeseen.

## Ensimmäinen kysymys: mikä oikeasti tuntuu hitaalta

Ennen mitään benchmarkia kannattaa kirjoittaa auki yksi arkinen kysymys:

- latautuuko malli liian hitaasti
- loppuuko VRAM kesken
- romahtaako nopeus pidemmässä kontekstissa
- nouseeko melu tai lämpö epämukavaksi
- pysähtyykö käyttö siihen, että yksi malli mahtuu ja toinen ei

Tämä kuulostaa banaalilta, mutta auttaa erottamaan kaksi eri tilannetta:

- **haluan lisää mukavuutta**
- **minulla on selvä tekninen este**

Jos et tiedä kumpi on kyseessä, ostat helposti väärän päivityksen.

## 1. Mittaa mahtuuko oma työkuorma nykyiseen VRAMiin

Tämä on tärkein yksittäinen mittaus. Ei yleinen "paljonko VRAMia on", vaan **paljonko juuri sinun käyttämäsi malli, kvantisointitaso ja konteksti oikeasti syövät.**

Kirjaa ainakin nämä:

- käytetty malli
- kvantisointi
- kontekstin pituus
- VRAM-kulutus idle-tilassa
- VRAM-kulutus aktiivisessa ajossa
- tapahtuuko CPU-offloadia

Jos nykyinen käyttö kaatuu juuri siihen, että 8–12 Gt VRAM ei riitä haluttuun malliin tai kontekstiin, GPU-päivitys on usein perusteltu. Jos taas malli jo mahtuu, mutta käyttö tuntuu silti hitaalta, syy voi olla muualla.

## 2. Mittaa tokens/s kahdessa tai kolmessa oikeassa skenaariossa

Yksi kuivaharjoitustesti ei riitä. Käyttäisin vähintään näitä skenaarioita:

1. lyhyt tavallinen chat
2. pitkä konteksti tai dokumenttipohjainen kysely
3. se raskain malli, jota oikeasti yrität käyttää

Kirjaa ylös:

- ensimmäisen tokenin viive
- tasainen generointinopeus
- muistinkäyttö
- toteutuuko nopeus vakaasti vai sahaako se

Tämä vaihe on tärkeä, koska joskus kone tuntuu hitaalta nimenomaan ensimmäisessä tokenissa, ei tasaisessa generoinnissa. Silloin syy voi olla mallin latauksessa, levyssä tai ohjelmistopinossa, ei pelkässä GPU:ssa.

## 3. Tarkista CPU-RAMin ja offloadin käyttäytyminen

Moni paikallinen LLM-kone toimii juuri ja juuri siksi, että osa työstä valuu keskusmuistiin. Tämä voi olla täysin käyttökelpoinen ratkaisu, mutta samalla se voi peittää alleen todellisen päivitystarpeen.

Siksi mittaisin:

- paljonko RAMia kuluu rinnalla
- milloin offload alkaa
- kuinka jyrkästi suorituskyky putoaa offloadin jälkeen
- muuttuuko käyttökokemus vain hieman vai täysin

Jos nopeus romahtaa aina siinä kohtaa, kun malli ei enää mahdu VRAMiin, lisä-VRAM on todennäköisesti oikea vastaus. Jos ero on pieni, parempi investointi voi olla jokin muu.

## 4. Mittaa mallin latausajat erikseen

Tämä kohta unohtuu yllättävän usein. Hidas käyttökokemus ei aina johdu inferenssistä vaan siitä, että malli latautuu hitaasti tai ympäristö lämpenee ja hyytyy ennen kuin työ pääsee kunnolla alkuun.

Kirjaa:

- kylmä lataus ensimmäisellä käynnistyksellä
- lämmin lataus välimuistin jälkeen
- levyn käyttö ja siirtonopeus
- vaikuttaako hidas SSD käyttökokemukseen enemmän kuin itse generointi

Jos ajat paljon eri malleja edestakaisin, levy ja I/O voivat olla paljon tärkeämpiä kuin moni ensin uskoo.

## 5. Katso lämpö, melu ja virrankulutus oikeana järjestelmäkysymyksenä

GPU-päivitys ei ole vain suorituskykypäätös. Se on myös:

- virtalähdepäätös
- jäähdytyspäätös
- kotelopäätös
- melupäätös

Mittaisin ainakin yhden pidemmän ajon aikana:

- GPU-lämpötilan
- hotspotin, jos saatavilla
- tuuletinprofiilin käytännössä
- seinästä mitatun kulutuksen
- lämpeneekö koko huone epämukavaksi

Tällä on väliä erityisesti kotilabrassa. Jos koneesta tulee päivityksen jälkeen äänekäs ja kuuma kompromissi, et ehkä käytä sitä niin paljon kuin ajattelit.

## 6. Varmista, että ohjelmistopino ei ole varsinainen pullonkaula

Tämä on ehkä yleisin väärä diagnoosi. Ennen ostoa tarkistaisin ainakin:

- käytössä olevat ajurit
- runtime-version
- kvantisoinnin sopivuuden omalle raudalle
- käytössä olevat asetukset ja oletusarvot
- onko samaa mallia testattu liian eri tavoilla eri päivinä

Jos vertaat huonosti viritettyä nykykonetta kuviteltuun uuteen GPU:hun, päätös vääristyy helposti. Pieni ohjelmistosäätö voi joskus siirtää kallista rautapäätöstä kuukausilla.

## Milloin GPU-päivitys on selvästi oikea liike

Päivittäisin GPU:n melko luottavaisin mielin, jos useampi näistä pitää paikkansa:

- nykyinen haluttu malli ei mahdu VRAMiin ilman raskasta offloadia
- pitkä konteksti tekee käytöstä selvästi liian hidasta
- ensimmäinen token ja generointi ovat hitaita vaikka ohjelmistopino on kunnossa
- käyttö on päivittäistä eikä vain satunnaista kokeilua
- koneen muu rakenne tukee päivitystä jo valmiiksi

Tällöin uusi GPU ei ole vain "kiva lisä", vaan poistaa aidon käytännön esteen.

## Milloin en ostaisi vielä mitään

Jättäisin ostoksen tekemättä ainakin hetkeksi, jos:

- et pysty nimeämään yhtä selkeää pullonkaulaa
- et ole mitannut nykyistä käyttöäsi
- nykyinen ongelma liittyy lähinnä mallin lataukseen tai SSD:hen
- järjestelmämuisti loppuu ennen VRAMia
- lämpö ja virta ovat jo nykyisellään epämukavia

Tässä tilanteessa turvallisin ratkaisu on yleensä mitata viikon ajan omaa käyttöä eikä arvailla kaupan sivulla.

## Minun käytännön ostoslistani ennen GPU-päivitystä

Jos tekisin päätöksen itse, haluaisin taulukkoon ainakin nämä rivit:

- malli ja kvantisointi, jota oikeasti käytän
- VRAM-käyttö tavallisessa ajossa
- VRAM-käyttö pahimmassa ajossa
- tokens/s kolmessa skenaariossa
- ensimmäisen tokenin viive
- RAM-käyttö ja offload-käyttäytyminen
- mallin latausaika
- GPU-lämpö ja seinäkulutus
- nykyisen virtalähteen ja kotelon rajat

Kun nämä ovat näkyvissä, GPU-päivitys muuttuu tunteesta päätökseksi.

## Yhteenveto

Mitä kannattaa mitata ennen uuden GPU:n ostamista? **Ainakin VRAM-käyttö, oikea generointinopeus, offloadin vaikutus, latausajat ja koko koneen lämpö- sekä virtakäyttäytyminen.**

Paikallisessa LLM-koneessa paras päivitys ei ole aina tehokkain GPU paperilla. Paras päivitys on se, joka poistaa juuri sinun käytöstäsi selkeimmän rajoitteen ilman että samalla syntyy uusi ongelma melun, lämmön tai budjetin puolelle.

## Lähteet

- https://github.com/ggml-org/llama.cpp
- https://ollama.com/
