# Preserve official-source snapshots with normal certificate verification.
# Run explicitly to refresh sources; existing dated snapshots are never replaced.
#Requires -Version 7.0
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$projectRoot = Split-Path -Parent $PSScriptRoot
$rawDirectory = Join-Path $projectRoot 'data/raw/official'
New-Item -ItemType Directory -Path $rawDirectory -Force | Out-Null
$sources = @(
    @{ id='transport'; url='https://transport.yerevan.am/'; publisher='Yerevan Municipality'; file='transport.html' },
    @{ id='transport_150'; url='https://www.yerevan.am/en/news/150-dram-mek-owgheworowt-yan-hamar-ew-ansahmanap-ak-p-at-et-neri-erkarats-owm/'; publisher='Yerevan Municipality'; file='transport-150.html' },
    @{ id='electricity'; url='https://www.ena.am/Info.aspx?id=11&lang=2'; publisher='Electric Networks of Armenia'; file='electricity.html' },
    @{ id='gas'; url='https://www.psrc.am/contents/newsPress/gas-tariff-22'; publisher='Public Services Regulatory Commission'; file='gas.html' },
    @{ id='gas_2026'; url='https://psrc.am/contents/page/posts/natural-gas-tariffs-for-residents-will-stay-unchanged'; publisher='Public Services Regulatory Commission'; file='gas-2026.html' },
    @{ id='water'; url='https://www.veolia.am/en/news/2026-drinking-water-tariff-consumers-will-not-increase'; publisher='Veolia Djur'; file='water.html' },
    @{ id='water_units'; url='https://www.veolia.am/en/consumers/frequently-asked-questions'; publisher='Veolia Djur'; file='water-units.html' },
    @{ id='wage'; url='https://armstat.github.io/sdg-data-armenia/prod/en/headline/8-5-1-a.csv'; publisher='Armstat'; file='wage.csv' },
    @{ id='wage_metadata'; url='https://sdg.armstat.am/8-5-1-a-iframe/'; publisher='Armstat'; file='wage-metadata.html' }
)
$metadata = foreach ($source in $sources) {
    $destination = Join-Path $rawDirectory $source.file
    if (-not (Test-Path -LiteralPath $destination)) {
        Invoke-WebRequest -Uri $source.url -OutFile $destination -TimeoutSec 60 -MaximumRetryCount 1
    }
    $file = Get-Item -LiteralPath $destination
    [pscustomobject]@{
        source_id=$source.id; publisher=$source.publisher; url=$source.url
        local_file=('data/raw/official/' + $source.file)
        retrieved_utc=$file.LastWriteTimeUtc.ToString('o')
        bytes=$file.Length; sha256=(Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
        status='downloaded; extraction and relevance require separate validation'
    }
    Write-Host ("Obtained: " + $source.id)
}
$metadata | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $rawDirectory 'source-metadata.json') -Encoding utf8
