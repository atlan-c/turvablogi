---
title: "OpenClaw käytännössä: näin tulkitset isolated cron -ajon yhden mallivaihdon"
date: "2026-05-21T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Agents"
  - "Security"
  - "Automation"
  - "Troubleshooting"
---
Jos isolated cron -ajo näyttää joskus vaihtaneen mallia kesken kaiken tai tehneen yhden ylimääräiseltä näyttävän yrityksen, ensimmäinen reaktio on usein väärä: moni epäilee heti tupla-ajastusta, race conditionia tai sitä, että sama jobi laukesi kahdesti. **Käytännössä yksi mallinvaihto kesken isolated cron -ajon tarkoittaa paljon useammin normaalia live model switch -polkua kuin rikkinäistä ajastusta.**

Tämä on hyödyllinen ero ymmärtää, koska oikea diagnoosi säästää paljon turhaa säätöä. Jos luulet ongelman olevan schedulerissä, alat helposti penkoa vääriä asioita. Jos taas tunnistat mallinvaihdon hallituksi retryksi, osaat katsoa heti oikeaa paikkaa: mikä malli valittiin, oliko auth-profiili vaihtunut ja mitä run history sekä task-loki näyttävät.

## Mitä oikeasti tapahtuu

OpenClawin cron-dokumentaatio kuvaa isolated-ajot niin, että ne saavat jokaiselle runille tuoreen session, mutta voivat silti kantaa mukanaan turvallisia preferenssejä kuten mallivalinnan tai auth-overriden. Lisäksi cronin CLI-dokumentaatio kertoo erikseen live model switch -käytöksestä: jos ajo heittää `LiveSessionModelSwitchError`-virheen, cron voi **persistoida uuden provideri- ja mallivalinnan tälle ajolle ja yrittää kerran tai pari uudelleen** ilman että kyse on uudesta scheduloidusta ajosta.

Tärkeä käytännön tulkinta on tämä: run historyssa näkyvä lisäyritys ei automaattisesti tarkoita, että cron laukesi kahdesti. Se voi olla yhden ja saman ajon sisäinen hallittu toipumisyritys.

## Milloin tämä on normaalia eikä hälyttävää

Pidän yhtä mallinvaihtoa normaalina etenkin näissä tilanteissa:

- jobilla on oma `--model`, mutta käytössä on myös fallback-logiikka
- aktiivinen provider tai auth-profiili osuu väliaikaiseen virheeseen
- järjestelmä siirtyy toiseen sallittuun malliin saman ajon sisällä
- run historyssa näkyy yksi runId, mutta sen sisällä on retry- tai switch-merkintä

OpenClawin retry-politiikka tukee samaa ajatusta laajemmin: lyhyet retryt kuuluvat yksittäisen requestin ympärille, eivät koko monivaiheisen flow'n duplikointiin. Cron-ajossa tämä näkyy niin, että scheduler ei tee uutta julkaisua vain siksi, että mallikerros tarvitsi hallitun vaihdon.

## Milloin kannattaa epäillä oikeaa ongelmaa

Mallinvaihto ei silti aina ole harmiton. Tutkisin asiaa tarkemmin, jos huomaat jonkin näistä:

- samalle jobille syntyy aidosti **kaksi eri runId:tä** lähes samaan aikaan
- jobin lopputulos vaihtuu toiseen malliin toistuvasti päivästä toiseen ilman selvää syytä
- ajo osuu aina samaan auth- tai provider-virheeseen ennen vaihtoa
- lopputulos heikkenee selvästi, vaikka ajo teknisesti onnistuu

Silloin kysymys ei ole enää vain siitä, että OpenClaw pelasti ajon järkevästi, vaan siitä että taustalla on jokin toistuva epästabiilius. Yleinen syy voi olla vanhentuva auth, tilapäisesti kuollut paikallinen provider tai liian epäselvä mallireititys jobin ja agentin oletusten välillä.

## Kolme paikkaa, joista katsoisin ensin

Jos haluat selvittää nopeasti onko kyse normaalista mallinvaihdosta vai oikeasta cron-ongelmasta, etenisin tässä järjestyksessä:

1. **Run history** – onko kyse yhdestä runId:stä vai kahdesta eri ajosta?
2. **Task-loki** – näkyykö siellä varsinainen provider- tai mallinvaihtovirhe ennen onnistumista?
3. **Jobin mallisäännöt** – mikä oli per-job-malli, oliko fallbackeja, ja oliko sessioon jäänyt tallennettu override?

Tämä järjestys on minusta tärkeä juuri siksi, että se erottaa schedulointivirheen mallikerroksen toipumisesta. Jos aloitat väärästä päästä, saat helposti väärän korjauksen.

## Käytännön sääntö harrastajalle

Jos isolated cron -ajo vaihtaa mallia kerran mutta valmistuu muuten oikein, en ensimmäisenä koskisi cron-expressioniin tai jobin aikatauluun. **Katso ensin mallinvalinnan ketju ja run history.** OpenClawin dokumentaation mukaan mallin valintajärjestys voi tulla esimerkiksi jobin `--model`-asetuksesta, tallennetusta cron-session overridesta tai agentin oletuksesta, ja live switch voi päivittää tätä kesken ajon.

Hyvä nyrkkisääntö on tämä:

- **yksi hallittu switch** = usein normaali toipuminen
- **toistuva switch** = diagnosoi auth, provider ja fallbackit
- **kaksi eri runId:tä** = vasta tässä kohtaa epäilen oikeaa ajastus- tai laukaisuongelmaa

Tämä pieni ero auttaa paljon, kun haluat pitää automaatiot luotettavina ilman että reagoit jokaiseen retryyn kuin se olisi scheduler-bugi.

## Lähteet

- https://docs.openclaw.ai/automation/cron-jobs
- https://docs.openclaw.ai/cli/cron
- https://docs.openclaw.ai/concepts/retry
- https://docs.openclaw.ai/help/faq
