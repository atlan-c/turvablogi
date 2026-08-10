---
title: "Mitä PagedAttention oikeasti korjaa paikallisessa LLM-palvelimessa?"
date: "2026-08-10T10:15:00+03:00"
draft: false
phase: "new-era"
topic_family: "ai-models"
series:
  - "Tekoäly ja agentit"
tags:
  - "local-llm"
  - "pagedattention"
  - "kv-cache"
  - "vllm"
---
## Tiivistelmä
PagedAttention kuulostaa helposti samalta kuin yleinen "malli nopeammaksi" -nappi, mutta käytännössä se ratkaisee kapeamman ja tärkeän ongelman: **KV-välimuistin hallinnan silloin, kun samalla palvelimella elää monta eripituista pyyntöä tai agenttikierrosta yhtä aikaa**. Harrastajalle tärkein sääntö on tämä: **PagedAttention auttaa eniten palvelinkäytössä, jossa muistia pitää jakaa joustavasti, eikä niinkään yhdessä yksinäisessä chat-ikkunassa, jossa odotat ihmettä ensimmäiseen tokeniin**.

## Mistä ongelmasta tässä oikeasti puhutaan

Paikallisen LLM-palvelimen suorituskyky ei kaadu vain mallin kokoon. Toinen nopeasti kasvava kuluerä on KV-cache eli muisti, johon aiempien tokenien attention-tila tallennetaan. Kun pyyntöjä tulee sisään eri pituisina ja eri aikaan, tätä muistia pitää varata, kasvattaa ja vapauttaa jatkuvasti.

Hugging Facen TGI-katsaus sanoo asian käytännön kielellä: decode-vaihe on muistirajoitteinen, ja käytettävissä oleva VRAM määrää suoraan paljonko tokeneita voidaan käsitellä rinnakkain. Tämä on juuri se ympäristö, jossa huono KV-muistin hallinta näkyy nopeasti joko tehottomuutena tai tarpeettoman varovaisina rajoina.

## Mitä PagedAttention tekee

vLLM:n dokumentaatio kuvaa PagedAttentionin ytimen näin: key- ja value-cache pilkotaan kiinteän kokoisiin lohkoihin, joita voidaan pitää muistissa epäjatkuvina paloina yhden ison yhtenäisen varauksen sijaan. TGI:n selitys täydentää käytännön vaikutuksen: pyyntö käyttää tarvitsemansa määrän sivuja, ja sivut voidaan vapauttaa pyynnön päätyttyä uusille pyynnöille.

Tärkeä seuraus on tämä:

- koko KV-cachea ei tarvitse käsitellä yhtenä isona yhtenäisenä muistialueena
- eri pituiset pyynnöt eivät sotke muistia yhtä helposti
- uusia pyyntöjä voidaan palvella ilman että välimuistia rakennetaan jatkuvasti uudelleen alusta

Tämä ei poista mallin peruskustannuksia. Se tekee ennen kaikkea **muistin jakamisesta siistimpää ja joustavampaa**.

## Missä se näkyy kotipalvelimessa oikeasti

Parhaiten hyöty näkyy tällaisissa tilanteissa:

- samalla palvelimella on useita käyttäjiä, agentteja tai taustatehtäviä
- pyyntöjen pituus vaihtelee paljon
- käytössä on jatkuva batching tai muu samanaikaisuutta kasvattava palvelin
- haluat puristaa VRAMista enemmän hyödyllistä työtä ilman jatkuvaa OOM-pelkoa

Jos taas ajat mallia pääasiassa yksin yhdestä chat-ikkunasta, PagedAttention ei välttämättä tunnu arkikielessä "paljon nopeampana". Se voi silti auttaa palvelimen vakaudessa ja kapasiteetissa, mutta dramaattinen tunne-ero syntyy yleensä vasta kun kuormaa on enemmän kuin yksi suoraviivainen keskustelu.

## Yleisin väärinkäsitys: PagedAttention ei ole sama asia kuin FlashAttention

Näitä kahta sekoitetaan jatkuvasti. Ne eivät ratkaise samaa ongelmaa.

TGI:n katsaus tekee eron hyvin näkyväksi. Sen mukaan PagedAttention liittyy KV-cachen muistinhallintaan ja sivujen uudelleenkäyttöön. FlashAttention taas vähentää turhaa muistiliikennettä attention-laskennassa ja auttaa erityisesti padittomien tensorien ja pidempien sekvenssien tehokkuudessa.

Käytännön sääntö on siis tämä:

- jos ongelma on "palvelin kestää huonosti monta elävää pyyntöä", katso PagedAttention-tyyppistä muistinhallintaa
- jos ongelma on "attention-laskenta itsessään on raskas", katso FlashAttentionia ja siihen liittyviä taustakytkimiä

Molemmat voivat olla päällä samassa pinossa, mutta ne eivät ole keskenään vaihtoehtoja.

