---
title: "Kannattaako NPU-läppäriä ostaa paikalliseen LLM-käyttöön?"
date: "2026-08-31T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "ai-hardware"
  - "npu"
  - "windows-ml"
---
## Tiivistelmä
Jos mietit vuonna 2026, kannattaako NPU-läppäri ostaa paikallista LLM:ää varten, lyhyt vastaus on tämä: **ostaisin NPU:n bonuksena, en pääsyynä**. NPU auttaa erityisesti pienissä paikallisissa AI-ominaisuuksissa, kiinteissä ONNX-putkissa ja akkukestoa painottavassa käytössä. Varsinainen yleiskäyttöinen paikallinen chat-malli, koodiapuri tai agentin päämalli nojaa silti useimmiten GPU:hun tai joskus CPU:hun, ei NPU:hun.

Tämä ei tarkoita, että NPU olisi turha. Se tarkoittaa, että ostoperuste pitää asettaa oikein. Jos kuvittelet NPU:n korvaavan kunnollisen GPU:n paikallisessa LLM-ajossa, petyt helposti. Jos taas ymmärrät sen sivutyöläiseksi, joka hoitaa osan kuormasta energiatehokkaasti, se voi olla oikein järkevä lisä.

## Mitä Windowsin oma dokumentaatio kertoo suoraan

Microsoftin Windows AI -FAQ tekee yhden käytännössä tärkeän eron hyvin selväksi. Windows AI API:t vaativat Copilot+ PC:n ja NPU:n, mutta Foundry Local toimii millä tahansa Windows-laitteella, jossa on DirectX 12 -kelpoinen GPU. Lisäksi Windows ML tukee CPU:ta, GPU:ta ja NPU:ta.

Harrastajalle tästä seuraa heti ensimmäinen ostosääntö: **NPU ei ole edellytys sille, että voit ajaa paikallisia malleja.** Se on edellytys tietyille Windowsin valmiille laitekohtaisille AI-ominaisuuksille, mutta ei yleiselle paikallisen mallin käytölle.

Jos päätavoitteesi on ajaa avoimia paikallisia LLM-malleja, vertailla kvantisointeja, pitää oma API käynnissä tai rakentaa agenttia, tärkein kysymys ei ole "onko tässä NPU" vaan:

- kuinka hyvä GPU tai iGPU koneessa on
- paljonko muistia oikeasti on käytettävissä
- miten paljon lämpö- ja tehorajoitukset kuristavat pitkää ajoa

## Missä NPU on oikeasti hyvä

Microsoftin Windows ML -dokumentaatio kuvaa NPU:n tyypilliseksi valinnaksi akkuystävälliseen ja jatkuvaan paikalliseen inferenssiin. AMD:n Ryzen AI -dokumentaatio menee vielä käytännöllisemmälle tasolle: sen mukaan LLM:iä voidaan ajaa Ryzen AI -koneilla NPU-only-, hybrid- ja GPU-tiloissa. Samassa taulukossa GPU-tila on liitetty `llama.cpp`:hen, kun taas NPU- ja hybriditilat nojaavat ONNX Runtime GenAIhin.

Tästä saa hyvän käytännön mallin:

- NPU sopii hyvin ennalta optimoituihin malleihin ja rajattuihin putkiin
- hybridiajo voi olla järkevä, jos alusta tukee sitä hyvin
- GPU on edelleen tavallisin ratkaisu, kun haluat yleiskäyttöistä paikallista LLM-ajamista

Toisin sanoen NPU loistaa silloin, kun tehtävä on suhteellisen vakio: tiivistys, OCR, luokittelu, kevyt avustaja, pieni sisäinen apumalli tai muu sovelluskohtaisesti optimoitu ajo. Se on paljon heikompi ostoperuste, jos haluat harrastaa vapaasti eri mallien, eri runtimejen ja eri kvantisointien kanssa.

## Missä moni ostaja ymmärtää NPU:n väärin

Yleisin harha on ajatella, että NPU olisi "LLM-kiihdytin" samalla tavalla kuin isompi GPU on LLM-kiihdytin. Käytännössä näin ei kannata ajatella.

Windows ML sanoo suoraan, että käyttöjärjestelmä hoitaa execution providerien jakelua ja päivitystä, mutta **sinun vastuullasi on silti mallin optimointi eri laitteille**. Se on iso vihje siitä, ettei NPU ole mikään universaali "aja mitä vain nopeammin" -nappi. Jotta saat NPU:sta iloa, mallin ja runtimen pitää osua hyvin yhteen laitteen kanssa.

Sama näkyy AMD:n dokumentaatiossa: NPU- ja hybridiajo perustuvat tuettuihin, optimoituihin malleihin ja omaan runtime-polkuunsa. Tämä on täysin eri maailma kuin se, että lataat illalla uuden GGUF-mallin ja kokeilet sitä saman tien paikallisessa palvelimessa.

