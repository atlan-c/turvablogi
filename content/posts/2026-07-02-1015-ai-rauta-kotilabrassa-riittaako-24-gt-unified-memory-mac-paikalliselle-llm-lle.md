---
title: "AI-rauta kotilabrassa: riittääkö 24 Gt unified memory Mac paikalliselle LLM:lle?"
date: "2026-07-02T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-rauta kotilabrassa"
tags:
  - "AI-rauta"
  - "Apple Silicon"
  - "Unified memory"
  - "Ollama"
  - "Paikalliset LLM:t"
---
Kun paikallista LLM-konetta mietitään Macille, vanha kysymys oli pitkään "riittääkö 16 gigaa". Vuonna 2026 käytännöllisempi kysymys on tämä: **riittääkö 24 Gt unified memory Mac paikalliseen LLM-käyttöön vai kannattaako hypätä heti ylempään muistiluokkaan?** Oma lyhyt vastaukseni on: **24 Gt riittää hyvin yhdelle käyttäjälle, yhdelle mallille ja kohtalaiselle kontekstille, mutta se ei ole huoleton valinta, jos haluat pitää useita malleja lämpimänä, kasvattaa kontekstia tai tehdä samaan aikaan muuta raskasta työtä.**

Tärkein syy on Apple Siliconin rakenne. Erillisen näytönohjaimen VRAMia ja järjestelmä-RAMia ei ole erikseen, vaan sama unified memory ruokkii sekä käyttöjärjestelmää että mallia. Siksi "24 Gt kone" ei tarkoita käytännössä 24 gigaa LLM:lle, vaan 24 gigaa koko järjestelmälle.

## Miksi 24 Gt tuntuu paperilla isommalta kuin se oikeasti on

Ollaman dokumentaation mukaan Apple-laitteilla GPU-kiihdytys tapahtuu Metalin kautta. Se on hyvä uutinen, koska paikalliset mallit osaavat käyttää Apple GPU:ta suoraan ilman erillistä CUDA- tai ROCm-rumbaa. Huono uutinen on se, että sama muistipooli palvelee kaikkea muutakin: selainta, editoria, Spotlightia, taustaprosesseja ja itse mallia.

Apple neuvoo katsomaan Activity Monitorista erityisesti `Memory Pressure`-, `Compressed`- ja `Swap Used` -mittareita. Tämä on paikallisen LLM:n kannalta paljon tärkeämpi tapa arvioida koneen sopivuutta kuin pelkkä myyntisivun muistimäärä. Jos memory pressure pysyy vihreänä, järjestelmä on vielä mukavuusalueella. Jos paine muuttuu keltaiseksi ja swap alkaa kasvaa heti pidemmässä ajossa, olet jo lähellä rajaa vaikka malli "mahtuisi" käynnistymään.

## Mitä 24 Gt yleensä riittää tekemään

Pidän 24 Gt unified memorya järkevänä miniminä, jos käyttö näyttää tältä:

1. ajat yhtä mallia kerrallaan
2. pidät kontekstin maltillisena
3. et nosta rinnakkaisten pyyntöjen määrää
4. et tee samalla koneella raskasta videotyötä, Docker-kuormaa tai suurta IDE-projektia

Tällaisessa käytössä 24 Gt Mac voi olla oikein miellyttävä paikallinen LLM-kone. Käytännössä se sopii hyvin henkilökohtaiseen chattiin, muistiinpanojen tiivistämiseen, kevyeen koodiapuun ja satunnaiseen agenttikäyttöön, jossa yksi malli tekee yhden asian kerrallaan.

Ollaman FAQ tukee tätä käytännön havaintoa epäsuorasti mutta tärkeällä tavalla: tarvittava RAM kasvaa sekä kontekstin että rinnakkaisten pyyntöjen mukana, ja jos muistia ei ole tarpeeksi, uudet pyynnöt joutuvat odottamaan tai malleja puretaan pois muistista. Toisin sanoen 24 Gt ei yleensä hajoa ensimmäiseen demoon, mutta se alkaa tuntua pieneltä heti kun käyttö muuttuu "yksi prompti silloin tällöin" -tasosta jatkuvaksi työksi.

## Missä kohtaa 24 Gt alkaa kiristää

24 Gt:n luokka alkaa minusta olla liian tiukka, jos jokin näistä pitää paikkansa:

