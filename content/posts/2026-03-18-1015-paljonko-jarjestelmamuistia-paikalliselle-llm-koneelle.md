---
title: "Paljonko järjestelmämuistia paikalliselle LLM-koneelle oikeasti kannattaa varata?"
date: 2026-03-18T10:15:00+02:00
draft: false
---

Paikallisia malleja rakentaessa huomio menee melkein aina GPU:hun ja VRAMiin. Se on ymmärrettävää, koska juuri ne ratkaisevat usein sen, mahtuuko malli kokonaan näytönohjaimelle ja miten nopeasti generointi kulkee. Mutta harrastajalla tulee nopeasti vastaan toinen kysymys: **paljonko tavallista RAM-muistia koneessa pitäisi oikeasti olla?**

Lyhyt vastaus on tämä: jos rakennat paikallista LLM-konetta vuonna 2026, **32 Gt on käyttökelpoinen minimi, 64 Gt on monelle oikea mukavuusluokka, ja 128 Gt kannattaa vasta silloin kun ajat tarkoituksella isoja malleja osittain CPU:lla, pitkiä konteksteja tai useita raskaita prosesseja rinnakkain**.

Tärkein pointti on, että järjestelmämuisti ei korvaa VRAMia. Se kuitenkin määrää, kuinka kivuliaaksi elämä muuttuu silloin, kun malli ei mahdu kokonaan GPU:lle, kun kontekstia nostetaan, tai kun samaan koneeseen aletaan kasata RAGia, vektorihakua, editoria, selainta ja pari terminaalia samaan aikaan.

## Miksi RAM ei ole vain "muu komponentti"

Ollaman dokumentaatio tekee yhden käytännön asian selväksi: malli voi olla joko kokonaan GPU:lla, kokonaan CPU-muistissa tai osittain molemmissa. `ollama ps` näyttää tämän suoraan esimerkiksi muodossa `100% GPU`, `100% CPU` tai `48%/52% CPU/GPU`. Tämä on harrastajalle tärkeä tieto, koska juuri tässä kohtaa järjestelmämuisti muuttuu kriittiseksi.

Jos malli ei mahdu VRAMiin, kone ei taianomaisesti lopeta yrittämistä. Se alkaa käyttää järjestelmämuistia enemmän. Se voi olla aivan kelvollinen kompromissi testaukseen, mutta samalla vasteajat, tasaisuus ja koko käyttökokemus voivat muuttua paljon.

Siksi RAM kannattaa ajatella näin:

- **VRAM ratkaisee sujuvuuden ensin**
- **RAM ratkaisee kuinka paljon kompromisseja kone ylipäätään kestää**

Jos VRAM on niukka mutta RAMia on runsaasti, saat enemmän asioita edes käyntiin. Jos taas RAM loppuu kesken, kone muuttuu nopeasti epämukavaksi, vaikka GPU olisi muuten ihan järkevä.

## Mitä 32 Gt, 64 Gt ja 128 Gt käytännössä tarkoittavat?

### 32 Gt: toimii, jos tiedät mitä teet

32 gigatavua riittää monelle aloittelevalle tai hillitylle harrastajalle, jos käyttö näyttää tältä:

- ajat pääosin 7B–14B-luokan kvantisoituja malleja
- pidät kontekstin maltillisena
- et odota, että iso malli pyörii mukavasti osittain CPU:lla
- kone ei ole samaan aikaan täynnä muuta raskasta tavaraa

Tämä on edelleen täysin käyttökelpoinen taso. Ongelma ei ole se, etteikö 32 Gt toimisi, vaan se, että siihen ei jää paljon hengitysvaraa. Kun avaat selaimen, editorin, embedding-ajon, tietokannan tai pidennät kontekstia, vapaa muisti hupenee nopeasti.

### 64 Gt: paras yleissuositus useimmille harrastajille

Jos joku pyytää minulta yhtä järkevää suositusta paikalliselle LLM-koneelle, vastaan nykyään yleensä **64 Gt RAM**. Se ei ole näyttävä ostos, mutta se poistaa yllättävän monta arjen kitkaa.

64 Gt on usein hyvä kohta, koska se antaa liikkumavaraa näihin:

- mallin osittainen CPU/GPU-jako ilman välitöntä ahdistusta
- pidempi konteksti kuin perusasetuksilla
- kevyt RAG tai embedding-putki samaan aikaan
- normaali työpöytäkäyttö LLM-ajon rinnalla
- testailu ilman että jokainen virhe päätyy swapin puolelle

Tämä on juuri se muistiluokka, jossa kone alkaa tuntua harrastelun sijaan työkalulta.

### 128 Gt: hyödyllinen vain tietyssä profiilissa

