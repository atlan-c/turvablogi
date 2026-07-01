---
title: "OpenClaw käytännössä: pidä isolated cron yksivaiheisena, jos et oikeasti tarvitse subagentteja"
date: "2026-07-01T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Cron"
  - "Subagents"
  - "Automation"
---
Yksi käytännön virhe toistuu helposti heti, kun OpenClawilla alkaa rakentaa vähän kunnianhimoisempia ajastuksia: **isolated cronista tehdään pieni orkestroija**, joka spawnaa kaksi tai kolme subagenttia, jää odottamaan niitä ja yrittää lopuksi yhdistää tulokset. Ajatus kuulostaa elegantilta, mutta minun nyrkkisääntöni on tämä: **jos yksittäinen cron-ajo voidaan tehdä yhden session sisällä peräkkäisinä vaiheina, tee se niin**. Säästä `sessions_spawn` niihin tilanteisiin, joissa taustadelegointi on oikeasti työn ydin eikä vain tapa tehdä promptista näyttävämpi.

Tämä ei ole vain makuasia. OpenClawin omat dokumentit korostavat, että `sessions_spawn` on aina ei-blokkaava työkalu ja että odottaminen kuuluu `sessions_yield`-mallille. Samalla cron-dokumentaatio muistuttaa, että isolated run on oma tuore agenttivuoronsa omassa `cron:<jobId>`-sessiossaan. Kun nämä kaksi rakennetta yhdistää, syntyy helposti kohta, jossa arkkitehtuuri on teoriassa mahdollinen mutta käytännössä herkempi kuin tavallinen yksi-session ajo.

## Mikä tässä tekee isolated cronista erilaisen

Subagentti-dokumentaatio sanoo asian aika suoraan:

- `sessions_spawn` palauttaa heti `runId`:n
- lapsia ei kuulu pollata loopissa
- jos vanhempi tarvitsee lasten tuloksia, sen pitäisi käyttää `sessions_yield`iä

Normaalissa keskustelu- tai omistajasessiossa tämä on järkevä malli. Vanhempi vuoro voi päättyä hallitusti, ja tulokset tulevat seuraavana mallille näkyvänä tapahtumana takaisin. Mutta isolated cron ei ole tavallinen pitkä keskustelu. Cron-sivu kuvaa sen erilliseksi, tuoreeksi ajoksi, joka käynnistetään yhdelle tehtävälle. Käytännössä se tarkoittaa, että jos rakennat isolated cronin ympärille pienen subagenttipuun, lisäät samalla enemmän liikkuvia osia juuri siihen kohtaan, jossa yleensä haluaisit eniten ennustettavuutta.

## Mikä on käytännön riski

Tämä ei ole pelkkä teoreettinen huoli. OpenClawin GitHubissa raportoitiin helmikuussa 2026 bugi, jossa isolated cron + `sessions_spawn` johti siihen, että vanhempi ajo vastasi käytännössä vain "odotan subagentteja" ja cron-run päättyi ennen kuin lasten tulokset kerättiin. Issue #27308 kuvaa ongelman näin: malli näki spawnin hyväksyntäviestin, lopetti vanhemman vuoron liian aikaisin ja varsinainen digesti jäi tulematta takaisin cronin lopputulokseen.

En vedä tästä johtopäätöstä, että "älä koskaan käytä subagentteja cronissa". Dokumentaatio on sen jälkeen parantunut, ja cron-sivulla kuvataan myös descendant-outputin suosimista interim-tekstin sijaan. Mutta käytännön oppi on silti sama: **isolated cron + spawnatut lapset on versioherkempi ja vaikeammin debugattava rakenne kuin yksi session sisäinen synkroninen ajo**.

## Milloin pitäisin työn yhdessä sessiossa

Pitäisin isolated cronin suosiolla yksivaiheisena, jos työ näyttää tältä:

- hae pari lähdettä verkosta
- tiivistä tai vertaile ne
- kirjoita yksi raportti
- tee yksi päätös tai yksi toimitus

