---
title: "Nopeuta paikallista agenttia: pidä malli muistissa ja mittaa prefill erikseen"
date: "2026-07-28T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoaly ja agentit"
tags:
  - "local-llm"
  - "agent"
  - "ollama"
  - "llama.cpp"
  - "latency"
---
## Testaa tämä ensin

Yksi hyödyllinen testi paljastaa paljon: pyydä paikalliselta agentilta hyvin lyhyt tehtävä kahdesti peräkkäin. Jos toinen kierros tuntuu selvästi ensimmäistä nopeammalta, pullonkaula ei todennäköisesti ole "malli ajattelee hitaasti" vaan se, että ensimmäinen kierros maksoi erikseen latauksen ja promptin esikäsittelyn. Silloin oikea ensikorjaus ei ole uusi rauta vaan lämpimänä pysyvä malli ja näkyvyys prefill-vaiheeseen.

## Missä viive oikeasti syntyy

Kun agentti tekee pieniä mutta toistuvia tehtäviä, kokonaiskokemus määräytyy usein ensimmäisestä sekunnista eikä siitä, kuinka nopeasti sata viimeistä tokenia tulostuu. Käytännössä pyyntö jakautuu ainakin kolmeen osaan:

- mallin lataus muistiin
- promptin käsittely eli prefill
- tokenien varsinainen generointi

Ollaman `generate`-rajapinta tekee tämän näkyväksi suoraan vastauksessa. Sieltä saa erikseen `load_duration`-, `prompt_eval_duration`- ja `eval_duration`-kentät. Tämä on hyödyllinen muistutus: jos agentti tuntuu hitaalta, sinun ei kannata mitata vain "tokens per second" vaan myös sitä, paljonko aikaa palaa ennen ensimmäistä hyödyllistä tokenia.

llama.cpp:n dokumentaatio tukee samaa ajattelua toisesta kulmasta. Server-rajapinnassa on `timings_per_token`-asetus, jolla saat prompt processing- ja text generation -nopeudet näkyviin vastauksiin. Toisin sanoen runtime itse kertoo, että prefill ja generointi ovat eri vaiheita, joilla on eri pullonkaulat.

## Miksi tämä korostuu juuri agenteilla

Chat-käytössä yksi pitkä vastaus voi peittää paljon syntiä. Agentti taas tekee usein:

- lyhyitä taustakyselyitä
- useita tool-kutsuja
- pieniä tarkentavia jatkoprompteja
- saman mallin toistuvaa käyttöä saman session aikana

Tällöin kylmäkäynnit ja promptin uudelleenkäsittely alkavat dominoida kokemusta. Jos joka vaiheessa odotat ensin mallin latausta tai pitkän järjestelmäpromptin esipureskelua, agentti tuntuu hitaalta vaikka raakaa generointinopeutta olisi paperilla paljon.

Juuri siksi "malli tekee 80 tokenia sekunnissa" voi olla käytännössä huonompi kokemus kuin hitaampi malli, joka pysyy lämpimänä muistissa ja saa yhteisen prefiksin hyödynnettyä.

## Ensimmäinen korjaus: lopeta turhat cold startit

Ollaman FAQ sanoo suoraan kaksi hyödyllistä asiaa:

1. mallin voi esiladata tyhjällä pyynnöllä
2. `keep_alive`-parametrilla tai `OLLAMA_KEEP_ALIVE`-ympäristömuuttujalla voi päättää, kuinka kauan malli pysyy muistissa

Oletus on dokumentaation mukaan viisi minuuttia. Se on monessa harrastajakäytössä ihan järkevä, mutta agentille liian lyhyt, jos tehtävät tulevat pieninä ryppäinä. Jos taas asetat `keep_alive`-arvon liian aggressiivisesti nollaan, maksat mallin latauksen lähes joka kierroksella uudestaan.

Käytännön sääntö:

- jos agentti tekee töitä purskeissa, pidä aktiivinen malli muistissa pidempään
- jos kone on ahdas ja vaihdat jatkuvasti mallista toiseen, seuraa samalla muistipainetta
- jos latenssi tuntuu satunnaisen huonolta, katso ensin onko ongelma juuri `load_duration`

Tämä on usein nopein voitto, koska se ei vaadi mallinvaihtoa, kvantisoinnin uusintaa eikä rautakauppaa.

## Toinen korjaus: mittaa prefill erikseen, älä arvaa

