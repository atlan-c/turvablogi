---
title: "Paikallinen LLM käytännössä: erota embedding-malli chat-mallista ennen RAGia"
date: "2026-07-27T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoaly ja agentit"
tags:
  - "local-llm"
  - "rag"
  - "embeddings"
  - "ollama"
  - "agent"
---
## Tiivistelmä
Paikallisen dokumenttiagentin laatu ratkaistaan usein jo ennen ensimmäistä vastausta. Jos haku perustuu heikkoon tai jatkuvasti vaihtuvaan embedding-polkuun, lopullinen chat-malli saa eteensä väärät palaset ja näyttää huonommalta kuin oikeasti on. Siksi turvallinen oletus on tämä: **anna embedding-mallille oma roolinsa ja pidä se erillään vastaavasta chat-mallista**.

## Missä virhe syntyy

RAG-putkessa on helppo tuijottaa vain sitä mallia, joka lopulta vastaa käyttäjälle. Mutta retrieval ei ala vastauksesta vaan siitä, miten dokumentit muutetaan vektoreiksi ja miten kysymys haetaan samasta avaruudesta takaisin. Jos tämä vaihe on hutera, varsinainen LLM ei pelasta tilannetta.

Siksi "yksi malli kaikkeen" kuulostaa siistiltä arkkitehtuurilta, mutta on paikallisessa käytössä usein huono kompromissi:

- generointimalli ei välttämättä ole paras embedding-malli
- retrieval-ongelma näyttää helposti chat-mallin ongelmalta
- sama raskas runtime tekee enemmän työtä kuin olisi pakko
- mallinvaihto sotkee indeksoinnin, jos embedding-polku ei ole eriytetty

Ollaman embedding-dokumentaatio kertoo tämän epäsuorasti mutta aika selvästi. Embeddings-kyvykkyys on oma polkunsa, ja dokumentaatio suosittelee siihen nimenomaan erillisiä malleja kuten `embeddinggemma`, `qwen3-embedding` ja `all-minilm`.

## Mitä erillinen embedding-malli ostaa käytännössä

Ensimmäinen hyöty on yksinkertainen: vika löytyy helpommin oikeasta paikasta.

Jos haet dokumenteista huonoja osumia, voit testata embedding-polun erikseen ilman että samalla epäilet promptia, tool callingia tai itse vastaavaa mallia. Tämä on kotilabrassa iso etu, koska useimmat "RAG on huono" -hetket eivät johdu siitä, että päämalli olisi tyhmä, vaan siitä että väärä sisältö päätyi promptiin asti.

Toinen hyöty on operatiivinen. Open WebUI:n RAG-dokumentaatio muistuttaa, että embedding-mallin vaihto vaatii koko tietopohjan reindeksoinnin, koska eri mallien embeddingit elävät eri vektoriavaruuksissa eivätkä ole keskenään yhteensopivia. Kun tämä pitää mielessä, chat-mallin ja embedding-mallin erottaminen tekee muutoksista hallittavampia:

- voit vaihtaa vastaavaa chat-mallia ilman että koko tietopohja menee uusiksi
- tiedät milloin reindex on pakollinen ja milloin ei
- retrievalin laatu pysyy vertailukelpoisena mallitestien välillä

Kolmas hyöty on resurssipuolella. Open WebUI:n suorituskykyohje sanoo suoraan, että pienissä paikallisissa asennuksissa kevyt `all-MiniLM-L6-v2` CPU:lla on usein tehokkaampi kuin kokonaisen Ollama-instanssin pyörittäminen samalla Raspberry Pi:llä vain embeddingeja varten. Tämä on hyvä muistutus siitä, että retrieval-pino ei aina kaipaa samaa raskasta GPU-polkuasi kuin chat.

## Milloin yksi malli on vielä hyväksyttävä kompromissi

En väitä, että kaksi mallia olisi aina pakollinen ratkaisu. Yhden mallin viritys on täysin ok, jos:

