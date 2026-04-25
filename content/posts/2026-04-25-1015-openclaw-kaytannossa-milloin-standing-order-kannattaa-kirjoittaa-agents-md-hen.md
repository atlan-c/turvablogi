---
title: "OpenClaw käytännössä: milloin standing order kannattaa kirjoittaa AGENTS.md:hen?"
date: 2026-04-25T10:15:00+03:00
draft: false
topic_family: "openclaw"
---

OpenClawin automaatiossa yksi pieni mutta tärkeä suunnittelukysymys on tämä: milloin jokin toistuva työ kannattaa nostaa standing orderiksi suoraan `AGENTS.md`:hen, eikä vain jättää yksittäisen cron-jobin prompttiin. Lyhyt käytännön vastaus on tämä: jos kyse on pysyvästä toimintatavasta tai ohjelmasta, kirjoita se standing orderiksi. Jos kyse on vain yhdestä ajastetusta suorituksesta, cron-prompti riittää usein yksinään.

Tämä ero on hyödyllinen, koska muuten tärkeä työn logiikka jää hajalleen eri cron-riveihin, eikä agentilla ole kunnollista pysyvää muistia siitä, mikä on lupa, mikä tavoite ja milloin pitää eskaloida.

## Mitä standing order oikeastaan tekee

Dokumentaation mukaan standing order antaa agentille pysyvän toimivallan määritellyssä ohjelmassa. Ajatus ei siis ole vain "tee tämä huomenna kello 8", vaan enemmänkin "sinä omistat tämän jatkuvan työn näillä rajoilla ja näillä eskalointisäännöillä".

Tämä on iso ero. Cron vastaa siihen, milloin herätys tapahtuu. Standing order vastaa siihen, mitä agentti on valtuutettu tekemään kerta toisensa jälkeen.

## Milloin AGENTS.md on oikea paikka

Standing order kannattaa yleensä laittaa `AGENTS.md`:hen, kun jokin näistä pitää paikkansa:

- toiminta on pitkäikäinen eikä vain kertaluonteinen
- samaa ohjelmaa käynnistää useampi eri triggeri
- haluat että säännöt ovat aina mukana session bootstrapissa
- työn rajoja, hyväksyntäportteja tai eskalointeja pitää kuvata selvästi
- et halua kopioida samaa ohjetta moneen cron-jobiin

Dokumentaatio korostaa tätä suoraan: `AGENTS.md` on suositeltu paikka, koska se injektoidaan joka sessioon automaattisesti. Tämä tekee siitä hyvän kodin pysyville toimintaperiaatteille.

## Milloin pelkkä cron-prompti riittää

Pelkkä cron-prompti on usein täysin riittävä, jos tehtävä on pieni ja itsenäinen. Esimerkiksi:

- yksittäinen muistutus
- yksi rajattu raportti
- yksi täsmällinen tarkistus, jolla ei ole laajempaa ohjelmaluonnetta

Tällöin standing order olisi helposti turhan raskas rakenne. Jos koko työn logiikka mahtuu yhteen selkeään cron-viestiin ilman toistoa ja ilman epäselviä valtuuksia, sitä ei tarvitse väkisin nostaa AGENTS.md:hen.

## Käytännön hajuhaitta: liian paljon logiikkaa cronissa

Huono merkki on se, jos cron-jobin viesti alkaa sisältää kaikkea tätä yhtä aikaa:

- tavoite
- toistuva toimintalupa
- hyväksyntärajat
- virhetilanteiden käsittely
- monivaiheiset pysyvät säännöt

Silloin cron ei enää ole vain ajastus vaan siitä on tullut piilossa oleva toimintaohje. Tämä toimii hetken, mutta ylläpidettävyys heikkenee nopeasti. Seuraava ihminen, tai seuraava sinä, joutuu arvailemaan mikä on pysyvä ohjelma ja mikä vain yhden jobin hetkellinen prompti.

## Oma nyrkkisääntö

Minun käytännön sääntöni olisi tämä:

1. jos asia on pysyvä toimintamalli, kirjoita se `AGENTS.md`:hen standing orderiksi
2. jos asia on vain ajastus, pidä se cronissa
3. jos cron-viesti alkaa sisältää paljon valtuus- ja eskalointilogiikkaa, nosta ydinsäännöt standing orderiksi ja jätä cron herätteeksi

Tämä tekee automaatiosta helpommin luettavaa. Standing order kertoo politiikan. Cron kertoo kellonajan.

## Miksi tämä on käytännössä hyvä jako

OpenClawissa samat asiat voivat muuten päätyä kolmeen paikkaan yhtä aikaa: cron-jobiin, muistiinpanotiedostoon ja AGENTS.md:hen. Jos standing orderit pidetään oikeasti pysyvien ohjelmien kotina, kokonaisuus selkenee huomattavasti.

Silloin agentti voi lukea `AGENTS.md`:stä mitä saa tehdä ja miksi, ja cron voi yksinkertaisesti sanoa: "suorita tämä ohjelma nyt".

## Yhteenveto

Milloin standing order kannattaa kirjoittaa `AGENTS.md`:hen? Silloin, kun kyse ei ole enää vain yksittäisestä ajastetusta tehtävästä vaan pysyvästä ohjelmasta, jolla on omat rajat, säännöt ja eskalaatiot.

Lyhyin muistilappu on tämä: cron kertoo milloin, standing order kertoo valtuuden ja toimintatavan.

## Lähteet

- https://docs.openclaw.ai/automation/standing-orders
- https://docs.openclaw.ai/automation/cron-jobs
