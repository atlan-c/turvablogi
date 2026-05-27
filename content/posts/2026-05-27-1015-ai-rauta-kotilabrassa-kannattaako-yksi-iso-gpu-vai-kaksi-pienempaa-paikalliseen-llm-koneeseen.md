---
title: "AI-rauta kotilabrassa: kannattaako yksi iso GPU vai kaksi pienempää paikalliseen LLM-koneeseen?"
date: 2026-05-27T10:15:00+03:00
draft: false
topic_family: "llm-hardware"
---

Paikallista LLM-konetta suunnitellessa kahden näytönohjaimen idea näyttää paperilla houkuttelevalta: samalla rahalla voi joskus saada enemmän yhteenlaskettua VRAMia kuin yhdellä isolla kortilla. **Useimmille harrastajille ja kotilabran rakentajille käytännöllisempi valinta on silti yksi mahdollisimman iso GPU, ei kaksi pienempää.** Kaksi korttia alkaa kannattaa vasta silloin, kun tiedät jo valmiiksi käyttäväsi ohjelmistoa, joka oikeasti osaa jakaa mallin usealle GPU:lle, ja hyväksyt lisääntyvän säädön, virrankulutuksen ja yhteensopivuusriskin.

Tärkein syy on yksinkertainen: kaksi GPU:ta ei automaattisesti käyttäydy kuin yksi isompi GPU. Se riippuu täysin siitä, miten käyttämäsi inference-ohjelma jakaa mallin, KV-cachen ja GPU:iden välisen liikenteen.

## Miksi kaksi pienempää korttia kuulostaa paremmalta kuin usein on

Ajatus menee yleensä näin:

- yksi 24 Gt kortti on kallis
- kaksi 12 Gt korttia voi näyttää halvemmalta
- yhteensä muistia olisi siis 24 Gt
- ehkä 20B- tai 30B-luokan malli mahtuisi näin halvemmalla

Tämä logiikka ei ole täysin väärä, mutta siitä puuttuu tärkeä käytännön ehto: **VRAM ei yhdisty taikaiskusta yhdeksi yhteiseksi altaaksi.** Ohjelmiston täytyy osata pilkkoa malli tarkoituksella useille korteille, ja samalla suorituskyky voi muuttua paljonkin huonommaksi kuin yksittäisellä isolla kortilla.

Jos tavoite on vain ajaa tavallisia 7B–14B-malleja sujuvasti omassa työpöytäkäytössä, kahden kortin rakenne on usein monimutkaisempi kuin tarve oikeasti vaatii.

## Ollama kertoo jo ensimmäisen käytännön rajan

Ollaman GPU-dokumentaatio näyttää heti yhden hyödyllisen realiteetin: jos koneessa on monta NVIDIA-GPU:ta, voit rajata näkyvät kortit esimerkiksi `CUDA_VISIBLE_DEVICES`-muuttujalla. Tämä on hyvä operointiominaisuus, mutta samalla se paljastaa jotain olennaista: **moni arkinen työnkulku käsittelee useita GPU:ita ennemmin valittavina laitteina kuin yhtenä ongelmattomasti yhdistyvänä resurssina.**

Eli jo peruspolussa kannattaa kysyä kaksi asiaa:

1. tukeeko käyttämäni työkalu oikeasti mallin jakamista usealle GPU:lle
2. vai valitsenko vain, mille yksittäiselle GPU:lle ajo menee

Jos tähän ei ole varmaa kyllä-vastausta, yhden ison kortin ostaminen on paljon turvallisempi raha- ja aikapäätös.

## `llama.cpp`:ssä multi-GPU toimii, mutta sillä on hintansa

`llama.cpp`:n oma multi-GPU-dokumentaatio on tässä kohtaa rehellisen hyödyllinen. Siinä monen GPU:n käyttöä suositellaan etenkin kahdessa tilanteessa:

