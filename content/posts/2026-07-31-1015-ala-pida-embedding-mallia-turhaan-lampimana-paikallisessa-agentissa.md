---
title: "Älä pidä embedding-mallia turhaan lämpimänä paikallisessa agentissa"
date: "2026-07-31T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "embeddings"
  - "ollama"
  - "vram"
  - "agent"
---
## Tiivistelmä
Jos paikallinen agentti tuntuu raskaalta jo ennen kuin varsinainen chat-malli edes alkaa vastata, syy voi olla yllättävän arkinen: koneessa pidetään samaan aikaan lämpimänä myös embedding-mallia, vaikka indeksointia tehdään vain satunnaisesti. Siksi minun käytännön oletukseni on tämä: **pidä generointimalli muistissa, mutta anna embedding-mallin sammua ellei ingest tai haku oikeasti tarvitse sitä juuri nyt**.

Tämä ei ole mikään uskonnollinen sääntö. Jos ajat jatkuvaa dokumenttisyöttöä tai monta käyttäjää, eri ratkaisu voi olla parempi. Mutta yhden harrastajan paikallisessa agentissa turha "aina päällä" -ajattelu syö helposti juuri sitä muistibudjettia, jota vastaava malli tarvitsisi eniten.

## Miksi tämä unohtuu

Kun RAG tai dokumenttiagentti toimii ensi kerran, on houkuttelevaa jättää koko putki pysyvästi päälle. Se tuntuu siistiltä: yksi palvelin, yksi workflow, kaikki aina valmiina. Käytännössä työkuorma on usein epäsymmetrinen:

- embeddingejä tarvitaan eniten silloin, kun ingestaat uusia dokumentteja
- chat-mallia tarvitaan jatkuvasti, kun itse kysyt järjestelmältä jotain
- sama kone joutuu kantamaan molempien muistijäljen, vaikka vain toinen tekee aktiivista työtä

Ollaman API-dokumentaatio tukee tätä ajattelua kahdella tavalla. Ensinnäkin embeddingit ovat oma rajapintansa eikä vain chatin sivuvaikutus. Toiseksi sekä chat- että embedding-kutsuissa on `keep_alive`, jolla mallin voi pitää muistissa vain halutun ajan. Pelkkä olemassaolo kertoo, että mallien elinkaarta kannattaa ohjata tarkoituksella eikä jättää oletuksen varaan.

## Mitä hyötyä kylmästä embedding-mallista on

Suurin hyöty on yksinkertainen: enemmän tilaa sille mallille, joka oikeasti vastaa käyttäjälle.

Ollaman context length -dokumentaatio muistuttaa, että agentit, web-haku ja koodityökalut tarvitsevat helposti vähintään 64k kontekstia. Se taas tarkoittaa lisää muistipainetta juuri sille mallille, joka pyörittää työkalukutsuja, ohjeita ja pitkää keskustelua. Jos samalla pidät toista mallia lämpimänä ilman akuuttia tarvetta, annat VRAM- tai RAM-budjetista palan väärään paikkaan.

Käytännössä tästä seuraa kolme hyötyä:

- generointimallille jää enemmän tilaa pidemmälle kontekstille
- yhden käyttäjän koneessa vältät turhaa mallien välistä kilpailua muistista
- vianhaku helpottuu, koska tiedät kumpi malli on aktiivisesti työssä

Tämä on erityisen hyödyllistä silloin, kun embedding-malli on käytössä lähinnä kahdessa tilanteessa:

- dokumenttien alkureindeksoinnissa
- satunnaisessa uuden materiaalin lisäyksessä

Jos kumpikaan ei pyöri jatkuvasti, 24/7 lämmin embedding-malli on usein enemmän tapa kuin tarve.

## Milloin en tekisi tätä

Kylmä embedding-malli ei ole paras oletus jokaiseen ympäristöön. Jättäisin sen lämpimäksi, jos:

- ingest on jatkuvaa eikä vain satunnaista
- käyttäjiä on monta ja hakuja tulee koko ajan
- vasteajan pitää olla tasainen myös juuri ensimmäisessä haussa
- käytössä on tarkoituksella eriytetty embedding-palvelu omalla resurssillaan

Open WebUI:n suorituskykyohje antaa hyvän käytännön muistutuksen samasta teemasta. Pienissä paikallisissa asennuksissa kevyt CPU:lla ajettava `all-MiniLM-L6-v2` voi olla tehokkaampi kuin kokonainen Ollama-instanssi samalla pienellä koneella vain embeddingeille. Tulkintani tästä on suora: jos embedding-polku ei ole jatkuvasti kuuma, sitä ei kannata väkisin kohdella kuin pääasiallista palvelua.

## Kaksi toimivaa mallia harrastajalle

Yhden käyttäjän kotikoneessa pitäisin vaihtoehdot yksinkertaisina.

### 1. Embeddingit CPU:lla, chat-malli GPU:lla

Tämä on turvallinen oletus, jos ingestimäärät ovat pieniä mutta haluat vapaan GPU-muistin itse agentille. Open WebUI suosittelee juuri tällaisiin matalan speksin tilanteisiin kevyttä paikallista embedding-polkuja CPU:lle.

### 2. Embeddingit Ollamassa, mutta vain työn ajaksi lämpimänä

Jos haluat saman API-pinnan kaikkeen, tämä on hyvä kompromissi. Ollaman `/api/embed` tukee `keep_alive`-asetusta, joten voit pitää mallin muistissa vain ingestion tai aktiivisen hakusarjan ajan ja antaa sen sitten purkautua.

Minusta tämä on usein parempi kuin "kaikki pysyy aina ladattuna", koska se säilyttää yksinkertaisen arkkitehtuurin mutta pakottaa tekemään resurssipäätöksen tietoisesti.

## Käytännön sääntö

Jos rakennat paikallista agenttia itsellesi, etenisin näin:

1. Pidä vastaava chat-malli ensisijaisena muistibudjetin omistajana.
2. Aja embeddingit CPU:lla tai pidä embedding-malli lämpimänä vain ingestion aikana.
3. Mittaa vasta sen jälkeen, onko ensimmäisen haun viive oikeasti ongelma.
4. Jos on, pidennä embedding-mallin `keep_alive`-aikaa hallitusti sen sijaan, että jätät sen ikuisesti päälle.

Tämä järjestys on tylsä, mutta yleensä toimiva. Liian moni optimoi ensin "kaikki heti valmiiksi" eikä huomaa, että juuri se heikentää chat-mallin käytettävyyttä.

## Johtopäätös

Paikallisessa agentissa embedding-malli on tärkeä, mutta se ei tarkoita että sen pitäisi asua muistissa koko päivän. Jos ingest ei ole jatkuvaa, kylmä tai lyhyesti lämmin embedding-polku on usein parempi kompromissi kuin kaksi pysyvästi ladattua mallia samalla koneella.

Harrastajan koneessa tärkein kysymys ei yleensä ole "saanko tämänkin mallin pidettyä päällä", vaan "mikä malli ansaitsee muistibudjetin juuri nyt". Useimmiten vastaus on se, joka puhuu käyttäjälle.

## Lähteet

- https://docs.ollama.com/api/embed
- https://docs.ollama.com/api/chat
- https://docs.ollama.com/capabilities/embeddings
- https://docs.ollama.com/context-length
- https://docs.openwebui.com/troubleshooting/performance/
