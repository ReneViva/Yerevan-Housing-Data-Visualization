# Render ONLY the generated companion with a dedicated invisible native Word.
# No software installation, macro execution, recent-file entry, or user-option edit.
#Requires -Version 7.0
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$inputDoc = Join-Path $root 'Yerevan_Housing_Code_Companion.docx'
$renderDir = Join-Path $root '_archive/revision-checks/word-pages'
New-Item -ItemType Directory -Path $renderDir -Force | Out-Null
$pdf = Join-Path $renderDir 'Yerevan_Housing_Code_Companion.pdf'
if (-not (Test-Path -LiteralPath $inputDoc -PathType Leaf)) { throw 'Generated companion is missing.' }
$word = $null
$documents = $null
$document = $null
$ownsApplication = $false
try {
    $word = New-Object -ComObject Word.Application
    $documents = $word.Documents
    if ($documents.Count -ne 0) { throw 'Refusing to use a Word instance with existing documents.' }
    $ownsApplication = $true
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3
    $document = $documents.Open($inputDoc, $false, $true, $false)
    $document.Repaginate()
    $document.ExportAsFixedFormat($pdf, 17, $false)
    Write-Output "Native Word PDF export: $pdf"
}
finally {
    if ($null -ne $document) {
        $document.Close(0)
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($document) | Out-Null
    }
    if ($ownsApplication -and $null -ne $word) { $word.Quit(0) }
    if ($null -ne $documents) { [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($documents) | Out-Null }
    if ($null -ne $word) { [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) | Out-Null }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
if (-not (Test-Path -LiteralPath $pdf -PathType Leaf)) { throw 'Word did not produce the expected PDF.' }
& pdfinfo.exe $pdf
if ($LASTEXITCODE -ne 0) { throw 'PDF inspection failed.' }
& pdftoppm.exe -r 110 -png $pdf (Join-Path $renderDir 'page')
if ($LASTEXITCODE -ne 0) { throw 'Page image rendering failed.' }
Write-Output 'Native Word and Poppler rendering finished. Inspect every page before delivery.'
