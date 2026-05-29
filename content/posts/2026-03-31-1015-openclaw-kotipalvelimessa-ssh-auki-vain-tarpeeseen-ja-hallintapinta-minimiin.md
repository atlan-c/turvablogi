---
title: "OpenClaw kotipalvelimessa: SSH auki vain tarpeeseen ja hallintapinta minimiin"
date: "2026-03-31T10:15:00+03:00"
draft: false
topic_family: "openclaw"
series:
  - "OpenClaw käytännössä"
tags:
  - "OpenClaw"
  - "Agents"
  - "Linux"
  - "Security"
  - "Homelab"
---
OpenClawia kotipalvelimessa ajava törmää nopeasti samaan käytännön kysymykseen kuin muussakin itsehostauksessa: **pitääkö SSH avata internetiin varmuuden vuoksi, vai pitäisikö hallintapinta rajata minimiin heti alusta asti?** Moni lähtee liikkeelle ajatuksesta, että turvallisuus syntyy riittävän vahvasta salasanasta tai portin vaihtamisesta pois numerosta 22. Käytännössä OpenClaw-koneen järkevä minimitaso on paljon arkisempi: salli vain se mitä oikeasti tarvitset, estä loput oletuksena ja nojaa avainpohjaiseen kirjautumiseen.

Lyhyt käytännön vastaus on tämä: **jos OpenClaw-hosti ei oikeasti tarvitse avointa SSH-pääsyä kaikkialta internetistä, sitä ei kannata pitää auki.** Rajattu pääsy lähiverkosta, Tailscale-/VPN-tyylisen hallitun yhteyden kautta tai muuten tarkasti rajatuista lähteistä on yleensä parempi oletus kuin "annetaan olla näkyvissä ja kovennetaan vähän".

## Miksi "vain tarpeeseen" on parempi oletus kuin "auki mutta kovennettu"?

Tietoturvassa yksi hyödyllisimmistä periaatteista on hyökkäyspinnan pienentäminen. Jos palvelu ei ole julkisesti saavutettavissa, sitä ei voi yhtä helposti kokeilla, skannata tai häiritä internetin laidalta.

Tämä kuulostaa itsestään selvältä, mutta arjessa moni tekee silti toisin. Ajatus menee usein näin:

- tarvitsen ehkä joskus etäyhteyden
- laitan SSH:n näkyville jo valmiiksi
- lisään myöhemmin kovennuksia

Ongelma on, että "myöhemmin" jää helposti tekemättä. Siksi turvallisempi oletus on kääntää ajattelu toisinpäin: **avaa vain ne yhteydet, joille on selvä käyttötarve juuri nyt**.

## Mitä hyvä minimitaso käytännössä tarkoittaa?

Kotipalvelimen SSH:n kohdalla hyvä minimitaso on usein yllättävän pieni paketti:

- julkinen sisääntulo estetään oletuksena palomuurilla
- SSH sallitaan vain niistä verkoista tai lähteistä, joista hallintaa oikeasti tehdään
- kirjautuminen tehdään avaimilla, ei salasanoilla
- root-kirjautuminen estetään suoraan SSH:n yli

Tässä ei ole mitään eksoottista. Tämä on enemmänkin siisti perusasetelma kuin "hardcore hardening".

Ubuntu-yhteisön UFW-dokumentaatio kuvaa mallin hyvin: kun palomuuri kytketään päälle oletussäännöillä, **incoming-liikenne estetään oletuksena** ja vain erikseen sallittu liikenne pääsee läpi. Juuri tämä on kotipalvelimessa hyvä lähtökohta. Kun SSH sallitaan vain tarvittavasta lähiverkosta tai tietyistä lähteistä, vahingossa liian avoimeksi jäävä hallintapinta muuttuu paljon epätodennäköisemmäksi.

## Miksi avainpohjainen SSH on oikea oletus?

OpenSSH:n dokumentaatio tukee useita kirjautumistapoja, mutta käytännössä kotipalvelimen järkevä oletus on **public key authentication**. Syy ei ole pelkästään se, että avaimet ovat vahvoja, vaan myös se, että ne vähentävät kokonaisen hyökkäysluokan houkuttelevuutta.

Kun salasanakirjautuminen on käytössä, internetiin näkyvä SSH-palvelu kiinnostaa automaattisia kokeiluja ihan eri tavalla. Kun taas kirjautuminen perustuu avainpariin, hyökkääjän tie vaikeutuu heti. Tämä ei tee koneesta maagisesti turvallista, mutta se poistaa yhden kaikkein tavallisimmista ja turhimmista riskeistä.

OpenSSH:n `sshd_config`-manuaali dokumentoi suoraan esimerkiksi asetukset **`PubkeyAuthentication`**, **`PasswordAuthentication`** ja **`PermitRootLogin`**. Juuri nämä kolme kertovat paljon siitä, miten palvelin kannattaa ajatella:

- avainkirjautuminen päälle
- salasanakirjautuminen pois
- suora root-SSH pois

Tämä kolmikko on käytännössä paljon arvokkaampi kuin esimerkiksi pelkkä portin numeron vaihtaminen. Portin vaihto voi vähentää lokiroskaa, mutta se ei korvaa oikeaa pääsynrajausta tai vahvaa kirjautumismallia.

