---
title: "OpenClaw käytännössä: älä sido työthreadia ilman idle- ja max-age-rajoja"
date: "2026-07-07T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Sessions"
  - "Threads"
  - "Automation"
---
Moni huomaa OpenClawin kanssa nopeasti, että oma threadi tai topic tekee pitkästä työstä paljon siistimmän. Sitten tulee toinen vaihe: samaan paikkaan jää vanhoja sidontoja, unohtuneita alatehtäviä ja keskusteluita, joista kukaan ei enää tiedä ovatko ne vielä eläviä. Siksi minun käytännön sääntöni on tämä: **älä sido OpenClaw-työtä omaan threadiin ilman valmiiksi päätettyä poistumistietä**. Käytännössä se tarkoittaa yleensä kahta asetusta tai komentoa: `idle` ja `max-age`.

Pelkkä thread-bound-sessio ei ole vielä hyvä operatiivinen rakenne. Se on vasta alku. Hyvä rakenne syntyy vasta silloin, kun päätät myös milloin sidonta purkautuu itsestään ja milloin se katkaistaan, vaikka työ jäisi lojumaan.

## Mikä tässä menee käytännössä pieleen

Threadiin sitominen tuntuu aluksi ilmaiselta hyödyltä:

- follow-upit pysyvät samassa kontekstissa
- pääkeskustelu ei täyty välivaiheista
- yksi työ saa oman näkyvän paikkansa

Ongelma alkaa vasta myöhemmin. Jos threadi jää sidotuksi käytännössä loputtomasti, seuraava viesti voi palata vanhaan työtilaan vahingossa. Samalla ihmiselle jää helposti epäselväksi, onko kyseessä aktiivinen työ, historiallinen loki vai puolikuollut agenttisessio. Tämä on erityisen helppo moka silloin, kun OpenClawia käytetään Discord-threadeissä tai Telegram-topiceissa useisiin rinnakkaisiin töihin.

OpenClawin dokumentaatio tarjoaa tähän suoraan työkalut. `threadBindings`-ominaisuuksissa on sekä **inaktiivisuuteen perustuva auto-unfocus** että **kova enimmäisikä**. Minusta nämä eivät ole lisämukavuuksia vaan perushygieniaa.

## Mitä `idle` ja `max-age` ratkaisevat eri tavalla

Näitä kahta ei kannata ajatella samana asiana.

`idle` ratkaisee kysymyksen: **jos tähän threadiin ei kosketa hetkeen, pitäisikö sidonnan purkautua automaattisesti?** Tämä suojaa ennen kaikkea unohtuneilta tai kertaluonteisilta työthreadeilta. Jos tutkimus tai debuggaus jäi eilen kesken eikä kukaan jatkanut sitä, threadin ei tarvitse kaapata ensi viikon follow-upia vahingossa.

`max-age` taas ratkaisee toisen ongelman: **vaikka threadi olisi ajoittain aktiivinen, kuinka kauan sen pitäisi saada elää yhtenä sidottuna työtilana?** Tämä on tärkeä raja siksi, että kaikki aktiivisuus ei ole hyödyllistä jatkuvuutta. Jos samaan threadiin kaadetaan viikkojen ajan uusia sivupolkuja, vanhan kontekstin hyöty alkaa muuttua sekaannukseksi.

Minun tulkintani on yksinkertainen:

- `idle` suojaa unohtuneelta threadilta
- `max-age` suojaa liian vanhalta threadilta

Tarvitset usein molemmat.

## Milloin avaisin threadin heti

Avaan tai sidon oman threadin mielelläni heti, jos työ täyttää vähintään kaksi näistä ehdoista:

- työ jatkuu useassa viestissä eikä valmistu yhdellä vastauksella
- välitulokset ovat hyödyllisiä mutta sotkisivat pääkeskustelua
- samaa työtä pitää ehkä jatkaa tunnin tai parin päästä
- haluan erottaa yhden tutkimus-, debuggaus- tai julkaisuajon näkyvästi muista aiheista

Juuri näissä tilanteissa thread-bound-malli on hyvä. Mutta samalla asettaisin sille heti myös elinkaaren. En jättäisi sidontaa "toistaiseksi" vain siksi, että se tuntuu helpolta.

