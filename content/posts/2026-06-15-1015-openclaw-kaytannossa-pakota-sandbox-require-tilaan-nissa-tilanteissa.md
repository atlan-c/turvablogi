---
title: "OpenClaw käytännössä: pakota sandbox `require` -tilaan näissä tilanteissa"
date: "2026-06-15T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Sandbox"
  - "Security"
  - "Automation"
---
Yksi helpoimmin sivuutettavista OpenClaw-päätöksistä on se, **luotatko ympäristön oletuksiin vai pakotatko eristyksen silloin kun työ todella sitä tarvitsee**. Tämä tulee vastaan erityisesti silloin, kun spawnataan lapsisessioita tai subagentteja: `sessions_spawn` tekee kyllä erillisen session, mutta erillinen sessio ei automaattisesti tarkoita samaa asiaa kuin tietoisesti vaadittu sandbox.

Oma käytännön sääntöni on yksinkertainen: **jos tehtävä saa lukea, kirjoittaa tai ajaa komentoja tavalla, jonka haluat varmasti pysyvän eristettynä, käytä `sandbox: "require"` etkä jätä päätöstä vain ambienttien oletusten varaan**.

Tämä ei ole vain turvallisuusnysväämistä. Se on myös työnkulun selkeyttä. Kun vaadit sandboxin nimenomaan siinä kohdassa, missä riski syntyy, myöhempi ylläpito on paljon helpompaa: seuraavan kerran kun katsot työnkulkua, näet yhdellä silmäyksellä mikä oli tarkoitus.

## Miksi pelkkä "non-main" ei aina riitä ajattelumalliksi

OpenClawin sandboxing-dokumentaatio kertoo, että `agents.defaults.sandbox.mode` voi olla esimerkiksi `off`, `non-main` tai `all`. `non-main` on hyödyllinen oletus, jos haluat pitää normaalit pääkeskustelut hostilla mutta eristää muut sessiot. Ongelmana on, että tämä on ympäristöpolitiikkaa, ei yksittäisen työn itsensä lausuma vaatimus.

Toisin sanottuna:

- ympäristö voi olla tänään `non-main`, huomenna `off`
- eri agentilla voi olla oma override
- joku voi myöhemmin muuttaa sandbox-scopen tai backendin
- sama työnkulku voi siirtyä toiseen asennukseen, jossa oletukset ovat eri

Jos kriittinen turvallisuus- tai eristysoletus elää vain globaalissa konfiguraatiossa, työnkulku itsessään ei kerro lukijalle riittävästi. Silloin syntyy klassinen "toimi minun koneellani" -harha, mutta automaation ja agenttien tasolla.

## Mitä `sandbox: "require"` käytännössä ostaa

Session tools -dokumentaatio nostaa tämän esiin suoraan: `sessions_spawn` tukee valintaa `sandbox: "require"` lapselle. Minun tulkintani siitä on käytännössä tämä: kun lapsityö tarvitsee eristyksen osana tehtävän määritelmää, se kannattaa ilmaista spawn-kohdassa eikä vain toivoa, että agentin yleinen sandbox-politiikka tekee oikean asian.

Ajattele asiaa samalla tavalla kuin infrastruktuurissa ajatellaan riippuvuuksia: jos jokin ominaisuus on pakollinen, se kannattaa ilmoittaa eksplisiittisesti siinä rajapinnassa missä sitä tarvitaan.

Hyötyjä tulee heti kolme:

- työn turvallisuusvaatimus näkyy suoraan koodissa tai promptissa
- siirrettävyys paranee, koska sama työnkulku ei nojaa yhtä vahvasti paikallisiin oletuksiin
- virheiden diagnosointi nopeutuu, koska "pitikö tämän olla sandboxissa?" ei jää arvailuksi

## Neljä tilannetta, joissa pakotan `require`-tilan lähes aina

### 1. Kun lapsisessio käsittelee epävarmaa tai sotkuista syötettä

Jos spawnattu työ lukee ulkoista dataa, generoi komentoja sen pohjalta tai käsittelee sisältöä, jonka laatuun et täysin luota, eristys kannattaa ilmaista kovempana vaatimuksena. Tämä on tavallinen tilanne esimerkiksi:

- isossa repoanalyysissa
- lokien tai bugiraporttien läpikäynnissä
- web-hausta tai issue-ketjuista rakennetussa tutkimusajossa
- agentissa, joka tekee paljon shell-askelia käyttäjän tekstin perusteella

Tässä kohtaa ei riitä, että "yleensä meidän ei-main-sessiot ovat sandboxissa". Juuri tällaisessa työssä haluan mieluummin eksplisiittisen takuun kuin hiljaisen oletuksen.

### 2. Kun työn pitää kirjoittaa workspaceen, mutta ei hostille laajemmin

Sandboxing-dokumentaatio muistuttaa, että sandbox ei ole täydellinen turvaraja, mutta se rajoittaa merkittävästi tiedosto- ja prosessipääsyä silloin kun malli tekee jotain typerää. Tämä on minusta oikea tapa ajatella asiaa myös arjessa: sandbox ei tee agentista maagisesti turvallista, mutta se pienentää vahinkosädettä.

Jos tehtävä saa muokata vain tiettyä workspacea tai kontrolloitua kopioita työpuusta, `require` tekee tarkoituksesta eksplisiittisen. Ilman sitä työnkulku voi alkaa ajan myötä nojata siihen, että "nykyinen agentti sattuu olemaan oikein konfiguroitu".

### 3. Kun sama automaatio on tarkoitus jakaa tai siirtää toiseen ympäristöön

