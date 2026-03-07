---
title: "Paikallinen malli arjessa: 6 kysymystä, jotka säästävät tunteja"
date: 2026-03-07T12:05:00+02:00
draft: false
---

Kun paikallinen malli tuntuu "melkein toimivalta", ongelma on yleensä workflowssa, ei yhdessä asetuksessa. Tässä nopea Q&A-runko, jolla saat arjen käyttöön vakautta.

## Q&A: toimiva local-model workflow

**1) Missä malli ajetaan: CPU, GPU vai hybridi?**  
Aja aina ensisijaisesti GPU:lla, jos tavoite on sujuva keskustelu tai koodiapu. CPU toimii testiin, mutta pitkissä sessioissa viive kasvaa nopeasti.

**2) Miten valitsen kvantisoinnin käytännössä?**  
Aloita keskitasosta (esim. 4–6 bit) ja mittaa laatu yhdellä omalla testipromptilla. Jos vastauslaatu hajoaa, nosta tarkkuutta; jos nopeus ei riitä, laske pykälä.

**3) Miten estän "toimii tänään, rikki huomenna" -tilanteen?**  
Lukitse versiot: runtime, malli ja tärkeimmät riippuvuudet. Tee pieni `README` omaan projektikansioon, jossa on käynnistyskomento ja tunnetut rajat.

**4) Tarvitaanko eri malli eri tehtäville?**  
Kyllä, usein kannattaa. Pidä yksi kevyt malli nopeaan luonnosteluun ja yksi laadukkaampi viimeistelyyn. Yhden mallin pakottaminen kaikkeen syö aikaa.

**5) Miten mittaan, paraniko workflow oikeasti?**  
Seuraa kahta mittaria viikon ajan: ensimmäisen tokenin viive ja tehtävän läpimenoaika (esim. "luonnos valmiiksi"). Tunne ei riitä, mittaa.

**6) Milloin paikallinen malli ei ole järkevä valinta?**  
Kun tarvitset jatkuvasti uusinta mallia, suurta kontekstia tai tiimijaon ilman omaa ylläpitoa. Silloin hybridi (paikallinen + API) on usein käytännöllisin.

## Käyttöönottorunko 30 minuutissa

1. Valitse yksi päätehtävä (esim. koodin refaktorointi).  
2. Valitse siihen yksi malli ja yksi varamalli.  
3. Tee kaksi vakio-promptia: "luonnos" ja "tarkistus".  
4. Mittaa viive + läpimenoaika viidellä toistolla.  
5. Tallenna toimiva profiili ja lopeta säätäminen viikoksi.

Pieni standardointi voittaa jatkuvan mikrotuunauksen.

## Lähteet

- Ollama Documentation: https://ollama.com/library
- llama.cpp Documentation (GGUF, quantization): https://github.com/ggerganov/llama.cpp/blob/master/docs
- Hugging Face Transformers documentation: https://huggingface.co/docs/transformers/index
