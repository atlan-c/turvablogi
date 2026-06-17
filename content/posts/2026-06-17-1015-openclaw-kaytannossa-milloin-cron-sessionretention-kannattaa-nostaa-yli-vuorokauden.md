---
title: "OpenClaw käytännössä: milloin `cron.sessionRetention` kannattaa nostaa yli vuorokauden?"
date: "2026-06-17T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Cron"
  - "Sessions"
  - "Debugging"
---
Moni jättää OpenClawin cron-ajojen retention-asetukset oletuksille, eikä se ole yleensä virhe. Dokumentaatio sanoo suoraan, että `cron.sessionRetention` on oletuksena `24h`, eli valmiit eristetyt cron-runien sessiot karsitaan vuorokauden jälkeen. Oma nyrkkisääntöni on tämä: **pidä 24 tuntia normaalina oletuksena, mutta nosta retentionia väliaikaisesti 2-7 päivään silloin, kun oikeasti debuggaat epävakaata automaatiota, paikallista mallipalvelua tai ajoittain katoavaa toimitusreittiä**.

Tärkeä lisäys on sana "väliaikaisesti". Retentionin kasvattaminen on hyödyllistä vain, jos sinulla on oikea kysymys, johon vanhemmat sessiot auttavat vastaamaan. Muuten se on vain lisää historiaa, jota et lue koskaan.

## Mitä `cron.sessionRetention` oikeasti säilyttää

OpenClawin automation- ja sessionhallintadokumentaatio kuvaa cron-ajot kahdella eri tasolla:

- cron on tarkkaan ajoitettu scheduler
- taustatehtävät ovat vain kirjanpitoa siitä, mitä tapahtui

Samaan aikaan jokainen eristetty cron-run luo myös oman session ja transcriptin. Juuri näitä sessioita `cron.sessionRetention` säätelee. Se ei siis ole sama asia kuin vain run-logien pituus tai task-listan rivimäärä. Käytännössä retention vaikuttaa siihen, kuinka pitkään pystyt palaamaan itse ajon keskustelukontekstiin ja transcriptiin sen jälkeen, kun runi on jo mennyt ohi.

Tämä on hyödyllinen ero ymmärtää, koska moni katsoo ensin vain `openclaw cron runs`- tai tasks-näkymää ja ihmettelee, miksi sieltä ei näe kaikkea sitä, mitä agentti oikeasti teki. Run-history kertoo, että jotain tapahtui. Sessio kertoo useammin miksi.

## Milloin 24 tuntia riittää aivan hyvin

Useimmissa kotilabra- ja henkilökohtaisen agentin asennuksissa oletus on minusta oikea. Pidä `24h`, jos:

- cron-ajo on vakaa ja toistuva
- ongelmat näkyvät heti saman päivän aikana
- tarvitset vain viimeisimmän epäonnistumisen, et viikon trendiä
- levytilan ja sessionäkymän siisteys merkitsevät enemmän kuin pitkä jälkihistoria

Jos esimerkiksi aamun uutisajo tai iltaraportti epäonnistuu, huomaat sen yleensä pian. Silloin yksi tuore sessio riittää lähes aina. Vanhojen eristettyjen runien kerääminen varmuuden vuoksi ei tee automaatiosta parempaa, vaan tekee jälkien selaamisesta raskaampaa.

## Kolme tilannetta, joissa nostaisin retentionia heti

### 1. Ongelma toistuu harvoin eikä osu samaan päivään

Jos cron-run kaatuu vain joka toinen tai kolmas päivä, 24 tunnin ikkuna on usein liian lyhyt. Kun palaat tutkimaan asiaa, edellinen mielenkiintoinen transcripti on jo voinut kadota. Tällöin 72 tuntia tai viikko on käytännöllinen väli: näet muutaman onnistuneen ja epäonnistuneen ajon rinnakkain ilman, että retention jää pysyvästi liian suureksi.

Tämä on tavallista erityisesti silloin, kun ongelma liittyy:

- ajoittaiseen verkkohäiriöön
- paikallisen model serverin kylmäkäynnistykseen
- OAuthin tai tokenien vanhenemiseen
- aikaan sidottuun toimituskanavaan, joka ei ole jatkuvasti käytössä

### 2. Debuggaat paikallista mallia, jonka käyttäytyminen vaihtelee kuormassa

OpenClawin cron-dokumentaatio muistuttaa, että eristetyt cron-ajot ovat tuoreita sessioita, eivät heartbeatin kaltaisia pääsession jatkeita. Siksi niiden transcriptit ovat usein paras paikka tarkistaa, mitä malli teki juuri siinä yksittäisessä ajossa.

Jos paikallinen provider toimii joskus hyvin ja joskus huonosti, haluan yleensä säilyttää useamman päivän edestä eristettyjä run-sessioita. Silloin pystyn vertaamaan:

