---
title: "AI-rauta kotilabrassa: pitääkö Resizable BAR ottaa käyttöön paikalliselle LLM-koneelle?"
date: "2026-06-22T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-rauta kotilabrassa"
tags:
  - "AI-rauta"
  - "GPU"
  - "PCIe"
  - "Paikalliset LLM:t"
---
Moni paikallista LLM-konetta kasaava huomaa BIOSissa asetuksen nimeltä **Resizable BAR**, **Re-Size BAR** tai AMD-maailmassa **Smart Access Memory**. Se jää helposti tekemättä, koska asetus kuulostaa pelityökalulta eikä LLM-koneen peruspalikalta. Oma käytännön johtopäätökseni on yksinkertainen: **jos emolevy ja näytönohjain tukevat sitä, ominaisuus kannattaa yleensä laittaa päälle**. Se ei tee hitaasta koneesta nopeaa eikä lisää VRAM-määrää, mutta se voi poistaa turhan pullonkaulan CPU:n ja GPU:n välistä.

Paikallisessa LLM-ajossa tämä on hyödyllistä erityisesti silloin, kun malli tai sen osia siirtyy aktiivisesti PCIe-väylän yli. Tällaisia tilanteita ovat esimerkiksi mallin lataus, osittainen GPU-offload, rajallisen VRAMin kokoonpanot ja jotkin integroidut tai jaettua muistia hyödyntävät viritykset. Tässä kohtaa teen tietoisen tulkinnan lähteistä: valmistajien dokumentaatio puhuu ominaisuuden antavan prosessorille laajemman pääsyn GPU-muistiin ja Intel sanoo suoraan, että Arc-korteilla se on optimaalisen suorituskyvyn edellytys. Siitä ei seuraa automaattisesti "enemmän tokeneita sekunnissa joka mallilla", mutta siitä seuraa hyvin usein se, että et jätä yhtä helppoa yhteensopivuus- ja siirtotie-etua käyttämättä.

## Mitä Resizable BAR oikeasti tekee

Intel kuvaa Resizable BARin PCIe-ominaisuudeksi, jossa laitteen BAR-koon neuvottelu optimoidaan järjestelmäresurssien käyttöä varten. NVIDIA taas tiivistää asian käytännöllisemmin: CPU pääsee käsiksi koko GPU:n framebufferiin kerralla eikä vain pieniin ikkunoihin. AMD käyttää samasta ideasta nimeä Smart Access Memory ja korostaa nopeampia siirtoja prosessorin ja grafiikkamuistin välillä.

LLM-harrastajan näkökulmasta tärkeä havainto ei ole markkinointisana vaan tämä: **kun malli ei elä täysin yhden VRAM-poolin sisällä ilman siirtoja, muistialueen käsittelyn tehokkuudella voi olla väliä**. Jos käytät yhtä isoa GPU:ta ja koko malli mahtuu siihen siististi, erot voivat jäädä pieniksi. Jos taas elät kompromissikoneessa, jossa osa työstä nojaa PCIe-siirtoihin, jokainen kitkanpoisto on hyödyllinen.

## Missä tilanteessa hyöty näkyy eniten

En odottaisi suurinta hyötyä "valmis 24 GB VRAM + pieni 7B-malli" -tapauksessa. Sen sijaan kiinnittäisin huomiota näihin kokoonpanoihin:

- **Intel Arc**: Intelin oma ohje on poikkeuksellisen suora. ReBAR tai SAM pitää olla päällä optimaalista suorituskykyä varten kaikissa Arc A- ja B-sarjan sovelluksissa.
- **Osittainen GPU-offload**: jos osa kerroksista tai KV-cachea valuu järjestelmämuistin suuntaan, PCIe-polku ei ole vain käynnistysvaiheen yksityiskohta.
- **Pienemmän budjetin koneet**: kun yrität puristaa 16 GB tai 12 GB kortista enemmän irti, jokainen siirtotien parannus on käytännössä arvokkaampi kuin valmiiksi ylisuurella GPU:lla.
- **Viritykset ja suorituskyvyn metsästys**: llama.cpp-yhteisön RDNA4-kokeissa ReBAR nostetaan ihan ensimmäiseksi BIOS-tarkistukseksi ennen muuta hienosäätöä. Se ei ole tieteellinen takuu, mutta kertoo hyvin, että kokeneet harrastajat pitävät sitä perustason optimointina.