- testaat vasta ideaa etkä ylläpidä pysyvää tietopohjaa
- dokumentteja on vähän ja voit rakentaa indeksin uudestaan hetkessä
- koneessa on vain yksi helppo runtime-polku, jota et halua vielä monimutkaistaa
- hyväksyt sen, että retrieval-laatu ja mallin vaihto sotkeutuvat keskenään

Tämä toimii demossa. Ongelmia tulee siinä vaiheessa, kun samasta virityksestä halutaan luotettava päivittäinen agentti, wiki-haku tai dokumenttiavustaja.

## Käytännön sääntö harrastajalle

Minun nyrkkisääntöni menisi näin:

1. Valitse ensin embedding-malli retrievalia varten.
2. Indeksoi aineisto sillä ja pidä valinta vakaana jonkin aikaa.
3. Testaa chat-malleja vasta tämän päälle.
4. Reindeksoi vain silloin, kun vaihdat embedding-mallia tai chunkkausstrategiaa oikeasta syystä.

Jos teet tämän toisin päin, jokainen uusi generointimallikokeilu houkuttelee samalla rikkomaan koko dokumenttipinon vertailukelpoisuuden.

## Entä jos ajat kaiken Ollaman tai llama.cpp:n päällä

Sekin onnistuu, eikä tässä ole mitään uskonnollista rajaa. Tärkeä ero on enemmän looginen kuin tekninen.

Ollama tarjoaa embeddingeille oman rajapintansa ja suosittelee dedikoituja embedding-malleja. llama.cpp:n palvelindokumentaatio taas näyttää, että embeddingit ovat oma päätepisteensä, ja OAI-yhteensopiva käyttö kulkee `/v1/embeddings`-polun kautta. Molemmissa tapauksissa viesti on sama: embedding kannattaa ajatella omana palvelunaan tai ainakin omana käyttötapanaan, ei vain sivutuotteena chat-ajon kyljessä.

Tämä on hyödyllinen ajattelutapa erityisesti agenteille. Kun agentti käyttää omaa tietopohjaa, retrievalin pitää olla tylsän vakaa. Jos embedding-polku vaihtuu huomaamatta aina muun mallikokeilun mukana, agentin käytös alkaa näyttää ailahtelevalta vaikka varsinainen ongelma on indeksissä.

## Mitä tarkistaisin ennen kuin syytän paikallista LLM:ää

Jos paikallinen RAG tai dokumenttiagentti tuntuu huonolta, tarkistaisin nämä tässä järjestyksessä:

1. Onko käytössä oikeasti dedikoitu embedding-malli?
2. Onko tietopohja reindeksoitu viimeisimmän embedding-mallin jälkeen?
3. Ovatko chunkit niin pieniä, että embeddingeille ei jää kunnollista semanttista sisältöä?
4. Tuleeko promptiin oikeasti relevantteja osumia vai vain teknisesti "lähimpiä" vektoreita?
5. Onko chat-mallin konteksti liian pieni niille osumille, jotka retrieval palauttaa?

Juuri kolmas kohta unohtuu helposti. Open WebUI:n RAG-ohje huomauttaa, että liian aggressiivinen chunkkaus voi heikentää retrievalia ja lisätä samalla turhia embedding-operaatioita. Huono retrieval ei siis aina tarkoita "tarvitaan parempi LLM", vaan joskus "asiakirjat pilkottiin väärin".

## Johtopäätös

Jos rakennat paikallista RAGia tai omaa dokumentteja käyttävää agenttia, älä pidä embedding-mallia sivuseikkana. Se on koko haun perusta.

Siksi suosittelen aloittamaan kahdella roolilla:

- yksi malli tekee haut ja vektorit
- toinen malli lukee löydetyn materiaalin ja vastaa

Tämä ei ole hienostelua vaan tapa pitää järjestelmä diagnosoitavana, päivitettävänä ja kevyempänä. Paikallisessa käytössä juuri nämä kolme asiaa ratkaisevat useammin kuin se, mikä malli voitti viikon benchmarkin.

## Lähteet

- https://docs.ollama.com/capabilities/embeddings
- https://docs.openwebui.com/features/chat-conversations/rag/
- https://docs.openwebui.com/troubleshooting/rag/
- https://docs.openwebui.com/troubleshooting/performance/
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
