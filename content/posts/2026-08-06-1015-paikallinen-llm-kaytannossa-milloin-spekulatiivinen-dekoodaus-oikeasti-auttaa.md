---
title: "Paikallinen LLM käytännössä: milloin spekulatiivinen dekoodaus oikeasti auttaa?"
date: "2026-08-06T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "speculative-decoding"
  - "llama.cpp"
  - "vllm"
---
## Tiivistelmä
Spekulatiivinen dekoodaus kuulostaa helposti ilmaiselta nopeusnapilta: lisää pieni apumalli ison mallin rinnalle ja tokeneita alkaa tulla kaksinkertaista vauhtia. Käytännössä näin ei käy aina. Oma nyrkkisääntöni on tämä: **spekulatiivinen dekoodaus auttaa eniten silloin, kun varsinainen päämalli on decode-vaiheessa muistirajoitteinen, pyyntöjä ei ole liikaa rinnakkain ja draft-malli osuu riittävän usein oikein**. Jos yksikin näistä ehdoista rikkoutuu, lisärakenne voi syödä hyödyn pois.

## Mitä spekulatiivinen dekoodaus tekee

llama.cpp:n dokumentaatio kuvaa idean selvästi: pieni draft-malli arvaa useita seuraavia tokeneita etukäteen, ja päämalli tarkistaa ne yhdellä isommalla erällä. Ajatus toimii siksi, että usean tokenin käsittely yhdessä on usein tehokkaampaa kuin niiden laskeminen yksi kerrallaan.

vLLM:n dokumentaatio sanoo saman käytännön kielellä: ominaisuuden tavoite on pienentää tokenien välistä viivettä etenkin keski- ja matalan QPS:n tilanteissa, joissa työkuorma on muistirajoitteinen. Tämä on tärkeä täsmennys, koska moni harrastaja odottaa nopeutusta kaikkiin tilanteisiin, vaikka dokumentaatio itse rajaa hyödyllisen alueen paljon kapeammaksi.

## Missä tilanteessa hyöty on todennäköisin

Hyvä käyttökohde näyttää yleensä tältä:

- ajat yhtä isoa mallia yhdelle käyttäjälle tai pienelle joukolle
- pullonkaula on nimenomaan tokenien generoinnissa, ei mallin latauksessa
- GPU tai muu kiihdytin odottaa muistista tulevaa dataa enemmän kuin raakaa laskentaa
- pieni draft-malli mahtuu mukaan ilman että muistibudjetti rikkoutuu

Tällainen tilanne on tavallinen kotilabrassa, kun ajetaan esimerkiksi 14B- tai 32B-luokan mallia paikallisesti koodi- tai agenttitehtäviin. Päämalli on riittävän raskas, että jokainen hyväksytty draft-token säästää oikeaa aikaa.

## Milloin se ei ole paras ensimmäinen optimointi

Moni kokeilee spekulatiivista dekoodausta liian aikaisin. Jos perusasiat ovat vielä pielessä, aloittaisin ennemmin näistä:

- varmista että käytössä on oikea chat-template
- lukitse samplerit ja seed vertailua varten
- ota Flash Attention käyttöön jos ajomoottori ja rauta tukevat sitä
- varmista ettei draft-malli syö viimeisiä vapaita VRAM-gigatavuja

LM Studion oma julkaisuteksti varoittaa kahdesta käytännön riskistä suoraan: suorituskyky voi heiketä, jos draft-malli on liian suuri suhteessa koneen resursseihin, tai jos hyväksymisaste jää matalaksi. Toisin sanoen ylimääräinen malli ei auta, jos se vain lisää muistipainetta ja tuottaa arvauksia, jotka päämalli hylkää.

## Yhteensopivuus ratkaisee enemmän kuin moni arvaa

LM Studio korostaa, että pää- ja draft-mallin pitää olla yhteensopivia, käytännössä saman perheen tai ainakin hyvin lähellä toisiaan tokenisaation ja sanaston näkökulmasta. Tämä on erittäin käytännöllinen sääntö myös muualla kuin LM Studiossa.

