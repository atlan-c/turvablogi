---
title: "AI-rauta kotilabrassa: nopeuttaako NVMe paikallista LLM:ää vai vain mallin käynnistystä?"
date: "2026-06-10T10:15:00+03:00"
draft: false
topic_family: "llm-hardware"
series:
  - "AI-kotilabra"
tags:
  - "NVMe"
  - "SSD"
  - "Local LLM"
  - "Ollama"
  - "Hardware"
---
Nopea NVMe-levy on helppo ostos paikalliseen LLM-koneeseen, koska se tuntuu turvalliselta päivitykseltä. Speksitaulukossa luvut näyttävät hyviltä, eikä kukaan kadu ylimääräistä levytilaa. Silti käytännön kysymys on toinen: **nopeuttaako NVMe itse vastauksen tuottamista, vai vain sitä hetkeä kun malli ladataan ensimmäisen kerran muistiin?** Useimmissa kotilabroissa rehellinen vastaus on tämä: **NVMe auttaa eniten kylmäkäynnistyksissä, mallien vaihdossa ja aineistojen siirtelyssä, mutta ei yleensä ole ensimmäinen token/s-pullonkaula**.

Tämä ero kannattaa ymmärtää ennen kuin käyttää budjettia väärään paikkaan. Jos malli pysyy kokonaan GPU:ssa tai ainakin vakaasti RAMissa ilman jatkuvaa sivutusta, varsinainen generointi on useimmiten enemmän kiinni laskennasta ja muistihierarkiasta kuin siitä, kuinka nopea SSD koneessa on.

## Missä kohtaa levy oikeasti osallistuu peliin?

Ollaman FAQ kertoo kaksi käytännössä tärkeää asiaa. Ensinnäkin malli pyritään lataamaan yhdelle GPU:lle, jos se mahtuu sinne kokonaan, koska tämä vähentää PCIe-siirtoja inferenssin aikana. Toiseksi Ollama voi pitää malleja muistissa `keep_alive`-asetuksella, jolloin samaa mallia ei tarvitse ladata levyltä joka pyynnöllä uudelleen.

Tästä seuraa aika käyttökelpoinen nyrkkisääntö:

1. **Ensimmäinen lataus** hyötyy nopeasta levystä.
2. **Toistuva käyttö samasta muistissa pysyvästä mallista** hyötyy paljon vähemmän.
3. **Tokenien generointi** ei muutu maagisesti nopeaksi vain siksi, että SSD vaihtui SATA:sta NVMe:hen.

Jos siis ajat yhtä tai kahta mallia pitkissä sessioissa, nopeampi SSD tuntuu eniten alussa. Jos taas tapat ja vaihdat malleja koko ajan, levy alkaa näkyä arjessa selvästi enemmän.

## Miksi NVMe ei yleensä ratkaise token/s-nopeutta?

NVMe-standardijärjestön yleiskatsaus muistuttaa, että jo PCIe Gen3 x4 -tasoinen NVMe pystyy useiden gigatavujen sekuntinopeuksiin. Se on paljon levyksi, mutta silti eri mittaluokan asia kuin GPU:n oma muistiliikenne. Paikallisessa LLM-ajossa raskas osa ei tavallisesti ole "lue mallitiedosto kerran", vaan jatkuva laskenta ja muistiviittaukset generoinnin aikana.

Siksi moni harrastaja kokee saman ilmiön:

- uusi NVMe tekee mallin avaamisesta napakamman
- komentorivi tuntuu reagoivan nopeammin käynnistyksessä
- mutta varsinainen vastausnopeus muuttuu yllättävän vähän

Tämä ei tarkoita, että nopea levy olisi turha. Se tarkoittaa vain, että **SSD ja inferenssinopeus vaikuttavat usein eri kohtiin käyttökokemusta**.

## `mmap` tekee erosta käytännössä vielä tärkeämmän

`llama.cpp`:n CLI-dokumentaatio sanoo suoraan, että mallit muistikartoitetaan oletuksena (`mmap`). Tällöin järjestelmä voi ladata mallista tarvittavia osia tarpeen mukaan sen sijaan, että koko tiedosto nieltäisiin kerralla tavalliseen latauspolkuun. Sama dokumentaatio huomauttaa myös, että `--no-mmap` tekee latauksesta hitaamman, mutta voi vähentää pageout-ongelmia, jos käytössä ei ole `mlock`-lukitusta.

Käytännössä tästä saa kolme hyödyllistä johtopäätöstä:

- nopea levy auttaa erityisesti silloin, kun käyttö perustuu muistinkartoitukseen ja kylmiä latauksia tulee usein
- jos RAM on niukka ja kone alkaa sivuttaa, nopeakaan NVMe ei tee tilanteesta "hyvää", vain vähemmän huonoa
- jos malli pysyy jo hyvin muistissa eikä kuorma heilu paljon, levyn vaihto ei välttämättä näy vasteessa juuri lainkaan

Toisin sanoen NVMe voi pehmentää huonoa muistibudjettia, mutta ei poista sen juurisyytä.

## Milloin NVMe-päivitys tuntuu oikeasti hyödylliseltä?

Minun mielestäni nopea NVMe on perusteltu paikalliseen LLM-koneeseen etenkin näissä tilanteissa:

- vaihdat usein mallista toiseen testatessa kvantisointeja
- ajat useita eri agentteja tai projekteja, jotka herättelevät malleja vuorotellen
- käytät samaa konetta myös vektoridatoihin, dokumenttikorpuksiin tai muuhun I/O-raskaaseen työhön
- lataat säännöllisesti isoja GGUF-tiedostoja tai päivität mallikirjastoa usein

Näissä tapauksissa et ehkä saa valtavaa token/s-loikkaa, mutta saat vähemmän odottelua, vähemmän "miksei tämä ole vielä valmis" -kitkaa ja sujuvamman kehityssyklin.

## Milloin SATA SSD riittää edelleen aivan hyvin?

Monelle harrastajalle vastaus on: yllättävän usein. SATA SSD ei ole paikallisen LLM-koneen häpeäpilkku, jos:

- ajat pääosin yhtä mallia kerrallaan
- pidät mallin muistissa pitkään
- et rakenna samaan koneeseen raskasta RAG-pinoa
- todellinen pullonkaula on VRAM, RAM tai GPU:n laskentakyky

Jos kone avaa mallin aamulla ja palvelee sitä pitkän session ajan, nopeampi levy ei välttämättä siirrä arkikokemusta paljonkaan. Silloin raha menee usein paremmin suurempaan VRAMiin, lisä-RAMiin tai hiljaisempaan jäähdytykseen.

## Entä jos kone pageaa koko ajan?

Tässä kohtaa kannattaa olla tarkkana. `llama.cpp`:n dokumentaatio varoittaa suoraan, että `mmap` voi lisätä pageout-riskiä, jos malli on suurempi kuin käytettävissä oleva RAM tai jos muistia on muuten niukasti. Tässä tilanteessa NVMe voi auttaa sikäli, että sivutus osuu nopeammalle levylle. Mutta käytännön johtopäätös ei ole "osta nopeampi SSD ja ongelma ratkeaa", vaan:

1. pienennä mallia tai kvantisointia
2. laske kontekstia tai rinnakkaisuutta
3. lisää RAMia, jos käyttöprofiili sitä oikeasti tarvitsee
4. vasta sitten mieti, onko levy vielä seuraava kitkakohta

Nopea levy on hyvä turvaverkko. Se ei ole sama asia kuin terve muistibudjetti.

## Oma ostojärjestykseni kotilabran LLM-koneessa

Jos budjetti on rajallinen, etenisin yleensä näin:

1. riittävä VRAM sille malliluokalle, jota oikeasti aiot ajaa
2. riittävä RAM, jotta käyttö ei kaadu jatkuvaan sivutukseen
3. SSD, joka on jo vähintään järkevä SSD eikä vanha mekaaninen levy
4. vasta tämän jälkeen premium-NVMe, jos vaihtelet malleja paljon tai teet muutakin I/O-raskasta

Tärkein raja kulkee siis usein **HDD:n ja SSD:n** välillä, ei niinkään "ihan ok SSD:n" ja "todella nopean NVMe:n" välillä.

## Tiivis johtopäätös

**NVMe nopeuttaa paikallisessa LLM-koneessa ennen kaikkea mallin latausta, mallinvaihtoa ja yleistä tiedostotyötä.** Se voi parantaa käyttökokemusta paljonkin, jos vaihdat malleja usein tai kone sivuaa levyä jatkuvasti. Sen sijaan puhdasta generointinopeutta se ei tavallisesti ratkaise, jos varsinainen työ tapahtuu jo GPU:ssa tai vakaasti RAMissa.

Jos siis mietit seuraavaa päivitystä, kysy ensin tämä: odotatko eniten **mallin käynnistymistä** vai **itse vastausta**? Ensimmäiseen NVMe auttaa usein selvästi. Jälkimmäiseen vastaus löytyy useammin VRAMista, RAMista tai GPU:sta.

## Lähteet

- https://docs.ollama.com/faq
- https://github.com/ggml-org/llama.cpp/blob/master/tools/cli/README.md
- https://nvmexpress.org/wp-content/uploads/NVMe_Overview.pdf