## Paikallinen agentti tarvitsee yleensä muutakin kuin yhden inference-polun

Kun ihmiset sanovat haluavansa "paikallisen agentin", he tarkoittavat usein paljon muutakin kuin yhtä chat-vastausta:

- päämalli keskusteluun tai suunnitteluun
- embedding- tai reranker-malli haulle
- joskus puhetta, OCR:ää tai kuvien analysointia
- työkaluja, tiedostolukuja ja muuta tavallista ohjelmakoodia ympärille

Juuri tässä NPU voi olla hyödyllinen, mutta ei yleensä pääroolissa. NPU sopii hyvin sivutöihin, jotka halutaan ajaa hiljaisesti ja energiatehokkaasti. Päämalli kannattaa silti mitoittaa sen mukaan, mikä backend tukee oikeaa työkuormaasi parhaiten ja missä muistibudjetti riittää.

Käytännössä siis:

- NPU voi auttaa agentin apuvaiheissa
- GPU ratkaisee useammin agentin pääläpimenon
- CPU tekee edelleen osan esikäsittelystä, jälkikäsittelystä ja tavallisesta sovelluslogiikasta

Microsoftin Copilot+ PC -kehittäjäohje tukee tätä ajattelua yllättävän hyvin. Siellä painotetaan mittaamaan erikseen mallin latausaikaa, yksittäisten inferenssien kestoa, CPU:n esityötä ja NPU:n käyttöä. Tämä on juuri oikea tapa ajatella myös kotilabrassa: **älä oleta pullonkaulaa, mittaa se**.

## Milloin ostaisin NPU-läppärin

Ostaisin NPU-läppärin paikalliseen AI-käyttöön, jos useampi näistä pitää paikkansa:

- haluat hyvän akkukeston ja hiljaisen laitteen
- käytät paljon valmiita Windowsin paikallisia AI-ominaisuuksia tai ONNX-pohjaisia malleja
- sinulla on yksi tai muutama selkeä työkuorma, joita haluat ajaa toistuvasti samalla koneella
- arvostat sitä, että osa AI-kuormasta voidaan siirtää pois GPU:lta

Tällöin NPU on oikea ominaisuus, koska se palvelee koko laitteen käyttötapaa eikä vain yhtä benchmarkia.

## Milloin en ostaisi NPU:n takia

En maksaisi NPU:sta ekstraa, jos päätavoite on jokin näistä:

- ajaa mahdollisimman vapaasti uusia paikallisia chat-malleja
- kokeilla paljon GGUF-malleja ja eri inference-stackeja
- käyttää konetta paikallisena LLM-palvelimena pidempiin sessioihin
- hakea mahdollisimman paljon raakaa LLM-suorituskykyä rahalle

Näissä tapauksissa hyöty tulee useammin GPU:sta, muistista, jäähdytyksestä ja yleensä koko koneen pitkäkestoisesta tehonkestosta kuin NPU:sta.

## Oma nyrkkisääntöni vuonna 2026

Ajattelen NPU-läppäriä tällä hetkellä näin:

1. Hyvä valinta liikkuvalle kehittäjälle tai harrastajalle, joka haluaa paikallisia AI-ominaisuuksia myös ilman raskasta GPU-ajoa.
2. Keskinkertainen valinta, jos tavoitteena on yksi kone kaikkeen ja odotat sen korvaavan kunnollisen paikallisen LLM-työaseman.
3. Huono valinta, jos ostat sen vain siksi, että markkinointi vihjaa NPU:n tarkoittavan automaattisesti parempaa paikallista LLM-kokemusta.

Paras tulos tulee, kun ostat koneen edelleen kokonaisuutena. Katso ensin muistia, GPU:ta, jäähdytystä, melua ja todellista runtime-tukea. Katso NPU:ta vasta sen jälkeen.

## Johtopäätös

**Kannattaako NPU-läppäri ostaa paikalliseen LLM-käyttöön?** Kyllä, jos ostat sen energiatehokkaaksi AI-yleiskoneeksi. Ei, jos ostat sen korvaamaan GPU-pohjaisen paikallisen LLM-koneen. NPU on juuri nyt parhaimmillaan hyvä sivumoottori, ei koko auton moottori.

Siksi pitäisin NPU:ta vuonna 2026 plussana, joka voi tehdä paikallisesta agentista sulavamman ja akkukäytöstä miellyttävämmän, mutta en käyttäisi sitä yksin ostopäätöksen perustana. Jos budjetti pakottaa valitsemaan, ottaisin useimmiten ensin enemmän muistia ja paremman todellisen model runtime -tuen.

## Lähteet

- https://learn.microsoft.com/en-us/windows/ai/faq
- https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/accelerate-ai-models
- https://learn.microsoft.com/en-us/windows/ai/npu-devices/
- https://ryzenai.docs.amd.com/en/latest/llm/overview.html
- https://onnxruntime.ai/docs/execution-providers/CoreML-ExecutionProvider.html