- haluat käyttää pitkää kontekstia säännöllisesti
- haluat pitää useita malleja valmiina muistissa
- aiot nostaa rinnakkaisten pyyntöjen määrää
- käytät samaa konetta vakavaan kehitystyöhön, selaimen välilehtiviidakkoon ja LLM-ajoon yhtä aikaa
- tavoite ei ole vain "toimii", vaan "toimii ilman että muistinkäyttöä tarvitsee vahtia"

Tässä kohtaa unified memoryn varjopuoli näkyy selvästi. Erillisellä GPU:lla voit joskus ajatella, että järjestelmä-RAM ja VRAM ovat eri ongelmia. Macilla ne ovat sama ongelma. Jos IDE, selain ja malli syövät kaikki samasta kulhosta, joustovaraa on vähemmän kuin moni ensi silmäyksellä odottaa.

## Käytännön ostopolku vuonna 2026

Tämänhetkisissä Apple-kokoonpanoissa 24 Gt ei ole enää vain "pro-koneiden erikoisuus". Esimerkiksi MacBook Airin M5-malli on saatavilla 24 tai 32 Gt unified memorylla, ja MacBook Pron M5 Pro -luokka alkaa 24 Gt:stä ja skaalautuu paljon ylemmäs. Tämä on hyvä kehitys, koska 24 Gt on paljon uskottavampi lähtötaso paikallisille malleille kuin vanhat 8-16 Gt kuluttajamallit.

Silti ostosuositukseni on aika selkeä:

1. Osta 24 Gt, jos haluat yhden hyvän henkilökohtaisen paikallisen LLM-koneen etkä odota siltä monen mallin laboratoriota.
2. Osta 32-48 Gt tai enemmän, jos haluat pidemmän käyttöiän, enemmän kontekstia ja vähemmän muistibudjetin vahtimista.
3. Osta isompi muistiluokka heti, jos tiedät jo nyt että käytät agentteja, paljon taustasovelluksia tai pidät useita työkuormia käynnissä samanaikaisesti.

Macissa muistia ei yleensä päivitetä jälkikäteen, joten tämä päätös kannattaa tehdä kerran kunnolla. Minusta juuri tässä kohdassa moni säästää väärässä paikassa: prosessorin yksi lisäydin ei yleensä muuta paikallisen LLM:n arkea yhtä paljon kuin yksi muistiluokka ylöspäin.

## Oma nyrkkisääntöni

Jos kysyt minulta "riittääkö 24 Gt", vastaan näin:

- kyllä, jos käyttö on yhden käyttäjän, yhden mallin ja kurinalaisen kevyt
- ehkä, jos käyttö on sekalainen mutta olet valmis elämään muistibudjetin kanssa
- ei, jos haluat huoletonta kasvunvaraa

Siksi pitäisin 24 Gt unified memorya **kelvollisena miniminä**, en ihannetasona. Se on paljon parempi lähtökohta kuin vanha 16 Gt, mutta se ei poista sitä perusfysiikkaa, että paikallinen malli, käyttöjärjestelmä ja muu työkuorma taistelevat kaikki samasta muistista.

## Tiivis johtopäätös

**24 Gt unified memory Mac riittää paikalliselle LLM:lle, kun käyttö on yksinkertaista ja ennustettavaa.** Se ei kuitenkaan ole automaattinen "osta tämä ja unohda muistirajat" -luokka. Jos haluat vain oman paikallisen tekoälyassistentin ja käytät yhtä mallia kerrallaan, 24 Gt voi olla erittäin järkevä valinta. Jos taas haluat enemmän rinnakkaisuutta, enemmän kontekstia tai enemmän työrauhaa, suurempi muistiluokka maksaa itsensä takaisin yllättävän nopeasti.

Paras käytännön testi oston jälkeen on tylsä mutta luotettava: avaa Activity Monitor, aja oma oikea työkuormasi ja katso memory pressurea sekä swapin kasvua. Jos ne pysyvät kurissa, kone on sinulle riittävä. Jos eivät pysy, ongelma ei ole "huono optimointi" vaan liian pieni muistibudjetti juuri siihen käyttöön.

## Lähteet

- https://docs.ollama.com/gpu
- https://docs.ollama.com/faq
- https://support.apple.com/guide/activity-monitor/view-memory-usage-actmntr1004/mac
- https://support.apple.com/en-us/126320
- https://support.apple.com/en-us/126318
