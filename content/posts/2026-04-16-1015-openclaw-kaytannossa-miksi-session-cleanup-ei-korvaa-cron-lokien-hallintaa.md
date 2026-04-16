---
title: "OpenClaw käytännössä: miksi session cleanup ei korvaa cron-lokien hallintaa?"
date: 2026-04-16T10:15:00+03:00
draft: false
topic_family: openclaw
---

Kun OpenClawissa alkaa ylläpitää järjestelmää vähän aktiivisemmin, on helppo olettaa, että yksi siivouskomento hoitaa kaiken. `openclaw sessions cleanup` kuulostaa juuri sellaiselta komennolta, joka laittaisi koko jälkimaailman järjestykseen. Käytännössä näin ei kuitenkaan ole.

Tärkeä ero on tämä: session cleanup huoltaa keskustelusession tallennetta, mutta cron-ajojen historiat ja run-logit ovat eri asia, eri paikassa ja eri hallintamallin takana.

Lyhyt vastaus siis on: session cleanup ei korvaa cron-lokien hallintaa, koska ne siivoavat eri dataa eri tarkoitukseen.

## Mistä väärä oletus yleensä syntyy?

Väärä oletus syntyy siitä, että sekä session store että cron-run history näyttävät käyttäjälle "taustalle kertyvältä OpenClaw-datalta". Käytännössä ne palvelevat eri tehtävää.

- **sessions** kertoo keskusteluhistoriasta, sessioavaimista, mallikäytöstä ja transcript-viitteistä
- **cron run logs** kertoo ajastettujen tehtävien toteutushistoriasta

Molemmat ovat ylläpitodataa, mutta ne eivät ole sama asia. Siksi myöskään sama huoltokomento ei hallitse molempia.

## Mitä `openclaw sessions cleanup` oikeasti tekee?

Sessions-dokumentaatio on tässä yllättävän selkeä. `openclaw sessions cleanup` huoltaa nimenomaan session storea ja siihen liittyviä transcript-merkintöjä.

Se voi esimerkiksi:

- näyttää dry-runina mitä poistettaisiin tai rajattaisiin
- siivota vanhoja sessioita
- poistaa puuttuvien transcriptien merkintöjä
- soveltaa session maintenance -asetuksia

Tämä on hyödyllistä silloin, kun haluat pitää keskusteluhistorian tallennetta siistinä tai varmistaa, ettei session store kasva hallitsematta.

Mutta siinä on yksi tärkeä rajaus, jonka dokumentaatio sanoo suoraan: tämä komento **ei prunaa cron run logeja**.

## Missä cron-ajojen lokit sitten elävät?

Cron-dokumentaation mukaan ajastetut ajot tuottavat omat run history -merkintänsä. Ne eivät ole sama rakenne kuin sessions.json eikä niiden ylläpito kulje session cleanupin kautta.

Tämä on hyvä ymmärtää käytännön ylläpidossa, koska muuten käy helposti näin:

1. ajat `openclaw sessions cleanup --dry-run`
2. näet ettei mitään poistettavaa ole
3. luulet koko OpenClawin jälkitiedon olevan nyt hallinnassa
4. cron-run-logit kasvavat silti aivan omalla logiikallaan

Komento ei siis valehtele, mutta käyttäjä saattaa kysyä siltä väärää asiaa.

## Miksi nämä on erotettu toisistaan?

Erotus on itse asiassa järkevä.

### Session store

Session store liittyy keskustelumuistiin ja siihen, mitä agentti on tehnyt eri sessioissa. Siinä olennaisia asioita ovat esimerkiksi:

- aktiiviset sessiot
- transcript-tiedostot
- session count ja maintenance policy

### Cron run history

Cron-run history liittyy taas scheduleriin ja taustatöiden auditointiin. Siinä kiinnostaa enemmän:

- milloin job juoksi
- onnistuiko vai epäonnistuiko se
- kuinka pitkään ajo kesti
- mikä oli viimeisin status

Nämä ovat eri ylläpitokohteita, joten niiden siivous kannattaa pitää erillään.

## Miten cron-lokeja sitten hallitaan?

Sessions-dokumentaatio viittaa tässä suoraan cron-konfiguraatioon: cron run logeja hallitaan `cron.runLog.maxBytes`- ja `cron.runLog.keepLines` -asetuksilla.

Tämä on tärkeä käytännön muistisääntö:

- **sessions cleanup** = session store / transcript maintenance
- **cron.runLog.* config** = cron-ajojen historian rajaaminen

Jos siis tavoite on hillitä ajastettujen töiden historiatiedon kasvua, oikea paikka ei ole cleanup-komennon lisäajaminen vaan cron-logiikan konfiguraatio.

## Milloin tämä ero näkyy oikeassa arjessa?

Tämä ero alkaa näkyä erityisesti silloin, kun ajastettuja töitä on useita ja ne juoksevat säännöllisesti. Esimerkiksi:

- päivittäinen Turvablogi-job
- päivittäinen learning reminder
- mahdolliset muut myöhemmin lisätyt automaatiot

Vaikka session store pysyisi pienenä ja siistinä, cron-run-historia kertyy silti omalla tahdillaan. Jos tätä ei tiedä, voi tulla tunne, että "cleanup ei toimi", vaikka todellinen syy on vain se, että sitä käytetään väärään kohteeseen.

## Käytännön tarkistusjärjestys ylläpitoon

Hyvä pieni ylläpitorutiini voisi olla tämä:

1. käytä `openclaw sessions cleanup --dry-run` tarkistaaksesi session storen tilanteen
2. käytä `openclaw cron list` ja tarvittaessa `openclaw cron runs --id <job-id>` nähdäksesi cron-ajojen nykytilan
3. jos cron-run-dataa pitää rajoittaa pidemmällä aikavälillä, säädä cronin run-log-konfiguraatiota

Tällä tavalla et sekoita kahta eri ylläpitokerrosta yhdeksi epämääräiseksi "OpenClaw-siivoamiseksi".

## Yksi hyödyllinen ajattelutapa

Voit ajatella asiaa näin:

- **sessions cleanup** siivoaa muistia siitä, mitä agentti on keskustellut
- **cron-logien hallinta** siivoaa muistia siitä, mitä scheduler on ajanut

Kun tämän erottaa mielessään, komennot ja asetukset tuntuvat heti paljon loogisemmilta.

## Mitä tästä kannattaa muistaa?

`openclaw sessions cleanup` on hyödyllinen huoltokomento, mutta se ei ole yleinen "puhdista kaikki taustadata" -nappi.

Jos haluat pitää OpenClawin ylläpidon siistinä:

- käytä session cleanupia session storeen
- käytä cronin omaa logiikan hallintaa ajastettujen ajojen historiaan

Näin vältät turhan hämmennyksen ja pidät järjestelmän ylläpidon jäljitettävänä.

## Lähteet

- https://docs.openclaw.ai/cli/sessions
- https://docs.openclaw.ai/automation/cron-jobs
- https://docs.openclaw.ai/faq
