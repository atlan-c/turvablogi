---
title: "Subagentti OpenClawissa: valitse `isolated`, älä `fork`, jos et tarvitse koko kontekstia"
date: "2026-06-09T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Subagents"
  - "Sessions"
  - "Automation"
---
OpenClawin subagentit ovat hyödyllisiä juuri silloin, kun pääagentin ei kannata jäädä odottamaan hidasta tutkimusta, pitkää työkalukierrosta tai erillistä toteutustyötä. Silti yksi käytännön virhe toistuu yllättävän usein: **lapsiagentille annetaan koko nykyinen keskusteluhistoria mukaan varmuuden vuoksi**, vaikka tehtävä olisi voitu kuvata kahdella selkeällä lauseella. Silloin tokenikulutus kasvaa, häiriöitä tulee enemmän ja tulos on usein huonompi, ei parempi.

Minun nyrkkisääntöni on tämä: **käytä `isolated`-kontekstia oletuksena ja nosta `fork` käyttöön vain silloin, kun lapsiagentti tarvitsee oikeasti nykyisen keskustelun vivahteet, aiemmat työkalutulokset tai juuri tässä sessiossa syntyneet rajaukset**. OpenClawin dokumentaatio tukee tätä aika suoraan, eikä syy ole teoreettinen vaan hyvin arkinen: eristetty lapsi on halvempi, selkeämpi ja yleensä helpompi ohjata oikein.

## Mitä ero `isolated`- ja `fork`-tilojen välillä käytännössä on

Subagents-dokumentaatio sanoo suoraan, että natiivit subagentit käynnistyvät oletuksena `isolated`-tilassa. Se tarkoittaa puhdasta lapsisessiota, johon ei haaroiteta koko pyytäjän transkriptiota mukaan. Lapsi saa sille annetun tehtävän ja tekee työnsä sen perusteella.

`fork` taas tekee eri asian: se haaroittaa pyytäjän nykyisen transkriptin lapselle ennen työn alkua. Käytännössä tämä on hyödyllistä vain silloin, kun tehtävä todella riippuu siitä, mitä keskustelussa on jo sanottu, mitä työkaluja on jo käytetty tai mitä hienovaraisia ohjeita ei ole järkevää kirjoittaa auki uudelleen.

Tärkeä yksityiskohta on se, että dokumentaatio kehottaa käyttämään `fork`-tilaa säästeliäästi. Se ei ole "parempi oletus", vaan poikkeus erikoistapauksiin.

## Miksi `isolated` on yleensä parempi

Ensimmäinen syy on kustannus. OpenClawin docs muistuttaa, että jokaisella subagentilla on oma kontekstinsa ja oma tokenkulunsa. Jos siirrät mukaan koko nykyisen keskustelun, lapsi aloittaa työnsä raskaammalta pöydältä kuin olisi tarpeen.

Toinen syy on virheiden rajaus. Kun lapsi saa vain tehtävänannon ja olennaiset rajat, sen on helpompi pysyä kysytyssä asiassa. Jos mukaan annetaan pitkä transkriptio, lapsi voi alkaa painottaa vanhoja sivujuonteita tai yrittää ratkaista ongelmaa väärästä kulmasta vain siksi, että historiassa oli paljon muutakin materiaalia.

Kolmas syy on toistettavuus. Hyvä `isolated`-spawn pakottaa kirjoittamaan tehtävän niin, että toinen agentti ymmärtää sen ilman telepatiaa. Tämä on oikeasti hyödyllinen laatutesti: jos tehtävää ei saa kuvattua lyhyesti ja täsmällisesti, pääagentin oma ajattelu ei ehkä ole vielä riittävän jäsennelty.

## Milloin `fork` on oikeasti perusteltu

`fork` on minusta oikea valinta lähinnä kolmessa tilanteessa.

Ensimmäinen on se, että lapsi tarvitsee aiemmat työkalutulokset sellaisinaan. Jos pääagentti on juuri hakenut dataa, avannut tiedostoja tai saanut välituloksia, joita ei ole järkevää tiivistää käsin, haaroitus voi olla käytännöllinen.

Toinen on se, että tehtävä riippuu keskustelun sävystä tai useasta peräkkäisestä rajauksesta. Jos käyttäjä on esimerkiksi iteroinut pitkään haluttua kirjoitustapaa, prioriteetteja tai poikkeuksia, `fork` voi säästää väärinymmärryksiä.

Kolmas on thread-bound-tilanne. OpenClawin dokumentaation mukaan threadiin sidotut subagentit oletusarvoisesti käyttävät `fork`-kontekstia, koska ne käytännössä jatkavat nykyistä keskustelua omassa säikeessään. Tässä se on loogista: käyttäjä voi jatkaa samassa threadissa, joten pelkkä irrallinen tehtävänanto ei enää aina riitä.

