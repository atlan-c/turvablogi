---
title: "OpenClaw käytännössä: milloin pitkä työ kannattaa siirtää subagentille paikallista mallia ajettaessa?"
date: "2026-06-13T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Local LLM"
  - "Automation"
  - "Subagents"
---
Kaikki OpenClaw-työt eivät kuulu samaan sessioon, vaikka se olisi teknisesti mahdollista. Tämä korostuu erityisesti silloin, kun ajat agenttia paikallisella mallilla: pitkä tutkimusajo, iso koodimuutos tai useita työkaluaskeleita sisältävä tehtävä voi sitoa pääsession turhaan, kasvattaa kontekstia ja tehdä koko käytöstä tahmeamman kuin sen tarvitsee olla. Siksi oma nyrkkisääntöni on tämä: **jos työ kestää selvästi pitkään, tarvitsee erillistä työrauhaa tai voi epäonnistua ilman että pääkeskustelun pitäisi jäädä jumiin, siirrä se subagentille tai erilliseen spawnattuun sessioon**.

Tämä ei ole vain "siistimpi arkkitehtuuri" -temppu. OpenClawin omat dokumentit painottavat, että subagenttien pääidea on rinnakkaistaa hidas työ ilman että pääajo blokkaantuu. Session-työkalujen dokumentaatio taas muistuttaa, että `sessions_spawn` on oletuksena ei-blokkaava: se palauttaa heti ja lapsisessio jatkaa työn tekemistä omassa kontekstissaan. Käytännössä tämä tarkoittaa, että sinun ei tarvitse pitää kaikkea yhdessä pitkässä ketjussa vain siksi, että voit.

## Milloin sama sessio on vielä oikea paikka

Kaikkea ei kannata hajottaa. Jos tehtävä on lyhyt ja vastaus tarvitaan heti, pääsessio on yleensä paras paikka. Esimerkiksi nämä kuuluvat tavallisesti samaan keskusteluun:

- yksi nopea komentotarkistus
- pieni konfiguraatiomuutos, jonka vaikutus pitää nähdä heti
- yksittäinen dokumentaatiokysymys
- lyhyt "katso tämä tiedosto ja kerro mikä mättää" -tehtävä

Minun mielestäni hyvä testi on tämä: **odottaisitko itse paikallista mallia rauhassa loppuun asti ilman että haluat tehdä sillä välin mitään muuta?** Jos vastaus on kyllä ja työ loppuu pian, inline-ajo on täysin ok.

## Milloin subagentti tai spawnattu sessio alkaa voittaa

Heti kun työ muuttuu monivaiheiseksi, pitkäksi tai epävarmaksi, erillinen sessio alkaa olla parempi oletus. OpenClawin subagent-dokumentaatio nimeää tämän suoraan: tarkoitus on rinnakkaistaa tutkimus, pitkä työ ja hitaat työkalut ilman että päävirta jää kiinni.

Käytännössä siirrän työn pois pääsessiosta erityisesti näissä tilanteissa:

- tehtävä sisältää laajaa tutkimusta tai useita lähteitä
- komento tai testiajo voi kestää useita minuutteja
- työn aikana haluan pystyä vastaamaan muihin viesteihin
- tehtävä tarvitsee eri työtilan tai tiukemman eristyksen
- epäonnistuminen ei saisi sotkea pääkeskustelun kontekstia

Paikallista mallia käytettäessä tämä korostuu vielä enemmän. Hitaampi tokennopeus, rajallisempi konteksti-ikkuna ja mahdollinen työkalukierrosten määrä tekevät siitä kalliimpaa pitää yksi iso tehtävä samassa sessiossa. Vaikka kone olisi oma, "ilmainen" ei tarkoita kitkatonta. Jos yksi pitkä tehtävä syö koko huomion ja paisuttaa kontekstin, käyttökokemus huononee heti.

## Miksi tämä auttaa juuri paikallisen mallin kanssa

Pilvipalvelussa moni sietää huonompaakin rakennetta, koska raakaa nopeutta on enemmän. Paikallisessa ajossa pullonkaulat näkyvät nopeammin. Yleisiä oireita ovat:

- malli alkaa toistaa tilannepäivityksiä sen sijaan että etenisi
- pitkä historiaketju tekee seuraavista askelista hitaampia
- yksi tutkimus- tai build-ajo pitää keskustelun "varattuna"
- käyttäjä lähettää uuden viestin, mutta hyödyllinen vaste tulee vasta myöhemmin

OpenClawin docs-sivut ja GitHub-keskustelut kuvaavat tätä samaa ongelmaluokkaa eri kulmista: pitkä inline-ajo blokkaa helposti käyttöä, kun taas `sessions_spawn`-malli ja subagentit on tehty juuri tällaisten töiden irrottamiseen. Minun käytännön tulkintani on, että paikallisilla malleilla tämä kannattaa tehdä mieluummin liian aikaisin kuin liian myöhään.

## Yksinkertainen päätöspuu

Jos haluan päättää nopeasti, ajan asian tämän neljän kysymyksen läpi:

1. Kestääkö työ todennäköisesti yli pari minuuttia?
2. Tarvitseeko se useita työkaluaskelia tai paljon lukemista?
3. Haluanko, että pääkeskustelu pysyy käyttökelpoisena sillä välin?
4. Haluanko pitää tämän työn historian erillään muusta keskustelusta?

Jos yksi vastaus on "kyllä", harkitsen spawnia. Jos kaksi tai useampi on "kyllä", siirrän työn lähes aina erilliseen sessioon.

