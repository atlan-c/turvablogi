---
title: "Miksi valitsin staattisen blogin tietoturvasyistä"
date: 2026-02-27
draft: false
---

Valitsin staattisen blogin ennen kaikkea siksi, että halusin minimoida hyökkäyspinnan.
Kun sivusto koostuu valmiiksi generoiduista HTML-tiedostoista, julkisessa ympäristössä ei ole
sovelluslogiikkaa, kirjautumisjärjestelmää tai tietokantaa, joihin kohdistaa yleisiä hyökkäyksiä.

Dynaamisissa järjestelmissä turvallisuus rakentuu monesta liikkuvasta osasta: lisäosat,
käyttäjähallinta, palvelinkonfiguraatio, päivitykset ja integraatiot. Staattisessa mallissa tämä
ketju on selvästi lyhyempi. Vähemmän liikkuvia osia tarkoittaa yleensä vähemmän riskiä.

Toinen tärkeä syy oli ylläpidon selkeys. Julkaisu tapahtuu versionhallinnan kautta,
ja kaikki muutokset jäävät näkyviin commit-historiaan. Tämä tekee virheiden jäljittämisestä,
palautuksista ja auditoinnista suoraviivaisempaa.

Käytännössä oma toimintamallini on nyt tämä:
1. Kirjoitan sisällön Markdownina.
2. Ajan paikallisen buildin.
3. Julkaisen versionhallinnan kautta.
4. Varmistan, että live-sivu vastaa odotetusti.

Staattinen blogi ei tietenkään poista kaikkea riskiä. Esimerkiksi tilien suojaus,
väärin asetetut oikeudet tai huolimattomasti julkaistu sisältö voivat silti aiheuttaa ongelmia.
Mutta lähtökohta on turvallinen: yksinkertainen arkkitehtuuri, selkeä julkaisuputki,
ja vähän julkisia hyökkäyskohteita.
