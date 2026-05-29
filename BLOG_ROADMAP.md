# BLOG_ROADMAP

## Tavoite

Pitää Turvablogi kevyenä, staattisena, nopeana ja käytännönläheisenä blogina, joka keskittyy paikalliseen AI:hin, OpenClaw-agentteihin, kotilabroihin ja tietoturvatietoiseen ylläpitoon.

## Pääsarjat

### 1. OpenClaw käytännössä
- oikeat käyttötavat arjen agenttityössä
- sessionhallinta, cronit, taskit ja muistikäytännöt
- virhetilanteet, diagnostiikka ja palautuspolut

### 2. AI-kotilabra
- GPU-, VRAM-, RAM- ja tallennusvalinnat
- pullonkaulat ennen turhia hankintoja
- melu, lämpö, virrankulutus ja käytännön kompromissit

### 3. Paikalliset LLM:t
- milloin paikallinen malli riittää
- milloin pilvi on käytännössä parempi
- RAG, kvantisointi, konteksti, nopeus ja käyttökokemus

### 4. Windows IT ja AI
- tukihenkilön AI-apuvälineet
- PowerShell + AI -työnkulut
- dokumentointi, triage ja automaation rajat

### 5. Tietoturvan minimikäytännöt
- pienet muutokset, jotka vähentävät riskiä oikeasti
- staattisen sivuston, kotipalvelimen ja agenttiympäristön perushygienia
- mitä ei kannata monimutkaistaa ilman selkeää hyötyä

## Julkaisuperiaatteet

- yksi käytännön kysymys per postaus
- vähemmän hypeä, enemmän mittaamista ja rajauksia
- kerro myös mikä ei toiminut
- suosi evergreen-sisältöä, mutta reagoi ajankohtaisiin ilmiöihin kun niistä on oikeaa hyötyä
- pidä postaukset linkitettävissä ja helposti selattavina myös kuukausien päästä

## Artikkeli-ideat

### OpenClaw käytännössä
1. Miten rakennat pienen mutta kestävän cron-ajon ilman prompttispagettia
2. Milloin agentin kannattaa kirjoittaa MEMORY.md:hen ja milloin ei
3. Miten erotat oikean tuotantovirheen väärästä hälystä OpenClaw-ajossa
4. Mitä hyötyä on topic-eristyksestä usean projektin rinnakkaistyössä
5. Milloin current-session-sidonta on oikea valinta ja milloin ansa

### AI-kotilabra
6. Miten paljon kotilabran sähkö- ja melukulu lopulta maksaa kuukaudessa
7. Milloin halpa käytetty workstation on parempi kuin uusi kuluttajapelikone
8. Miten valitset kotilabraan virtalähteen, kun GPU-päivitys on vasta suunnitteilla
9. Onko PCIe-riser tai ulkoinen GPU-kehikko koskaan järkevä paikalliselle LLM:lle
10. Milloin jäähdytyksen parantaminen tuo enemmän hyötyä kuin seuraava CPU-päivitys

### Paikalliset LLM:t
11. Milloin 7B-malli on käytännössä parempi kuin huonosti mahtuva 14B-malli
12. Miten arvioit, onko pitkä konteksti oikeasti hyödyllinen omassa työssäsi
13. Milloin RAG tuo lisäarvoa ja milloin se vain lisää vikapisteitä
14. Miten vertailla llama.cpp:ta ja Ollamaa ilman benchmark-teatteria
15. Mikä on riittävä minimilaatu paikalliselle mallille tukityössä

### Windows IT ja AI
16. Miten AI auttaa tukipyyntöjen triagessa ilman että siitä tulee uusi riski
17. PowerShell + AI: lokien tiivistäminen niin, että alkuperäinen data säilyy auditoitavana
18. Miten kirjoitat AI:lle hyvän ympäristökuvauksen Windows-vianrajausta varten
19. Milloin helpdesk-tiimin kannattaa käyttää paikallista mallia eikä pilveä
20. Mitä AI:lle ei kannata koskaan syöttää yritysympäristössä ilman erillistä päätöstä

### Tietoturvan minimikäytännöt
21. Staattisen blogin kovennuslista: headerit, julkaisuputki ja vähimmän ylläpidon malli
22. Miten pienennät kotipalvelimen hyökkäyspintaa ilman että ylläpito muuttuu tuskaksi
23. OAuth-vanheneminen automaatiossa: tunnista, rajoita, palauta siististi
24. Mitkä lokit kannattaa oikeasti säilyttää agenttiympäristössä ja kuinka kauan
25. Milloin sisäinen wiki kannattaa pitää irrallaan agentin pitkästä muistista
26. Miten arvioit uuden automaation tietoturvariskiä ennen käyttöönottoa

## Seuraavaksi kirjoitettavat draftit

- OpenClaw käytännössä: mitä agentilta kannattaa oikeasti pyytää?
- AI-kotilabra: mitä kannattaa mitata ennen uuden GPU:n ostamista?
- Windows-tukihenkilön AI-työkalupakki
- Paikallinen LLM vai pilvimalli: käytännön valintakriteerit
- Staattisen blogin tietoturva: miksi yksinkertainen on usein parempi

## Manuaalinen toimitustyö myöhemmin

- tarkista tagien heuristiikka vanhoista postauksista satunnaisotannalla
- nosta parhaat sarjat näkyviin myös navigaatioon, jos sisältöä kertyy lisää
- harkitse erillistä "aloita tästä" -sivua, jos uusien lukijoiden määrä kasvaa
- lisää mahdollinen kevyt hakusivu vain jos tagi- ja otsikkosuodatus ei enää riitä
