---
title: "OpenClaw käytännössä: milloin puhdas subagentti on parempi kuin forkattu konteksti?"
date: "2026-05-13T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Agents"
  - "Local LLM"
  - "Troubleshooting"
  - "Automation"
---
OpenClawissa pieni mutta käytännössä tärkeä valinta on tämä: käynnistätkö subagentin puhtaana vai kopioitko sille nykyisen keskustelun `context: "fork"` -tilassa. Oletus on syystäkin puhdas `isolated`. Se pitää tokenikulun alempana, vähentää sivupolkujen sotkua ja pakottaa kirjoittamaan tehtävänannon niin, että lapsisessio voi oikeasti toimia itsenäisesti.

Lyhyt sääntö on tämä: **aloita aina `isolated`-ajattelusta ja nosta subagentti `fork`-tilaan vasta silloin, kun työ todella tarvitsee vanhan transcriptin sisältöä**. Jos tämän säännön unohtaa, delegointi alkaa nopeasti näyttää kätevältä mutta muuttuu kalliiksi, hitaaksi ja vaikeammin toistettavaksi.

## Miksi `isolated` on hyvä oletus

OpenClawin subagenttidokumentaatio sanoo tämän suoraan: native-subagentit alkavat oletuksena eristettyinä. Se ei ole vain turvallisuus- tai toteutusdetalji, vaan käytännön käyttöohje.

Puhtaalla subagentilla on kolme etua:

- se saa vain sen mitä tehtävätekstissä oikeasti tarvitsee
- tokeneita ei pala vanhan keskustelun mukana turhaan
- epäolennainen aiempi sähläys ei vuoda mukaan uuden työn päätöksiin

Tämä sopii erityisen hyvin tutkimukseen, pitkään työkalukutsuun, tiedostonmuokkaukseen tai muuhun työhön, joka voidaan kuvata selkeänä briiffinä. Jos tehtävä on mahdollista kirjoittaa yhdellä napakalla promptilla, `fork` on usein merkki siitä, että tehtävänantoa ei vielä jäsennetty kunnolla.

## Milloin `fork` on oikeasti perusteltu

`fork` kannattaa ottaa käyttöön silloin, kun lapsityö **riippuu nimenomaan nykyisen requester-session transcriptista**, ei vain samasta yleisestä tavoitteesta.

Käytännössä hyviä syitä ovat esimerkiksi nämä:

1. **Nyanssit ovat jo keskustelussa mutta vaikeita tiivistää ilman hävikkiä.**
   Esimerkiksi pitkä suunnittelukeskustelu, jossa useita vaihtoehtoja on jo rajattu pois.

2. **Lapsen pitää nähdä aiemmat työkalutulokset sellaisinaan.**
   Jos päätös riippuu juuri äsken haetusta lokista, diffistä tai analyysistä, transcriptin haarauttaminen voi olla siistimpi ratkaisu kuin kaiken liittäminen käsin uuteen tehtävään.

3. **Työ jatkaa samaa ongelmaa eikä aloita uutta alitehtävää.**
   Jos subagentti on enemmän “jatka tästä tarkemmalla analyysillä” kuin “tee oma rajattu osasi”, `fork` voi säästää aikaa.

Tärkeä rajaus on tämä: `fork` ei ole oikotie huonon tehtävänannon yli. OpenClawin dokumentaatio sanoo suoraan, että sitä kannattaa käyttää säästeliäästi eikä korvikkeena selkeälle promptille.

## Missä kohtaa `fork` alkaa maksaa liikaa

Subagentit eivät peri vain tunnelmaa vaan myös kustannusta. OpenClawin docs muistuttaa, että jokaisella subagentilla on oma konteksti ja oma tokenkulunsa. Kun lapselle haarautetaan pitkä keskustelu, mukaan siirtyy helposti paljon sellaista, joka ei auta juuri tätä yhtä tehtävää.

Silloin näkyy yleensä ainakin yksi näistä oireista:

- lapsi toistaa vanhaa keskustelua ennen kuin tekee mitään uutta
- työn käynnistyminen hidastuu ilman että lopputulos paranee
- sama delegointi toimii eri kerroilla eri tavalla, koska taustalla oleva transcripti on eri mittainen tai eri vaiheessa

Jos tunnistat nämä oireet, ongelma ei välttämättä ole mallissa vaan siinä, että delegoit käytännössä liian ison muistikuorman.

## Hyvä käytännön testi ennen spawnia

Ennen kuin spawnat subagentin, kysy yksi asia:

**Voinko kirjoittaa tämän tehtävän niin, että ulkopuolinen osaava tekijä pärjää ilman koko aiempaa keskustelua?**

Jos vastaus on kyllä, käytä `isolated`-tilaa.

Jos vastaus on ei, kysy vielä miksi ei:

- puuttuuko tehtävätekstistä olennainen rajaus
- pitäisikö mukaan liittää vain yksi tiedosto tai tiivistelmä
- vai onko transcriptissa oikeasti sellaista päätöshistoriaa, jota ei kannata tiivistää uudelleen

Yllättävän usein oikea korjaus ei ole `fork`, vaan parempi briiffi.

## Entä thread-bound sessiot?

Tässä kohtaa moni kompastuu. Session-työkalujen dokumentaatio huomauttaa, että **thread-bound native-subagentit oletusarvoisesti käyttävät `fork`-kontekstia**, ellei asetuksissa ole muuta määritelty. Se on järkevää, koska threadiin sidottu jatkotyö on usein aidosti saman keskustelun haara.

Silti sama käytännön harkinta pätee: kaikki threadiin sidottu työ ei automaattisesti tarvitse koko historiaa. Jos tarkoitus on vain tehdä rajattu taustatyö ja palata threadiin tuloksen kanssa, puhdas konteksti on usein edelleen parempi, jos ajotapa sen sallii.

## Oma nyrkkisääntöni

Jos subagentin tehtävä alkaa sanoilla “tutki”, “tarkista”, “kirjoita”, “muokkaa” tai “aja tämä workflow”, aloitan lähes aina eristetyllä kontekstilla. Jos tehtävä alkaa käytännössä sanoilla “jatka tästä samasta keskustelusta”, harkitsen `fork`-tilaa.

Tämä pieni ero tekee delegoinnista paljon vakaampaa. Puhdas subagentti pakottaa selkeyteen. `Fork` taas kannattaa säästää niihin tilanteisiin, joissa jatkuvuus on oikeasti osa tehtävää eikä vain mukavuuslisä.

## Lähteet

- https://docs.openclaw.ai/tools/subagents
- https://docs.openclaw.ai/concepts/session-tool
- https://docs.openclaw.ai/concepts/context-engine
