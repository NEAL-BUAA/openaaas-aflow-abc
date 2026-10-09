# Run only after creating an EMPTY public GitHub repo named openaaas-aflow-abc under NEAL-BUAA.
# Uses Git installed on your Windows PC. No secret files should be in this repo.
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$target = 'https://github.com/NEAL-BUAA/openaaas-aflow-abc.git'
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git not installed' }
if (-not (Test-Path '.git')) { git init; if ($LASTEXITCODE -ne 0) {throw 'git init failed'} }
git branch -M main
# Explicit caution: do not submit AFLOW database, auth files, runtime config.
git add .
if ($LASTEXITCODE -ne 0) {throw 'git add failed'}
Write-Host 'Review the staged files. No API keys, AFLOW database, private config or token should appear:'
git diff --cached --name-only
$answer = Read-Host 'Type PUBLISH to commit and upload to your public GitHub repository'
if ($answer -cne 'PUBLISH') { Write-Host 'Cancelled'; exit 1 }
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { git commit -m 'Assignment 2: OpenAaaS A-C-B AFLOW architecture'; if ($LASTEXITCODE -ne 0) {throw 'commit failed'} }
$existing = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {git remote set-url origin $target} else {git remote add origin $target}
if ($LASTEXITCODE -ne 0) {throw 'remote configuration failed'}
git push -u origin main
if ($LASTEXITCODE -ne 0) {throw 'push failed; check GitHub repository and authentication'}
Write-Host "Published to $target"