128 Gt kuulostaa houkuttelevalta, mutta sitä ei kannata ostaa vain siksi, että "enemmän on parempi". Se on järkevä vasta silloin, kun käyttö on oikeasti tätä:

- ajat tarkoituksella liian isoja malleja osittain CPU-muistista
- haluat kokeilla pitkiä konteksteja ilman että kaikki muu loppuu heti kesken
- kone toimii sekä LLM-palvelimena että muuna kotilabran työhevosena
- teet rinnakkaisia ajoja tai useampia käyttäjiä palvelevaa ympäristöä

Monelle yksittäiselle harrastajalle 128 Gt ei tee 7B- tai 14B-mallien arjesta merkittävästi parempaa verrattuna 64 gigaan. Se alkaa maksaa itseään takaisin vasta silloin, kun ajat paljon kompromisseja RAMin varassa.

## Pitkä konteksti syö muistia yllättävän nopeasti

Tässä kohtaa moni aliarvioi järjestelmämuistin tarpeen. Ollaman dokumentaatio sanoo suoraan, että oletuskonteksti riippuu käytettävissä olevasta VRAMista, ja että suurempi konteksti kasvattaa muistitarvetta. Käytännössä tämä tarkoittaa, että sama kone voi tuntua kevyessä chat-käytössä täysin riittävältä, mutta muuttua paljon raskaammaksi heti kun alat nostaa kontekstia agentteja, koodausta tai dokumenttityötä varten.

Jos ajat aina oletusasetuksilla, RAM-vaatimus voi pysyä varsin kohtuullisena. Mutta jos tavoite on 32k tai 64k konteksti, kyse ei enää ole vain mallin painoista. Myös välimuistit kasvavat mukana.

Tämän takia monet tekevät väärän johtopäätöksen raudasta. He näkevät, että malli "käynnistyy", ja olettavat koneen olevan kunnossa. Todellisuudessa kokemus voi hajota vasta pidemmässä istunnossa, kun konteksti paisuu ja muistia alkaa kulua muuhunkin kuin itse malliin.

## Hitaus ei aina tarkoita, että tarvitset lisää RAMia

Toinen yleinen virhe on syyttää kaikkea hitautta muistimäärästä. llama.cpp:n suorituskykyohje varoittaa tästä hyvin käytännöllisesti: jos säiemäärä on pielessä, CPU voi ylisaturoitua ja tokeninopeus romahtaa. Dokumentin esimerkeissä liian suuri thread-arvo voi tehdä ajosta paljon hitaampaa kuin järkevämpi asetus.

Tämä on hyvä muistutus siitä, että ennen kuin ostat lisää muistia, tarkista ainakin nämä:

1. **Onko malli oikeasti GPU:lla vai osittain CPU:ssa?**
2. **Onko konteksti nostettu turhan korkeaksi?**
3. **Onko runtime säädetty järkevästi, erityisesti threadit ja GPU-offload?**
4. **Onko ongelma nopeus, laatu vai kapasiteetti?**

Lisä-RAM auttaa kapasiteettiongelmaan. Se ei korjaa huonoa konfiguraatiota.

## Käytännön ostosuositus vuonna 2026

Jos rakentaisin nyt harrastajalle paikallista LLM-konetta, miettisin RAMia näin:

- **32 Gt**, jos budjetti on tiukka ja käyttö pysyy pienissä tai keskikokoisissa kvantisoiduissa malleissa
- **64 Gt**, jos haluat fiksun, pitkäikäisemmän ja vähemmän ärsyttävän yleiskoneen
- **128 Gt**, jos tiedät jo etukäteen ajavasi osittain CPU:lle valuvia malleja, pitkiä konteksteja tai raskasta moniajoa

Jos pitäisi antaa vain yksi neuvo, se olisi tämä: **osta ensin riittävästi VRAMia käyttötapaasi varten, mutta älä kurista loppukonetta 32 gigaan vain siksi, että kaikki rahat menivät GPU:hun**. Paikallinen LLM-kone tuntuu paljon paremmalta, kun myös järjestelmämuistissa on oikeasti pelivaraa.

RAM ei ole paikallisen AI-koneen sankariosa, mutta liian pieni RAM on hyvin usein se näkymätön syy, miksi muuten lupaava kokoonpano tuntuu jatkuvasti vähän väärältä.

## Lähteet

- Ollama Docs – Context length: https://docs.ollama.com/context-length
- Ollama Docs – FAQ (`ollama ps`, CPU/GPU-jako, oletuskonteksti): https://docs.ollama.com/faq
- llama.cpp – Token generation performance tips: https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md
- Hugging Face – Llama 3.1 inference memory requirements: https://huggingface.co/blog/llama31#inference-memory-requirements
