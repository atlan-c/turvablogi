---
title: "AI-rauta kotilabrassa: kannattaako 64 gigatavua RAMia, jos GPU:ssa on jo 24 Gt VRAMia?"
date: "2026-04-01T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "GPU"
  - "Hardware"
  - "Homelab"
  - "Troubleshooting"
---
Paikallista LLM-konetta rakentaessa huomio menee lähes aina ensin GPU:hun. Se on ymmärrettävää, koska juuri **VRAM** ratkaisee usein ensimmäisenä sen, mahtuuko malli mukavasti näytönohjaimelle vai ei. Siksi moni kysyy vasta myöhemmin toisen tärkeän kysymyksen: **jos koneessa on jo esimerkiksi 24 Gt VRAMia, onko 64 Gt järjestelmämuisti oikeasti hyödyllinen vai riittääkö 32 Gt RAM edelleen hyvin?**

Lyhyt käytännön vastaus on tämä: **jos rakennat paikallista LLM-konetta 16–24 Gt VRAMin ympärille, 32 Gt RAM on yhä käyttökelpoinen minimi, mutta 64 Gt on usein paljon järkevämpi mukavuusraja.** Se ei yleensä tee tokeneista maagisesti nopeampia samalla tavalla kuin parempi GPU, mutta se vähentää muistipainetta, helpottaa hybridiajoa, jättää tilaa useammalle työkalulle ja tekee koko koneesta vähemmän herkästi “juuri ja juuri riittävän”.

Oleellinen oivallus on tämä: **GPU:n VRAM ja järjestelmän RAM eivät kilpaile samasta roolista, vaan täydentävät toisiaan.** Kun paikallinen ajotapa muuttuu vähänkin raskaammaksi, RAM ei ole enää vain käyttöjärjestelmän sivurooli.

## Miksi tämä kysymys on juuri nyt tärkeä?

llama.cpp:n dokumentaatio muistuttaa kahdesta asiasta, jotka näkyvät suoraan harrastajakoneessa:

- kvantisointi pienentää muistinkäyttöä
- CPU+GPU-hybridiajo mahdollistaa mallit, jotka eivät kokonaan mahdu VRAMiin

Tämä on hyvä uutinen, koska se tarkoittaa, ettei jokainen projekti kaadu heti siihen, ettei koko malli mahdu näytönohjaimelle. Mutta samaan aikaan siitä seuraa yksi käytännön totuus: **jos aiot nojata hybridiajoon edes joskus, järjestelmämuistista tulee heti paljon tärkeämpi osa kokonaisuutta.**

Myös Ollaman FAQ kertoo tämän käytännönläheisesti. `ollama ps` näyttää, onko malli ladattu kokonaan GPU:lle, kokonaan CPU:lle vai osittain molempiin. Toisin sanoen paikallinen käyttö ei ole binäärinen “GPU tai ei mitään” -maailma, vaan oikeissa kokoonpanoissa kuorma voi jakautua VRAMin ja järjestelmämuistin välillä.

Tästä seuraa suoraan ostosuositus: **jos koneessa on 24 Gt VRAMia, mutta vain niukka määrä RAMia, koko setup voi silti alkaa yskiä heti kun malli, konteksti tai rinnakkaiset työkalut kasvavat vähänkin.**

## Mitä RAM oikeasti tekee paikallisessa LLM-koneessa?

Järjestelmämuistiä tarvitaan paikallisessa AI-koneessa tyypillisesti ainakin neljään asiaan:

- käyttöjärjestelmälle ja tavallisille taustaprosesseille
- mallien CPU-puoleiselle lataukselle tai osittaiselle offloadille
- embeddingeille, vektorikannoille, RAG-putkelle tai muille lisäpalikoille
- useamman samanaikaisen työkalun, editorin, selaimen ja terminaalien pyörittämiseen

