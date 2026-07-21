---
title: "Milloin 64 Gt RAM on oikea pari 24 Gt LLM-näytönohjaimelle?"
date: "2026-07-21T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Paikalliset LLM:t"
  - "RAM"
  - "VRAM"
  - "ROCm"
---
Kun paikallista LLM-konetta suunnitellaan, huomio menee lähes aina ensin näytönohjaimeen. Se on ymmärrettävää, koska VRAM ratkaisee paljon. Silti yllättävän moni 24 gigatavun GPU:n ostaja parittaa sen vielä 32 gigatavun keskusmuistin kanssa ja ihmettelee myöhemmin, miksi kone tuntuu ahtaalta juuri silloin kun käyttö muuttuu oikeaksi työksi. **Jos rakennat paikallista LLM-konetta 24 Gt näytönohjaimen ympärille, 64 Gt RAM ei ole ylellisyyttä vaan usein käytännöllinen peruspari.**

Ajatus ei tule vain harrastajien mutu-tuntumasta. AMD:n ROCm-dokumentaatio suosittelee nimenomaan vaativiin AI/ML-työkuormiin, kuten suuriin kielimalleihin, yhdistelmää jossa on 24 Gt GPU-muistia ja 64 Gt keskusmuistia. Samalla Ollaman dokumentaatio muistuttaa, että jo pelkkä kontekstin kasvattaminen lisää muistitarvetta, ja että web-haun, agenttien ja koodityökalujen kaltaisille tehtäville kannattaa varata vähintään 64k konteksti. Siitä seuraa yksinkertainen käytännön kysymys: **milloin 64 Gt RAM oikeasti auttaa enemmän kuin seuraava pieni CPU-päivitys?**

## Mitä 64 Gt RAM ratkaisee käytännössä

24 Gt VRAM voi riittää erittäin hyvin siihen, että malli pysyy kokonaan GPU:lla tai ainakin paljon useammin GPU:lla kuin 12-16 Gt korteilla. Mutta se ei tarkoita, että muu kone lakkaisi olemasta tärkeä. Keskusmuistiin jää yhä monta asiaa:

- käyttöjärjestelmä ja taustapalvelut
- Ollaman tai muun runtime-kerroksen puskurit
- pitkät promptit, dokumenttiaineistot ja välitulokset
- rinnakkaiset työkalut kuten editori, selain, vektorikanta tai agenttirunko
- tilanteet, joissa kaikkea ei pystytä pitämään kokonaan VRAMissa

Siksi 32 Gt RAM voi näyttää paperilla "ihan riittävältä", mutta alkaa kiristyä silloin kun koneella tehdään muutakin kuin yksi lyhyt chat-ikkuna.

## Miksi juuri 24 Gt GPU muuttaa muistikeskustelua

Ollama asettaa oletuskontekstin VRAM-määrän perusteella. Alle 24 GiB korteilla oletus on 4k, mutta 24-48 GiB luokassa oletus nousee 32k:hon. Sama dokumentaatio sanoo lisäksi, että web-haku, agentit ja koodityökalut kannattaa asettaa vähintään 64k kontekstiin. Tämä on tärkeä kohta, koska 24 Gt kortti on juuri se taso, jossa moni harrastaja siirtyy "testaan paikallista mallia" -vaiheesta "rakennan oikean työkalun" -vaiheeseen.

Toisin sanoen 24 Gt GPU ei ole vain isompi näytönohjain. Se houkuttelee käyttämään pidempää kontekstia, isompia malleja ja pidempiä työjonoja. Juuri siksi myös järjestelmämuistin paine kasvaa samaan aikaan.

## Missä 32 Gt RAM alkaa tuntua ahtaalta

32 Gt ei ole automaattisesti virheostos. Jos käyttö näyttää tältä, se voi riittää aivan hyvin:

- yksi käyttäjä
- yksi malli kerrallaan
- maltillinen konteksti
- ei raskasta dokumentti- tai koodityökalukäyttöä samanaikaisesti

Ongelma alkaa, kun sama kone tekee enemmän kuin yhden asian. Tyypillisiä esimerkkejä:

- agentti lukee repoa tai pitkää dokumenttipinoa
- selain, editori ja paikallinen malli ovat kaikki auki yhtä aikaa
- konteksti nostetaan 64k:hon, koska työnkulku sitä oikeasti tarvitsee
- osa työstä tai mallin kerroksista valuu CPU:n puolelle

