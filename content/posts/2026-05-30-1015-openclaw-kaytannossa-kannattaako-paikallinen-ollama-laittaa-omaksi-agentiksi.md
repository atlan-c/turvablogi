---
title: "OpenClaw käytännössä: kannattaako paikallinen Ollama laittaa omaksi agentiksi?"
date: "2026-05-30T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Ollama"
  - "Local LLM"
  - "Automation"
---
Paikallinen malli kuulostaa OpenClawissa houkuttelevalta oletusratkaisulta: data pysyy kotona, kustannus per ajo voi pudota rajusti ja testailu nopeutuu heti. Silti käytännössä **paikallinen Ollama tai muu OpenAI-yhteensopiva palvelin kannattaa usein laittaa ensin omaksi agentikseen, ei koko setupin oletusmalliksi**. Syy ei ole ideologinen vaan tekninen: paikallinen malli voi olla aivan riittävä rajattuihin töihin, mutta koko agenttilooppi on herkempi konteksti-ikkunalle, työkalukutsuille, viiveelle ja API-yhteensopivuuden pienille eroille kuin tavallinen yksittäinen chat-kutsu.

Minun käytännön suositukseni on tämä: **pidä pääagentti sellaisessa mallissa, johon luotat vaikeissa tehtävissä, ja anna paikalliselle mallille oma agentti tai halpa sub-agentti taustatutkimukseen, luonnoksiin ja toistuviin rajattuihin ajoihin.** Näin saat paikallisen mallin hyödyt ilman että koko järjestelmä alkaa horjua sen heikoimmista kohdista.

## Miksi sama malli ei aina sovi koko OpenClaw-pinoon

OpenClawin paikallisia malleja koskeva ohje on tarkoituksella varovainen. Dokumentaatio muistuttaa, että paikalliset mallit nostavat laitteisto-, konteksti- ja turvallisuusvaatimuksia, ja että pienet tai aggressiivisesti kvantisoidut mallit ovat alttiimpia prompti-injektion ja katkeilevan kontekstin ongelmille. Tämä on tärkeä käytännön huomio, koska OpenClaw ei lähetä mallille vain yhtä pientä käyttäjäviestiä, vaan usein mukaan tulee myös työkalupintaa, järjestelmäohjeita, workspace-kontekstia ja joskus pitkiäkin välituloksia.

Toisin sanoen paikallinen malli voi näyttää hyvältä pienessä testikutsussa mutta silti kompastua oikeassa agenttisilmukassa.

## Miksi oma agentti on turvallisempi kuin oletusmallin vaihto

OpenClawin agenttikonfiguraatio tukee per-agentti-mallia. Dokumentaation mukaan `agents.list[]`-määrityksissä agentille voi antaa oman `model`-arvon, jolloin yksi agentti voi käyttää eri mallia kuin koko järjestelmän oletus. Samalla sub-agenttiopas suosittelee suoraan pitämään pääagentin laadukkaammassa mallissa ja siirtämään raskaat tai toistuvat työt halvemmille malleille.

Tämä on juuri se rakenne, jota suosittelisin paikallisen Ollaman kanssa:

- pääagentti hoitaa korkean epävarmuuden tehtävät, joissa työkalukutsujen pitää osua oikein
- paikallinen agentti tekee rajatut luonnokset, yhteenvedot ja luokittelut
- tarvittaessa pääagentti delegoi työn sub-agentille eikä vaihda koko persoonansa tai oletusmallinsa toimintatapaa

Kun eristät paikallisen mallin omaksi agentikseen, rajoitat samalla vikapinta-alaa. Jos malli alkaa hallusinoida työkalunimiä, jumiutuu pitkään kontekstiin tai yksinkertaisesti hidastuu liikaa, koko pääkäyttö ei kaadu mukana.

## Ollama on yhteensopiva, mutta se ei poista mallikohtaista kitkaa

Ollaman OpenAI-yhteensopivuusdokumentaatio on tässä hyvä uutinen ja samalla pieni varoitus. Hyvä uutinen on se, että Ollama tarjoaa OpenAI-yhteensopivia rajapintoja ja tukee nykyään myös `v1/responses`-polkua. Tämä tekee sen liittämisestä OpenClawiin paljon helpompaa kuin vielä aiemmin.

Varoitus on se, että yhteensopivuus ei tarkoita automaattisesti samaa käyttökokemusta kuin vahvassa pilvimallissa. Dokumentaatio kertoo esimerkiksi, että `v1/responses`-rajapinta on Ollamassa ei-tilallinen, eikä OpenAI-API tarjoa suoraa tapaa säätää konteksti-ikkunaa pyynnön sisällä. Käytännössä tämä tarkoittaa, että mallin koko, `num_ctx`, työkalukäytös ja viive vaikuttavat edelleen paljon siihen, kuinka vakaasti agentti toimii.

Jos siis paikallinen malli toimii hienosti suorassa `chat.completions`-testissä, siitä ei vielä seuraa, että se olisi heti paras koko OpenClaw-agentin oletusmoottori.

## Llama.cpp-palvelin on hyvä vaihtoehto, mutta rajat kannattaa tuntea