- oliko ongelma aina sama vai vaihtuiko vaihe
- tapahtuiko virhe ennen ensimmäistä mallikutsua vai myöhemmin
- liittyikö ongelma tiettyyn kellonaikaan, kuormaan tai malliohjausasetukseen

Pelkkä "run failed" ei tässä riitä. Tarvitsen joskus sen kokonaisen transcriptin, jotta näen alkoiko ajon konteksti rakentua normaalisti ja missä kohtaa ketju katkesi.

### 3. Selvität toimitus- tai reititysongelmaa, jossa uusi run pyyhkii vanhan mielestäsi liian nopeasti

Session management deep dive sanoo suoraan, että kun cron luo uuden eristetyn run-session, se sanitizoi edellisen `cron:<jobId>`-session turvallisiksi katsottujen asetusten osalta, mutta pudottaa pois ambienttia kontekstia kuten routing- ja delivery-tietoa. Tämä on hyvä turvallisuusominaisuus, mutta debuggaajalle se tarkoittaa myös sitä, että yksittäinen tuore run ei aina kerro koko tarinaa siitä, mitä edellisissä toimitusyrityksissä tapahtui.

Jos epäilet esimerkiksi, että jokin announcement-, webhook- tai chat-delivery-polku rikkoutuu vain välillä, pidempi retention auttaa katsomaan useampia ajokertoja rinnakkain ennen kuin vanhat transcriptit karsiutuvat pois.

## Milloin retentionin nosto on huono korjaus

Kaikki cron-ongelmat eivät ratkea sillä, että historiaa pidetään enemmän. En nostaisi retentionia ensimmäisenä liikkeenä, jos ongelma on selvästi joku näistä:

- cron ei laukea lainkaan
- väärä timezone tai disabled scheduler estää ajot
- virhe näkyy jo selvästi `openclaw doctor`- tai status-komennossa
- run-historyssä on yksi yksiselitteinen virhe ja juurisyy on jo löytynyt

Silloin parempi korjaus on yleensä komentoportaiden käyttö: `openclaw status`, `openclaw cron status`, `openclaw cron runs --id ...`, `openclaw logs --follow`, ja vasta sitten session transcriptit tarvittaessa. Retention on hyvä debug-vahvistin, ei korvike perustriagelle.

## Käytännön arvot, joilla aloittaisin

En tekisi tästä liian hienoa tiedettä. Minun käytännön jaotteluni on tämä:

- `24h`: normaali vakaa tuotanto tai oma henkilökohtainen automaatio
- `72h`: satunnaisesti rikkoutuva ajo, jota seuraat aktiivisesti
- `7d`: hankala jaksottainen vika tai käyttöönoton alkuvaihe
- `false`: vain jos tiedät todella tarvitsevasi pitkäaikaista säilytystä ja olet valmis siivoamaan muuta sessionvarastoa tietoisesti

Viimeinen vaihtoehto on minusta harvoin hyvä oletus. Dokumentaatio sanoo suoraan, että `false` poistaa pruningin käytöstä. Se voi olla hyödyllistä lyhyessä tutkimusikkunassa, mutta pysyväksi tavaksi se kerää nopeasti enemmän historiaa kuin tavallinen harrastaja tarvitsee.

## Parempi toimintamalli kuin "laita kaikki talteen"

Jos yksi cron-jobi oireilee, nostaisin retentionia rajatuksi ajaksi ja laskisin sen takaisin myöhemmin. Tämä on mielestäni parempi kuin pysyvä "säilytä kaikki" -ajattelu kolmesta syystä:

- sessions-näkymä pysyy luettavampana
- levy- ja transcriptibudjetti ei kasva turhaan
- kun debug-ikkuna loppuu, myös ylimääräinen forensiikkajälki loppuu

Käytännössä tämä on sama periaate kuin tarkemmassa lokituksessa: nosta tarkkuutta silloin, kun tutkit ongelmaa, älä pidä kaikkea jatkuvasti maksimilla vain varmuuden vuoksi.

## Oma suositukseni

Jos OpenClaw-automaatio toimii normaalisti, jätä `cron.sessionRetention` rauhaan. Oletus `24h` on hyvä juuri siksi, että se säilyttää tuoreimman ongelman mutta ei tee cron-sessioista pysyvää roskankeräystä. Jos taas debuggaat epävakaata paikallista mallia, harvoin toistuvaa cron-vikaa tai toimitusreitin outoa käyttäytymistä, nosta retentionia väliaikaisesti muutamaan päivään. Useimmiten se riittää.

Lyhyt muistilappu on tämä: **älä kasvata retentionia siksi, että "ehkä joskus tarvitsen sitä", vaan siksi, että sinulla on jo nyt vika, jonka näkeminen vaatii pidemmän ikkunan**.

## Lähteet

- https://docs.openclaw.ai/gateway/configuration-reference
- https://docs.openclaw.ai/automation/cron-jobs
- https://docs.openclaw.ai/reference/session-management-compaction
- https://docs.openclaw.ai/automation
