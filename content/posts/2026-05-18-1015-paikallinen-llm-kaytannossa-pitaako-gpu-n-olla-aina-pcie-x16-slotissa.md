---
title: "Paikallinen LLM käytännössä: pitääkö GPU:n olla aina PCIe x16 -slotissa?"
date: "2026-05-18T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "Local LLM"
  - "GPU"
  - "Hardware"
  - "Troubleshooting"
  - "Homelab"
---
Moni paikallista LLM-konetta kasaava jumittuu samaan huoleen heti emolevyä valitessa: jos vapaa paikka on vain PCIe x8 tai pahimmillaan sähköisesti x4, tappaako se koko projektin? Lyhyt käytännön vastaus on tämä: **yhdellä GPU:lla ajettava paikallinen LLM ei yleensä tarvitse täyttä x16-kaistaa tokenien generointiin, mutta liian kapea väylä alkaa silti näkyä mallin latauksessa, promptin syötössä ja kaikissa CPU:n ja GPU:n välisissä hybridikuvioissa**.

Toisin sanoen: älä maksa turhaan x16-paniikista, mutta älä myöskään kuvittele, että kaikki slotit ovat käytännössä samanarvoisia.

## Missä PCIe-kaista oikeasti näkyy

Paikallisessa LLM-ajossa on hyödyllistä erottaa kaksi asiaa toisistaan:

- **tokenien generointi** eli varsinainen vastausnopeus
- **datan ja painojen siirtely** eli mallin lataus, promptin käsittely ja mahdollinen CPU/GPU-offload

Jos malli mahtuu kokonaan GPU:n VRAMiin ja ajo pysyy muutenkin yhden kortin sisällä, PCIe-väylä ei ole yleensä ensimmäinen pullonkaula. GPU tekee raskaan työn omassa muistissaan, eikä jokaisesta tokenista tarvitse ravata takaisin emolevyn yli.

Sen sijaan PCIe alkaa merkitä heti enemmän, jos jokin näistä toteutuu:

- malli ei mahdu kokonaan VRAMiin
- osa painoista jää RAMiin tai CPU:lle
- promptit ovat pitkiä ja niitä syötetään usein
- käytät useampaa GPU:ta tai epäsymmetristä offloadia
- käynnistelet mallia usein uudelleen etkä pidä sitä lämpimänä muistissa

Tämä on minusta se olennaisin oivallus: **PCIe-kaista ei yleensä määritä "voiko tällä ajaa LLM:ää", vaan sitä kuinka paljon kitkaa käyttöön tulee ympärillä**.

## Mitä x16 vs x8 näyttää käytännön mittauksissa

Samuel Zhangin MI50-benchmark on kiinnostava juuri siksi, että se mittaa samaa malliluokkaa usealla PCIe-kokoonpanolla. Yhden 32 Gt GPU:n testissä PCIe 3.0 x16 ja x8 olivat eval-nopeudessa käytännössä lähes samat: deepseek-r1-mallilla noin 15,6–16,8 tokenia sekunnissa ja gemma3:lla noin 17,8–19,4 tokenia sekunnissa. Ero jäi muutaman prosentin sisään.

Käytännön tulkinta harrastajalle on aika rauhoittava: **jos malli mahtuu kortille, x8 ei yleensä romahduta generointinopeutta**. Tämä sopii hyvin siihen, mitä moni huomaa arjessa myös käytetyllä palvelinraudalla ja kuluttaja-alustoilla.

Samassa aineistossa näkyy myös toinen hyödyllinen asia: lisä-GPU ei automaattisesti nopeuta ajoa, jos yhdellä kortilla on jo tarpeeksi VRAMia. Silloin lisää kaistoja tai lisää kortteja ei kannata tuijottaa suorana pikavoittona.

## Miksi x8 voi olla ihan fine, vaikka x16 kuulostaa "oikealta"

LLM-harrastuksessa tulee helposti ajatusvirhe, että näytönohjaimen pitää toimia samoin kuin peleissä tai muussa jatkuvassa host-device-siirrossa. Inference ei aina käyttäydy niin.

Kun painot ovat valmiiksi VRAMissa, seuraava token syntyy pääosin GPU:n omalla muistialueella ja laskennalla. Siksi väylän leventäminen x8:sta x16:een ei automaattisesti tuo näkyvää lisähyötyä. Usein tärkeämpiä ovat nämä:

- paljonko kortissa on VRAMia
- mahtuuko malli järkevällä kvantisoinnilla kokonaan sinne
- kuinka nopea kortin oma muistijärjestelmä on
- kuinka hyvin backend, kvantisointi ja batch-asetukset sopivat raudalle