Aloittelija ajattelee helposti, että jos malli “mahtuu GPU:lle”, RAMilla ei ole enää paljon väliä. Käytännössä näin ei mene. Usein juuri RAM antaa koneelle sen puskurin, jonka ansiosta työ pysyy vakaana eikä jokainen uusi välilehti, dokumentti-indeksointi tai toinen malli ala syödä käyttökokemusta.

Tämä korostuu erityisesti silloin, kun kone ei ole pelkkä yksittäisen promptin testipenkki vaan oikea päivittäinen työasema.

## Missä tilanteessa 32 Gt RAM riittää edelleen hyvin?

32 Gt on minusta edelleen täysin perusteltu valinta, jos oma käyttö näyttää enimmäkseen tältä:

- ajat yhtä mallia kerrallaan
- pyrit pitämään mahdollisimman paljon kuormasta GPU:n VRAMissa
- et käytä pitkiä konteksti-ikkunoita oletuksena
- et pyöritä raskasta RAG-putkea samassa koneessa
- et tarvitse jatkuvasti useita rinnakkaisia AI-prosesseja

Tällaisessa käytössä 32 Gt ei ole “väärä” määrä. Jos koneessa on hyvä GPU ja oma työ on lähinnä yksi paikallinen avustaja, kevyt koodiapu tai satunnainen tekstityö, 32 Gt voi toimia pitkäänkin ilman jatkuvaa kipua.

Mutta tärkeä lisäys on tämä: **32 Gt riittää yleensä parhaiten silloin, kun myös käyttökuria on.** Jos mallivalinnat pysyvät järkevinä ja muu kuorma on siisti, kaikki tuntuu vielä hyvältä. Jos tapa käyttää konetta laajenee, marginaali hupenee nopeasti.

## Milloin 64 Gt alkaa olla oikeasti parempi valinta?

64 Gt RAM muuttuu mielestäni selvästi järkevämmäksi valinnaksi heti, jos yksikin näistä pitää paikkansa:

- käytät joskus hybridiajoa, koska kaikki ei aina mahdu VRAMiin
- haluat pitää useamman mallin tai prosessin valmiina
- ajat paikallisen LLM:n lisäksi esimerkiksi embeddings- tai RAG-työkaluja
- pidät paljon selainvälilehtiä, IDE:tä ja muuta työpöytäkuormaa auki samaan aikaan
- haluat koneelle enemmän elinkaarta kuin yhden tämänhetkisen mallisukupolven verran

Tässä kohtaa 64 Gt ei ole enää “hifistelyä”, vaan käytännöllinen tapa ostaa väljyyttä. Samalla se vähentää yhtä yleistä harrastajavirhettä: rakennetaan hyvä GPU-kone, mutta säästetään juuri siinä muistimäärässä, joka määrää kuinka paljon säätöä arjessa lopulta tulee.

## Konteksti-ikkuna on usein piilossa oleva RAM- ja muistipainekysymys

Ollama käyttää oletuksena 4096 tokenin konteksti-ikkunaa, mutta sitä voi kasvattaa. Tämä kuulostaa harmittomalta asetukselta, kunnes muistaa mitä suurempi konteksti tekee muistille.

NVIDIAn tekninen kirjoitus KV-välimuistin offloadista sanoo tämän hyvin suoraan: **KV-cache kasvaa konteksti-ikkunan ja batch-koon mukana.** Esimerkkitasolla he kuvaavat, että jo suuren mallin 128k kontekstin KV-välimuisti voi nousta kymmeniin gigatavuihin.

Kotilabran harrastajalle tästä ei tarvitse vetää sitä johtopäätöstä, että pitäisi ostaa GH200-luokan superpiiri. Oleellisempi oppi on arkisempi: **pitkä konteksti ei syö vain vähän lisää muistia, vaan voi muuttaa koko muistibudjetin luonteen.**

