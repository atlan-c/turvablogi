# Turvablogi (avaimet käteen -runko)

Tämä projekti on turvallisuus edellä rakennettu staattinen blogi:
- ei kirjautumista julkiseen sivuun
- ei backendiä / tietokantaa internetiin
- ilmaiset komponentit (Hugo + GitHub + GitHub/Cloudflare Pages)

## Paikallinen käyttö

1. Asenna Hugo Extended
2. Aja projektin juuressa:
   ```bash
   hugo server -D
   ```
3. Avaa `http://localhost:1313`

## Selkokielinen wrapperi (ohjauspaneeli)

Aja projektin juuressa:

```bash
python -m streamlit run control_panel.py
```

Paneelissa on napit:
- Luo postaus
- Testaa build
- Julkaise tuotantoon (helppo moodi)
- Tarkista että live-sivu vastaa
- Avaa Actions
- Näytä seurattavat henkilöt ja aiheet

## Uusi postaus

PowerShell:
```powershell
./scripts/new-post.ps1 -Title "Oma otsikko"
```

## Julkaisurutiini (suositus)

Helppo moodi (vain `main`-haarassa):

```powershell
./scripts/publish.ps1 -Message "Uusi postaus"
```

`publish.ps1` tekee nyt:
- branch-tarkistuksen (pitää olla `main`)
- pre-publish laatutarkistuksen (`tools/pre_publish_check.py --staged`)
- commit
- `git pull --rebase origin main`
- push
- päivittää editorial-tilan (`data/editorial_state.json`)

## Deploy tuotantoon

### Vaihtoehto A: GitHub Pages (automaattinen)
1. Luo GitHub-repo tästä kansiosta
2. Push `main`-haaraan
3. GitHub: Settings → Pages → Source: GitHub Actions
4. Workflow `hugo.yml` ("Deploy Hugo site to Pages") julkaisee automaattisesti

### Vaihtoehto B: Cloudflare Pages
- Luo Pages-projekti ja linkitä repo
- Build command: `hugo --minify`
- Output directory: `public`
- `_headers` tiedosto lisää turvallisuusheaderit

## Seurantalista (AI + rauta + tietoturva)

- CSV: `data/people_watchlist.csv`
- Dokumentaatio: `docs/watchlist.md`

Tätä listaa voi käyttää postausaiheiden rotaation ja lähdevalintojen monipuolistamiseen.

## Editorial state + laatuportti

- Tiedosto `data/editorial_state.json` säilyttää viimeisimmän postauksen metatietoa (otsikkorakenne, intro-hash, lähdedomaanit).
- Skripti `tools/pre_publish_check.py` tarkistaa ennen julkaisua mm.:
  - frontmatter-kentät
  - minimisisällön
  - pakollisen `## Lähteet`-osion
  - vähintään 2 lähde-URLia
  - toiston eston (otsikkorakenne + aloituskappale)

## Turvallisuussuositukset
- Ota GitHub-tilille 2FA
- Käytä branch protectionia (`main`)
- Älä tallenna repoosi salaisuuksia
- Pidä ulkoiset scriptit minimissä (tässä CSP estää scriptit oletuksena)

## Mitä minä voin ylläpitää
- sisällön julkaisuputki
- automaattinen post-deploy health check (varmistaa että sivu vastaa)
- viikoittaiset health-checkit
- riippuvuuksien päivitys PR-mallilla
- turvallisuusasetusten jatkuva tarkistus
