---
title: "OpenClaw käytännössä: milloin kannattaa käyttää thread-bound ACP-sessiota?"
date: 2026-04-02T10:15:00+03:00
draft: false
topic_family: "openclaw"
---
OpenClawin kanssa vastaan tulee nopeasti käytännön valinta, joka ei ensi silmäyksellä näytä kovin tärkeältä: **ajanko tämä työn tavallisena taustadelegointina vai sidonko sen omaan pysyvämpään threadiin ACP-sessiona?**

Moni käyttää näitä aluksi lähes satunnaisesti. Jos jokin tehtävä kuulostaa isolta, se heitetään “johonkin agenttiin”, ja toivotaan että lopputulos tulee takaisin siististi. Käytännössä ero on kuitenkin iso. Väärä malli tekee keskustelusta sekavan, paisuttaa kontekstia ja vaikeuttaa jatkokysymyksiä. Oikea malli taas tekee pitkästäkin työstä yllättävän hallittavaa.

Lyhyt vastaus on tämä:

- **käytä tavallista subagenttia**, kun haluat yhden rajatun työn valmiiksi ja tiiviin yhteenvedon takaisin
- **käytä thread-bound ACP-sessiota**, kun työ jatkuu useassa vaiheessa, tarvitsee omaa keskustelutilaa tai haluat pitää saman ulkoisen harnessin — kuten Codexin tai Claude Coden — elossa follow-uppeja varten

Tämä kuulostaa pieneltä erotukselta, mutta arjessa se säästää paljon turhaa kitkaa.

## Mitä thread-bound ACP-sessio oikeastaan ratkaisee?

OpenClawin dokumentaatiossa ACP-sessio on tarkoitettu tilanteisiin, joissa halutaan ajaa **ulkoinen harness-runtime** OpenClawin kautta. Se ei siis ole vain “toinen tapa spawnata agentti”, vaan oma käyttömallinsa. Oleellinen juttu on, että sessio voidaan **sitoa nykyiseen keskusteluun tai omaan threadiin**, jolloin follow-up-viestit jatkavat samaa työtilaa.

Käytännössä tästä saa kolme hyötyä kerralla:

- sama työ ei huku uuden pyynnön alle pääkeskustelussa
- follow-upit menevät samaan runtimeen ilman että koko tehtävää alustetaan joka kerta uudestaan
- pitkä työ saa oman selvästi rajatun paikan, mikä pitää pääsession siistimpänä

Jos olet joskus huomannut, että yksi tutkimus-, debuggaus- tai koodauskeikka alkaa vallata koko keskustelua, juuri tätä ongelmaa thread-bound malli korjaa.

## Milloin tavallinen subagent riittää paremmin?

Subagentti on oikein hyvä oletus silloin, kun tehtävä on selvästi **yksi paketti**:

- hae tietoa yhdestä aiheesta
- tee yksi analyysi
- muokkaa yksi tiedosto tai pieni kokonaisuus
- aja yksi tarkistus ja raportoi takaisin

OpenClawin sub-agent-dokumentaatio painottaa juuri tätä: spawn on **non-blocking**, työ tehdään omassa sessiossa ja lopuksi tulos **announcataan takaisin pyytäjälle**. Tällainen malli on erinomainen silloin, kun et oikeasti tarvitse jatkuvaa interaktiota työn aikana.

Tämä on hyvä kysymys itselle ennen delegointia:

**haluanko vain lopputuloksen, vai haluanko myös oman työhuoneen jatkokeskustelulle?**

Jos haluat vain lopputuloksen, subagentti on yleensä siistimpi.

## Milloin ACP-thread on parempi valinta?

Thread-bound ACP-sessio kannattaa ottaa käyttöön, kun vähintään yksi näistä täyttyy:

- työ kestää pitkään ja siihen tulee todennäköisesti jatko-ohjeita
- haluat pitää saman harnessin elossa useiden viestien ajan
- tehtävä sisältää iterointia: “kokeile tämä”, “kiristä lokitusta”, “tee sama vielä toiselle repossa”
- haluat erottaa työn pääkeskustelusta näkyvästi omaan threadiin
- kyse ei ole vain OpenClaw-native delegoinnista, vaan nimenomaan ulkoisen ACP-runtime-agentin käytöstä

Tämä näkyy myös OpenClawin ohjeissa aika suoraan. ACP-agenttien dokumentaatio suosittelee thread-bound persistent -sessioita juuri silloin, kun halutaan käyttää esimerkiksi Codexia tai Claude Codea jatkuvampana työtilana eikä kertaluonteisena ajona.

## Käytännön nyrkkisääntö: kertatulos vs jatkuva työtila

Minun mielestäni selkein tapa erottaa nämä on näin:

### Valitse subagentti, jos

- tehtävä on rajattu
- yksi loppuraportti riittää
- et tarvitse samaa sessiota enää työn jälkeen
- haluat pitää kustannuksen ja kontekstin pienenä

