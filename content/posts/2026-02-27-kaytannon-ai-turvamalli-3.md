---
title: "Käytännön AI-turvamalli harrastajalle: pidä tämä yksinkertaisena"
date: 2026-02-27T22:28:00+02:00
draft: false
---

AI-projekteissa tietoturva tuntuu helposti monimutkaiselta. Harrastajalle toimivin malli on yllättävän selkeä.

## 1) Erottele kolme tasoa
- **Kokeilu** (sandbox / testidata)
- **Tuotantoa muistuttava** (rajattu oikea data)
- **Julkinen julkaisu** (ei salaisuuksia, ei write-oikeuksia)

## 2) Vähennä oikeuksia oletuksena
Anna työkaluillesi vain se, mitä ne tarvitsevat juuri nyt. Tämä yksin pienentää vahinkoriskiä merkittävästi.

## 3) Dokumentoi vain olennainen
Pidä yksi tiedosto, jossa on:
- mitä ajat
- missä ajat
- mitä dataa käytät
- miten palautat edelliseen toimivaan versioon

## 4) Julkaisussa tärkein kysymys
"Jos tämä commit vuotaa julkisuuteen, onko siitä haittaa?"

Jos vastaus on "ehkä", älä julkaise ennen kuin poistat riskikohdan.

## Mini-checklist ennen pushia
- [ ] Ei avaimia/tokenia
- [ ] Ei henkilötietoa
- [ ] Build menee läpi
- [ ] Sivu aukeaa ja sisältö on oikein

Yksinkertainen malli voittaa hienon mutta käytössä unohtuvan mallin lähes aina.
