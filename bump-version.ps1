# bump-version.ps1 — Atualiza versão no etograma.html e cria git tag
# Uso: .\bump-version.ps1 [patch|minor|major] [--dry-run]
#
# Exemplos:
#   .\bump-version.ps1          # patch (1.0.0 → 1.0.1)
#   .\bump-version.ps1 minor    # minor (1.0.0 → 1.1.0)
#   .\bump-version.ps1 major    # major (1.0.0 → 2.0.0)
#   .\bump-version.ps1 --dry-run

param(
    [string]$Type = "patch",
    [switch]$DryRun
)

$file = Join-Path $PSScriptRoot "etograma.html"

# Lê versão atual
$content = Get-Content $file -Raw
if ($content -notmatch "const APP_VERSION = '(\d+)\.(\d+)\.(\d+)'") {
    Write-Error "APP_VERSION não encontrada em etograma.html"
    exit 1
}

[int]$major = $Matches[1]
[int]$minor = $Matches[2]
[int]$patch = $Matches[3]
$current = "$major.$minor.$patch"

# Calcula nova versão
switch ($Type) {
    "major" { $major++; $minor = 0; $patch = 0 }
    "minor" { $minor++; $patch = 0 }
    default { $patch++ }
}
$next = "$major.$minor.$patch"

Write-Host "Versão: $current → $next" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host "[dry-run] Nenhuma alteração aplicada." -ForegroundColor Yellow
    exit 0
}

# Atualiza etograma.html
$updated = $content -replace "const APP_VERSION = '$current'", "const APP_VERSION = '$next'"
Set-Content $file $updated -NoNewline

# Atualiza cache name no sw.js
$swFile = Join-Path $PSScriptRoot "sw.js"
$swContent = Get-Content $swFile -Raw
$swUpdated = $swContent -replace "const CACHE = 'etograma-v$current'", "const CACHE = 'etograma-v$next'"
Set-Content $swFile $swUpdated -NoNewline

# Commit + tag
git add etograma.html sw.js
git commit -m "chore: bump version to $next"
git tag "v$next"

Write-Host "Tag v$next criada. Use 'git push && git push --tags' para publicar." -ForegroundColor Green
