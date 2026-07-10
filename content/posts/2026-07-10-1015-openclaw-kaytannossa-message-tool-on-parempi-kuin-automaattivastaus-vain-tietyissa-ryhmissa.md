---
title: "OpenClaw käytännössä: `message_tool` on parempi kuin automaattivastaus vain tietyissä ryhmissä"
date: "2026-07-10T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Groups"
  - "Automation"
  - "Message Tool"
---
Moni näkee `messages.groupChat.visibleReplies: "message_tool"` -asetuksen ja ajattelee heti, että sehän on selvästi fiksumpi tapa ajaa ryhmähuonetta: agentti puhuu vain silloin kun itse päättää puhua. Ajatus on hyvä, mutta käytännössä tämä tila on hyödyllinen vain tietyssä tilanteessa. Oma sääntöni on yksinkertainen: **käytä `message_tool`-vastauksia vain ryhmissä, joiden on tarkoitus olla aidosti aina päällä ja joissa malli osaa luotettavasti kutsua työkalua**. Tavallisessa kysymys-vastaus-kanavassa automaattivastaus on usein turvallisempi oletus.

Tärkein käytännön ero on tämä: `automatic`-tilassa lopullinen vastausteksti julkaistaan ryhmään normaalisti, mutta `message_tool`-tilassa OpenClaw ei julkaise mallin lopputekstiä näkyvästi lainkaan, ellei malli erikseen kutsu `message(action=send)` -työkalua. Jos työkalu jää kutsumatta, huoneessa voidaan nähdä pelkkä kirjoitusindikaattori ja lokissa tokenikulutus, mutta ei yhtään viestiä. Tämä ei ole bugi vaan asetuksen tarkoitus.

## Milloin valitsisin `message_tool`-tilan heti

Ottaisin tämän käyttöön lähinnä silloin, kun huone toimii enemmän ambient-kuuntelijana kuin tavallisena chatina:

- ryhmässä tulee paljon sivukeskustelua, jota agentin pitää seurata hiljaa
- haluat että mainitsematon puhe menee kontekstiksi eikä näkyväksi vastaukseksi
- agentin kuuluu puuttua keskusteluun vain silloin, kun sillä on oikeasti jotain hyödyllistä lisättävää
- käytössä on malli, joka osaa työkalukutsut varmasti myös ryhmätilanteissa

OpenClawin dokumentaatio suosittelee juuri tätä yhdistelmää: `unmentionedInbound: "room_event"` ja `visibleReplies: "message_tool"` samaan aina auki olevaan huoneeseen. Silloin agentti kuuntelee, mutta näkyvä vastaus vaatii aina eksplisiittisen `message`-työkalun.

## Milloin pitäisin `automatic`-tilan

Jättäisin ryhmän automaattivastauksiin, jos huone on käytännössä normaali kysy-botilta-jotain -kanava:

- käyttäjät odottavat, että @maininta tai suora kysymys tuottaa heti näkyvän vastauksen
- käytössä on heikompi tai epävarmempi paikallinen malli
- haluat minimoida tilanteet, joissa agentti "vastasi", mutta mitään ei näkynyt huoneessa
- ryhmä ei ole aina päällä oleva taustahuone vaan lähinnä käyttöliittymä agentille

Tämä on minun mielestäni se yleisin väärä optimointi. `message_tool` kuulostaa siistiltä, mutta jos malli ei hahmota toimitusmallia varmasti, saat vain vaikeammin diagnosoitavan järjestelmän. Dokumentaatio sanoo tämän melko suoraan: työkalupakotettu näkyvä reply toimii parhaiten vahvoilla, työkaluja luotettavasti kutsuvilla malleilla. Muuten `automatic` on parempi valinta.

## Mitä moni ymmärtää väärin

Yleinen harha on ajatella, että `message_tool` tarkoittaa vain "agentti saa olla välillä hiljaa". Oikeasti se tarkoittaa myös sitä, että **pelkkä lopullinen tekstivastaus ei enää riitä näkyvään julkaisuun**. Hiljaisuus ei siis synny `NO_REPLY`-sopimuksella, vaan siitä että työkalua ei kutsuttu.

Toinen helppo väärinkäsitys liittyy vikadiagnoosiin. Kun huoneessa näkyy kirjoitusindikaattori mutta ei viestiä, ensimmäinen epäily on usein kanavaintegraatio tai oikeusongelma. Se voi toki olla mahdollista, mutta dokumentaation perusteella paljon tavallisempi syy on se, että ryhmä on asetettu `message_tool`-näkyvyystilaan ja malli palautti vain yksityiseksi jäävän lopputekstin.

## Käytännön päätössääntö

Jos rakentaisin OpenClaw-huonetta omaan käyttöön, tekisin näin:

1. Aloita `automatic`-tilasta, jos ryhmässä esitetään suoria kysymyksiä botille.
2. Siirry `message_tool`-tilaan vasta, kun haluat oikeasti ambient-tyylisen aina päällä olevan huoneen.
3. Kytke samalla `unmentionedInbound: "room_event"`, koska muuten saat vain työkalupakotetun vastauksen ilman varsinaista ambient-kuuntelun hyötyä.
4. Jos huone menee hiljaiseksi "väärällä tavalla", tarkista ensin näkyvä vastaustila ja mallin työkaluluotettavuus ennen kuin alat syyttää kanavapluginia.

Minun nyrkkisääntöni on tämä: **`message_tool` on huonepolitiikka, ei yleinen laatupäivitys**. Se kannattaa ottaa käyttöön silloin, kun haluat agentin kuuntelevan paljon ja puhuvan vähän. Jos taas haluat vain luotettavan ryhmäbotin, automaattivastaus on yleensä parempi oletus.

## Yhteenveto

`messages.groupChat.visibleReplies: "message_tool"` ei ole "pro mode" kaikkiin ryhmiin. Se on paras silloin, kun rakennat ambient-huonetta vahvalla mallilla ja haluat näkyvät puheenvuorot vain eksplisiittisillä työkalukutsuilla. Tavallisessa ryhmäkanavassa, jossa ihmiset odottavat suoraa vastausta, `automatic` on useimmiten vähemmän yllättävä ja käytännössä parempi valinta.

## Lähteet

- https://docs.openclaw.ai/channels/groups
- https://docs.openclaw.ai/channels/ambient-room-events
- https://docs.openclaw.ai/gateway/config-channels
