param(
  [Parameter(Mandatory=$true)] [string]$Title
)

$slug = ($Title.ToLower() -replace '[^a-z0-9\s-]','' -replace '\s+','-').Trim('-')
$date = Get-Date -Format 'yyyy-MM-dd'
$path = "content/posts/$date-$slug.md"
@"
---
title: "$Title"
date: $date
draft: false
---

Kirjoita sisältö tähän.
"@ | Set-Content -Path $path -Encoding UTF8
Write-Host "Created $path"
