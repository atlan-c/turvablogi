---
title: "OpenClaw käytännössä: milloin status --deep riittää ja milloin kannattaa ajaa health --json?"
date: 2026-04-12T10:15:00+03:00
draft: false
topic_family: openclaw
---

Kun OpenClawissa jokin tuntuu oudolta, ensimmäinen ongelma ei usein ole itse vika vaan se, että käytössä on monta melkein samanlaista diagnostiikkakomentoa. `openclaw status`, `openclaw status --deep`, `openclaw health`, `openclaw health --json` ja `openclaw gateway status` näyttävät paperilla läheisiltä, mutta ne vastaavat vähän eri kysymyksiin.

Käytännössä yleisin valinta on kahden komennon välillä: `status --deep` vai `health --json`.

Lyhyt vastaus on tämä: käytä `status --deep` silloin, kun haluat ihmisen luettavan nopean tilannekuvan, ja käytä `health --json` silloin, kun haluat tarkemman koneellisesti jäsennellyn snapshotin gatewayn nykytilasta tai kun pieni status-teksti jättää jotain epäselväksi.

## Mitä `status --deep` tekee hyvin?

OpenClawin terveysdokumentaatio kuvaa `openclaw status --deep` -komennon käytännössä live health probe -tarkistuksena. Se kysyy käynnissä olevalta gatewaylta syvemmän tilakuvan kuin tavallinen `status`, ja voi sisältää myös channel-probeja silloin kun niitä tuetaan.

Tärkein hyöty on luettavuus. Saat yhdellä komennolla selkeän yhteenvedon siitä:

- onko gateway tavoitettavissa
- mikä versio on käytössä
- onko palvelu käynnissä
- näkyykö session, eventien tai tehtävien puolella jotain outoa
- miltä channel-tila näyttää kokonaisuutena

Tämä on yleensä paras "ensimmäinen kunnollinen tarkistus" heti tavallisen `openclaw status` -ajon jälkeen.

## Milloin `status --deep` riittää yksinään?

Se riittää hyvin, kun kysymys on jokin näistä:

- "onko OpenClaw ylipäätään terve"
- "onko gateway käynnissä ja saavutettavissa"
- "näyttääkö channel tai heartbeat normaalilta"
- "onko päivityksen jälkeen kaikki suunnilleen kunnossa"

Toisin sanoen, kun tarvitset operatiivisen nopean kuvan ihmiselle, `status --deep` on yleensä oikea valinta. Se on nimenomaan hyvä komentorivinen tilannekuva, ei raakadataa seuraavaa analyysia varten.

## Missä `status --deep` alkaa jäädä vajaaksi?

Ongelma tulee vastaan silloin, kun summary on vähän liian tiivis.

Esimerkiksi channel voi näkyä ihmislukuisessa tilassa "configured" tai "OFF", mutta jäät silti miettimään:

- onko kanava oikeasti käynnissä vai vain konfiguroitu
- mikä account on mukana
- onko tokenia olemassa vai ei
- onko kyse aidosta viasta vai vain disabloidusta tilasta

Tällaisessa kohdassa `status --deep` on usein liian hyvä yleiskuva mutta liian karkea tarkempiin johtopäätöksiin.

## Mitä `health --json` tekee paremmin?

`openclaw health --json` pyytää gatewaylta koneellisesti luettavan health-snapshotin. Dokumentaation mukaan se on tarkoitettu nimenomaan jäsenneltyyn ulostuloon. Se ei ole vain "toinen status", vaan tarkempi tilaesitys, jossa kentät näkyvät eksplisiittisemmin.

Käytännössä tämä auttaa etenkin silloin, kun haluat erottaa toisistaan esimerkiksi nämä:

- `configured: true`
- `running: false`
- `tokenSource: none`
- `lastError: null`

Tällainen yhdistelmä kertoo paljon enemmän kuin pelkkä sanallinen tila. Se voi esimerkiksi selittää sen, että kanava on edelleen konfiguroitu mutta tarkoituksella pois päältä, eikä kyse ole oikeasta häiriöstä.

## Milloin `health --json` kannattaa ajaa?

Hyviä tilanteita ovat esimerkiksi nämä:

### 1. Kun tekstimuotoinen tila tuntuu ristiriitaiselta

Jos `status --deep` näyttää esimerkiksi kanavan olevan "configured" mutta samalla pois päältä, `health --json` auttaa purkamaan tilanteen kentiksi. Näet, onko channel oikeasti pysäytetty, puuttuuko token, onko viime virhettä, ja mikä account on kyseessä.

### 2. Kun haluat vertailla ennen-jälkeen-tiloja

Päivityksen, doctor-korjauksen tai channel-muutoksen jälkeen JSON-snapshot on hyvä, koska siitä on helpompi nähdä, mikä kenttä muuttui oikeasti. Tekstimuotoinen output on ihmisen silmälle hyvä, mutta huono täsmälliseen vertailuun.

### 3. Kun haluat turvallisen pohjan myöhemmälle analyysille

Jos olet tekemässä omaa pientä tarkistusrunbookia tai haluat kirjata havaintoja muistiin täsmällisemmin, JSON on parempi lähde kuin värillinen yhteenveto. Se pakottaa tilanteen eritellyksi tilaksi eikä tulkinnaksi.

## Entä `gateway status`, missä se tulee kuvaan?

Tämä on hyvä pitää erillään. `openclaw gateway status` ei korvaa kumpaakaan edellä mainittua komentoa, vaan vastaa eri kysymykseen. Se näyttää erityisen hyvin palvelu-vs-runtime-tiedot:

- mitä systemd oikeasti ajaa
- mitä config-polkua palvelu käyttää
- mikä bind/port on käytössä
- onko RPC probe ok

Jos siis mietit "onko juuri tämä palvelu oikealla entrypointilla ja oikeassa bindissä", `gateway status` on paras. Jos mietit "miltä koko runtime näyttää käytännössä", aloita `status --deep`:stä. Jos jokin jää epäselväksi, jatka `health --json`:iin.

## Käytännön sääntö kolmessa vaiheessa

Useimmissa ongelmissa tämä järjestys toimii hyvin:

1. `openclaw status`
2. `openclaw status --deep`
3. tarvittaessa `openclaw health --json`

Tämä säästää aikaa, koska et aloita aina raskaimmasta tai yksityiskohtaisimmasta näkymästä. Ensin katsot kokonaiskuvan, ja vasta sitten poraudut kenttiin.

## Mitä tästä kannattaa muistaa?

`status --deep` ja `health --json` eivät oikeasti kilpaile keskenään. Ne ovat eri työkaluja eri tarkkuustasolle.

- **`status --deep`** on paras nopea ihmislukuinen terveyskuva
- **`health --json`** on paras silloin, kun summary ei riitä ja haluat kenttäkohtaisen snapshotin

Jos haluat tehdä diagnostiikasta rauhallista ja järjestelmällistä, aloita ensin tilanteen lukemisesta ihmiselle ja siirry vasta sitten JSON-tarkkuuteen. Se vähentää turhaa säätöä ja tekee vianrajauksesta paljon siistimpää.

## Lähteet

- https://docs.openclaw.ai/gateway/health
- https://docs.openclaw.ai/cli/sessions
- https://docs.openclaw.ai/faq