Tämä ei ole virallinen sääntö vaan toimiva harrastajan sääntö. Se pitää päätöksen kevyenä eikä vaadi joka kerta täydellistä arkkitehtuurikeskustelua.

## Mitä hyötyä erillisestä sessiosta oikeasti tulee

Suurin hyöty ei ole se, että järjestelmä näyttää hienommalta, vaan se että käyttö pysyy ennakoitavana.

Ensinnäkin pääsessio säilyy siistimpänä. Kun pitkä tutkimus tai iso muokkausketju menee omaan lapsisessioonsa, tavallinen keskustelu ei täyty välivaiheista, lokipätkistä ja puolivalmiista tilamerkinnöistä.

Toiseksi vikatilanteet rajautuvat paremmin. Jos subagentti eksyy huonoon ratkaisupolkuun, tekee turhan pitkän työkaluketjun tai tarvitsee uuden yrityksen, pääsession ajatuslanka ei mene samalla tavalla solmuun.

Kolmanneksi työtilan ja turvarajojen hallinta paranee. OpenClawin turvallisuusohjeissa korostetaan, että `sessions_spawn` kannattaa pitää sallittuna vain tarkoituksella ja että sandbox-vaatimusta voi käyttää silloin, kun työn pitää pysyä eristettynä. Tämä on hyödyllistä erityisesti silloin, kun kokeilet uutta työnkulkua, ajat epäluotettavampia työkaluja tai haluat erottaa "operaattorin keskustelun" varsinaisesta työhevosesta.

## Milloin pelkkä taustaprosessi riittää

Kaikki pitkä työ ei tarvitse kokonaista subagenttia. Jos työ on oikeasti vain yksi pitkä shell-komento, OpenClawin background exec -malli voi riittää hyvin. Dokumentaation mukaan exec-työkalu pystyy pitämään pitkän prosessin muistissa, ja process-työkalulla sitä voi hallita myöhemmin.

Oma jaotteluni menee näin:

- käytä taustaprosessia, jos ongelma on vain pitkä komento
- käytä subagenttia tai spawnattua sessiota, jos ongelma on koko tehtävän pituus, monivaiheisuus tai kontekstin sotkuisuus

Tämä ero on käytännössä tärkeä. Taustaprosessi on hyvä prosessin elinkaareen. Subagentti on hyvä ajattelun, työkalujen ja keskustelukontekstin elinkaareen.

## Missä kohtaa monet tekevät väärän valinnan

Yleisin virhe on yrittää ratkaista kaikki yhdellä pääsessiolla vain siksi, että se tuntuu aluksi yksinkertaiselta. Silloin syntyy helposti seuraava kuvio:

- pääsessiossa aloitetaan tutkimus
- samaan sessioon ajetaan testit
- samaan sessioon kirjoitetaan muutokset
- samaan sessioon odotetaan pitkää komentoa
- lopuksi ihmetellään, miksi malli vaikuttaa väsyneeltä tai alkaa hukata lankaa

Paikallisessa mallissa tämä näkyy usein vielä aikaisemmin kuin pilvimallissa. Konteksti paisuu, vasteet hidastuvat ja hyödyllisen työn suhde ympärillä pyörivään puheeseen heikkenee.

Toinen virhe on mennä toiseen ääripäähän ja spawnata kaikki. Sekään ei ole hyvä. Jos jokainen kahden minuutin tarkistus lähtee omaan sessioonsa, työnkulusta tulee hajanaisempi kuin tarpeen. Tarkoitus ei ole maksimoida agenttien määrää, vaan sijoittaa pitkä tai riskinen työ sinne missä se häiritsee vähiten muuta käyttöä.

## Oma käytännön suositukseni

Jos ajat OpenClawia paikallisella mallilla, käyttäisin tätä sääntöä oletuksena:

- pidä nopeat vastaukset ja pienet korjaukset pääsessiossa
- siirrä tutkimus, isot muokkaukset ja pidemmät ajot erilliseen sessioon
- käytä taustaprosessia vain silloin, kun kyse on oikeasti yhdestä pitkästä komennosta
- vaadi sandbox, jos työn pitää pysyä eristettynä eikä "inherit" riitä

Tällä mallilla käyttö pysyy jouhevampana, vaikka käytössä olisi vaatimattomampi GPU tai hitaampi paikallinen provider. Samalla pystyt lukemaan jälkeenpäin paremmin, mikä oli varsinainen keskustelu ja mikä oli delegoitu työ.

## Oma johtopäätökseni

Minun mielestäni tärkein käytännön oppi on tämä: **subagentti ei ole vain edistynyt orkestrointilelu, vaan tapa suojata pääsession käyttökelpoisuutta**. Paikallista mallia ajettaessa se kannattaa ottaa vakavasti jo varhain, koska juuri silloin kontekstin paisuminen, työkaluketjujen pituus ja hidas vaste alkavat tuntua oikeasti.

Jos tehtävä on lyhyt, pidä se samassa sessiossa. Jos tehtävä on pitkä, monivaiheinen tai voi sotkea keskustelun, irrota se. Useimmiten se on halvin tapa pitää sekä agentti että käyttäjä järjissään.

## Lähteet

- https://docs.openclaw.ai/tools/subagents
- https://docs.openclaw.ai/concepts/session-tool
- https://docs.openclaw.ai/gateway/background-process
- https://docs.openclaw.ai/gateway/security
- https://github.com/openclaw/openclaw/issues/50398
