---
title: "Kannattaako 24 Gt VRAM paikalliselle LLM-harrastajalle vuonna 2026?"
date: 2026-03-17T10:15:00+02:00
draft: false
---

24 gigatavua VRAMia on tällä hetkellä monelle harrastajalle se houkuttelevin raja: käytettyjä 3090-kortteja löytyy edelleen, uudemmissa korteissa muistimäärä ei aina kasva samassa suhteessa kuin hinta, ja juuri 24 Gt kuulostaa paperilla siltä pisteeltä, jossa "oikeat" paikalliset mallit alkavat onnistua. Käytännössä kysymys ei kuitenkaan ole vain siitä, mahtuuko malli käynnistymään, vaan siitä, **mahtuuko se kokonaan GPU:lle, millä kvantisoinnilla, ja mitä tapahtuu kun konteksti pitenee**.

Lyhyt vastaus: 24 Gt VRAM on edelleen erittäin käyttökelpoinen määrä paikalliseen LLM-käyttöön, mutta se on paras erityisesti 7B–14B-luokan malleille ja osalle keskikokoisista malleista kvantisoituina. Jos tavoite on ajaa 70B-luokan mallia mukavasti, 24 Gt ei ole enää "huoleton" taso vaan kompromissi, jossa offload, kvantisointi ja realistinen konteksti ratkaisevat paljon.

## Mitä 24 Gt oikeasti ostaa?

Hugging Facen Llama 3.1 -muistiyhteenveto antaa hyvän karkean mittakaavan: 8B-malli tarvitsee noin 16 Gt FP16-muodossa, 8 Gt FP8:na ja noin 4 Gt INT4:nä. 70B-malli taas nousee noin 140 Gt FP16:na, 70 Gt FP8:na ja noin 35 Gt INT4-tasolla. Taulukko ei suoraan kuvaa jokaista GGUF-ajotapaa, mutta käytännön viesti on selvä: 24 Gt riittää hyvin pienille ja keskisuurille malleille, mutta ei tee 70B-luokasta automaattisesti helppoa yhden kortin käyttöä.

Tämä on juuri se kohta, jossa moni ostaa väärin perustein. Jos katsot vain mallin parametreja tai yhtä benchmark-kuvaa, 24 Gt näyttää "melkein rajattomalta". Kun taas katsot muistia realistisesti, 24 Gt on ennen kaikkea **mukava yhden GPU:n harrastajaluokka**, ei universaali ratkaisu kaikkiin malleihin.

## Missä 24 Gt on parhaimmillaan?

24 Gt on vahva valinta, jos oma käyttösi näyttää tältä:

- ajat 7B–14B-instruct-malleja päivittäisiin tehtäviin
- haluat pitää mallin kokonaan GPU:lla ilman jatkuvaa CPU-sekoilua
- käytät kohtuullista kontekstia etkä väkisin 64k–128k ikkunoita joka ajossa
- arvostat hyvää vasteaikaa enemmän kuin sitä, että saat juuri ja juuri käyntiin mahdollisimman suuren mallin

Tässä profiilissa 24 Gt on usein parempi kuin "isompi mutta osittain CPU:lla roikkuva" ratkaisu. Paikallisen mallin käyttökokemus paranee eniten silloin, kun generointi pysyy tasaisena ja työkuorma on mahdollisimman paljon GPU:lla.

## Missä 24 Gt alkaa kiristää?

Raja tulee vastaan kolmessa tilanteessa.

Ensimmäinen on selvä: malli on yksinkertaisesti liian suuri. Jos tähtäät 70B-luokkaan, 24 Gt riittää korkeintaan aggressiivisesti kvantisoituihin kompromisseihin tai osittaiseen GPU-ajoon. Se voi silti olla hyödyllinen kokeiluun, mutta ei enää se luokka, josta kannattaa odottaa vaivatonta arkea.

Toinen raja on pitkä konteksti. Vaikka painot mahtuisivat, kontekstin kasvaessa myös KV-cache syö muistia. Hugging Facen yhteenveto muistuttaa tästä suoraan: mallin painojen lisäksi myös välimuisti tarvitsee tilaa, ja pitkässä kontekstissa siitä tulee nopeasti merkittävä osa kokonaiskulutusta.

