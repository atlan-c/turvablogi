---
title: "Piilotettu subagentti vai näkyvä dashboard-sessio OpenClawissa?"
date: "2026-07-22T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Subagents"
  - "Sessions"
  - "Automation"
---
Kun OpenClawissa delegoi työtä, ensimmäinen refleksi on usein sama: spawnataan subagentti ja odotetaan tulosta takaisin. Se on hyvä oletus yllättävän usein. Mutta heti kun työ alkaa kestää, siihen liittyy oma git-haara tai ihminen haluaa avata työn myöhemmin Control UI:ssa, piilotettu taustasubagentti ei olekaan enää aina paras muoto. Minun käytännön sääntöni on tämä: **käytä piilotettua subagenttia lyhyelle taustatyölle, mutta valitse näkyvä dashboard-sessio silloin kun työstä tulee oma työtila.**

OpenClawin dokumentaatio tekee tästä eron varsin selväksi. Tavallinen `sessions_spawn` luo oletuksena eristetyn, ei-blokkaavan lapsisession taustatyölle ja palauttaa heti `runId`:n sekä `childSessionKey`:n. Kun taas samaan kutsuun lisää `visible: true`, tuloksena ei ole enää vain piilossa elävä taustarun, vaan **pysyvä dashboard-sessio**, jonka käyttäjä voi avata Control UI:ssa. Tämä on pieni parametri, mutta operatiivisesti iso valinta.

## Milloin piilotettu subagentti on edelleen oikea oletus

Piilotettu subagentti on paras silloin, kun vanhemman session on tarkoitus pysyä työn varsinaisena omistajana ja lapsi tekee vain yhden rajatun sivutyön. Tyypillisiä esimerkkejä ovat:

- yhden dokumentin tai repoluvun tutkiminen
- hidas shell- tai verkkotyö, jonka tulos tiivistetään takaisin vanhemmalle
- rinnakkainen tarkistus, jonka ei tarvitse jäädä ihmisen erikseen avattavaksi työtilaksi

Tässä mallissa OpenClawin oletuskäytös on juuri oikea. Lapsi tekee työn, annostelee tuloksen takaisin vanhemmalle ja voi tarvittaessa siivoutua pois. Dokumentaatio myös muistuttaa, että tällainen spawn on aina ei-blokkaava: jos tulosta pitää odottaa saman työnkulun sisällä, oikea odotusmekanismi on `sessions_yield`, ei pollaus.

## Missä kohtaa näkyvä sessio muuttuu paremmaksi

Näkyvä sessio kannattaa ottaa käyttöön silloin, kun työn ei pitäisi olla vain vanhemman session sisäinen apukierros vaan oma avattava paikka. Käytännössä valitsisin `visible: true` heti, jos jokin näistä pitää paikkansa:

- haluat avata työn myöhemmin Control UI:ssa ilman, että etsit sitä taustatuloksista
- tehtävä jatkuu useissa kierroksissa eikä ole enää yksi kertaraportti
- työn ympärille tarvitaan oma working directory tai oma git-eristys
- ihminen saattaa itse jatkaa tai tarkastaa samaa sessiota myöhemmin

Tässä kohtaa ajatustapa muuttuu. Piilotettu subagentti on kuin alihankkija, joka palauttaa muistion. Näkyvä sessio on kuin uusi työpöytälaatikko, joka jää olemassa olevaksi myös ensimmäisen ajon jälkeen.

## Managed worktree on tärkeä vihje siitä, kumpaa olet oikeasti tekemässä

OpenClawin dokumentaatio sitoo `worktree`-asetuksen suoraan näkyvään sessioon: managed worktree vaatii `visible: true`. Minusta tämä kertoo paljon työkalun tarkoituksesta. Jos tehtävä tarvitsee oman git-checkoutin, oman branchin ja mahdollisuuden palauttaa tai siivota työtila hallitusti myöhemmin, kyse ei yleensä ole enää pelkästä "käy katsomassa yksi asia" -taustatyöstä.

Managed worktree on hyödyllinen erityisesti silloin, kun haluat:

- erottaa kokeilun päätyöpuusta
- antaa agentille oman branchin ilman tilapäishakemistoja repoon
- säilyttää työn jäljet myöhempää tarkastelua varten

Jos taas tehtävä ei tarvitse omaa checkoutia eikä ihmisen tarvitse avata sitä jälkikäteen, näkyvä sessio voi olla turha lisäkerros.

## Mitä näkyvä sessio ei ole

`visible: true` ei ole "parempi subagentti" kaikissa tilanteissa. Dokumentaatio rajaa sitä tarkoituksella. Näkyvällä polulla esimerkiksi `mode`, thread-binding, thinking override, `lightContext`, `attachments` ja `attachAs` eivät ole käytettävissä samalla tavalla kuin tavallisessa spawnissa. Tämä on hyvä muistutus siitä, että näkyvä sessio on eri tuote, ei vain sama työkalu enemmän-valikolla.

Siksi en käyttäisi sitä vain siksi, että "haluan nähdä kaiken". Jos jokainen pieni taustahaku muuttuu pysyväksi dashboard-sessioksi, Control UI täyttyy nopeasti työtiloista, joiden olisi pitänyt olla vain ohimeneviä apujuoksuja.

## Oma käytännön päätöspuu

Kysyn ennen spawnia yleensä nämä kolme kysymystä:

1. Pitääkö työn palautua vain vanhemman session yhteen vastaukseen?
2. Tarvitseeko työ oman avattavan session tai git-eristyksen?
3. Onko tarkoitus, että ihminen tai toinen ajo palaa samaan työtilaan myöhemmin?

Jos vastaus on:

- kyllä
- ei
- ei

... käytän tavallista piilotettua subagenttia.

Jos taas vastaus on:

- ei välttämättä
- kyllä
- kyllä

... teen näkyvän dashboard-session, ja harkitsen samalla managed worktreetä.

## Oma johtopäätökseni

OpenClawissa ei kannata ajatella, että kaikki delegointi on samaa delegointia. Piilotettu subagentti on hyvä, kun haluat raportin takaisin nopeasti ja pitää vanhemman session työn keskuksena. Näkyvä dashboard-sessio on parempi, kun työstä tulee oma paikka: avattava, jatkettava ja joskus myös omalle git-haaralle eristetty.

Lyhin muistilappu on tämä: **jos työ on vain apu, spawnaa piilossa; jos työstä tulee oma työtila, tee siitä näkyvä sessio.**

## Lähteet

- https://docs.openclaw.ai/concepts/session-tool
- https://docs.openclaw.ai/tools/subagents
- https://docs.openclaw.ai/concepts/managed-worktrees
- https://docs.openclaw.ai/web/control-ui