Jos yhdistät satunnaisesti eri malliperheitä vain siksi, että toinen on pieni ja toinen iso, draft-tokenien hyväksyntä jää helposti heikoksi. Silloin kone tekee ylimääräistä työtä ilman todellista hyötyä. Siksi turvallinen perussääntö on valita pieni ja suuri malli samasta suvusta, esimerkiksi Qwen + Qwen tai Llama + Llama.

## Harrastajalle tärkeä ero: nopeutuuko chat vai palvelin

Yksittäisessä chat-ikkunassa nopeutuminen tuntuu yleensä suoraan parempana virtaavuutena. Palvelinpuolella tilanne on mutkikkaampi. vLLM huomauttaa, että hyöty painottuu keski- ja matalan QPS:n kuormiin. Jos samalle instanssille tulee paljon rinnakkaisia pyyntöjä, järjestelmän kokonaiskäyttäytyminen muuttuu, eikä draft-mallin lisätyö välttämättä enää kannata.

Kotikäytössä tämä tarkoittaa yksinkertaista asiaa: jos ajat paikallista mallia pääasiassa itsellesi, spekulatiivinen dekoodaus voi olla järkevä kokeilu. Jos taas palvelet useita käyttäjiä tai agentteja rinnakkain, kannattaa mitata huolella ennen kuin julistaa sen yleiseksi nopeusvoitoksi.

## Mitä llama.cpp:n toteutuksista kannattaa ymmärtää juuri nyt

llama.cpp ei enää rajoitu yhteen draft-mallimalliin, vaan dokumentaatio listaa useita toteutustapoja kuten tavallisen draft-mallin, EAGLE-3:n sekä n-gram-pohjaisia vaihtoehtoja. Tämä on käytännössä hyvä uutinen, koska kaikki kuormat eivät hyödy samasta tekniikasta.

Erityisen kiinnostava harrastajalle on n-gram-lähestymistapa silloin, kun työssä on toistuvia rakenteita. llama.cpp:n dokumentaatio mainitsee koodin uudelleenkirjoituksen esimerkkinä tilanteesta, jossa historiasta löytyviä kuvioita voi käyttää draft-ehdokkaina ilman erillistä pientä mallia. Se voi olla fiksu tapa kokeilla ideaa ilman että VRAMiin pitää mahduttaa kahta mallia.

## Käytännön sääntö kotilabraan

Jos miettisin tänään omaa paikallista LLM-pinoa, etenisin näin:

1. mittaa ensin perusmallin tokeneita sekunnissa ja time-to-first-token ilman spekulointia
2. lisää pieni saman perheen draft-malli ja katso nouseeko hyväksyttyjen draft-tokenien määrä oikeasti korkeaksi
3. seuraa samalla muistinkäyttöä, koska liian ahdas VRAM-budjetti pilaa helposti koko hyödyn
4. pidä ominaisuus käytössä vain siinä työkuormassa, jossa se oikeasti voittaa tavallisen ajon

Jos et mittaa hyväksyntää ja muistipainetta, teet helposti päätöksen pelkän tunteen perusteella. Se on juuri väärä tapa optimoida paikallista tekoälykonetta.

## Johtopäätös

Spekulatiivinen dekoodaus ei ole humpuukia, mutta se ei myöskään ole yleispätevä "2x nopeampi" -temppu. Viralliset dokumentaatiot sanovat aika suoraan, milloin se toimii: kun draft-malli on pieni ja yhteensopiva, päämalli on muistirajoitteinen decode-vaiheessa ja kuorma pysyy kohtuullisena. Harrastajalle paras oppi on tämä: kokeile sitä vasta sen jälkeen, kun helpommat optimoinnit ovat kunnossa, ja pidä se käytössä vain jos mittaus näyttää aidon voiton omassa työssäsi.

## Lähteet

- https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md
- https://docs.vllm.ai/en/latest/features/speculative_decoding/
- https://lmstudio.ai/blog/lmstudio-v0.3.10