Kolmas raja on se, että moni luulee hitauden johtuvan aina liian pienestä GPU:sta. llama.cpp:n suorituskykyohje sanoo suoraan, että väärä `--threads`-arvo voi tehdä generoinnista yllättävän hidasta, ja että GPU-offload pitää varmistaa diagnostiikkariveistä eikä vain olettaa sen toimivan. Toisin sanoen 24 Gt kortti voi tuntua "liian hitaalta", vaikka todellinen ongelma olisi säikeissä tai siinä, ettei mallia ole oikeasti offloadattu kunnolla GPU:lle.

## Käytännön ostosääntö: osta käyttötavan, älä maksimimallin mukaan

Jos mietit 24 Gt korttia paikallisia malleja varten, kysy ensin tätä:

**Mitä ajan suurimman osan ajasta?**

Jos vastaus on:

- koodiapuri
- kirjoittaminen
- yhteenvetojen teko
- pieni RAG omille dokumenteille
- kevyt agenttityö tai komentorivikäyttö

...niin 24 Gt on erittäin järkevä. Se on usein se piste, jossa 8B–14B-luokan mallit tuntuvat oikeasti mukavilta käyttää, ja jossa voi vielä kokeilla joitakin suurempia kvantisointeja ilman että koko kokemus romahtaa.

Jos taas vastaus on:

- haluan aina parhaan mahdollisen suuren mallin paikallisesti
- haluan pitkän kontekstin ilman kompromisseja
- haluan ajaa useita raskaita sessioita rinnakkain samalla GPU:lla

...niin 24 Gt on enemmän välipysäkki kuin päätepiste.

## Miten testata ennen kuin syytät rautaa?

Ennen kuin päätät, että tarvitset lisää VRAMia, tarkista nämä:

1. **Onko malli oikeasti GPU:lla?** Ollaman FAQ neuvoo katsomaan `ollama ps`-komennolla, näkyykö ajossa `100% GPU` vai sekakäyttö CPU/GPU.
2. **Onko konteksti realistinen?** Oletuskonteksti on Ollamassa 4096 tokenia. Jos nostat `num_ctx`-arvoa reilusti, muistinkulutus kasvaa nopeasti.
3. **Onko säiemäärä pielessä?** llama.cpp suosittelee testaamaan myös pienemmillä thread-arvoilla, koska liian suuri säiemäärä voi ylisaturoida CPU:n ja sotkea suorituskyvyn.
4. **Onko ongelma laatu vai nopeus?** Jos malli on liian pieni tarpeeseesi, lisä-VRAM ei yksin ratkaise sitä. Jos taas laatu riittää mutta ajo on epätasaista, enemmän VRAMia tai parempi offload voi auttaa paljon.

Tämä järjestys säästää rahaa. Yllättävän usein pullonkaula ei ole heti kortin muistimäärä vaan väärä käyttöprofiili tai huonosti säädetty runtime.

## Oma suositus harrastajalle

Pidän 24 Gt VRAMia edelleen parhaana "vakava mutta vielä järkevä" -luokkana paikalliseen LLM-harrastukseen. Se ei ole halpa, mutta se on usein ensimmäinen muistimäärä, jossa käyttö tuntuu oikealta työkalulta eikä jatkuvalta taistelulta. Samalla on hyvä pitää odotukset kurissa: 24 Gt ei tee yhdestä GPU:sta rajatonta AI-palvelinta.

Jos haluat yhden käytännön nyrkkisäännön, se on tämä: **osta 24 Gt VRAM, jos tähtäät sujuvaan arkeen 7B–14B-luokassa ja haluat vähän kasvunvaraa; älä osta sitä kuvitellen, että 70B-luokka muuttuu yhdellä iskulla helpoksi.**

Juuri siksi 24 Gt on hyvä ostos monelle harrastajalle, mutta huono ostos väärällä tarinalla perusteltuna.

## Lähteet

- Hugging Face – Llama 3.1 inference memory requirements: https://huggingface.co/blog/llama31#inference-memory-requirements
- llama.cpp – Token generation performance tips: https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md
- Ollama FAQ – context size and GPU visibility: https://docs.ollama.com/faq