- malli ei mahdu yhden GPU:n VRAMiin
- haluat lisää läpimenoa tai suorituskykyä

Mutta sama dokumentti kertoo heti myös sen, miksi tämä ei ole automaattinen voitto. Käytössä on eri split-modeja, joilla on erilainen käyttäytyminen:

- **layer** jakaa peräkkäisiä kerroksia eri GPU:ille ja on oletuspolku
- **tensor** voi parantaa token-latenssia, mutta on edelleen kokeellinen
- suorituskyky riippuu voimakkaasti GPU:iden välisen yhteyden nopeudesta

Käytännön johtopäätös on tärkeä: **kaksi korttia voi auttaa mallin mahtumisessa, mutta ei takaa miellyttävää nopeutta.** Jos GPU:iden välinen liikenne kulkee hitaasti, multi-GPU-rakenne voi jopa tuntua pettymykseltä verrattuna odotuksiin.

`llama.cpp` sanoo tämän myös suoraan vianrajausosiossa: jos multi-GPU on hitaampi kuin yksi GPU, pullonkaula voi olla juuri GPU-interconnectissa, ja ratkaisu voi olla joko eri split-mode tai nopeampi yhteys kuten enemmän PCIe-kaistaa tai NVLink, jos sellaista ylipäätään on tarjolla.

Kotilabran näkökulmasta tämä tarkoittaa, että kaksi kuluttajakorttia tavallisessa emolevyssä ei ole sama asia kuin hieno monen GPU:n työasema.

## vLLM vahvistaa saman perusopin eri kulmasta

vLLM:n rinnakkaisuusohje osuu hyvin samaan kohtaan, vaikka se palvelee enemmän serving- ja suuremman mittaluokan käyttötapauksia. Dokumentaatio sanoo käytännössä näin:

- jos malli mahtuu yhdelle GPU:lle, hajautettu inference on todennäköisesti turha
- jos malli ei mahdu yhdelle GPU:lle mutta mahtuu yhden koneen useille GPU:ille, tensor parallelism on järkevä vaihtoehto
- jos koneessa ei ole NVLinkiä, pipeline parallelism voi olla joissain tilanteissa parempi kuin tensor parallelism

Tämä on minusta erittäin hyvä nyrkkisääntö myös harrastajalle. **Useampi GPU on ratkaisu ennen kaikkea "malli ei muuten mahdu" -ongelmaan, ei yleinen oikotie helpompaan paikalliseen LLM-käyttöön.**

Lisäksi vLLM:n ohjeet muistuttavat epäsuorasti toisesta käytännön hinnasta: mitä pidemmälle mennään monen GPU:n suuntaan, sitä enemmän mukaan tulee rinnakkaisuusasetuksia, runtime-valintoja ja klusterimäistä ajattelua. Se on hyvä asia oikeassa palvelinympäristössä, mutta kotilabran yhden käyttäjän koneessa se ei aina ole sen vaivan arvoista.

## Milloin yksi iso GPU on lähes aina parempi

Valitsisin yhden ison GPU:n lähes automaattisesti, jos useampi näistä pitää paikkansa:

- haluat mahdollisimman vähän säätöä
- ajat yhtä mallia kerrallaan interaktiivisesti
- tavoite on hyvä vasteaika, ei maksimaalinen laboratorio-throughput
- kone toimii myös työpöytä- tai kehityskoneena
- budjetti ei riitä datacenter- tai workstation-luokan multi-GPU-rakenteeseen

Yksi iso kortti voittaa tällöin yleensä neljällä tavalla:

1. **Yksinkertaisempi ohjelmistopolku.** Vähemmän split-tiloja, vähemmän yllätyksiä.
2. **Tasaisempi latenssi.** Ei yhtä paljon korttien välistä liikennettä.
3. **Vähemmän yhteensopivuusmurheita.** Vähemmän ajureita, vähemmän BIOS- ja lane-kysymyksiä.
4. **Siistimpi virta- ja lämpöbudjetti.** Kaksi korttia lämmittää, meluaa ja kuormittaa virtalähdettä enemmän.

