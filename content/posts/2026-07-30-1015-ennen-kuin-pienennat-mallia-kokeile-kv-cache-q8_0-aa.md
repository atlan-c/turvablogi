---
title: "Ennen kuin pienennät mallia, kokeile KV-cache q8_0:aa"
date: "2026-07-30T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "kv-cache"
  - "ollama"
  - "llama.cpp"
  - "context"
---
## Tiivistelmä
Aja yksi yksinkertainen koe: pidä sama malli, sama prompti ja sama kone, mutta nosta vain konteksti 8k:sta 32k:hon tai 64k:hon. Jos ongelmat alkavat vasta silloin, vika ei välttämättä ole liian suuri päämalli. Todennäköisempi selitys on kasvava KV-cache, ja silloin ensimmäinen korjaus löytyy usein cache-tyypistä eikä uudesta mallista.

Minun tämänhetkinen nyrkkisääntöni on yksinkertainen: jos haluat lisää kontekstia tai enemmän rinnakkaista käyttöä, kokeile ensin `q8_0`-tasoa KV-cachelle. Siirry `q4_0`:aan vasta, jos tiedät miksi teet sen ja hyväksyt selvemmän laadullisen riskin.

## Miksi tämä vipu unohtuu

Paikallista mallia virittäessä huomio menee helposti vain GGUF-tiedoston kokoon. Se on ymmärrettävää, koska juuri se näkyy levyllä ja mallikirjastoissa. Mutta pitkissä agenteissa, dokumenttihauissa ja koodityössä muistia kuluu myös siihen, mitä malli pitää aktiivisesti kontekstissa mukana.

Ollaman context length -dokumentaatio sanoo tämän suoraan: suurempi konteksti kasvattaa muistitarvetta. Siksi 16k:sta 64k:hon siirtyminen ei ole vain "sama malli vähän pidemmällä muistilla", vaan oikea kapasiteettipäätös. Jos painot jo mahtuvat, seuraava muistisyöppö on usein juuri KV-cache.

## Miksi aloittaisin juuri `q8_0`:sta

Ollaman FAQ antaa tähän poikkeuksellisen selkeän käytännön vihjeen. Kun Flash Attention on käytössä, KV-cache voidaan kvantisoida. Dokumentaation mukaan:

- `f16` on oletus ja käyttää eniten muistia
- `q8_0` käyttää noin puolet `f16`-muistista ja laadullinen vaikutus on yleensä hyvin pieni
- `q4_0` käyttää noin neljäsosan `f16`-muistista, mutta tarkkuustappio voi näkyä selvemmin varsinkin suurilla konteksteilla

Tästä tulee mielestäni paras käytännön sääntö harrastajalle: **jos ongelma on muistipaine pitkällä kontekstilla, `q8_0` on usein parempi ensimmäinen koe kuin pienempi päämalli**. Se säästää paljon muistia, mutta ei yleensä muuta mallin käytöstä yhtä rajusti kuin siirtyminen kokonaan heikompaan kvanttiin tai pienempään malliluokkaan.

## Missä tilanteessa tämä auttaa eniten

Tämä niksi on hyödyllisin silloin, kun malli tuntuu muuten oikealta mutta jokin näistä osuu vastaan:

- 32k tai 64k konteksti ei enää mahdu ilman aggressiivista säätöä
- useampi rinnakkainen pyyntö kasvattaa VRAM-paineen liian suureksi
- agentti tarvitsee paljon työkaluja, dokumentteja tai koodikontekstia
- et haluaisi pudota kokonaan pienempään malliin vain muistisyistä

Toisin sanoen tämä ei ole ensisijaisesti "tee hitaasta mallista nopea" -temppu. Tämä on "pidä nykyinen malli käyttökelpoisena pidemmällä kontekstilla" -temppu.

## Mitä llama.cpp kertoo samasta valinnasta