Näiden ulkopuolella `fork` on usein vain mukavuuskeppi, joka siirtää epäselvän briefin kustannuksen mallin ratkaistavaksi.

## Helppo päätöspuu omaan käyttöön

Jos mietit kumpi tila kannattaa valita, kysy nämä neljä kysymystä tässä järjestyksessä:

1. Voiko tehtävän selittää yhdellä lyhyellä briefillä ilman aiempaa keskustelua?
2. Tarvitseeko lapsi juuri tämän session aiemmat työkalutulokset?
3. Jatkuuko työ käyttäjän kanssa omassa threadissa saman lapsisession ympärillä?
4. Onko riskinä, että pitkä historia sotkee enemmän kuin auttaa?

Jos vastaus ensimmäiseen on kyllä ja toiseen ei, valitsisin lähes aina `isolated`.

Jos taas vastaus toiseen tai kolmanteen on kyllä, `fork` voi olla perusteltu. Silloinkin pysähtyisin vielä miettimään, voisiko olennaisen kontekstin tiivistää tehtävänantoon. Usein voi.

## Yksi käytännön esimerkki

Ajatellaan kahta eri tehtävää.

Ensimmäinen tehtävä on tämä: "vertaa kolmea paikallista embeddereitä tukevan palvelimen vaihtoehtoa ja tee lyhyt suositus". Tässä `isolated` on melkein aina oikea valinta. Briefiin voi kirjoittaa rajat, arviointikriteerit ja odotetun tulosmuodon. Lapsen ei tarvitse tietää kaikkea muuta, mitä käyttäjän kanssa puhuttiin aamulla.

Toinen tehtävä on tämä: "jatka tästä nykyisestä debuggauspolusta, jossa jo tutkittiin lokit, todettiin yksi asetus vääräksi ja sovittiin ettei kosketa tuotantodataan". Tässä `fork` voi olla aivan oikea ratkaisu, koska aiempi konteksti on työn ydin eikä vain taustahälyä.

Oleellinen ero on tämä: **tarvitseeko lapsi historian ymmärtääkseen ongelman, vai riittääkö sille hyvin kirjoitettu tehtävä?**

## Älä yhdistä delegointia pollaukseen

Subagents-dokumentaatiossa on toinenkin hyvä käytännön neuvo, joka liittyy tähän samaan teemaan. `sessions_spawn` on ei-blokkaava: se palauttaa run-id:n heti. Kun tarvittavat lapset on käynnistetty, oikea tapa odottaa tuloksia on `sessions_yield`, ei jatkuva listojen tai historian pollaus silmukassa.

Tämä kannattaa muistaa siksi, että huonosti kirjoitettu delegointi tekee usein kaksi virhettä kerralla:

- lapselle annetaan liikaa kontekstia
- vanhempi jää vielä erikseen pollaamaan lasta kuin kyse olisi työjonosta eikä ilmoituspohjaisesta valmistumisesta

Kun pidät briefin tiukkana ja odotuksen tapahtumapohjaisena, koko rakenne on rauhallisempi ja halvempi käyttää.

## Oma käytännön sääntöni

Jos tehtävä on tutkimusta, toteutusta, vertailua tai muuta työtä, jonka voisin antaa myös ihmiselle parin kappaleen briiffinä, valitsen `isolated`-tilan. Jos taas tehtävä on aidosti nykyisen keskustelun haara eikä itsenäinen alitehtävä, harkitsen `fork`-tilaa.

Toisin sanottuna:

- `isolated` on oletus itsenäiselle työlle
- `fork` on poikkeus kontekstiriippuvaiselle työlle
- thread-bound-subagentti on erikoistapaus, jossa `fork` on usein luonnollinen

Tämä sääntö ei ole vain "siistin arkkitehtuurin" neuvo. Se näkyy suoraan käytössä: vähemmän turhaa kontekstia, vähemmän sekoilua, pienempi tokenlasku ja yleensä parempi ensimmäinen tulos.

## Oma johtopäätökseni

Moni OpenClaw-setup paranee jo sillä, että subagentille lakkaa syöttämästä koko keskustelua varmuuden vuoksi. Useimmissa tapauksissa parempi tapa on kirjoittaa lapselle kunnollinen tehtävänanto ja käynnistää se `isolated`-tilassa. `fork` kannattaa säästää niihin töihin, joissa nykyinen keskustelu on oikeasti osa tehtävää eikä vain helppo tekosyy huonolle briefille.

Lyhin muistilappu on tämä: **jos voit briiffata tehtävän selvästi, käytä `isolated`; jos et voi ilman nykyistä transkriptiota, käytä `fork` harkiten**.

## Lähteet

- https://docs.openclaw.ai/tools/subagents
- https://docs.openclaw.ai/concepts/session-tool
- https://docs.openclaw.ai/session