Jos siis valitset emolevyn kahden muuten samanlaisen vaihtoehdon välillä, x16 on edelleen miellyttävämpi marginaali. Mutta jos hyvä kone tarjoaa GPU:lle vain x8-yhteyden, en hylkäisi kokoonpanoa sen takia yksin.

## Missä liian kapea väylä alkaa oikeasti sattua

Tästä kohtaa kannattaa olla rehellinen: **x8 on eri asia kuin x4, ja x4 on eri asia kuin jokin chipsetin takaa tuleva kompromissislot**.

`llama.cpp`-keskustelussa ja siihen liittyvässä kehitystyössä nousee hyvin esiin, että CPU+GPU-hybridiajossa promptin käsittelyn kannattavuus riippuu paitsi mallista myös PCIe-kaistasta. Jos iso määrä painoja on CPU:n puolella, niiden siirtäminen GPU:lle promptin käsittelyä varten voi maksaa enemmän aikaa kuin mitä offloadilla voitetaan. Toisin sanoen liian kapea väylä voi heikentää juuri sitä kohtaa, joka tuntuu käyttäjästä eniten "tahmealta": aikaa ensimmäiseen tokeniin.

Tästä seuraa hyvä käytännön sääntö:

- **x16** = paras yleisratkaisu, etenkin jos rakennat joustavaa konetta tulevia kokeiluja varten
- **x8** = yleensä täysin käyttökelpoinen yhdelle VRAMiin mahtuvalle mallille
- **x4** = voi olla hyväksyttävä hätävara, mutta vaatii enemmän kompromisseja eikä ole ihanteellinen vakavaan hybridiajoon
- **x1 / chipset-kiertotiet** = lähinnä kokeiluun, ei mukavaan päivittäiseen käyttöön

En siis sanoisi "x4 ei koskaan toimi". Sanoisin mieluummin: **älä suunnittele mukavaa paikallista LLM-konetta x4:n varaan, jos voit välttää sen**.

## Milloin kaistoja kannattaa priorisoida kovaa

Priorisoisin PCIe-kaistoja tavallista enemmän, jos jokin näistä osuu omaan suunnitelmaan:

- aiot jakaa mallia usean GPU:n välille
- iso osa mallista jää CPU:lle tai järjestelmämuistiin
- ajat paljon pitkiä dokumenttipromptteja tai RAG-kuormaa
- käytät MoE-malleja tai muita hybridejä, joissa painojen liike korostuu
- haluat käyttää samaa konetta myöhemmin myös muuhun kuin pelkkään yhteen valmiiksi sopivaan malliin

Silloin väylä ei ole vain pieni detalji vaan osa koko koneen käyttökelpoisuutta.

## Milloin priorisoisin jotain muuta ensin

Yllättävän usein tärkeämpi ostojärjestys on tämä:

1. riittävästi VRAMia
2. riittävästi RAMia ja siisti muistikonfiguraatio
3. järkevä jäähdytys ja virtalähde
4. vasta sen jälkeen täydellinen PCIe-ylellisyys

Jos vaihtoehdot ovat esimerkiksi:

- 24 Gt VRAM kortti x8-slotissa
- 12 Gt VRAM kortti x16-slotissa

valitsisin paikalliseen LLM-käyttöön useimmiten ensimmäisen. Liian pieni VRAM pysäyttää projektin paljon varmemmin kuin x8-yhteys.

## Yhteenveto

Pitääkö GPU:n olla aina PCIe x16 -slotissa paikallista LLM:ää varten? Ei. **Yhden GPU:n inference-ajossa x8 on usein aivan riittävä, jos malli mahtuu VRAMiin.**

Mutta kaistojen merkitystä ei myöskään kannata kuitata kokonaan. Kun mukaan tulee CPU-offload, pitkät promptit, useampi GPU tai jatkuva mallien latailu, liian kapea väylä alkaa näkyä nopeasti käyttötuntumassa.

Jos haluat helpon nyrkkisäännön, käyttäisin tätä:

- älä panikoi x8:sta
- suhtaudu x4:ään varauksella
- priorisoi VRAM ensin, kaistat heti sen jälkeen

Se on minusta paljon hyödyllisempi tapa ajatella asiaa kuin vanha reflexi "GPU kuuluu aina x16-slottiin tai koko kone on pilalla".

## Lähteet

- https://raw.githubusercontent.com/tinyredinc/paperhub/master/mi50-llm-performance/mi50_llm_performance.md
- https://github.com/ggml-org/llama.cpp/issues/17026
- https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md
