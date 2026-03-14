---
title: "Hidas paikallinen LLM? Tarkista nämä 4 pullonkaulaa ennen uutta GPU-ostoa"
date: 2026-03-14T17:29:00+02:00
draft: false
---

Kun paikallinen malli tuntuu tahmealta, ensimmäinen reaktio on usein sama: "tarvitsen isomman näytönohjaimen". Se on joskus totta, mutta yllättävän usein ongelma on workflowssa, asetuksissa tai siinä, ettei kone oikeasti käytä GPU:ta niin kuin luulet. Harrastajalle tämä on hyvä uutinen, koska ensimmäinen nopeutus tulee usein ilman uutta rautaa.

Tärkein käytännön kysymys on tämä: **onko malli kokonaan GPU:lla, osittain GPU:lla vai käytännössä CPU:lla?** Ollaman `ollama ps` näyttää tämän suoraan `Processor`-sarakkeessa. Jos siellä näkyy `100% CPU`, hidas vaste ei ole mysteeri vaan odotettava seuraus. Jos taas malli on vain osittain GPU:lla, VRAM on jo pullonkaula ja suorituskyky voi vaihdella paljon mallin koon, kvantisoinnin ja konteksti-ikkunan mukaan.

## 1) Varmista ensin, että GPU-offload oikeasti tapahtuu

llama.cpp:n dokumentaatio korostaa, että GPU-offload pitää tarkistaa diagnostiikasta, ei oletuksesta. Kun malli käynnistyy oikein, lokissa näkyy paljonko kerroksia siirrettiin GPU:lle ja paljonko VRAMia käytetään. Jos tätä ei näy, olet helposti tilanteessa jossa "GPU-kone" käyttäytyy käytännössä CPU-koneena.

Tämä on tavallinen harrastajan moka etenkin silloin, kun asennus on tehty nopeasti tai CUDA-/ajuripuoli jäi puolivalmiiksi. Ennen kuin ostat mitään, tarkista että runtime todella osaa käyttää GPU:ta ja että malli mahtuu järkevästi sinne.

## 2) Liian suuri säie-määrä voi tehdä koneesta hitaamman

Toinen epäintuitiivinen kohta on CPU-säikeet. llama.cpp:n suorituskykyvinkeissä varoitetaan, että liian suuri `--threads`-arvo voi jopa heikentää tokeninopeutta. Jos kone tuntuu tukkoiselta tai generointi on epätasaisen hidasta, ongelma ei välttämättä ole liian heikko prosessori vaan ylilyöty säieasetuksen arvo.

Käytännön tapa testata tämä on yksinkertainen: aloita pienellä arvolla, mittaa vaste, nosta maltillisesti ja lopeta kun parannus katoaa. "Maksimit kaakkoon" ei ole hyvä oletusasetus local-LLM-käytössä.

## 3) Konteksti-ikkuna syö muistia nopeammin kuin moni arvaa

Ollaman FAQ muistuttaa, että oletuskonteksti ei ole loputon, ja suurempi konteksti kasvattaa muistipainetta. Harrastajan arjessa tämä näkyy niin, että malli tuntuu hyvältä lyhyissä kysymyksissä mutta romahtaa pitkissä keskusteluissa, RAG-kokeiluissa tai silloin kun mukaan tungetaan liikaa dokumentteja kerralla.

Jos tavoite on sujuva paikallinen käyttö, kannattaa ensin optimoida työnkulku eikä vain kasvattaa kontekstia. Tiivistä syötettä, pilko aineistoa ja pidä yksi realistinen oletusprofiili arjen käyttöä varten. Muuten päädyt maksamaan VRAMista ongelman, jonka olisi voinut ratkaista rakenteella.

## 4) Kaikki hitaus ei ole "mallin hitautta" vaan välimuistin ja inferenssin fysiikkaa

Hugging Facen optimointiohjeissa korostetaan kv-cachea: malli tallentaa aiempia avain-arvo-pareja, jotta kaikkea ei lasketa uudelleen jokaisella tokenilla. Tämä on hyvä muistutus siitä, että tokenien generointi ei ole tasakustanteista puuhaa. Mitä pidempi konteksti ja mitä raskaampi malli, sitä herkemmin jokainen lisäaskel maksaa.

Käytännössä tämä tarkoittaa kahta asiaa. Ensinnäkin pieni, hyvin istuva malli voi tuntua arjessa "paremmalta" kuin liian iso malli, joka mahtuu laitteeseen juuri ja juuri. Toiseksi pullonkaula voi olla muistissa ja datan liikkeessä, ei pelkästään raakatehossa. Siksi käytettävyyttä kannattaa arvioida vasteella ja vakaudella, ei vain mallin miljardiparametreilla.

## Nopea harrastajan tarkistuslista ennen ostoksia

1. Katso, onko malli oikeasti GPU:lla vai CPU:lla.
2. Kokeile pienempää tai paremmin sopivaa kvantisointia.
3. Laske konteksti-ikkunaa ja testaa sama prompti uudelleen.
4. Säädä säiemäärää sen sijaan että jätät sen oletuksen varaan.
5. Vasta jos nämä eivät auta, mieti lisää VRAMia tai toista GPU:ta.

Monessa kotilabrassa paras päivitys ei siis ole uusi kortti heti tänään, vaan kurinalainen mittaus: yksi prompti, yksi malli, yksi konteksti, muutama asetuskokeilu. Jos malli ei tälläkään asetu käyttökelpoiseksi, silloin uusi GPU on perusteltu hankinta eikä toiveikas arvaus.

## Lähteet

- llama.cpp: Token generation performance tips: https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md
- Ollama FAQ: https://docs.ollama.com/faq
- Hugging Face Transformers – Optimizing inference: https://huggingface.co/docs/transformers/main/en/llm_optims