Tämä on ehkä aliarvostetuin syy. Paikallisessa kotilabrassa moni muistaa omat oletuksensa ulkoa. Heti kun sama työnkulku annetaan toiselle agentille, toiselle koneelle tai myöhemmin omalle tulevalle itselle, dokumentoimattomat oletukset muuttuvat kalliiksi.

Jos lapsiajo on suunniteltu niin, että sen kuuluu pysyä eristettynä riippumatta siitä missä se ajetaan, vaatimus kannattaa kirjoittaa mukaan itse spawn-kutsuun. Näin työnkulku kantaa oman turvallisuusajatuksensa mukanaan.

### 4. Kun haluat rajata virheen vaikutuksen etkä vain "tehdä asiat siististi"

Moni käyttää subagentteja lähinnä siksi, että pääsessio ei blokkaisi. Se on hyvä alku, mutta samaan aikaan kannattaa kysyä toinen kysymys: **jos tämä delegoitu työ menee huonosti, kuinka ison alueen haluan sen voivan koskea?**

Jos vastaus on "mahdollisimman pienen", `sandbox: "require"` on yleensä oikea valinta. Tämä ei korvaa muuta politiikkaa, mutta se tukee sitä ajattelutapaa, että pitkä, monivaiheinen tai osittain epävarma työ ajetaan mahdollisimman rajatulla vaikutusalalla.

## Milloin en pakottaisi sitä

Aina ei kannata tehdä kovinta mahdollista rajaa. Jos työ tarvitsee tietoisesti hostin resursseja, paikallisia tunnisteita, nodea tai muuta ympäristöä, jota sandbox ei tarjoa, `require` voi olla väärä oletus. Samoin jos tehtävä on hyvin pieni, täysin luotettu ja tarkoituksella hostissa ajettava ylläpitotyö, eksplisiittinen sandbox-vaatimus voi vain tehdä työnkulusta turhan kankean.

Minun käytännön rajaukseni menee näin:

- käytä ambienttia oletusta, jos työ on pieni ja ympäristösidonnainen
- käytä `require`-tilaa, jos eristys on osa itse tehtävän määritelmää
- käytä host- tai elevated-polkuja vain silloin, kun tarvitset niitä oikeasti etkä vahingossa

## Tärkeä muistutus: sandbox ei yksin ratkaise kaikkea

OpenClawin dokumentaatio painottaa suoraan, että sandbox ei ole täydellinen security boundary. Lisäksi `tools.elevated` on nimenomainen pakoreikä, jolla `exec` voidaan ajaa sandboxin ulkopuolella, ja exec approvals -dokumentaatio muistuttaa, että host-komentojen kohdalla politiikka, allowlist ja mahdollinen hyväksyntä muodostavat oman turvalukkonsa.

Tästä seuraa tärkeä käytännön oppi: **`sandbox: "require"` ei korvaa työkalupolitiikkaa eikä hyväksyntäpolitiikkaa, vaan täydentää niitä**.

Jos haluat ajatella tämän mahdollisimman selvästi, OpenClawissa on kolme eri kysymystä:

1. Missä työkalu ajetaan?
2. Saako tätä työkalua käyttää lainkaan?
3. Jos se yrittää hostille, millä ehdoilla se pääsee sinne?

`sandbox: "require"` vastaa vain ensimmäiseen kysymykseen, mutta se on silti erittäin arvokas juuri siksi, että se tekee ensimmäisestä kysymyksestä eksplisiittisen.

## Entä Codex- tai app-server-ajot?

Tämä korostuu vielä enemmän, jos käytössä on Codex-harness-polku. Codex harness reference kertoo, että kun OpenClaw-sandbox on aktiivinen, OpenClaw ei luota siihen että Codexin omat natiivit pinnat olisivat "riittävän sama asia", vaan se fail-closed-mallissa poistaa sellaisia native execution surfaceja, jotka muuten juoksisivat hostilta. Minun mielestäni tämä on hyvä suunnitteluvihje myös omiin työnkulkuihin: jos eristyksellä on väliä, sitä ei pidä jättää implisiittiseksi.

## Yksinkertainen päätössääntö arkeen

Jos et halua miettiä asiaa joka kerta pitkän kaavan kautta, tämä riittää:

- jos delegoitu työ on vain pitkä mutta muuten luotettu, mieti ensin erillistä sessiota
- jos delegoitu työ on pitkä **ja** sen vaikutusalue pitää rajata, lisää `sandbox: "require"`
- jos työ tarvitsee hostin tietoisesti, älä teeskentele sandboxattua

Minulle hyödyllisin kysymys on tämä: **haluanko, että tämä työnkulku epäonnistuu ennemmin kuin ajaa väärässä paikassa?** Jos vastaus on kyllä, pakotan `require`-tilan.

## Oma johtopäätökseni

OpenClawissa eristys kannattaa nähdä osana työn määrittelyä, ei vain ympäristön taustakohinana. Siksi `sandbox: "require"` on erityisen hyvä silloin, kun spawnattu lapsiajo käsittelee epävarmaa syötettä, kirjoittaa workspaceen, on tarkoitus siirtää toiseen ympäristöön tai tarvitsee muuten selvästi rajatun vahinkosäteen.

Lyhyesti: **jos sandbox on tehtävän kannalta pakollinen, kirjoita se näkyviin tehtävään**. Se on pieni muutos, mutta usein juuri se erottaa luotettavan automaation automaatiosta, joka toimii vain niin kauan kuin kaikki hiljaiset oletukset sattuvat pysymään samoina.

## Lähteet

- https://docs.openclaw.ai/concepts/session-tool
- https://docs.openclaw.ai/gateway/sandboxing
- https://docs.openclaw.ai/tools/exec-approvals
- https://docs.openclaw.ai/plugins/codex-harness-reference