## Entä jos tarvitsen etäkäyttöä joskus myös kodin ulkopuolelta?

Silloinkaan ensimmäinen ratkaisu ei välttämättä ole avata SSH:tä koko internetiin pysyvästi. Kannattaa erottaa kaksi eri tarvetta:

1. **tarvitsen jatkuvan etähallinnan kaikkialta**
2. **tarvitsen joskus pääsyn hallitusti kodin ulkopuolelta**

Moni harrastaja kuuluu oikeasti enemmän kategoriaan 2. Silloin on järkevää miettiä ensin hallittua pääsytapaa, joka ei jätä SSH:ta jatkuvasti laajasti näkyviin. Olennaista ei ole yksi tietty tuote tai brändi, vaan periaate: **etähallinta kannattaa tehdä niin, että hallintapinta ei ole tarpeettomasti koko internetin ulottuvilla koko ajan**.

Tämä on myös linjassa CISA:n secure-by-design-ajattelun kanssa. Turvallisempi oletus ei ole se, että käyttäjä joutuu paikkaamaan riskialtista oletustilaa käsin, vaan se, että järjestelmä suunnitellaan jo lähtökohtaisesti pienemmälle riskille.

## Miksi root-SSH:n estäminen on edelleen hyvä idea?

Tässä kohtaa joku sanoo usein, että "mutta minulla on hyvät avaimet, miksi root-kirjautuminen pitäisi silti estää?" Siksi, että hallinnan erottelu on terve tapa myös silloin, kun kaikki toimii normaalisti.

Kun kirjaudut sisään tavallisella käyttäjällä ja käytät tarvittaessa erillistä korotusta hallintatehtäviin, saat vähintään kolme käytännön hyötyä:

- virheet eivät tapahdu koko ajan suoraan root-oikeuksilla
- lokit ja käyttöpolku pysyvät selkeämpinä
- yksi suora hyökkäyskohde poistuu turhaan näkyvistä

Tämä ei yksin ratkaise kaikkea, mutta se on hyvä esimerkki asetuksesta, joka maksaa vähän ja antaa paljon.

## Missä kohtaa ihmiset yleensä tekevät virhearvion?

Yleisin virhearvio ei ole tekninen vaan psykologinen. Ajatellaan, että koska palvelin on "vain kotona" tai koska sitä käyttää yksi ihminen, riskitaso olisi automaattisesti matala.

Todellisuudessa internetiin näkyvä hallintapalvelu on internetiin näkyvä hallintapalvelu riippumatta siitä, onko vastassa yrityspalvelin vai harrastajan mini-PC. Julkinen näkyvyys tuo mukanaan jatkuvaa automaattista kokeilua ja skannausta, eikä sitä kannata kutsua kylään ilman selvää syytä.

Toinen yleinen virhearvio on uskoa, että yksi yksittäinen temppu riittää:

- "vaihdoin portin"
- "laitoin pitkän salasanan"
- "asensin tämän yhden suojakerroksen"

Parempi ajattelutapa on kerroksellisuus:

- rajaa näkyvyys
- käytä palomuuria oletus-estolla
- käytä avainkirjautumista
- estä root-SSH
- pidä hallintamalli yksinkertaisena ja ymmärrettävänä

## Oma käytännön suositukseni

Jos rakentaisin kotipalvelimen tänään, pitäisin SSH:n minimitasona tätä:

- **palomuuri päällä**
- **inbound oletuksena deny**
- **SSH sallittu vain tarpeellisista lähteistä**
- **avainpohjainen kirjautuminen käytössä**
- **salasanakirjautuminen pois**
- **suora root-kirjautuminen pois**

Tämä ei ole maksimaalinen mahdollinen kovennus, mutta se on erinomainen **järkevä minimitaso**. Ja juuri minimitaso ratkaisee eniten, koska se jää helpoimmin myös pysyvästi käyttöön.

Jos tarvitset myöhemmin enemmän joustavuutta, sitä voi lisätä hallitusti. Mutta jos aloitat liian avoimesta mallista, turvallisuus jää helposti toiveeksi eikä toteutuneeksi rakenteeksi.

## Yhteenveto

OpenClaw-hostin SSH:n kohdalla tärkein kysymys ei ole "millä tempulla tästä tehdään turvallinen vaikka se olisi auki kaikkialle", vaan **pitääkö sen olla auki kaikkialle alun perinkään**.

Useimmille harrastajille oikea vastaus on yllättävän usein ei. Kun SSH on auki vain tarpeeseen, palomuuri estää loput oletuksena ja kirjautuminen perustuu avaimiin eikä salasanoihin, OpenClawin hallintakone on jo paljon paremmassa paikassa kuin moni monimutkaisemman mutta löysemmän setupin kanssa.

Tietoturvassa hillitty on usein parempi kuin näyttävä. OpenClaw-kotipalvelimessa se näkyy juuri tässä: **vähemmän näkyvyyttä, vähemmän riskiä, vähemmän turhaa säätöä**.

## Lähteet

- OpenBSD manual: sshd_config(5): https://man.openbsd.org/sshd_config
- Ubuntu Community Help Wiki: UFW: https://help.ubuntu.com/community/UFW
- CISA Secure by Design: https://www.cisa.gov/resources-tools/resources/secure-by-design