Moni ostaa vahingossa lisää monimutkaisuutta tilanteessa, jossa tarvittiin oikeasti vain enemmän VRAMia yhdessä kortissa.

## Milloin kaksi pienempää GPU:ta voi olla järkevä päätös

En tyrmäisi kahden GPU:n rakennetta kokonaan. Se voi olla fiksu ratkaisu, jos tiedät miksi olet tekemässä sitä.

Se alkaa kuulostaa järkevältä esimerkiksi silloin, kun:

- haluamasi malli ei mahdu yhdelle realistisen hintaiselle GPU:lle
- käytät nimenomaan `llama.cpp`:tä tai vLLM:ää, joissa monen GPU:n mallituki on oikeasti dokumentoitu
- hyväksyt sen, että suorituskyvyn viritys on osa harrastusta
- sinulla on emolevy, kotelo, jäähdytys ja virtalähde, jotka oikeasti kestävät kaksi korttia
- tavoite on enemmän kapasiteetti kuin mahdollisimman helppo käyttökokemus

Tässä maailmassa kaksi 12 Gt tai 16 Gt korttia voi olla tapa päästä suurempaan malliluokkaan ilman yhden todella kalliin kortin hintaa. Mutta silloin kannattaa ajatella koko pakettia, ei pelkkää VRAM-lukua.

## Mitä aloittelija usein aliarvioi

Kahden GPU:n suunnitelmassa aliarvioidaan usein ainakin nämä:

- **PCIe-linjat:** toinen kortti voi pudota hitaampaan slotiin
- **fyysinen tila:** paksut kortit peittävät slotteja ja ilmanvaihdon
- **virtalähde:** piikit voivat kasvaa ikävästi
- **lämpö:** toinen kortti syö helposti ensimmäisen hengitysilmaa
- **ohjelmistotuki:** kaikki työkalut eivät skaalaudu samalla tavalla
- **debuggaus:** kun jokin ei toimi, vikaa voi olla raudassa, ajureissa, backendissa tai asetuksissa

Siksi kaksi korttia ei ole vain "sama mutta enemmän". Se on eri tasoinen projekti.

## Oma käytännön suositukseni

Jos rakentaisin paikallista LLM-konetta yhdelle harrastajalle tai kehittäjälle, käyttäisin tätä sääntöä:

- **jos malli mahtuu yhdelle GPU:lle, osta yksi GPU**
- **jos malli ei mahdu yhdelle GPU:lle ja multi-GPU-tuki on todistetusti osa valittua ohjelmistopinoa, harkitse kahta GPU:ta**
- **jos et vielä tiedä mitä backendia oikeasti käytät päivittäin, älä rakenna konetta monen GPU:n varaan**

Toisin sanottuna yksi iso GPU ostaa yleensä ennustettavuutta. Kaksi pienempää GPU:ta ostaa kapasiteettia, mutta samalla myös kitkaa.

## Yhteenveto

Kannattaako paikalliseen LLM-koneeseen yksi iso GPU vai kaksi pienempää? **Useimmissa kotilabroissa yksi iso GPU on parempi valinta.** Se on helpompi saada toimimaan, helpompi pitää vakaana ja usein myös aidosti mukavampi käyttää.

Kaksi pienempää GPU:ta alkaa olla järkevä vasta silloin, kun ongelma on selvästi mallin mahtuminen eikä yleinen peruskäyttö, ja kun olet valmis hyväksymään multi-GPU-maailman kompromissit. Tässä aiheessa halvin tie VRAM-per-euro ei ole automaattisesti halvin tie käytännössä.

## Lähteet

- https://docs.ollama.com/gpu
- https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md
- https://github.com/vllm-project/vllm/blob/main/docs/serving/parallelism_scaling.md
