---
title: "Miksi paikallinen agentti hajoaa ennen kuin 128k konteksti täyttyy"
date: "2026-07-26T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoaly ja agentit"
tags:
  - "agent"
  - "context-window"
  - "ollama"
  - "llama.cpp"
  - "local-llm"
---
## Missä kohtaa ongelma alkaa
Yleinen kotilabran oire on tämä: malli toimii lyhyessä chatissa hyvin, mutta agentti alkaa pidemmässä tehtävässä sekoilla, hidastua tai kaatua, vaikka paperilla kontekstiikkunaa pitäisi olla runsaasti jäljellä. Syynä on usein se, että paikallinen agentti kuluttaa muistia ja kontekstia aivan eri tavalla kuin pelkkä keskustelumalli.

## Ongelma ei ole vain "liian pitkä prompti"

Tavallisessa chatissa on helppo kuvitella, että konteksti on yksi putki: käyttäjän viestit sisään, vastaukset ulos. Agentissa mukana kulkee enemmän tavaraa:

- järjestelmäohje
- työkaluskeemat
- aiemmat työkalukutsut
- työkalujen palauttamat tulokset
- mahdolliset välivaiheet, lokit ja haetut dokumenttipätkät

Siksi käytännön raja tulee vastaan usein ennen kuin nimellinen 128k olisi "täynnä". Ongelma ei ole vain tokenimäärä, vaan myös se, että agentin historia pitää säilyttää ehjänä rakenteena.

Open WebUI:n vianhakudokumentaatio kuvaa tämän hyvin: kun tool calling on päällä, assistantin työkalukutsu ja tool-vastaus muodostavat parin. Jos historiaa typistetään huolimattomasti keskeltä, lopputuloksena voi olla virheellinen rakenne eikä vain lyhyempi keskustelu. Toisin sanoen agentti voi rikkoutua jo ennen puhdasta kontekstirajaa, jos muistia hallitaan väärin.

## Ollaman viesti on käytännössä selvä

Ollaman nykyinen context length -dokumentaatio sanoo kaksi tärkeää asiaa suoraan:

1. oletuskonteksti riippuu käytettävissä olevasta VRAMista
2. web searchia, agentteja ja coding tools -tyyppisiä töitä varten konteksti kannattaa nostaa vähintään 64k tokeniin

Tämä on minusta hyvä reality check. Jos ajat paikallista agenttia 4k- tai 8k-ikkunassa, ongelma ei yleensä ole se että agentti olisi "tyhmä". Sillä ei vain ole tarpeeksi työtilaa.

Mutta tästä ei pidä vetää väärää johtopäätöstä. 128k ei ole automaattisesti parempi kuin 64k, jos suurempi ikkuna pakottaa mallin osittain CPU:lle tai syö kaiken muistin muulta kuormalta.

## Miksi iso konteksti voi olla silti huono valinta

llama.cpp:n multi-GPU-ohje muistuttaa, että `--ctx-size` vaikuttaa suoraan siihen, mahtuuko kokonaisuus muistibudjettiin. Sama ohje sanoo käytännössä myös tämän: jos saat OOM-virheitä, yksi ensimmäisistä korjausliikkeistä on pienentää `--ctx-size`, koska KV-välimuistin koko kasvaa suunnilleen suhteessa kontekstin kokoon.

Tämä on se kohta, jonka moni ohittaa. Paikallisessa agentissa et maksa pitkästä kontekstista vain tokeneina vaan muistina:

- suurempi `ctx-size` kasvattaa KV-välimuistia
- useampi rinnakkainen pyyntö kasvattaa varauksia lisää
- pidemmät työkalutulokset tekevät prefilleistä raskaampia
- jos malli ei enää mahdu siististi GPU:lle, nopeus romahtaa helposti

Jos siis nostat kontekstin varmuuden vuoksi maksimiin, voit samalla tehdä agentista hitaamman ja epävakaamman.

## Rinnakkaisuus tekee asiasta vielä vaikeamman

llama.cpp-projektissa käyty paged KV cache -keskustelu avaa hyvän taustan tälle. Nykyinen yhtenäinen KV-cache varaa muistia mallilla, jossa enimmäiskonteksti ja sekvenssien määrä lukitsevat suuren puskurin etukäteen. Käytännön seuraus on, että sallittu rinnakkaisuus määräytyy pahimman tapauksen mukaan, ei keskimääräisen työn mukaan.

Tämä näkyy kotilabrassa näin:

- yksi pitkä agenttisessio voi syödä tilaa usealta lyhyeltä
- suureksi asetettu maksimi rajoittaa samanaikaisia ajoja
- muisti loppuu juuri silloin kun agentti käyttää useita työkaluja ja pisintä historiaa

Jos ajat vain yhtä chattia kerrallaan, tämä ei ehkä haittaa. Mutta heti kun mukana on cron, editoriagentti, toinen taustatehtävä tai web-haku, kontekstiasetus muuttuu kapasiteettipäätökseksi.

## Oma nyrkkisääntöni paikalliselle agentille

Minun sääntöni on tämä:

- aloita sellaisesta kontekstista, jonka kone jaksaa varmasti pitää GPU-painotteisena
- kasvata ikkunaa vasta kun näet oikeita katkeamisia pitkissä työlenkeissä
- lyhennä ja tiivistä työkalujen tuloksia ennemmin kuin kasvatat kontekstia loputtomasti
- rajoita rinnakkaisuutta ennen kuin syytät itse mallia

Jos käytössä on pieni tai keskikokoinen paikallinen kone, 32k voi riittää yksinkertaisiin työkalukierroksiin. Kun mukana on koodihakua, web-hakua tai useita työkaluvaiheita, 64k on usein realistisempi lähtötaso. Sen jälkeen seuraava päivitys ei välttämättä ole 128k konteksti vaan parempi muistinhallinta, tiiviimpi tool loop tai pienempi rinnakkaisuus.

## Mitä säätäisin ensin käytännössä

Jos paikallinen agentti alkaa pätkiä, etenisin tässä järjestyksessä:

1. Tarkista, onko konteksti selvästi liian pieni agenttikäyttöön.
2. Tarkista, onko pitkä konteksti pakottanut mallin osittain CPU:lle.
3. Lyhennä työkalujen palautuksia ja keskusteluhistoriaa rakenteisesti, ei sokkona keskeltä.
4. Laske rinnakkaisuutta, jos sama kone ajaa useita sessioita.
5. Nosta `ctx-sizea` vasta sen jälkeen.

Tärkein oivallus on yksinkertainen: paikallisessa agentissa konteksti ei ole vain mallin ominaisuus vaan myös muistibudjetin ja palvelukapasiteetin asetus.

## Johtopäätös

Jos agentti hajoaa ennen kuin 128k täyttyy, se ei tarkoita että mallikortti valehteli. Usein se tarkoittaa, että käytössä oleva työkalusilmukka, historia, KV-cache ja rinnakkaisuus eivät mahdu yhteen sillä tavalla kuin kuvittelit.

Siksi en kysyisi ensimmäisenä "kuinka suuren kontekstin tämä malli tukee", vaan "millä kontekstilla tämä agentti pysyy kokonaan hyödyllisenä juuri minun koneellani". Se on paljon käytännöllisempi mittari kuin yksittäinen maksiminumero.

## Lähteet

- https://docs.ollama.com/context-length
- https://docs.openwebui.com/troubleshooting/context-window/
- https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md
- https://github.com/ggml-org/llama.cpp/discussions/21961