Jos `load_duration` on pieni mutta vastaus alkaa silti myöhään, syyllinen on usein prompti eikä malli. Pitkä järjestelmäohje, työkaluskeemat, keskusteluhistoria ja RAG-konteksti syötetään kaikki ensin mallin läpi ennen kuin ensimmäistäkään vastaustokenia syntyy.

Tämä näkyy käytännössä näin:

- lyhyetkin vastaukset tuntuvat hitailta
- tokenit alkavat tulla nopeasti vasta sen jälkeen kun mitään ei hetkeen tapahtunut
- jokainen lisätty ohje- tai kontekstiblokki kasvattaa alun odotusta

Siksi jokaisessa paikallisessa agentissa pitäisi ainakin kerran katsoa erikseen:

1. paljonko aikaa menee mallin lataukseen
2. paljonko aikaa menee promptin käsittelyyn
3. paljonko aikaa menee itse vastauksen generointiin

Jos et tee tätä jakoa, saatat ostaa lisää GPU-tehoa ongelmaan, joka syntyy oikeasti siitä että työnnät joka tool-kutsulla saman raskaan rungon uudestaan mallille.

## Kolmas korjaus: hyödynnä yhteinen prefiksi, jos runtime tukee sitä

llama.cpp-serverin dokumentaatiossa `cache_prompt` on oletuksena käytössä. Ideana on, että jos uusi pyyntö jakaa edellisen kanssa yhteisen prefiksin, samaa KV-välimuistia voidaan käyttää uudelleen eikä koko alkua tarvitse prosessoida taas nollasta.

Tämä sopii erityisen hyvin agentteihin, joissa:

- system prompt pysyy vakaana
- työkalumäärittelyt eivät muutu joka kutsulla
- vain viimeinen käyttäjä- tai tool-viesti vaihtuu

Tässä kohtaa iso käytännön oppi on arkkitehtuurinen, ei pelkästään mallikohtainen: pidä pyynnön alku mahdollisimman vakaana. Jos rakennat jokaisella kierroksella koko promptin eri järjestykseen, runtime ei pääse hyödyntämään yhteisiä osia yhtä hyvin.

## Mitä en tekisi ensimmäisenä

En aloittaisi näistä:

- kontekstin kasvattaminen varmuuden vuoksi maksimiin
- mallin vaihtaminen pelkän "tokeneita sekunnissa" -luvun takia
- uuden GPU:n ostaminen ennen mittausta

Ollaman FAQ muistuttaa myös, että rinnakkaisuus kasvattaa muistitarvetta: käytännössä vaadittu RAM skaalautuu `OLLAMA_NUM_PARALLEL * OLLAMA_CONTEXT_LENGTH` -kertoimella. Jos siis nostat samanaikaisuutta ja kontekstia sokkona, voit luoda itsellesi lisää muistipainetta samaan aikaan kun yrität parantaa latenssia.

## Oma nyrkkisääntö harrastajalle

Jos paikallinen agentti tuntuu hitaalta, etenisin tässä järjestyksessä:

1. varmista pysyykö malli muistissa riittävän kauan
2. mittaa erikseen `load_duration`, `prompt_eval_duration` ja `eval_duration`
3. lyhennä järjestelmäpromptia, työkaluskeemoja ja turhaa historian toistoa
4. pidä pyynnön alku vakaana, jotta prefiksin uudelleenkäyttö toimii
5. mieti vasta tämän jälkeen mallin tai raudan vaihtoa

Tämä järjestys säästää rahaa ja aikaa, koska se kohdistaa työn siihen vaiheeseen, jossa viive oikeasti syntyy.

## Johtopäätös

Paikallisen agentin hitaus ei useinkaan ala siitä kohdasta, josta dashboard näyttää näyttävimmät numerot. Usein ongelma on paljon arkisempi: malli ei pysy muistissa, prompti on paisunut tai sama alku prosessoidaan turhaan uudestaan.

Siksi hyödyllisin kysymys ei ole "kuinka nopea tämä malli on", vaan:

**kuinka nopeasti tämä agentti pääsee ensimmäiseen hyödylliseen tokeniin toistuvassa oikeassa työssä?**

Kun mittaat kylmäkäynnin, prefillin ja generoinnin erikseen, paikallisen agentin optimointi muuttuu arvailusta insinöörityöksi.

## Lähteet

- https://docs.ollama.com/faq
- https://docs.ollama.com/api/generate
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
