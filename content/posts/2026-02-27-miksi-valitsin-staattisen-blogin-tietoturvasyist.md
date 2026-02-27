---
title: "Miksi valitsin staattisen blogin tietoturvasyistä"
date: 2026-02-27
draft: false
---


Tämä on editoitu testisisältö.

[main 3720696] Remove duplicate deploy workflow and simplify healthcheck trigger
3 files changed, 2 insertions(+), 41 deletions(-)
delete mode 100644 .github/workflows/deploy-github-pages.yml
To https://github.com/atlan-c/turvablogi.git
2db281a..3720696 main -> main

exec
View
[main 3720696] Remove duplicate deploy workflow and simplify healthcheck trigger
 3 files changed, 2…
tool
6:18 PM
🦀

[[reply_to_current]]Siivous tehty ✅

Poistin ylimääräiset niin, että nyt jää:

1 deploy-workflow: hugo.yml (Deploy Hugo site to Pages)
1 health-check workflow: post-deploy-healthcheck.yml (laukeaa vain tuon deployn jälkeen)
plus security-check.yml
Lisäksi päivitin README:n vastaamaan tätä.

Nyt Actions-lista pysyy paljon selkeämpänä eikä samoja deploy-ajojä enää tule rinnakkain.

expert
6:18 PM
U
mitä tehdään nyt?

You
6:20 PM
🦀

[[reply_to_current]]Hyvä tilanne nyt: sivu on livenä ja workflowt siivottu.
Seuraavaksi suosittelen tätä järjestystä:

Varmistus: tarkista Actionsista että viimeisin deploy + health-check ovat vihreät
Sisältö: tehdään yksi oikea blogipostaus valmiiksi ja julkaistaan
Perusturva: laitetaan GitHubissa branch protection (main) + 2FA varmistus
Ylläpito: sovitaan kevyt rutiini (esim. viikoittainen päivitys/health check)
Jos haluat, aloitetaan heti kohdasta 2 ja minä annan taas yhden askeleen kerrallaan.