# Knit Yerevan_Housing_Research.Rmd with the project's pinned R 4.5.0 and RStudio Pandoc.
#   -Clean    : copy only the Rmd and data/ to a temporary folder and knit there
#               (proves the report reproduces; the project files are not touched).
#   (default) : knit in the project, updating outputs/ and figures/.
# Results for the Word companion are written to outputs/checks/results.json.
[CmdletBinding()]
param(
    [switch] $Clean,
    [string] $RscriptPath = 'D:\Softwares\Applications\R\R-4.5.0\bin\Rscript.exe',
    [string] $PandocDirectory = 'D:\Softwares\Applications\RStudio\resources\app\bin\quarto\bin\tools',
    [string] $TinyTexDirectory = "$env:APPDATA\TinyTeX\bin\windows"
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$script = Join-Path $PSScriptRoot 'knit_and_check.R'
$results = Join-Path $root 'outputs\checks\results.json'
foreach ($p in @($RscriptPath, (Join-Path $PandocDirectory 'pandoc.exe'))) {
    if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Not found: $p" }
}

# Sanitize locale only for the child R process.
foreach ($name in @('LANG', 'LANGUAGE', 'LC_ALL', 'LC_CTYPE', 'LC_COLLATE', 'LC_MESSAGES')) {
    Remove-Item "Env:$name" -ErrorAction SilentlyContinue
}
$env:RSTUDIO_PANDOC = $PandocDirectory
if (Test-Path -LiteralPath $TinyTexDirectory) { $env:PATH = "$TinyTexDirectory;$env:PATH" }

$work = $root
if ($Clean) {
    $work = Join-Path ([IO.Path]::GetTempPath()) ("yerevan-clean-" + [guid]::NewGuid().ToString('N').Substring(0, 8))
    New-Item -ItemType Directory -Path $work | Out-Null
    Copy-Item -LiteralPath (Join-Path $root 'Yerevan_Housing_Research.Rmd') -Destination $work
    Copy-Item -LiteralPath (Join-Path $root 'data') -Destination (Join-Path $work 'data') -Recurse
    $results = Join-Path $work 'outputs\checks\results.json'
}

Push-Location $work
try {
    & $RscriptPath --vanilla $script $root $results
    if ($LASTEXITCODE -ne 0) { throw "R exited with code $LASTEXITCODE" }
}
finally { Pop-Location }

$expected = @('outputs\Yerevan_Housing_Research.html', 'outputs\Yerevan_Housing_Research.pdf')
foreach ($f in $expected) {
    if (-not (Test-Path -LiteralPath (Join-Path $work $f))) { throw "Missing output: $f" }
}
$pngs = @(Get-ChildItem -LiteralPath (Join-Path $work 'figures') -Filter '*.png').Count
if ($pngs -ne 8) { throw "Expected 8 figures, found $pngs" }
foreach ($f in @('rentals.csv', 'sources.csv', 'tariffs.csv', 'wages.csv')) {
    if (-not (Test-Path -LiteralPath (Join-Path $work "data\$f"))) { throw "Missing data input: $f" }
}
Write-Output "PASS: HTML, PDF and 8 figures produced in $work"
Write-Output "Results: $results"
