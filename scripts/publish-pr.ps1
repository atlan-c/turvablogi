param(
  [Parameter(Mandatory=$true)] [string]$Message,
  [string]$BranchName = "",
  [string]$RepoUrl = "https://github.com/atlan-c/turvablogi"
)

if ([string]::IsNullOrWhiteSpace($BranchName)) {
  $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
  $BranchName = "content/$stamp"
}

git add .
git diff --cached --quiet
$hasChanges = $LASTEXITCODE -ne 0

if (-not $hasChanges) {
  Write-Host "No changes to publish."
  exit 0
}

git checkout -b $BranchName
if ($LASTEXITCODE -ne 0) { exit 1 }

git commit -m $Message
if ($LASTEXITCODE -ne 0) { exit 1 }

git push -u origin $BranchName
if ($LASTEXITCODE -ne 0) { exit 2 }

$prUrl = "$RepoUrl/compare/main...$BranchName?expand=1"
Write-Host "Open PR URL: $prUrl"
exit 0
