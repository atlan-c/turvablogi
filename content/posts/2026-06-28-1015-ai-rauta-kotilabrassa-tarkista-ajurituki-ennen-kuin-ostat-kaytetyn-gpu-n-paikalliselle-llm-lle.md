---
title: "AI-rauta kotilabrassa: tarkista ajurituki ennen kuin ostat käytetyn GPU:n paikalliselle LLM:lle"
date: "2026-06-28T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-rauta kotilabrassa"
tags:
  - "AI-rauta"
  - "GPU"
  - "Ajurit"
  - "Ollama"
  - "Paikalliset LLM:t"
---
Käytetty näytönohjain näyttää paikallisen LLM-koneen ostoslistalla usein houkuttelevalta. VRAM-määrä voi olla iso, myynti-ilmoituksen hinta järkevä ja Reddit täynnä ihmisiä, jotka väittävät saman kortin "toimivan ihan hyvin". Oma käytännön sääntöni on silti tämä: **ennen kuin ostat käytetyn GPU:n paikalliselle LLM:lle, tarkista ensin ajurituki ja backend-polku, vasta sen jälkeen kellotaajuudet ja synteettiset benchmarkit.** Harrastajalle kallein virhe ei yleensä ole se, että kortti on 8 prosenttia hitaampi kuin vaihtoehto, vaan se, että se pakottaa epäviralliseen viritykseen tai väärään käyttöjärjestelmään.

Juuri vuonna 2026 tämä näkyy hyvin siinä, miten eri polut jakautuvat. NVIDIA-kortilla riittää usein käytännössä se, että kortti on tarpeeksi uusi ja ajuriversio täyttää ohjelmiston ehdot. AMD:n kanssa kuva voi olla hyvä, mutta polku kulkee useammin ROCm-tuen, käyttöjärjestelmärajojen ja joskus kiertoteiden kautta. Paperilla kaksi korttia voi näyttää samalta "24 GB VRAM" -tasolla, mutta todellinen käyttöönoton kitka voi olla täysin eri.

## Miksi ajurituki ratkaisee enemmän kuin moni arvaa

Paikallinen LLM ei käytä GPU:ta samalla tavalla kuin yksittäinen peli tai satunnainen Blender-renderöinti. Kun ajat mallia päivästä toiseen, oleellista on:

1. löytyykö kortille suoraan tuettu laskentapolku
2. tunnistaako valitsemasi ohjelmisto kortin ilman käsin pakotettuja ympäristömuuttujia
3. toimiiko sama yhdistelmä myös sillä käyttöjärjestelmällä, jota oikeasti haluat käyttää

Ollaman virallisessa laitetukisivussa tämä on kirjoitettu yllättävän suoraan. NVIDIA-puolella tuki sidotaan compute capabilityyn ja ajuriversioon. AMD-puolella taas Linuxilla vaaditaan ROCm v7 -ajuripino, ja listaus perustuu nimenomaan tuettuihin kortteihin eikä vain siihen, että näytönohjaimessa on paljon muistia.

Käytännön käännös on yksinkertainen: **kaikki iso-VRAM-kortit eivät ole yhtä helppoja paikallisen LLM:n kortteja**, vaikka ilmoituksessa lukisi muuten hyvät speksit.

## NVIDIA on usein helpompi käytettynä, mutta ei täysin automaattinen

Ollaman dokumentaation mukaan NVIDIA-tuki edellyttää compute capabilityä 5.0 tai uudempaa sekä ajuriversiota 550 tai uudempaa. Lisäksi vanhemmat compute capability 5.0-6.2 -kortit tarvitsevat vielä uudemman 570-sarjan ajurin. Tämä on hyvä muistutus siitä, että "CUDA-kortti" ei ole riittävän tarkka ostokriteeri.

NVIDIAn omalta CUDA-sivulta näkee nopeasti, mihin luokkaan kortti kuuluu. Esimerkiksi RTX 4090 on compute capability 8.9, RTX 3090 on 8.6 ja RTX 2080 on 7.5. Jos ostat käytettyä korttia, tarkista ilmoituksen mallinimi tästä taulukosta ennen rahojen siirtoa. Se vie minuutin ja säästää helposti monta iltaa myöhempää säätöä.

Tämä ei tarkoita, että kaikki tuetut NVIDIA-kortit olisivat automaattisesti hyviä LLM-kortteja. Se tarkoittaa vain sitä, että virallinen polku on usein selkeämpi: kortti löytyy listalta, ajuri on dokumentoitu ja softa osaa yleensä käyttää sitä ilman että joudut ensimmäiseksi etsimään kiertoteitä.