## Milloin se ei ratkaise ongelmaa

Tässä kohtaa moni pettyy väärään asiaan. Resizable BAR:

- ei kasvata VRAMia
- ei korjaa liian hidasta järjestelmämuistia
- ei tee SATA-SSD:stä NVMe-levyä
- ei pelasta konetta, jossa malli on yksinkertaisesti liian iso jatkuvaan CPU-vuotoon

Jos paikallinen LLM tuntuu hitaalta, kysyn edelleen ensin nämä kysymykset:

1. Mahtuuko malli oikeasti GPU:lle vai valuuko se RAMiin?
2. Kuinka monta kerrosta on oikeasti GPU-offloadissa?
3. Onko pullonkaula VRAM, RAM, PCIe-kaistat, levy vai virransäästötila?

Resizable BAR on hyvä optimointi, mutta se on silti optimointi. Sitä ei pidä sekoittaa kapasiteettiongelmaan.

## Käytännön tarkistuslista

Jos kasaat tai päivität paikallista LLM-konetta, tekisin tämän järjestyksessä:

1. Päivitä emolevyn BIOS uusimpaan vakaaseen versioon.
2. Varmista, että kone käynnistyy UEFI-tilassa eikä vanhassa CSM/Legacy-tilassa.
3. Ota BIOSista käyttöön `Above 4G Decoding`.
4. Ota käyttöön `Resizable BAR` tai AMD-ympäristössä `Smart Access Memory`.
5. Tarkista käyttöjärjestelmästä tai valmistajan työkalusta, että ominaisuus on oikeasti aktiivinen.

Intel huomauttaa myös, että asetus voi näkyä eri emolevyillä eri nimillä. Siksi "en löytänyt ReBARia" ei aina tarkoita, ettei tukea olisi, vaan joskus nimi on juuri SAM tai jokin valmistajan oma muunnelma.

## Oma nyrkkisääntö

Jos käytät NVIDIA- tai AMD-korttia paikalliseen LLM-ajoon, pidän Resizable BARia matalan riskin perusasetuksena: **laita päälle, testaa vakaus, unohda sen jälkeen**. Jos käytät Intel Arcia, suhtautuisin siihen vielä painavammin, koska Intelin oma dokumentaatio sanoo sen olevan optimaalisen suorituskyvyn ehto eikä vain "kiva lisä". Käytännössä tämä tarkoittaa, että ReBAR kuuluu samaan aloitustarkistuslistaan kuin oikea PCIe-slot, muistikanavat, virtalähde ja järkevä jäähdytys.

Paikallisessa LLM-koneessa suurin virhe ei yleensä ole se, että yksi säätö jäi viimeistelemättä. Suurempi virhe on se, että BIOSin ilmaiset perusasetukset jätetään tekemättä ja sitten yritetään ratkaista kaikki ostamalla lisää rautaa. Resizable BAR ei korvaa isompaa GPU:ta, mutta se on juuri sellainen ilmainen asetus, joka kannattaa hoitaa kuntoon ennen seuraavaa hankintaa.

## Lähteet

- https://www.intel.com/content/www/us/en/support/articles/000090831/graphics.html
- https://www.intel.com/content/www/us/en/support/articles/000091128/graphics/intel-arc-dedicated-graphics-family.html
- https://www.intel.com/content/www/us/en/support/articles/000092416/graphics.html
- https://www.amd.com/en/gaming/technologies/smart-technologies.html
- https://www.amd.com/en/resources/support-articles/faqs/DH3-020.html
- https://www.nvidia.com/en-us/geforce/news/geforce-rtx-30-series-resizable-bar-support/
- https://github.com/ggml-org/llama.cpp/discussions/21043
