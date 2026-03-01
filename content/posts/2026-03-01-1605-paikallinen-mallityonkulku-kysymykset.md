---
title: "Paikallinen mallityönkulku: 6 kysymystä, joilla pääset heti käyttöön"
date: 2026-03-01T16:05:00+02:00
draft: false
---

Usein ongelma ei ole malli, vaan työnkulku. Alla kuusi käytännön kysymystä ja suorat vastaukset, joilla paikallinen ajo pysyy nopeana ja hallittuna.

## Kysymys 1: Missä malli kannattaa ajaa?

**Vastaus:** Aja malli palveluna (esim. Ollama tai llama.cpp server), älä jokaisen sovelluksen sisällä erikseen. Saat yhden hallintapisteen malliversioille, lokille ja resurssirajoille.

## Kysymys 2: Miten valitsen mallikoon arkeen?

**Vastaus:** Valitse pienin malli, joka läpäisee oman testisi. Tee 10 tyypillisen promptin lista ja vertaa laatua + token-nopeutta. Jos ero isompaan malliin on pieni, pidä pienempi tuotannossa.

## Kysymys 3: Kannattaako käyttää kvantisointia?

**Vastaus:** Kyllä, lähes aina kotikäytössä. Kvantisointi pienentää muistitarvetta ja parantaa käytännön nopeutta. Testaa vähintään kahta tasoa (esim. Q4 ja Q5) samalla tehtäväsetillä ennen päätöstä.

## Kysymys 4: Miten pidän kontekstin hallinnassa?

**Vastaus:** Rajoita syöte tarkoituksella. Käytä tiivistelmäkerrosta pitkille keskusteluille ja syötä mallille vain tehtävän kannalta oleellinen osa. Tämä vähentää viivettä ja hallusinaatioita.

## Kysymys 5: Miten teen työnkulusta toistettavan?

**Vastaus:** Lukitse kolme asiaa: malliversio, prompt-pohja ja arviointitestit. Ilman näitä et tiedä, paraniko vai heikkenikö lopputulos päivityksen jälkeen.

## Kysymys 6: Mikä on nopein tapa integroida omaan appiin?

**Vastaus:** Käytä OpenAI-yhteensopivaa rajapintaa, jos palvelin tarjoaa sen. Silloin voit vaihtaa paikallisen ja pilvimallin välillä pienillä koodimuutoksilla.

## Käytännön minimi (aloita tästä)

1. Yksi paikallinen palvelinprosessi
2. Yksi oletusmalli + yksi varamalli
3. Yksi vakioitu prompt-pohja per käyttötapaus
4. Yksi pieni regressiotestilista

Tämä riittää yllättävän pitkälle ennen kuin tarvitset monimutkaisempaa orkestrointia.

## Lähteet

- Ollama docs (mallien ajo ja API): https://docs.ollama.com/
- llama.cpp server docs / README: https://github.com/ggml-org/llama.cpp
- OpenAI API compatibility (Open WebUI): https://docs.openwebui.com/openapi-servers/openai-api-compatibility/