Kun käyttäjä kasvattaa kontekstia, ajaa isompaa mallia tai avaa rinnalle toisen prosessin, 32 Gt RAM voi muuttua nopeasti “riittää juuri nyt” -tasoksi. 64 Gt taas antaa enemmän tilaa virheille, kokeilulle ja kasvulle.

## Yleinen väärinkäsitys: “jos GPU:ssa on 24 Gt VRAMia, RAM ei enää merkitse paljon”

Tämä on minusta yksi sitkeimmistä väärinkäsityksistä.

24 Gt VRAM on erittäin arvokas kapasiteetti paikallisessa LLM-ajossa. Se tekee monesta mallista paljon mukavamman käyttää ja vähentää tarvetta CPU-offloadille. Mutta se ei poista RAMin tarvetta, koska:

- kaikki mallit eivät silti aina mahdu kokonaan GPU:lle
- konteksti ja välimuistit kasvattavat muistipainetta
- muu työympäristö elää samaan aikaan
- paikallinen AI-setup on usein enemmän kuin yksi yksittäinen inferenssiprosessi

Käytännössä 24 Gt VRAM + 32 Gt RAM on usein **toimiva** yhdistelmä. Mutta 24 Gt VRAM + 64 Gt RAM on paljon useammin **huoleton** yhdistelmä.

Ja juuri huolettomuudesta moni harrastaja lopulta maksaa mielellään vähän enemmän.

## Entä Apple Silicon ja muu yhtenäismuisti?

Tässä kohtaa on hyvä muistaa, että kaikki koneet eivät käyttäydy samalla tavalla. llama.cpp nostaa Apple Siliconin erikseen esiin ensiluokkaisena alustana, ja käytännössä yhtenäismuisti muuttaa koko asetelman: CPU ja GPU eivät nojaa erillisiin muistialtaisiin samalla tavalla kuin tavallisessa pöytäkoneessa, jossa on erillinen näytönohjain.

Siksi tätä RAM-kysymystä pitää tulkita eri tavalla kahdessa maailmassa:

- **erillinen GPU + oma VRAM**: järjestelmämuisti täydentää, mutta ei korvaa VRAMia
- **yhtenäismuisti**: sama muistipooli palvelee sekä laskentaa että muuta järjestelmää

Jos rakennat tavallista PC-kotilabraa RTX-kortin ympärille, 64 Gt RAM on usein paljon helpompi perustella kuin moni ensin uskoo. Jos taas ajat paikallisia malleja yhtenäismuistisessa koneessa, koko koneen muistimäärä ratkaisee vielä suoremmin.

## Oma käytännön suositukseni

Jos rakentaisin nyt paikallista LLM-konetta 16–24 Gt VRAM -luokkaan, käyttäisin tätä nyrkkisääntöä:

- **32 Gt RAM**: hyvä minimi, jos budjetti on tiukka ja käyttö pysyy rajattuna
- **64 Gt RAM**: paras yleissuositus harrastajalle, joka haluaa joustavamman koneen
- **yli 64 Gt**: perusteltu vasta silloin, kun tiedät jo ajavasi raskaampia malleja, pidempää kontekstia tai useita AI-palikoita rinnakkain

Toisin sanoen en pitäisikään 64 gigatavua “ylellisyystasona”, vaan yhä useammin **hyvänä paikallisen AI-koneen työmuistina**, jos GPU ei ole aivan entry-level-luokkaa.

Jos budjetissa pitää valita vain yksi iso parannus, ottaisin yleensä ensin tarpeeksi VRAMia. Mutta jos VRAM on jo kunnossa ja mietit seuraavaa fiksua päivitystä, **64 Gt RAM on usein käytännöllisempi sijoitus kuin moni pienempi suorituskykyparannus paperilla.**

## Lähteet

- https://github.com/ggml-org/llama.cpp/blob/master/README.md
- https://docs.ollama.com/faq
- https://developer.nvidia.com/blog/accelerate-large-scale-llm-inference-and-kv-cache-offload-with-cpu-gpu-memory-sharing/