Näissä tilanteissa 32 Gt RAM ei välttämättä kaada konetta, mutta se tekee siitä helpommin epävakaan tuntuisen. Swap alkaa hiipiä mukaan, käyttöjärjestelmä joutuu puristamaan välimuisteja, ja koko paikallinen "tekoälytyöasema" alkaa muistuttaa tavallista pöytäkonetta, joka vain sattuu myös ajamaan mallia.

## Mitä AMD:n suositus oikeasti kertoo

AMD:n ROCm-ohje sanoo kaksi asiaa, jotka on helppo lukea väärin. Ensinnäkin 64 Gt RAM ja 24 Gt GPU VRAM esitetään suosituksena monimutkaisille AI/ML-työkuormille, kuten LLM:ille. Toiseksi dokumentaatio sanoo, että järjestelmämuistia pitäisi olla vähintään saman verran kuin videomuistia.

Tästä ei pidä vetää liian kovaa lakia tyyliin "24 Gt GPU ei toimi alle 64 Gt RAMilla". Se olisi liian vahva tulkinta. Minun johtopäätökseni lähteistä on käytännöllisempi: **jos valmistaja itse suosittelee 64/24-yhdistelmää vaativaan käyttöön, 32 Gt kannattaa nähdä tietoisena kompromissina eikä oletusparina.**

## Milloin käyttäisin rahat ensin RAMiin

Jos koneessa on jo 24 Gt luokan näytönohjain ja harkitset seuraavaa päivitystä, nostaisin RAMin 64 gigatavuun ennen CPU:n hienosäätöä, jos yksikin näistä pitää paikkansa:

- käytät paikallista koodiapuria tai agenttia päivittäin
- pidät selaimen, editorin ja LLM-runtimejen auki yhtä aikaa
- syötät mallille paljon dokumentteja, repoja tai lokitekstiä
- ajat Linuxilla AMD-korttia ROCm-pinolla tai muuten rakennat koneesta nimenomaan AI-työasemaa
- et halua arpoa joka kerta, mikä palvelu pitää sulkea ennen seuraavaa ajoa

Tässä tilanteessa lisämuisti ostaa ennen kaikkea käyttörauhaa. Se ei välttämättä nosta tokennopeutta näyttävästi, mutta se vähentää muistipaineesta syntyvää kitkaa lähes joka ajossa.

## Milloin 32 Gt voi silti olla täysin ok

Pitäisin 32 Gt RAMia edelleen järkevänä, jos 24 Gt GPU tuli esimerkiksi käytettynä hyvään hintaan ja muu budjetti on tiukka juuri nyt. Tärkeintä on tunnistaa, mitä sillä kompromissilla ostaa:

- vähemmän pelivaraa pitkään kontekstiin
- enemmän tarvetta sulkea muuta työkuormaa
- huonompi sieto tilanteille, joissa osa ajosta osuu CPU:lle

Jos nämä rajat sopivat omaan käyttöön, 32 Gt ei ole katastrofi. Se vain ei ole enää "unohda muistiasia ja keskity malliin" -taso.

## Oma nyrkkisääntöni

Kun puhutaan paikallisesta LLM-koneesta, 24 Gt VRAM kertoo yleensä jo siitä, että tavoitteena on muutakin kuin kevyt kokeilu. Silloin 64 Gt RAM on useammin oikea pari kuin ylimitoitus.

Sanoisin sen näin:

- `24 Gt VRAM + 32 Gt RAM`: toimii, jos hyväksyt aktiivisesti kompromisseja
- `24 Gt VRAM + 64 Gt RAM`: paljon turvallisempi peruspari oikeaan työskentelyyn

Paikallisessa AI-raudassa helpoin väärä säästö ei aina ole liian hidas GPU. Se on se, että ostat vihdoin tarpeeksi VRAMia mutta jätät muun koneen edelleen siihen muistiluokkaan, joka sopi vanhaan käyttöön eikä siihen uuteen, jota varten päivitys tehtiin.

## Lähteet

- https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/prerequisites/prerequisitesrad.html
- https://docs.ollama.com/context-length
- https://docs.ollama.com/gpu
