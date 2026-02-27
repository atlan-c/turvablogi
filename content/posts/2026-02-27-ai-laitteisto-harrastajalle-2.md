---
title: "AI-harrastajan laitteisto 2026: mihin eurot kannattaa laittaa"
date: 2026-02-27T22:20:00+02:00
draft: false
---

Kun tavoitteena on paikallinen AI-käyttö, ensimmäinen kysymys ei ole "mikä on tehokkain", vaan "mikä on järkevin omiin töihin".

## Prioriteettijärjestys
1. **Muisti (VRAM/RAM)**
2. **Tallennus (nopea NVMe)**
3. **Laskentateho (GPU/NPU/CPU)**

Syynä on se, että käytännön pullonkaulat syntyvät usein muistista ja I/O:sta ennen raakaa laskentaa.

## Kolme profiilia
### Kevyt kokeilija
- pienet/kvantisoidut mallit
- tavoite: oppia workflowt

### Aktiivinen rakentaja
- useampi projekti, paikallinen inferenssi päivittäin
- tavoite: vakaus ja toistettavuus

### Pienimuotoinen "power user"
- pidemmät ajot, useita rinnakkaisia työkaluja
- tavoite: skaalautuva kotilabra ilman pilvikustannusten karkaamista

## Yksi käytännön sääntö
Jos kone alkaa swappaa usein AI-ajossa, seuraava päivitys kannattaa yleensä kohdistaa muistipuolelle ennen muuta.

## Nopea itsearvio
- Kuinka usein ajat mallia paikallisesti viikossa?
- Kuinka usein odotat latauksia tai levyä?
- Kuinka usein prosessi kaatuu resurssirajaan?

Näiden kolmen vastauksen perusteella laitepäivitys kannattaa suunnitella.
