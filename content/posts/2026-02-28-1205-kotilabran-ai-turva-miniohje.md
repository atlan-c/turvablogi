---
title: "Kotilabran AI-turva: 20 minuutin minimiohje"
date: 2026-02-28T12:05:00+02:00
draft: false
---

Jos ajat AI-malleja kotona, tärkein tavoite on rajata vahinko yhteen koneeseen ja yhteen käyttäjään. Tämä miniohje tekee sen ilman raskasta enterprise-viritystä.

## 1) Rajaa verkko ensin
- Aja mallipalvelu oletuksena vain localhostiin (127.0.0.1).
- Jos tarvitset etäkäytön, käytä VPN:ää tai SSH-tunnelia — älä avointa porttia internetiin.
- Varmista palomuurista, että vain tarvittavat portit ovat sallittuina.

## 2) Aja pienimmillä oikeuksilla
- Luo erillinen käyttäjä AI-ajolle (ei admin-oikeuksia).
- Erottele mallit ja työskriptit omaan kansioon, johon vain tämä käyttäjä kirjoittaa.
- Poista automaattinen käynnistys, jos et oikeasti tarvitse jatkuvaa palvelua.

## 3) Päivitykset ja palautus kuntoon
- Päivitä runtime ja käyttöjärjestelmä säännöllisesti.
- Ota varmuuskopio ainakin: konfiguraatiot, promptipohjat, automaatioskriptit.
- Testaa kerran kuussa, että palautus oikeasti toimii.

## 4) Suojaa syöte ja lokit
- Älä syötä mallille salasanoja, API-avaimia tai henkilödataa.
- Kytke lokitus päälle, mutta rajaa lokien säilytysaika.
- Tee kevyt tarkistuslista: "mitä tietoa tämä workflow käsittelee" ennen uuden automaation käyttöönottoa.

## 5) Tee nopea kuukausitsekki
- Mitkä palvelut kuuntelevat verkossa?
- Onko uusia käyttäjiä tai ajastettuja tehtäviä ilmestynyt?
- Onko malli/runtime vaihtunut ilman että dokumentoit sitä?

Kun nämä viisi kohtaa ovat rutiini, kotilabran AI-riski laskee paljon enemmän kuin yhdelläkään "turvapluginilla".

## Lähteet

- OWASP Top 10 for LLM Applications: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- CISA Secure by Design: https://www.cisa.gov/securebydesign
- Kyberturvallisuuskeskus (ohjeet ja varoitukset): https://www.kyberturvallisuuskeskus.fi/