## AMD voi olla erinomainen valinta, jos luet pienet kirjaimet

AMD:n kohdalla moni harrastaja katsoo ensin vain sitä, löytyykö kortti "ROCm toimii" -keskusteluista. Virallinen dokumentaatio kertoo tarkemman totuuden. ROCm:n järjestelmävaatimuksissa sanotaan suoraan, että jos GPU ei ole tuettujen listalla, se ei ole virallisesti AMD:n tukema. Lisäksi sama sivu kertoo erikseen, että monet Radeon- ja Radeon PRO -kortit ovat tuettuja vain tietyillä jakeluilla, käytännössä Ubuntu 22.04.5/24.04.4 ja tietyillä RHEL-versioilla.

Tämä on käytetyn ostajan kannalta tärkeä kohta. Voi olla, että kortti toimii hienosti, jos hyväksyt juuri tietyn Ubuntu-version ja juuri tietyn ROCm-polun. Mutta jos oma oikea tavoite on ajaa paikallista LLM-konetta esimerkiksi Debianilla, Proxmox-pohjaisessa kotilabrassa tai muuten poikkeavalla pinolla, virallinen polku ei välttämättä enää kanna. Silloin "halpa 7900-sarjan löytö" ei olekaan vain rautapäätös vaan käyttöjärjestelmäpäätös.

Ollaman dokumentaatio näyttää toisen hyödyllisen yksityiskohdan: Linuxilla voi joskus pakottaa lähellä olevan AMD GFX-version ympäristömuuttujalla `HSA_OVERRIDE_GFX_VERSION`. Tämä on hyvä pelastuskeino testaukseen, mutta huono ostoperuste. Jos käytetty kortti vaatii heti ensimmäisestä päivästä lähtien overrideja, sitä ei kannata käsitellä samantasoisena "helppona harrastajakorttina" kuin virallisesti tuettua vaihtoehtoa.

## Käytännön ostosääntö: osta virallinen polku, älä pelkkää sirua

Kun selaan käytettyjä GPU-ilmoituksia paikallista LLM-konetta varten, etenisin näin:

1. Tarkista ensin ohjelmiston virallinen tukisivu, ei keskustelupalstaa.
2. Varmista, että juuri se korttimalli löytyy tuettujen listalta.
3. Tarkista, millä käyttöjärjestelmillä tuki on oikeasti luvattu.
4. Tarkista, vaatiiko polku ROCm:n, Vulkanin, CUDA:n tai jotain erikoisempaa.
5. Kysy vasta sen jälkeen, riittääkö VRAM omalle malliluokalle.

Tällä järjestyksellä vältät yleisen harrastajavirheen: ostat ensin "tehokkaan diilin" ja alat vasta sitten miettiä, miksi asennusohjeet haarautuvat kolmeen eri epäviralliseen wikiin.

## Milloin hyväksyisin epävirallisen reitin

Hyväksyisin epävirallisen reitin lähinnä silloin, jos kaikki nämä ehdot täyttyvät:

1. kortti on poikkeuksellisen halpa suhteessa VRAMiin
2. kone on selvästi harrasteprojekti eikä päivittäinen työjuhta
3. olet valmis sitomaan koneen tiettyyn distro- ja ajuriversioon
4. tiedät jo etukäteen, että tuen katkeaminen seuraavassa päivityksessä ei ole katastrofi

Muissa tilanteissa maksaisin mieluummin hieman enemmän siitä, että asennuspolku on virallinen. Paikallisessa LLM-koneessa aikaa palaa helposti enemmän kuin rahaa. Jos yksi "säästöostos" aiheuttaa viikonlopun verran ROCm-, Vulkan- tai ajurivian selvitystä, se ei ollut enää halpa.

## Oma nyrkkisääntö vuonna 2026

Jos haluat mahdollisimman vähän kitkaa, käytetty NVIDIA-kortti virallisesti tuetulla compute capabilityllä on edelleen helpoin ostos. Jos taas katsot AMD:tä VRAMin ja hinnan takia, tarkista tuen lisäksi heti käyttöjärjestelmärajaus, ettet vahingossa rakenna koko konetta yhden herkän ohjelmistopinon ympärille.

Sanoisin asian näin: **paikallisen LLM-koneen paras käytetty GPU ei ole se, jossa on paperilla eniten muistia euroon nähden, vaan se, jonka saat virallisesti tuetulla polulla oikeasti töihin.** Kun ajurituki on kunnossa, vasta sitten kannattaa verrata VRAMia, muistiväylää, tehorajaa ja jäähdytystä.

## Lähteet

- https://docs.ollama.com/gpu
- https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html
- https://developer.nvidia.com/cuda/gpus