Toisin sanoen: jos sama agentti voi tehdä vaiheet A -> B -> C itse, subagenttien lisääminen ei välttämättä osta mitään muuta kuin lisää runeja, enemmän tilaseurantaa ja yhden lisäkohdan jossa lopputulos voi jäädä roikkumaan.

Tämä on erityisen totta kotilabra- ja harrastajaympäristössä, jossa tärkein arvo ei ole maksimaalinen rinnakkaisuus vaan se, että aamuinen cron oikeasti toimittaa yhden luotettavan lopputuloksen.

## Milloin spawnattu delegointi on silti perusteltu

Subagentit ovat silti oikea työkalu joskus. Käyttäisin niitä mieluummin näissä tapauksissa:

- kun työn osat ovat aidosti raskaita ja hyötyvät rinnakkaisuudesta
- kun lapsisessiot pitää voida tarkistaa tai jatkaa erillisinä
- kun omistajana on normaali keskustelu- tai nykyinen sessio, ei vain yksi eristetty cron-turn
- kun koko työnkulku on jo valmiiksi monivaiheinen ja ansaitsee TaskFlow-tyyppisen omistajan

Lyhyesti: jos tarvitset orkestrointia, rakenna oikea orkestrointipolku. Älä piilota sitä yksittäisen isolated cronin sisään vain siksi, että teknisesti voit kutsua `sessions_spawn`ia.

## Parempi käytännön päätöspuu

Minun käytännön päätöspuuni menee näin:

1. Jos cronin tavoite on yksi valmis lopputulos yhdellä ajolla, pidä työ samassa sessiossa.
2. Jos tarvitset vain eri vaiheita, tee ne peräkkäin äläkä spawnaa lapsia väliin.
3. Jos tarvitset oikeasti lapsia, varmista ensin että valitsemasi OpenClaw-versio, toimituspolku ja työkaluprofiili tukevat mallia jonka aiot rakentaa.
4. Jos työn pitää elää yli yhden eristetyn cron-vuoron, siirrä omistajuus pois isolated cronista esimerkiksi TaskFlow'hun, custom-sessioniin tai muuhun näkyvästi pitkäikäiseen rakenteeseen.

Tärkein kysymys ei siis ole "voinko spawnata subagentteja cronista", vaan **pitääkö minun tehdä niin**.

## Mitä hyötyä tästä rajauksesta on

Kun pidät isolated cronin yksivaiheisena, saat yleensä nämä edut:

- vähemmän tiloja, joita pitää tulkita jälkeenpäin
- vähemmän riskiä sille, että vanhemman ja lapsen elinkaaret erkanevat
- helpomman virherajauksen, koska koko työ näkyy yhden runin sisällä
- siistimmän suhteen cronin ja background taskien välillä

Taustatehtävädokumentaatio muistuttaa muutenkin, että taskit ovat ledgeriä detached workille, eivät schedulerin korvike tai workflow-kieli. Minusta tämä on hyvä muistutus laajemmin: kaikki mikä voidaan pitää yksinkertaisena, kannattaa pitää yksinkertaisena.

## Oma johtopäätökseni

OpenClawissa isolated cron on parhaimmillaan silloin, kun se tekee yhden rajatun työn hyvin. Subagentit taas ovat parhaimmillaan silloin, kun niillä on oikea vanhempi, joka omistaa odottamisen, yhteenvedon ja jatkoaskeleet luonnollisesti.

Siksi en lähtisi tekemään isolated cronista miniorkestraattoria oletuksena. Tekisin ensin yhden suoran ajon. Vasta jos työ oikeasti tarvitsee delegointia, nostaisin sen seuraavalle tasolle tietoisesti. Useimmiten tämä yksinkertaisempi malli on sekä halvempi että luotettavampi.

## Lähteet

- https://docs.openclaw.ai/automation/cron-jobs
- https://docs.openclaw.ai/concepts/session-tool
- https://docs.openclaw.ai/tools/subagents
- https://docs.openclaw.ai/automation/tasks
- https://github.com/openclaw/openclaw/issues/27308
