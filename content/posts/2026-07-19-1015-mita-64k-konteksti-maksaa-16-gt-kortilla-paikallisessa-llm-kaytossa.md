---
title: "Mitä 64k konteksti maksaa 16 Gt kortilla paikallisessa LLM-käytössä?"
date: "2026-07-19T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Paikalliset LLM:t"
  - "VRAM"
  - "Konteksti"
  - "Ollama"
---
Moni harrastaja ajattelee ensin mallin kokoa ja vasta sen jälkeen kontekstia. Paikallisessa LLM-käytössä järjestys kannattaa usein kääntää toisin päin. **Jos tavoite on oikeasti käyttää koodiapuria, agenttia tai dokumentteja penkovaa avustajaa 64k kontekstilla, 16 gigatavun näytönohjain ei ole automaattisesti liian pieni, mutta siitä tulee helposti koneen ensimmäinen käytännön raja.**

Tämän näkee suoraan nykyisestä Ollaman dokumentaatiosta. Yleinen kontekstiohje sanoo, että suurempi kontekstipituus kasvattaa muistitarvetta ja että parhaan suorituskyvyn vuoksi mallin offloadia CPU:lle kannattaa välttää. Lisäksi useat käytännön integraatiot, kuten OpenClaw ja OpenCode, suosittelevat paikallisille malleille vähintään 64k kontekstia. Tästä seuraa hyvin arkinen kysymys: **onko 16 Gt kortti vielä hyvä ostos, jos haluat käyttää paikallisia työkaluja kunnolla etkä vain lyhyttä chattia?**

## 64k ei ole vain suurempi numero

Konteksti ei kuluta muistia yksin, mutta se kasvattaa sitä työn osaa, joka ei näy pelkässä "malli on X gigatavua" -ajattelussa. Kun kontekstia nostetaan, mukaan tulevat ainakin:

- pidempi K/V-välimuisti
- runtimejen omat puskurit
- suurempi paine pitää koko ajo GPU:lla
- vähemmän tilaa mallille ja samanaikaisille pyynnöille

Ollaman kontekstiohjeessa tämä sanotaan suoraan: suurempi konteksti tarvitsee enemmän muistia. Samalla sivulla neuvotaan tarkistamaan `ollama ps` -komennolla, pysyykö ajo kokonaan GPU:ssa. Tämä on tärkeä yksityiskohta, koska paikallisen käytön ongelma ei yleensä ala kohdasta "malli ei käynnisty". Ongelma alkaa siitä, että **malli käynnistyy, mutta pitkän kontekstin kanssa käyttökokemus alkaa valua CPU-offloadin, suuremman latenssin ja kiristyvän VRAM-budjetin takia.**

## Miksi 16 Gt riittää vielä chattiin mutta alkaa kiristää työkalukäytössä

16 Gt on edelleen hyvä muistiluokka tavalliseen paikalliseen käyttöön. Kevyempi keskustelu, kohtalainen konteksti ja 7B-14B-luokan kvantisoidut mallit voivat toimia sillä aivan järkevästi. Mutta kun mukaan tulee oikea työkuorma, peli muuttuu:

- pitkä reposisältö tai dokumenttikonteksti
- agentit, jotka keräävät lisää tekstiä työkalujen kautta
- useampi yhtä aikaa auki oleva malli tai rinnakkaiset pyynnöt
- suuremmat koodimallit, joille jo 24 Gt on suositeltu taso

Ollaman OpenClaw-integraatio suosittelee vähintään 64k kontekstia paikallisille malleille. OpenCode-integraatio sanoo saman. Anthropic-yhteensopivuusohje taas toteaa suoraan, että `qwen3-coder` tarvitsee sujuvaan ajoon vähintään 24 Gt VRAMia ja että pidempi konteksti vaatii vielä enemmän. Tästä voi tehdä varovaisen mutta käytännössä hyödyllisen johtopäätöksen: **16 Gt on hyvä "ajan paikallista mallia" -luokka, mutta se ei ole enää huoleton "ajan paikallista työkalumallia 64k muistilla" -luokka.**

