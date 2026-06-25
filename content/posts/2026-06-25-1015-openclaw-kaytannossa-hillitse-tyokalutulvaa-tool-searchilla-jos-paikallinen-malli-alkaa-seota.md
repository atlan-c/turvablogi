---
title: "OpenClaw käytännössä: hillitse työkalutulvaa `tool_search`illa, jos paikallinen malli alkaa seota"
date: "2026-06-25T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Local Models"
  - "Tool Search"
  - "Automation"
---
Paikallista mallia ajaessa ongelma ei ole aina itse malli vaan se, **kuinka paljon tavaraa sille dumpataan heti vuoron alussa**. Jos OpenClaw-runissa on iso työkalupinta, pitkä keskusteluhistoria ja ehkä vielä MCP- tai plugin-katalogeja, pienempi paikallinen backend alkaa helposti oireilla oudosti: työkalukutsut menevät väärin, malli unohtaa että työkaluja edes on, tai koko pyyntö paisuu tarpeettoman raskaaksi.

Oma käytännön sääntöni on tämä: **jos paikallinen malli toimii muuten, mutta täysi agenttivuoro alkaa hajota työkalujen kanssa, yritän ensin pienentää näkyvää työkalupintaa enkä heti vaihda mallia**. OpenClawissa tähän on kaksi eri polkua, jotka on helppo sekoittaa:

- yleisissä OpenClaw-ajoissa voi käyttää `tools.toolSearch`-ominaisuutta
- heikommille paikallisille malleille voi lisäksi ottaa käyttöön `experimental.localModelLean`
- Codex-harness-ajoissa taas nojataan Codexin omaan searchable-työkalupintaan, ei tähän kokeelliseen OpenClaw Tool Searchiin

Juuri tämän eron ymmärtäminen säästää paljon turhaa säätöä.

## Mistä tunnistat työkalutulvan

OpenClawin experimental features -dokumentaatio kuvaa paikallisen mallin lean-tilan nimenomaan paineenpurkuventtiiliksi tilanteeseen, jossa pienempi tai tiukempi backend tukehtuu täyteen työkalupintaan. Minusta tuo on hyvä ajattelumalli, koska ongelma näkyy usein näin:

1. Malli vastaa yksinkertaiseen testipromptiin ihan oikein.
2. Varsinainen agenttivuoro epäonnistuu vasta silloin, kun mukana ovat työkalut ja oikea konteksti.
3. Virhe näyttää malliongelmalta, vaikka todellinen ongelma on liian iso tai liian monimutkainen työkalukuorma.

Tyypillisiä oireita ovat esimerkiksi:

- malli antaa vapaan tekstivastauksen, vaikka työkalua pitäisi käyttää
- työkalukutsu menee väärällä parametrilla tai väärään työkaluun
- OpenAI-yhteensopiva paikallinen palvelin palauttaa virheen liian isosta työkalupayloadista
- pitkä keskustelu toimii huonommin heti sen jälkeen, kun mukaan lisätään iso joukko työkaluja

Tässä kohtaa en ensimmäisenä osta uutta GPU:ta enkä vaihda koko työnkulkua. Yritän ensin tehdä näkyvästä työkalupinnasta kapeamman.

## Mitä `tools.toolSearch` oikeasti tekee

OpenClawin Tool Search -sivu sanoo asian suoraan: sen idea on antaa agentille yksi kompakti tapa löytää ja kutsua suuri työkalukatalogi ilman, että kaikki skeemat näytetään mallille etukäteen. Käytännössä tämä tarkoittaa, että malli ei saa koko työkalumetsää suoraan promptiin, vaan etsii tarvitsemansa työkalun, lataa sen tarkan skeeman vasta tarvittaessa ja kutsuu sitä OpenClawin normaalin politiikkapolun läpi.

Tämä on tärkeää kahdesta syystä:

- alkuperäinen pyyntö pienenee
- vahingossa valittu väärä työkalu vähenee, kun malli ei näe kerralla kymmeniä lähes samannäköisiä skeemoja

Dokumentaation mukaan Tool Search sopii nimenomaan isoihin katalogeihin, erityisesti silloin kun mukana on MCP- ja plugin-työkaluja. Pienessä työkalusetissä suora näkyvyys on edelleen usein paras oletus.

Minun käytännön tulkintani on tämä: **Tool Search ei ole "enemmän älyä", vaan tapa siirtää skeemakuormaa pois vuoron alusta.**

## Milloin `localModelLean` kannattaa kytkeä päälle

Jos ajat pienempää paikallista mallia, pelkkä Tool Search ei aina riitä tai sitä ei ole erikseen konfiguroitu. Tässä kohtaa `experimental.localModelLean` on hyödyllinen. Dokumentaation mukaan se poistaa oletuksena kolme raskasta työkalua suoraan näkyvistä: `browser`, `cron` ja `message`. Samalla se ottaa käyttöön structured Tool Search -oletuksen, jos `tools.toolSearch` ei ole jo erikseen määritelty.

Tämä on käytännössä hyvä ensimmäinen korjaus silloin, kun:

- kevyt malliajo toimii, mutta täysi agenttivuoro ei
- ongelma alkaa vasta työkalujen kanssa
- käytössä on pieni paikallinen OpenAI-yhteensopiva backend
- et tarvitse joka vuorossa selainta, viestitystä tai cronin täyttä skeemaa mallin nenän eteen

Dokumentaatio myös varoittaa hyvin selvästi, että lean-tila ei ole uusi normaali oletus vaan workaround. Olen samaa mieltä. Jos vahvempi malli tai hyvin resursoitu paikallinen stack käsittelee täyden työkalupinnan puhtaasti, lean-tilaa ei kannata ottaa käyttöön vain varmuuden vuoksi.

## Tärkeä rajaus: Codex-harness ei käytä samaa Tool Searchia

Tässä moni menee harhaan. OpenClawin Tool Search -sivu sanoo suoraan, että se dokumentoi OpenClawin omaa kokeellista Tool Search -ominaisuutta, **ei Codexin natiivia tool searchia tai deferred dynamic tools -pintaa**. Codex harness -dokumentaatio täydentää tätä: OpenClawin dynaamiset työkalut ladataan Codexille oletuksena `searchable`-mallilla, jotta koko työkalupintaa ei tungeta alkuun suoraan.

Käytännössä tämä tarkoittaa näin:

- jos ajat tavallista OpenClaw-runia, voit säätää `tools.toolSearch`-ominaisuutta
- jos ajat Codex-harnessia, luotat Codexin omaan searchable-lataukseen ja OpenClawin dynaamisten työkalujen deferred-malliin
- näitä ei kannata sekoittaa keskenään, vaikka nimi "tool search" kuulostaa melkein samalta

Juuri tästä syystä väärä korjausyritys on yleinen. Joku laittaa `tools.toolSearch`-asetusta uusiksi ja ihmettelee, miksi Codex-harnessin käytös ei juuri muuttunut. Syynä voi olla se, että kyseisessä runtimessa käytössä on jo eri mekanismi.

## Nopea käytännön päätöspuu

Jos paikallinen malli alkaa oireilla työkalujen kanssa, etenisin näin:

1. Varmista ensin, että malli osaa vastata yksinkertaiseen testipromptiin ylipäätään.
2. Tarkista hajoaako vuoro vasta täyden työkalupinnan kanssa.
3. Jos kyllä, pienennä näkyvää työkalukuormaa ennen kuin vaihdat koko mallin.
4. Tavallisessa OpenClaw-ajossa harkitse `tools.toolSearch`ia.
5. Heikommassa paikallisessa setupissa kokeile `experimental.localModelLean: true`.
6. Jos käytät Codex-harnessia, tarkista ensin harnessin oma searchable dynamic tools -käytös äläkä oleta, että OpenClawin kokeellinen Tool Search on se vipu jota juuri käytetään.

Minusta tärkein oppi on tämä: **jos malli hajoaa vasta silloin kun työkalut tulevat mukaan, vika voi olla vähemmän "malli on huono" ja enemmän "syötit sille liian paljon skeemaa väärässä muodossa".**

## Mitä en tekisi ensimmäisenä

En tekisi ainakaan näitä kolmea asiaa heti alkuun:

- en piilottaisi satunnaisesti työkaluja ilman että ymmärrän mikä runtime on käytössä
- en säätäisi kokeellisia lippuja tuotantoon kaikille agenteille vain yhden paikallisen mallin takia
- en syyttäisi heti keskusteluhistoriaa, jos oikea pullonkaula on työkaluskeemojen määrä

Jos haluat pysyvän kapeamman työkalupinnan yhdelle agentille, dokumentaatio muistuttaa ihan oikein, että vakaammat vivut ovat edelleen `tools.profile`, `tools.allow` ja `tools.deny`. Lean-tila on enemmän ensiapu kuin lopullinen arkkitehtuuriratkaisu.

## Oma johtopäätökseni

Paikallisen mallin kanssa kannattaa erottaa kaksi eri ongelmaa toisistaan:

- onko malli liian heikko itse tehtävään
- vai onko vuoron työkalupinta liian raskas sille mallille

Jos jälkimmäinen on totta, OpenClawissa on jo valmiiksi hyviä keinoja helpottaa painetta. Tavallisissa ajoissa `tools.toolSearch` voi pienentää alkuperäistä kuormaa selvästi. Heikommissa paikallisissa seteissä `localModelLean` voi siivota pahimmat työkaluskeemat näkyvistä ja jättää isot katalogit search-pinnan taakse. Codex-harnessissa taas kannattaa ymmärtää, että käytössä on oma searchable dynamic tools -polku.

Lyhyesti: **älä yritä ratkaista jokaista työkalukaaosta isommalla mallilla, jos oikea korjaus on pienempi työkaluprompti.**

## Lähteet

- https://docs.openclaw.ai/tools/tool-search
- https://docs.openclaw.ai/concepts/experimental-features
- https://docs.openclaw.ai/plugins/codex-harness