## Miksi tämä liittyy suoraan agenttityöhön

Agenttikuorma on hankalampi kuin tavallinen yksi kysymys ja yksi vastaus. Sama palvelin voi pitää auki:

- pitkää järjestelmäpromptia
- työkalumäärittelyjä
- useita rinnakkaisia alitehtäviä
- vaihtelevan pituisia välivastauksia

Juuri tällöin KV-cache alkaa elää epätasaisesti. Osa pyynnöistä on lyhyitä, osa roikkuu pitkään, ja osa jatkaa samaa keskustelua uudella kierroksella. PagedAttentionin hyöty on siinä, että tämä sotku ei pakota palvelinta kohtelemaan jokaista pyyntöä kuin yhtä suurta yhtenäistä muistimöykkyä.

Siksi pitäisin PagedAttentionia enemmän **palvelininfrastruktuurin ominaisuutena** kuin yksittäisen promptin optimointina.

## SGLangin käytännön opetus: sivukoko on kompromissi

SGLangin dokumentaatio tuo mukaan yksityiskohdan, joka on hyödyllinen myös harrastajalle. `page_size` määrää, kuinka monta tokenia niputetaan yhteen KV-cache-lohkoon. Dokumentaatio sanoo suoraan, että prefix cache toimii vain, jos yhteinen alku täyttää vähintään yhden kokonaisen sivun. Jos sivukoko on 64 ja yhteinen alku on vain 32 tokenia, siitä ei tule osumaa.

Tästä seuraa käytännön kompromissi:

- pieni sivukoko parantaa prefix-osumia ja joustavuutta
- suurempi sivukoko voi parantaa attention-kernelin suorituskykyä

Toisin sanottuna kaikki "paged" toteutukset eivät käyttäydy samalla tavalla. Jos omassa pinossa korostuu toistuva vakaa promptin alku, pienempi sivukoko voi olla hyödyllisempi. Jos taas tärkeintä on raakapalveluteho tietyllä backendillä, suurempi natiivi sivukoko voi olla oikea valinta.

## Milloin PagedAttention ei ole ensimmäinen asia jota säätäisin

En aloittaisi tästä, jos ongelma on jokin näistä:

- väärä chat-template
- liian suuri malli suhteessa VRAMiin
- liian pitkä konteksti yhdelle kortille
- huono batching-strategia
- yksittäisen käyttäjän korkea first-token-viive ilman muuta kuormaa

Näissä tapauksissa PagedAttention voi kyllä olla mukana ratkaisussa, mutta se ei ole ensimmäinen vipu. Se on enemmän kapasiteetin ja muistijärjestelyn optimointi kuin yleinen "tee kaikesta nopeaa" -korjaus.

## Käytännön sääntö kotilabraan

Jos arvioisin tänään omaa paikallista LLM-palvelintani, etenisin näin:

1. katso ensin palveleeko instanssi oikeasti useita pyyntöjä rinnakkain vai vain yhtä käyttäjää
2. mittaa erikseen time-to-first-token, tokenit sekunnissa ja kuinka monta yhtäaikaista pyyntöä palvelin kestää ennen jonotusta tai OOM-tilannetta
3. jos ongelma näkyy vasta rinnakkaiskuormassa, painota KV-cachen hallintaa, batchingia ja palvelinmoottoria
4. jos käytät SGLangia tai muuta sivupohjaista toteutusta, tarkista myös page size eikä vain "onko ominaisuus päällä"

Hyvä nyrkkisääntö on tämä: **PagedAttention kannattaa ymmärtää keinona nostaa palvelimen hyötysuhdetta, ei lupauksena siitä että yksi ainoa keskustelu tuntuisi välittömästi täysin erilaiselta**.

## Johtopäätös

PagedAttention korjaa paikallisessa LLM-palvelimessa ennen kaikkea muistin pirstaloitumisen ja jäykän KV-cache-hallinnan ongelmia. Siksi se on erityisen hyödyllinen silloin, kun palvelimella elää monta erimittaista pyyntöä yhtä aikaa, kuten agentti- ja monikäyttäjäkuormassa. Jos taas käyttösi on yksi ihminen, yksi chat ja vähän rinnakkaisuutta, hyödyn suurin osa voi jäädä näkymättömäksi arjen tunteessa. Harrastajalle oikea kysymys ei siis ole "onko PagedAttention moderni", vaan **onko oma kuorma sellainen, että joustavampi KV-muistin hallinta oikeasti ratkaisee pullonkaulan**.

## Lähteet

- vLLM docs: https://docs.vllm.ai/en/latest/design/paged_attention/
- vLLM docs overview: https://docs.vllm.ai/en/latest/
- SGLang attention backend docs: https://docs.sglang.io/docs/advanced_features/attention_backend
- Hugging Face TGI overview: https://huggingface.co/blog/martinigoyanes/llm-inference-at-scale-with-tgi
