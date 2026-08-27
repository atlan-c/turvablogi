---
title: "KV-cache-kvantisointi säästää VRAMia vain jos konteksti on oikeasti pitkä"
date: "2026-08-27T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "kv-cache"
  - "quantization"
  - "vram"
---
## Tiivistelmä
KV-cache-kvantisointi kuulostaa helposti ilmaiselta keinolta saada paikallisesta LLM:stä enemmän irti, mutta käytännössä siitä on eniten hyötyä vasta silloin, kun **konteksti on pitkä, rinnakkaisia pyyntöjä on useita tai VRAM loppuu juuri KV-muistiin eikä mallipainoihin**. Harrastajalle tärkein sääntö on tämä: **jos ongelma tulee jo mallin latauksessa, KV-cache-kvantisointi ei pelasta sinua, mutta jos ongelma alkaa vasta pitkissä keskusteluissa tai agenttikierroksissa, se voi lykätä uuden GPU:n ostoa yllättävän paljon**.

## Mikä tässä syö muistia oikeasti

Paikallista LLM:ää säätäessä puhutaan usein vain painokvantisoinnista, vaikka pitkässä käytössä toinen iso kuluerä on KV-cache. Se tallentaa aiempien tokenien attention-tilan, jotta samaa laskentaa ei tarvitse tehdä joka tokenille uudelleen. Hyöty on selvä, mutta välimuisti kasvaa koko ajan keskustelun tai agenttiajon mukana.

Hugging Face arvioi asian konkreettisesti: Llama-2 7B -luokan mallilla 10 000 tokenin KV-cache voi viedä noin 5 gigatavua muistia fp16-tarkkuudella. Tämä on juuri se syy, miksi moni harrastaja huomaa koneensa toimivan hyvin lyhyissä testeissä mutta tökkivän, kun samaan koneeseen tulee pitkä chatti, RAG-kontekstia tai useita agenttikierroksia peräkkäin.

## Milloin kvantisointi auttaa eniten

KV-cache-kvantisoinnin idea on yksinkertainen: välimuisti tallennetaan matalammalla tarkkuudella kuin tavallinen fp16, jotta samaan VRAM-määrään mahtuu enemmän tokeneita tai enemmän rinnakkaisia pyyntöjä.

Käytännössä suurin hyöty näkyy näissä tilanteissa:

- ajat pitkiä keskusteluja tai isoja järjestelmäprompteja
- samalla palvelimella on useita käyttäjiä tai agentteja
- käytät korkeaa kontekstipituutta "varmuuden vuoksi"
- malli mahtuu jo koneeseen, mutta decode-vaiheen aikana VRAM täyttyy myöhemmin

Jos taas kone kaatuu jo mallia ladattaessa, ensimmäinen korjaus on lähes aina pienempi malli, painokvantisointi tai lisää muistia. KV-cache-kvantisointi vaikuttaa ennen kaikkea käyttötilanteeseen, jossa malli on jo käynnissä mutta keskustelun pituus kasvattaa muistijalanjälkeä.

## Missä kohtaa harrastaja usein tulkitsee tilanteen väärin

Yleinen virhe on katsoa vain mallin nimellistä kokoa. Todellinen pullonkaula voi tulla vasta käytössä. 14B-malli voi tuntua täysin vakaalta lyhyellä promptilla, mutta sama instanssi voi hajota tai alkaa jonottaa pahasti, kun mukaan tulee:

- pitkä työkalukuvaus
- RAG-hausta tullut lisäkonteksti
- useita aiempia viestejä
- toinen rinnakkainen käyttäjä tai taustaprosessi

Silloin ongelma ei välttämättä ole "väärä malli", vaan se että KV-cache kasvaa käyttöprofiilin mukana. Tähän kvantisointi osuu paljon paremmin kuin sokea näytönohjaimen päivittäminen.

## Entä suorituskyky, hidastuuko kaikki

Hidastumisen mahdollisuus on todellinen, eikä tätä kannata myydä ilmaisena lounaana. Hugging Facen käytännön mittauksissa int4-KV-cache säilytti laadun varsin hyvin, mutta suuremmilla batch-koilla nopeus voi laskea, koska kvantisointi ja dekvantisointi lisäävät omaa työtään joka generaatiokierroksella.

Sama perussääntö näkyy myös vLLM:n dokumentaatiossa toisesta kulmasta. vLLM:n FP8-KV-cache on tarkoitettu juuri muistijalanjäljen pienentämiseen, jotta muistiin mahtuu enemmän tokeneita ja palvelin pystyy suurempaan läpimenoon tai pidempään kontekstiin. Se ei siis ole ensisijaisesti "ensimmäinen tokeni nopeammaksi" -asetus, vaan tapa käyttää olemassa oleva VRAM hyödyllisemmin.

## Käytännön päätössääntö ennen uuden GPU:n ostoa

Tekisin kotilabrassa päätöksen näin:

1. mittaa ensin, kaatuuko tai hidastuuko ajo mallin latauksessa vai vasta pitkän keskustelun aikana
2. jos ongelma tulee vasta kontekstin kasvaessa, testaa ensin KV-cache-kvantisointia
3. jos käytät agentteja, mittaa erikseen yksi pitkä sessio ja usea rinnakkainen lyhyempi sessio
4. jos nopeus romahtaa kvantisoinnin kanssa, palaa tavalliseen cacheen ja lyhennä kontekstia ennen rautapäätöstä

Tämä on tärkeä kohta: **KV-cache-kvantisointi kannattaa yleensä testata ennen GPU-päivitystä silloin, kun olet jo lähellä toimivaa kokoonpanoa**. Jos nykyinen kone ajaa mallia muuten hyvin, mutta pitkä käyttö syö viimeiset gigat, ohjelmistopuolen muutos voi olla paljon halvempi ratkaisu kuin uusi kortti.

## Milloin en vaivautuisi tällä ensimmäisenä

En aloittaisi KV-cache-kvantisoinnista, jos:

- käytät lähinnä lyhyitä yhden käyttäjän chatteja
- kontekstipituus on pieni
- pullonkaula on ensimmäisen tokenin viive eikä muistikatto
- malli ei mahdu kunnolla koneeseen edes ilman pitkää historiaa

Näissä tilanteissa suurempi hyöty tulee usein muualta: oikeasta chat-templatesta, pienemmästä mallista, aggressiivisemmasta painokvantisoinnista tai siitä, ettei kontekstikattoa aseteta turhaan valtavan suureksi.

## Johtopäätös

KV-cache-kvantisointi on hyödyllinen nimenomaan silloin, kun paikallisen LLM:n ongelma alkaa **käytön aikana** eikä heti käynnistyksessä. Se ei korvaa väärän kokoisen mallin valintaa eikä tee hitaasta koneesta taianomaisesti nopeaa, mutta se voi vapauttaa juuri sen verran VRAMia, että pitkä keskustelu, RAG ja agenttikuorma pysyvät hallinnassa samalla raudalla. Siksi pitäisin sitä yhtenä parhaista "kokeile ennen kuin ostat" -vipusimista harrastajan AI-koneessa.

## Lähteet

- Hugging Face blog: https://huggingface.co/blog/kv-cache-quantization
- Hugging Face Transformers docs: https://huggingface.co/docs/transformers/kv_cache
- vLLM docs: https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/
- KIVI paper: https://arxiv.org/abs/2402.02750
