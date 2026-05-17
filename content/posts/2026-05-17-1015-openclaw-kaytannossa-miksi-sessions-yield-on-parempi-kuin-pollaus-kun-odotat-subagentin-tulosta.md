---
title: "OpenClaw käytännössä: miksi `sessions_yield` on parempi kuin pollaus, kun odotat subagentin tulosta?"
date: 2026-05-17T10:15:00+03:00
draft: false
topic_family: "openclaw"
---

Moni tekee OpenClawissa saman virheen heti kun ensimmäinen taustalla ajettava subagentti alkaa tuntua hyödylliseltä: spawnataan lapsi ja sitten jäädään kyselemään silmukassa joko `subagents`- tai `sessions_list`-työkalulla, joko se jo valmistui. Se toimii joskus, mutta on useimmiten huono oletus. **Käytännössä oikea oletus on tämä: jos tarvitset vain lapsen valmistumisen, spawnin jälkeen kannattaa lopettaa oma vuoro `sessions_yield`-kutsulla eikä rakentaa pollaussilmukkaa.**

Tämä on sekä halvempi että selkeämpi tapa orkestroida työtä. OpenClawin subagenttidokumentaatio sanoo tämän aika suoraan: valmistuminen on push-pohjainen, ja agentin pitäisi antaa tuloksen tulla seuraavana näkyvänä viestinä sen sijaan että se kyselee tilaa loopissa. Samasta syystä myös session tools -dokumentaatio kuvaa `sessions_yield`-työkalun nimenomaan vuoron päättämisenä, jotta seuraava viesti voi olla odotettu follow-up-tapahtuma.

## Miksi pollaus on huono oletus

Pollaus näyttää harmittomalta, mutta se sotkee kolmea asiaa yhtä aikaa:

- se polttaa turhia työkalu- ja mallikutsuja odottamiseen eikä varsinaiseen työhön
- se tekee transcriptista levottoman, koska lokiin kertyy "vieläkö valmis?" -kyselyitä
- se kasvattaa riskiä, että pääagentti jää blokkaamaan itseään odotuslogiikalla

OpenClawin oma dokumentaatio painottaa, ettei `subagents list`, `sessions_list` tai `sessions_history` -kyselyitä pidä ajaa loopissa vain valmistumisen odottamiseen. Niitä kuuluu käyttää silloin, kun tarvitset debuggausta, ohjausta tai väliintuloa — ei korvikkeena tapahtumapohjaiselle valmistumiselle.

## Mitä `sessions_yield` käytännössä tekee

`sessions_yield` ei ole vain "nuku vähän" -apu. Sen idea on tärkeämpi: se **lopettaa nykyisen vuoron tarkoituksella**, jotta seuraava mallille näkyvä viesti voi olla alityön valmistumisesta tullut jatkotapahtuma. Tästä syntyy käytännössä siistimpi orkestrointimalli:

1. spawnataan yksi tai useampi lapsityö
2. lopetetaan oma vuoro `sessions_yield`-kutsulla
3. jatketaan vasta kun tulos oikeasti saapuu

Minusta tämä on yksi niistä OpenClaw-kuvioista, joissa pieni työkaluerottelu tekee ison eron. Kun odotus erotetaan varsinaisesta päätöksenteosta, myös pääsession rooli pysyy selkeänä: se koordinoi, ei päivystä.

## Milloin pollaus silti on perusteltu

Pollaus ei ole aina väärin. Se on perusteltu silloin, kun tarvitset aktiivista valvontaa etkä vain loppuraporttia. Esimerkiksi näissä tilanteissa:

- haluat tarkistaa onko lapsi jumissa ja pitääkö sitä ohjata `subagents`-työkalulla
- tarvitset väliaikatilaa tai lokia debuggausta varten
- epäilet, että completion-reitti on rikki ja haluat varmistaa missä vaiheessa ajo oikeasti on

Ero on tärkeä: **pollaa diagnoosia varten, älä normaaliksi odotusmekanismiksi**.

## Tärkeä poikkeus: cron + `sessions_yield` kannattaa varmistaa omassa versiossa

Tässä on yksi käytännön mutka. GitHubiin raportoitiin maaliskuussa 2026 bugi, jossa `sessions_yield`-jatko cronin eristetyssä sessiossa heräsi kyllä subagentin valmistuessa, mutta orkestroija kuoli yhden LLM-vuoron jälkeen. Jos ajat monivaiheista cron-putkea juuri tällaisessa mallissa, pelkkä hyvä perusperiaate ei riitä, vaan oma OpenClaw-versio kannattaa testata.

Tämä ei kumoa pääsääntöä. Se vain muistuttaa, että tapahtumapohjainen orkestrointi on oikea malli, mutta tuotantoon vietävä cron-ketju pitää aina varmistaa sillä versiolla, jota itse oikeasti ajat.

## Käytännön sääntö harrastajalle

Jos subagentin tehtävä on vain tehdä taustatyö ja palauttaa valmis tulos, käytä tätä oletusta:

- **spawn ensin**
- **yield heti perään**
- **pollaa vain jos jokin näyttää epäilyttävältä**

Tämä pitää kustannuksen alempana, transcriptin siistimpänä ja agentin käyttäytymisen lähempänä sitä, mitä OpenClawin oma orkestrointimalli on alun perin tarkoitettu tekemään.

## Lähteet

- https://docs.openclaw.ai/tools/subagents
- https://docs.openclaw.ai/concepts/session-tool
- https://github.com/openclaw/openclaw/issues/49572
