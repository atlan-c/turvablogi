---
title: "Mitä kannattaa päivittää ensin paikalliseen LLM-koneeseen: VRAM vai RAM?"
date: 2026-05-25T10:15:00+03:00
draft: false
topic_family: "llm-hardware"
---

Kun paikallinen LLM tuntuu tahmealta, ensimmäinen ostohalu kohdistuu helposti väärään paikkaan. Joku lisää tavallista RAM-muistia, vaikka pullonkaula on oikeasti näytönohjaimen muistissa. Toinen taas haaveilee uudesta GPU:sta, vaikka ajaa mallia käytännössä enimmäkseen CPU:n puolella. **Useimmille harrastajille oikea nyrkkisääntö on tämä: jos haluat mallin mahtuvan ja pysyvän mahdollisimman pitkälle GPU:lla, päivitä ensin VRAMia. Jos taas ajat tarkoituksella CPU:lla tai osittain CPU/GPU-hybridinä, RAM ratkaisee sen, pysyykö kone käyttökelpoisena ja mahtuuko malli ylipäänsä muistiin.**

Tämä kuulostaa itsestään selvältä, mutta käytännössä moni sekoittaa kaksi eri kysymystä:

1. missä malli lasketaan
2. mihin malli ja sen välimuistit mahtuvat

Ne eivät ole sama asia.

## VRAM ratkaisee, saatko "100 % GPU" -polun

Ollaman dokumentaatio sanoo tämän aika käytännöllisesti: `ollama ps` näyttää, onko malli ladattu kokonaan GPU:lle, kokonaan CPU:lle vai osittain molempiin. Juuri tämä jako kertoo, kumpi päivitys ostaa enemmän hyötyä.

Jos näkymä on tällainen:

- `100% GPU` → GPU-muisti riittää
- `100% CPU` → malli elää järjestelmämuistissa
- `48%/52% CPU/GPU` → ajat jo kompromissilla

Kun tavoitteena on nopeampi interaktiivinen käyttö, VRAM on yleensä se ensimmäinen kallis mutta oikea vipu. Syy on yksinkertainen: mitä suurempi osa mallista pysyy GPU:lla, sitä vähemmän joudut nojaamaan hitaampaan järjestelmämuistiin ja prosessoripolkuun tokenien generoinnissa.

Jos nykyinen kortti pakottaa mallin puoliksi CPU:lle, pelkkä RAM-lisäys ei muuta sitä maagisesti aidoksi GPU-kokemukseksi. Se voi estää kaatumisen, mutta ei välttämättä tee käytöstä paljon nopeampaa.

## RAM ratkaisee, kuinka kivuliasta hybridiajo on

Tämä ei silti tarkoita, että RAM olisi sivuroolissa. Päinvastoin: jos malli ei mahdu kokonaan VRAMiin, tavallinen RAM toimii käytännössä turvaverkkona. `llama.cpp`-keskusteluissa ja issueissa näkyy hyvin tuttu harrastajaskenaario: osa mallin kerroksista offloadataan GPU:lle, loput jäävät RAMiin, ja näin saadaan ylipäätään ajettua malli, joka ei mahtuisi yksin kumpaankaan muistiin.

Esimerkiksi `llama.cpp`-issue #1964 kuvaa suoraan tilanteen, jossa 32 Gt RAM + 24 Gt VRAM pystyy ajamaan 65B 4bit -mallia, vaikka se ei mahtuisi järkevästi pelkkään RAMiin tai pelkkään VRAMiin. Samassa tekstissä korostetaan kuitenkin myös haitta: käyttöjärjestelmä joutuu taistelemaan fyysisestä muistista, ja koko kone voi muuttua tahmeaksi tai epämukavaksi käyttää.

Eli RAM ei ole vain "lisää on kiva" -päivitys. Se määrittää, onko hybridiajo siedettävää vai tuntuuko siltä, että kone meni rikki.

## Miksi VRAM voittaa yleensä ensimmäisenä nopeudessa

