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

## Uusi postaus

PowerShell:
```powershell
./scripts/new-post.ps1 -Title "Oma otsikko"
```

## Julkaisurutiini (suositus)

1. Luo postaus:
   ```powershell
   ./scripts/new-post.ps1 -Title "Otsikko"
   ```
2. Julkaise yhdellä komennolla:
   ```powershell
   ./scripts/publish.ps1 -Message "Uusi postaus"
   ```

Push `main`-haaraan käynnistää automaattisen deployn.

## Deploy tuotantoon

### Vaihtoehto A: GitHub Pages (automaattinen)
1. Luo GitHub-repo tästä kansiosta
2. Push `main`-haaraan
3. GitHub: Settings → Pages → Source: GitHub Actions
4. Workflow `deploy-github-pages.yml` julkaisee automaattisesti

### Vaihtoehto B: Cloudflare Pages
- Luo Pages-projekti ja linkitä repo
- Build command: `hugo --minify`
- Output directory: `public`
- `_headers` tiedosto lisää turvallisuusheaderit

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

## Seuraavat 3 hyväksyntää sinulta
1. GitHub-repon luonti / oikeudet
2. Pages-julkaisun aktivointi
3. (Valinnainen) Cloudflare-domainin DNS-valtuutus