### Valitse thread-bound ACP-sessio, jos

- työstä tulee todennäköisesti pieni oma projekti
- haluat jatkaa samassa työkontekstissa myöhemmin
- ulkoinen harness tekee työn paremmin kuin natiivi subagentti
- haluat erillisen threadin, jossa ihmiset tai agentit voivat seurata etenemistä

Tämä ei ole vain tekninen valinta vaan myös käytettävyysvalinta. Pääkeskustelu pysyy käyttökelpoisempana, kun kaikki raskas tai iteratiivinen työ ei valu samaan viestiketjuun.

## Mikä menee yleensä pieleen?

Yleisin virhe on käyttää pysyvää sessiota silloinkin, kun oikea tarve oli vain kertaluonteinen ajo. Silloin lopputuloksena on helposti:

- ylimääräinen threadi, jota kukaan ei enää käytä
- tarpeettomasti eloon jäävä runtime-konteksti
- epäselvyys siitä, mihin follow-upit pitäisi lähettää

Toinen yleinen virhe on tehdä täsmälleen päinvastoin: ajetaan pitkä, monivaiheinen työ yhä uudelleen kertaspawneina, vaikka kaikki merkit viittaisivat siihen, että samaa työtilaa tarvitaan useita kierroksia. Silloin työ alkaa muistuttaa sitä, että käynnistäisit editorin ja sulkisit sen jokaisen rivimuutoksen jälkeen.

## Entä kustannus ja hallittavuus?

Tässä kohtaa kannattaa olla käytännöllinen. OpenClawin dokumentaatio muistuttaa, että jokaisella subagentilla on oma konteksti ja oma tokenkulunsa. Sama perusajatus pätee myös pysyvämpiin sessioihin: jos pidät runtimen elossa, saat vastineeksi jatkuvuutta, mutta et ilmaiseksi.

Siksi thread-bound ACP-sessio ei ole “aina parempi”, vaan parempi vain silloin, kun jatkuvuus oikeasti tuottaa arvoa. Hyvä kysymys on:

**säästänkö tällä toistoa ja epäselvyyttä enemmän kuin lisään ylläpidettävää sessiotilaa?**

Jos vastaus on kyllä, pysyvämpi ACP-thread on usein oikea ratkaisu.

## Miten tämä liittyy topic isolation -ajatteluun?

OpenClawin omassa käytössä yksi hyödyllisimmistä tavoista välttää kontekstisotkua on pitää aiheet erillään. Kun infra, tutkimus, koodaus ja ylläpito valuvat samaan keskusteluun, agentin työ huononee nopeasti.

Thread-bound ACP-sessio on tavallaan topic isolationin tekninen vastine:

- yksi pitkä työ saa oman rajatun paikan
- follow-upit eivät saastuta pääkeskustelua
- samaan aiheeseen liittyvät päätökset ja korjaukset pysyvät yhdessä näkyvissä

Jos siis tiedät jo etukäteen, että tehtävästä tulee useamman viestin mittainen kokonaisuus, oman threadin avaaminen ei ole turhaa hienostelua. Se on usein se yksinkertaisin tapa pitää kokonaisuus ymmärrettävänä.

## Oma käytännön suositukseni

Jos pitäisi antaa vain yksi käyttökelpoinen sääntö, se olisi tämä:

**käytä subagenttia oletuksena, mutta siirry thread-bound ACP-sessioon heti kun huomaat tarvitsevasi saman ulkoisen harnessin jatkuvuutta tai oman keskustelutilan työn ympärille.**

Toisin sanoen:

- **yksi rajattu tehtävä** → subagentti
- **jatkuva, iteratiivinen tai koodipainotteinen työ omassa threadissa** → ACP-sessiona

Tällä mallilla välttää kaksi tavallista ongelmaa yhtä aikaa: pääsession tukkeutumisen ja tarpeettoman sessioiden kerrostamisen.

## Yhteenveto

OpenClawissa tärkeä ero ei ole vain “delegoinko vai en”, vaan **minkälaiseen työmuotoon delegoin**.

Subagentti on hyvä, kun haluat valmiin vastauksen takaisin. Thread-bound ACP-sessio on hyvä, kun haluat jatkuvan työtilan, jossa sama harness voi jatkaa usean viestin yli ilman että kaikki sotkee pääkeskustelua.

Käytännössä tämä on yksi niistä pienistä valinnoista, jotka tekevät agenttiympäristöstä joko siistin ja hallittavan tai vähitellen raskaan ja sekavan. Siksi sitä kannattaa ajatella etukäteen.

## Lähteet

- OpenClaw Docs, Session Tools: https://docs.openclaw.ai/concepts/session-tool
- OpenClaw Docs, ACP Agents: https://docs.openclaw.ai/tools/acp-agents
- OpenClaw Docs, Sub-Agents: https://docs.openclaw.ai/tools/subagents