`llama.cpp`-keskustelu #6124 osuu tähän kivuliaan hyvin. Siinä 14 gigatavun mallia ajetaan koneella, jossa on 8 Gt VRAM ja 32 Gt RAM. Osa kerroksista offloadataan GPU:lle, mutta nopeushyöty jää vain noin 1,5-kertaiseksi verrattuna täyteen CPU-ajoon. Keskustelussa avataan myös syy siihen, miksi jatkuva edestakainen siirtely RAMin ja VRAMin välillä ei ole mikään taikatemppu: PCIe-siirto syö aikaa nopeasti.

Käytännön opetus on tärkeä: **jos malli ei mahdu nätisti GPU:lle, RAM voi auttaa mahtumaan, mutta se ei välttämättä tee ajosta sulavaa.** Siksi suorituskykyä hakevalle harrastajalle VRAM on yleensä arvokkaampi ensimmäinen euro.

## Mutta pitkä konteksti voi muuttaa päätöksen

Ollaman context length -sivu muistuttaa, että suurempi konteksti kasvattaa muistitarvetta. Dokumentaatio antaa myös aika paljastavan oletuksen:

- alle 24 GiB VRAM → oletuksena 4K-konteksti
- 24–48 GiB VRAM → oletuksena 32K-konteksti
- 48 GiB tai enemmän → oletuksena 256K-konteksti

Tämä kertoo käytännössä siitä, että pelkkä "malli mahtuu" ei riitä. Myös konteksti syö muistia. Jos nostat kontekstin pitkäksi agentti- tai koodikäyttöä varten, VRAM-budjetti kiristyy nopeasti.

Tässä kohtaa moni tekee virheen: ostetaan vähän lisää RAMia, vaikka todellinen ongelma on se, että pitkä konteksti pakottaa mallin pois GPU:lta osittain tai kokonaan. Silloin oikea korjaus on usein enemmän VRAMia tai lyhyempi konteksti, ei uusi RAM-kampa yksinään.

## Milloin ostaisin ensin VRAMia

Päivittäisin ensin näytönohjaimen muistia tai koko GPU:n, jos useampi näistä osuu:

- haluat nopeamman chat- tai koodiapurin paikallisesti
- `ollama ps` näyttää usein osittaista CPU/GPU-jakoa
- ajat 7B–14B-luokan malleja ja haluaisit ne kokonaan GPU:lle
- käytät pidempää kontekstia, joka syö pois GPU-headroomin
- koneen CPU on jo kohtuullinen, mutta generointi tuntuu silti laahaavalta

Tässä tilanteessa lisä-RAM auttaa yleensä vähemmän kuin toivot.

## Milloin ostaisin ensin RAMia

Päivittäisin ensin järjestelmämuistia, jos useampi näistä osuu:

- ajat mallia tietoisesti ilman kunnon GPU:ta
- käytät mini-PC:tä, työasemaa tai vanhaa konetta CPU-ajoon
- kone alkaa swapata tai muu käyttö muuttuu tukkoiseksi mallin lataamisen jälkeen
- ajat hybridinä mallia, joka juuri ja juuri mahtuu vain osittaisella offloadilla
- haluat pitää muutkin ohjelmat käyttökelpoisina samaan aikaan

Tässä tilanteessa RAM ei ehkä tee mallista nopeaa, mutta se tekee koneesta huomattavasti vähemmän tuskallisen käyttää.

## Minun käytännön sääntöni harrastajalle

Jos budjetissa on tilaa vain yhdelle oikealle päivitykselle, kysy ensin tämä:

**Yritänkö saada mallin mahtumaan ja pysymään GPU:lla, vai yritänkö vain selvitä isommasta mallista nykyisellä raudalla?**

- jos ensimmäinen → osta ensin enemmän VRAMia
- jos toinen → osta ensin enemmän RAMia

Toisin sanoen VRAM ostaa yleensä nopeutta, RAM ostaa yleensä selviytymiskykyä. Molempia tarvitaan, mutta ne ratkaisevat eri ongelmaa.

Juuri siksi "paljonko muistia tarvitsen" on liian epätarkka kysymys. Parempi kysymys on: **missä haluan tämän mallin oikeasti pyörivän?**

## Lähteet

- https://docs.ollama.com/faq
- https://docs.ollama.com/context-length
- https://github.com/ggml-org/llama.cpp/issues/1964
- https://github.com/ggml-org/llama.cpp/discussions/6124