Sama ajatus pätee myös `llama.cpp`:n `llama-server`-polkuun. Projektin dokumentaatio kuvaa sen kevyeksi OpenAI-yhteensopivaksi HTTP-palvelimeksi, ja `v1/chat/completions`-yhteensopivuus tekee siitä hyödyllisen erityisesti itse rakennetuille GGUF-seteille.

Silti käytännön raja on hyvä tiedostaa: `llama-server`-dokumentaatio korostaa ennen kaikkea chat completion -yhteensopivuutta, ja vielä vuonna 2026 projektissa on erikseen avoin ominaisuuspyyntö `v1/responses`-tuen laajentamisesta. Tästä en vetäisi johtopäätöstä, että `llama.cpp` olisi huono valinta. Vetäisin johtopäätöksen, että **mitä enemmän paikallinen backend poikkeaa OpenClawin pääpolusta, sitä järkevämpää on pitää se ensin rajatussa agentissa eikä koko järjestelmän oletusmallina**.

## Milloin paikallinen malli kannattaa ehdottomasti eriyttää

Minusta erillinen agentti on selvästi parempi ratkaisu ainakin näissä tilanteissa:

- käytät 7B- tai 8B-luokan mallia rajallisella VRAMilla
- vasteaika kasvaa paljon heti kun prompti pitenee
- työkalukutsut onnistuvat vain osan aikaa
- backend on OpenAI-yhteensopiva "riittävästi", mutta ei aivan samalla tavalla kuin vahvin pilvipolku
- haluat ajaa paljon halpoja taustatöitä ilman että tärkein keskustelu hidastuu

Tällöin paikallinen agentti voi olla erinomainen esimerkiksi:

- pitkien lokien tiivistämiseen
- raakatekstin luokitteluun
- luonnosten kirjoittamiseen
- hakutulosten ensimmäiseen seulontaan
- ei-kriittisiin kokeiluihin uudella mallilla

Näissä tehtävissä pieni epätarkkuus ei yleensä riko koko työnkulkua.

## Milloin paikallinen malli voi olla myös oletusmalli

Reiluuden vuoksi: joskus paikallinen malli voi olla myös oikea oletus. OpenClawin paikallismalliopas sanoo suoraan, että ennen varsinaisia agenttiajoja kannattaa testata sekä palvelimen OpenAI-yhteensopivuus että kevyempi paikallinen inferenssipolku. Jos nämä testit menevät läpi mutta oikeat agenttiajot edelleen takkuavat, dokumentaatio ehdottaa jopa `localModelLean`-asetuksen kokeilemista, jotta promptikuorma kevenee.

Tästä voi päätellä, että koko järjestelmän vieminen paikalliseen malliin on realistista vasta, kun nämä asiat pitävät:

- backend vastaa luotettavasti OpenAI-yhteensopivilla pääpoluilla
- konteksti riittää oikeaan agenttikäyttöön, ei vain pikkupromptiin
- työkalukäyttö pysyy vakaana
- laitteisto kestää viiveen ilman että käyttökokemus hajoaa

Jos nämä ehdot täyttyvät, oletusmallin vaihto voi olla täysin järkevä. Mutta jos yksikin niistä epäilyttää, aloittaisin erillisestä agentista.

## Käytännön etenemisjärjestys, joka säästää hermoja

Jos rakentaisin tämän nollasta tänään, etenisin näin:

1. Kytke Ollama tai `llama-server` OpenAI-yhteensopivana providerina.
2. Testaa ensin pieni paikallinen inferenssikutsu eikä koko agenttia.
3. Tee paikalliselle mallille oma agentti, jolla on selkeä tehtävärajaus.
4. Anna pääagentin delegoida vain sellaiset työt, joissa pieni laatuero ei ole kohtalokas.
5. Vasta tämän jälkeen harkitse, kannattaako paikallisesta mallista tehdä oletus.

Tämä järjestys tuntuu ehkä varovaiselta, mutta käytännössä se on nopeampi kuin koko setupin kääntäminen kerralla väärään malliin ja ongelmien etsiminen jälkikäteen.

## Yhteenveto

Kannattaako paikallinen Ollama laittaa omaksi agentiksi? **Useimmiten kyllä.** Se on siistein tapa hyödyntää paikallista LLM:ää silloin, kun haluat säästää rahaa ja pitää datan lähellä, mutta et halua altistaa koko OpenClaw-kokemusta paikallisen mallin konteksti-, latenssi- tai yhteensopivuusrajoille.

Minun nyrkkisääntöni on yksinkertainen: **jos paikallinen malli ei ole jo todistanut pärjäävänsä oikeassa agenttisilmukassa, älä tee siitä heti oletusmallia. Tee siitä oma agentti, anna sille rajatut työt ja ylennä se vasta sitten, jos käytäntö todella tukee päätöstä.**

## Lähteet

- https://docs.openclaw.ai/gateway/local-models
- https://docs.openclaw.ai/gateway/config-agents
- https://docs.openclaw.ai/subagents
- https://docs.ollama.com/api/openai-compatibility
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- https://github.com/ggml-org/llama.cpp/issues/19138