## Oma oletuspolitiikkani

Jos työ on tavallinen käytännön tehtävä, pitäisin nyrkkisääntönä tätä:

1. Sido työ threadiin tai topiciin vasta kun tiedät, että follow-upeja oikeasti tulee.
2. Aseta heti `idle`, jotta sidonta purkautuu itsestään jos työ unohtuu.
3. Aseta lisäksi `max-age`, jos on pienikin riski että threadistä tulee puolipysyvä roskakori kaikelle samantyyppiselle työlle.
4. Käytä manuaalista `/unfocus`ia silloin, kun tiedät työn olevan oikeasti valmis.

Tämä kuulostaa ehkä byrokraattiselta, mutta käytännössä se säästää yllättävän paljon virheitä. Vanha sidonta on usein hankalampi huomata kuin vanha tiedosto, koska se näkyy vasta silloin kun uusi viesti reitittyy "väärin mutta uskottavasti".

## Millaiset rajat valitsisin

En usko yhteen oikeaan numeroon, mutta käytännön heuristiikka toimii:

- muutaman tunnin tutkimus- tai debuggaustyö: lyhyt `idle`, esimerkiksi saman päivän mittainen
- päivän tai kahden mittainen projektihaara: `idle` joka siivoaa hiljaisuuden, plus selvä `max-age`
- pysyväksi uhkaava operatiivinen threadi: älä luota vain aktiivisuuteen, vaan aseta aina myös kova yläraja

Ajatus on sama kuin lokien tai cronien kanssa: jos jollain on oma elinkaari, sillä pitää olla myös siivouspolitiikka. Muuten "väliaikaisesta" tulee pysyvä.

## Miksi tämä on tärkeää erityisesti paikallisilla malleilla

Jos ajat OpenClawia paikallisella mallilla tai muuten rajallisessa ympäristössä, huono thread-hygienia maksaa tavallista enemmän. Vanha tai turhan pitkä jatkuvuus lisää helposti kontekstikuormaa, väärän työn jatkamisen riskiä ja operaattorin tulkintavirheitä. Ongelma ei aina näy tokeni- tai VRAM-mittarina, vaan siinä että sama threadi alkaa kantaa liian monta tarkoitusta.

Siksi pitäisin thread-bound-sessiota enemmän työtilana kuin muistina. Muisti kuuluu niihin paikkoihin, jotka on tehty muistia varten. Threadi on hyvä, kun sillä on rajattu tehtävä ja rajattu elinkaari.

## Missä tilanteessa en sitoisikaan threadia

En sitoisikaan omaa threadia, jos:

- työ valmistuu yhdellä tai kahdella viestillä
- follow-upit eivät oikeasti tarvitse samaa sessiota
- pääkeskustelun sekaan tuleva lisäteksti olisi minimaalista
- käyttäjä ei todennäköisesti koskaan palaa juuri tähän haaraan

Silloin erillinen threadi voi olla enemmän hallintavelkaa kuin hyötyä. Threadi ei ole palkinto siitä, että jokin työ on olemassa. Se on työkalu jatkuvuudelle.

## Oma johtopäätökseni

OpenClawissa thread-bound-sessio on hyödyllinen vasta silloin, kun myös sen poistuminen on mietitty. Jos sidot työn omaan threadiin mutta et määritä `idle`- tai `max-age`-rajoja, rakennat helposti järjestelmän joka näyttää siistiltä ensimmäisen viikon ja alkaa tuntua arvaamattomalta myöhemmin.

Siksi en kysyisi vain "pitäisikö tämä työ sitoa omaan threadiin", vaan myös: **milloin tämän threadin pitäisi lakata olemasta erityinen?** Jos siihen on valmis vastaus, sidonta on yleensä hyvä idea. Jos siihen ei ole vastausta, pitäisin työn mieluummin tavallisena kertaluonteisena ajona.

## Lähteet

- https://docs.openclaw.ai/gateway/configuration
- https://docs.openclaw.ai/gateway/config-agents
- https://docs.openclaw.ai/channels/discord
- https://docs.openclaw.ai/tools/subagents
- https://docs.openclaw.ai/help/faq