Tämä viimeinen lause on oma tulkintani lähteiden pohjalta, ei suora speksirivi. Dokumentaatio ei sano, että 16 Gt olisi käyttökelvoton. Se sanoo, että pitkä konteksti kasvattaa muistitarvetta ja että monet käytännön agentti- ja koodityökalut on suunniteltu 64k-luokan muistille. Siksi 16 Gt kortin omistajan pitää useammin tehdä kompromisseja mallin koon, kontekstin pituuden tai molempien kanssa.

## Miltä tämä tuntuu arjessa

Käytännössä 16 Gt kortin ongelma ei ole useimmiten dramaattinen virheviesti vaan hidas kasa pieniä myönnytyksiä:

- konteksti pudotetaan 64k:sta 32k:hon tai 16k:hon
- valitaan pienempi malli kuin oikeasti haluttaisiin
- vältetään rinnakkaisia pyyntöjä
- hyväksytään se, että osa ajosta karkaa CPU:n puolelle

Jos taas 24 Gt tai suurempi kortti pitää saman mallin ja saman kontekstin kokonaan GPU:ssa, hyöty ei näy vain "enemmän mahtuu" -tasolla. Se näkyy siinä, että kone tuntuu vakaammalta, vaste pysyy tasaisempana eikä jokaista työnkulkua tarvitse aloittaa muistibudjettia arpomalla.

## Milloin 16 Gt on yhä täysin järkevä

En pitäisi 16 Gt korttia huonona ostoksena, jos oma käyttö näyttää tältä:

- pääosin tavallista chattia tai kevyttä koodiapua
- yksi käyttäjä kerrallaan
- realistinen malli- ja kontekstibudjetti
- ei tarvetta pitää agenttityökalua jatkuvasti 64k tilassa

Silloin 16 Gt voi olla juuri oikea hinta-suorituskykykohta. Varsinkin jos vaihtoehtona on paljon kalliimpi tai kuumempi kortti, jota et oikeasti tarvitse joka päivä.

## Milloin valitsisin suoraan enemmän VRAMia

Valitsisin 24 Gt tai suuremman kortin herkemmin, jos yksikin näistä osuu omaan käyttöön:

- haluat paikallisen OpenClaw-, OpenCode- tai vastaavan työkalukäytön pitkällä muistilla
- ajat paljon koodimalleja
- et halua tarkistaa jokaisen mallin kohdalla, pysyykö ajo vielä kokonaan GPU:ssa
- haluat ostaa enemmän pelivaraa seuraavan 1-2 vuoden mallikasvulle

Tässä tapauksessa lisä-VRAM ei ole luksusta vaan tapa ostaa pois jatkuvaa säätöä.

## Oma nyrkkisääntöni

Jos kysymys on "riittääkö 16 Gt paikalliseen LLM:ään", vastaus on usein kyllä. Jos kysymys on "riittääkö 16 Gt hyvään 64k-kontekstiseen paikalliseen työkalukäyttöön", vastaus muuttuu paljon varovaisemmaksi.

Sanoisin sen näin:

- `16 Gt`: hyvä paikallisen mallin perusluokka
- `24 Gt+`: paljon turvallisempi luokka, jos 64k konteksti ja työkalut ovat oikeasti osa arkea

Paikallisessa LLM-koneessa nopein tapa pettyä ei yleensä ole ostaa liian hidasta GPU:ta. Se on ostaa juuri sen verran liian vähän muistia, että malli toimii vain silloin kun käytät sitä varovaisemmin kuin oikeasti haluaisit.

## Lähteet

- https://docs.ollama.com/context-length
- https://docs.ollama.com/integrations/openclaw
- https://docs.ollama.com/integrations/opencode
- https://docs.ollama.com/api/anthropic-compatibility
