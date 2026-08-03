---
title: "Vertaatko paikallisia malleja? Lukitse seed ja samplerit ensin"
date: "2026-08-03T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "benchmark"
  - "sampling"
  - "ollama"
---
## Tiivistelmä
Paikallisen LLM:n vertailu menee helposti harhaan, vaikka käyttäisit samaa promptia ja samaa mallia. Syynä on usein se, että **seed, temperature, top_p, top_k tai maksimivastaus vaihtuvat huomaamatta** eri ajokertojen tai runtimejen välillä. Tällöin et enää vertaile mallia vaan eri sampling-profiileja.

Käytännön sääntö on yksinkertainen: jos haluat tietää onko malli parempi koodissa, agenttitehtävässä tai rakenteisessa vastauksessa, **lukitse ensin seed ja tärkeimmät sampleriasetukset**. Vasta sen jälkeen mallien erot alkavat kertoa jotain hyödyllistä.

## Miksi tämä vääristää vertailua näin paljon

Ollaman Modelfile-dokumentaatio listaa generation-parametrit suoraan mallin ajon osiksi: mukana ovat muun muassa `seed`, `temperature`, `top_k`, `top_p`, `min_p` ja `num_predict`. vLLM:n `SamplingParams` kertoo saman toisella tavalla: myös siellä sampling-asetukset ovat nimenomaan pyynnön osa, eivät vain käyttöliittymän koristeita.

Tästä seuraa käytännössä kolme asiaa:

- jos seed vaihtuu, vastaus voi muuttua vaikka malli ja prompti pysyvät samoina
- jos temperature tai top_p vaihtuu, "parempi malli" voi olla vain varovaisempi sampling
- jos `max_tokens` tai `num_predict` vaihtuu, toinen malli voi näyttää heikommalta vain siksi että vastaus katkaistiin aiemmin

Moni harrastaja huomaa tämän vasta silloin, kun yksi runtime tuottaa "järkevämpiä" vastauksia kuin toinen. Todellisuudessa ero voi olla lähes kokonaan sampling-profiilissa.

## Seed ei ole pikkujuttu vaan vertailun pohja

Ollaman dokumentaatio sanoo suoraan, että tietty seed tuottaa saman tekstin samalle promptille. Tämä ei tarkoita, että kaikki olisi aina täydellisen determinististä jokaisessa ympäristössä, mutta se tekee vertailusta heti paljon reilumman. Ilman sitä ensimmäinen testi mittaa osittain sattumaa.

Jos vertailet kahta kvantisointia tai kahta eri mallia, aloittaisin näin:

1. sama prompti
2. sama system-ohje
3. sama seed
4. sama `temperature`, `top_k`, `top_p` ja `min_p`
5. sama vastauskatto (`num_predict` tai `max_tokens`)

Vasta tämän jälkeen katsoisin laatua, nopeutta ja rakennetta.

## llama.cpp:n cache-huomio on helppo unohtaa

Tässä kohtaa llama.cpp:n serveridokumentaatio on erityisen hyödyllinen. Se kertoo, että `cache_prompt` voi käyttää aiemman pyynnön KV-välimuistia uudelleen, mutta samalla dokumentaatio varoittaa, että eri batch-kokojen vuoksi logitit eivät välttämättä ole bittitasolla identtisiä. Seurauksena voi olla nondeterministisiä eroja.

Tämä on tärkeä käytännön opetus: **pelkkä kiinteä seed ei aina riitä**, jos vertailuympäristön välimuistikäytös tai request-polku muuttuu.

Siksi tekisin vertailut kahdessa vaiheessa:

- ensin kylmä testi: uusi ajo ilman epäselvää prompt-cache-jatkumoa
- sitten lämmin testi: sama kuorma tuotantotyyliin, jos oikea käyttö nojaa cacheen

Näin erotat toisistaan mallin laadun ja tuotantopolun suoritusoptimoinnit.

## Missä tämä näkyy eniten käytännössä

Suurin vahinko syntyy yleensä tilanteissa, joissa vastaus arvioidaan "fiilispohjalta":

- yksi malli tuntuu täsmällisemmältä
- toinen tuntuu luovemmalta
- kolmas vaikuttaa huonommalta JSON:ssa

Jos asetukset eivät ole samat, johtopäätös voi olla väärä. Matalampi temperature näyttää usein fiksummalta koodissa ja rakenteisessa ulostulossa, vaikka itse mallissa ei olisi eroa. Korkeampi top_p taas voi näyttää paremmalta ideoinnissa mutta huonommalta toistettavissa agenttityövaiheissa.

Erityisesti paikallisissa agenteissa tämä korostuu, koska samaa mallia käytetään usein:

- työkalukutsuihin
- rakenteiseen JSON-ulostuloon
- tavalliseen keskusteluun
- pitkän ketjun korjauskierroksiin

Yksi sampling-profiili ei palvele kaikkia näitä hyvin. Siksi "mikä malli on paras" on usein väärä kysymys. Parempi kysymys on: **millä kiinteillä asetuksilla malli toimii tässä työssä?**

## Oma käytännön tarkistuslista ennen kuin julistat voittajan

Ennen kuin päätän että malli A voittaa mallin B:n, tarkistan nämä:

- seed on lukittu
- `temperature`, `top_k`, `top_p` ja mahdollinen `min_p` ovat samat
- vastauskatto on sama
- prompt-cache-käytös ei vaihdu huomaamatta
- arvioin mallia oikealla tehtävällä, en yhdellä irtokysymyksellä

Hyvä testi ei ole "kirjoita hauska kappale" vaan pieni oikea työ:

- tuota tietty JSON-rakenne
- tee yksi työkalukutsu oikein
- vastaa lyhyesti annetulla politiikalla
- korjaa yksi rikkinäinen koodinpätkä ilman lisähöpötystä

Jos malli häviää näissä samoilla asetuksilla, vertailu alkaa jo merkitä jotain.

## Johtopäätös

Paikallisten mallien vertailussa suurin virhe ei usein ole väärä benchmark vaan liian löysä ajohygienia. Jos seed ja samplerit elävät testistä toiseen, lopputulos kertoo yhtä paljon arpaonnesta ja runtime-oletuksista kuin itse mallista. Käytännössä nopein tapa tehdä parempia valintoja on tylsä mutta tehokas: lukitse asetukset, testaa oikealla tehtävällä ja pidä cache-käytös kurissa.

## Lähteet

- https://docs.ollama.com/modelfile
- https://docs.vllm.ai/en/v0.6.4/dev/sampling_params.html
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
