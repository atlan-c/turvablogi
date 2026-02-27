param(
  [Parameter(Mandatory=$true)] [string]$Message
)

git add .
if (-not (git diff --cached --quiet)) {
  git commit -m $Message
  git push origin main
  Write-Host "Published to main. GitHub Actions will deploy automatically."
} else {
  Write-Host "No changes to publish."
}