llama.cpp:n CLI- ja server-dokumentaatio tukevat samaa kuvaa käytännön työkalutasolla. Sekä komentorivi että palvelin tukevat erikseen KV-cachen K- ja V-puolen tyyppivalintoja, esimerkiksi `f16`, `q8_0` ja `q4_0`. Tämä on tärkeä yksityiskohta siksi, että runtime itse kohtelee KV-cachea omana säädettävänä muistialueenaan, ei vain mallin sivutuotteena.

Jos ajat `llama.cpp`:ta suoraan, tästä seuraa hyvin konkreettinen kokeilujärjestys:

1. Aja ensin omalla normaalilla kontekstillasi `f16`-oletuksella.
2. Jos muisti tai rinnakkaisuus tulee vastaan, kokeile samaa kuormaa `q8_0`-cachella.
3. Vasta jos tämä ei riitä, arvioi onko `q4_0` hyväksyttävä kompromissi vai onko parempi pienentää kontekstia tai vaihtaa rautaa.

Tämä järjestys säilyttää yleensä mallin laadun paremmin kuin se, että aloitat heti rankemmasta päämallin kvantisoinnista.

## Milloin en menisi heti `q4_0`:aan

Ollaman FAQ varoittaa suoraan, että `q4_0`:n laadullinen haitta voi näkyä enemmän korkeilla kontekstipituuksilla. Siksi en käyttäisi sitä sokkona silloin, kun työnkulku vaatii:

- tarkkaa muistamista pitkän keskustelun yli
- työkalukutsujen ja skeemojen luotettavuutta
- dokumenttifragmenttien tarkkaa palautusta
- koodin tai konfiguraation yksityiskohtien säilymistä ilman sekoilua

Juuri näissä tehtävissä on helppo luulla, että "malli on huono". Todellinen syy voi olla se, että muistia säästettiin väärästä kohdasta liian aggressiivisesti.

## Käytännön päätöspuu

Jos paikallinen malli alkaa takkuilla pitkän kontekstin kanssa, etenisin näin:

1. Varmista ensin, että ongelma liittyy oikeasti kontekstiin tai muistipaineeseen eikä kylmäkäynnistykseen, huonoon prompttiin tai CPU-offloadiin.
2. Jos käytät Ollamaa ja backend tukee sitä, kokeile Flash Attentionia ja KV-cache-tyyppiä `q8_0`.
3. Jos käytät `llama.cpp`:ta, kokeile `-ctk q8_0 -ctv q8_0` samalla mallilla ja samalla kuormalla.
4. Mittaa vasta sen jälkeen, tarvitsetko oikeasti pienemmän mallin, lyhyemmän kontekstin tai lisää VRAMia.

Tämä on tärkeä järjestys, koska se erottaa kaksi eri kysymystä:

- onko nykyinen malli sinänsä liian suuri
- vai onko vain aktiivisen kontekstin muisti liian kallis nykyisillä asetuksilla

Liian moni tekee heti ensimmäisen diagnoosin, vaikka ongelma olisikin toinen.

## Johtopäätös

Jos paikallinen LLM toimii hyvin lyhyellä kontekstilla mutta alkaa hajota vasta pidemmällä muistilla, en pienentäisi mallia ensimmäisenä. Kokeilisin ensin KV-cachea.

Vuonna 2026 järkevin oletus ei minusta ole enää "aina `f16` tai ei mitään", mutta ei myöskään "vedä kaikki heti `q4_0`:aan". Käytännöllinen välimuoto on tämä:

- pidä `f16`, jos muistia on selvästi tarpeeksi
- kokeile `q8_0`:aa, kun tarvitset lisää pelivaraa ilman isoa laatuhaittaa
- käytä `q4_0`:aa vasta tietoisena kompromissina

Se on usein halvempi, nopeampi ja vähemmän peruuttamaton liike kuin koko mallin vaihtaminen.

## Lähteet

- https://docs.ollama.com/faq
- https://docs.ollama.com/context-length
- https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
