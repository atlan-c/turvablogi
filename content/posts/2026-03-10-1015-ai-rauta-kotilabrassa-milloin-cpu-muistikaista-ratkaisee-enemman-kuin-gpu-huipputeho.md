---
title: "OpenClaw käytännössä: miten erotat BUILDER- ja OPERATOR-työt ilman turhaa kitkaa?"
date: 2026-03-10T10:15:00+02:00
draft: false
topic_family: "openclaw"
---
Monessa OpenClaw-ympäristössä hyödyllisin jako ei ole tekninen vaan toiminnallinen: **rakennetaanko nyt jotakin uutta vai operoidaanko jo olemassa olevaa järjestelmää?** Tätä varten BUILDER- ja OPERATOR-ajattelu on käytännössä hyvä, koska se pakottaa kysymään, mikä tämän työn riskitaso ja tavoite oikeasti on.

BUILDER-työssä saa olla enemmän tutkimusta, vaihtoehtojen vertailua, luonnostelua ja kokeilua. OPERATOR-työssä taas arvokkaita ovat toistettavuus, lokit, varmistukset ja varovainen eteneminen. Jos nämä kaksi sekoittaa samaan toimintatapaan, syntyy helposti kitkaa: ylläpitotyöstä tulee liian improvisoitua tai suunnittelusta liian jäykkää.

Minun mielestäni yksinkertainen sääntö toimii hyvin. Jos tehtävä muuttaa rakennetta, prosessia, promptia, dokumentaatiota tai työtapaa, se on usein BUILDER-työtä. Jos tehtävä toteuttaa olemassa olevan runbookin, ajaa tarkistuksen, päivittää tilaa tai valvoo rutiinia, se on usein OPERATOR-työtä. Tämä ei ole muodollinen pakko, mutta se auttaa valitsemaan oikean tason varmistuksia ja oikean paikan keskustelulle.

## Käytännön hyöty

- BUILDER: enemmän suunnittelua, vaihtoehdot näkyviin, rauhallinen kokeilu
- OPERATOR: vähemmän improvisaatiota, selkeä runbook, parempi audit trail
- jaottelu vähentää sitä, että vahingossa "suunnitellaan" keskellä tuotantotyyppistä ajoa

## Lähteet

- https://github.com/openclaw/openclaw
- https://docs.openclaw.ai/automation
- https://docs.openclaw.ai/concepts/session-tool
