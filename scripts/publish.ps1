param(
  [Parameter(Mandatory=$true)] [string]$Message
)

$ErrorActionPreference = 'Continue'

# Ensure we are on main in easy mode
$branch = (git rev-parse --abbrev-ref HEAD).Trim()
if ($branch -ne "main") {
  Write-Error "Current branch is '$branch'. Switch to main before publishing in Easy mode."
  exit 3
}

git add .
git diff --cached --quiet
$hasChanges = $LASTEXITCODE -ne 0

if (-not $hasChanges) {
  Write-Host "No changes to publish."
  exit 0
}

python tools/pre_publish_check.py --staged
if ($LASTEXITCODE -ne 0) {
  Write-Error "Pre-publish quality check failed."
  exit 5
}

git commit -m $Message
if ($LASTEXITCODE -ne 0) {
  Write-Error "Commit failed."
  exit 1
}

git pull --rebase origin main
if ($LASTEXITCODE -ne 0) {
  Write-Error "Pull --rebase failed. Resolve conflicts and retry."
  exit 4
}

git push origin main
if ($LASTEXITCODE -ne 0) {
  Write-Error "Push failed."
  exit 2
}

python tools/pre_publish_check.py --update-state | Out-Null
Write-Host "Published to main. GitHub Actions will deploy automatically."
exit 0
