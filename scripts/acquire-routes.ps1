# Obtain network-model outputs, not observed or public-transit journey times.
# Public OSRM car demo; two directions, no straight-line fallback, cached replies.
#Requires -Version 7.0
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$sourcePath = Join-Path $root 'data/raw/housing_wse_catalogue_facts_2026-11-05.csv'
$routeDirectory = Join-Path $root 'data/raw/routes_2026-11-05'
New-Item -ItemType Directory -Path $routeDirectory -Force | Out-Null
$rows = @(Import-Csv -LiteralPath $sourcePath | Where-Object {
    $_.city_source -eq 'Ереван' -and $_.currency_original -eq 'AMD' -and
    [double]$_.rooms -eq 2 -and [double]$_.area_m2 -ge 45 -and [double]$_.area_m2 -le 75 -and
    $_.is_duplicate_source -eq 'False' -and $_.is_part_of_house_source -eq '0' -and
    $_.furniture_feature_present -eq 'True' -and $_.repeated_centre_coordinate_flag -eq 'False' -and
    $_.outside_town_name_flag -eq 'False' -and $_.arinj_border_name_flag -eq 'False'
})
$rows = @($rows | Group-Object property_signature_sha256 | ForEach-Object {
    $_.Group | Sort-Object source_created_at -Descending | Select-Object -First 1
} | Sort-Object { [int]$_.listing_id })
foreach ($row in $rows) {
    if ([double]$row.latitude -lt 40.05 -or [double]$row.latitude -gt 40.30 -or
        [double]$row.longitude -lt 44.35 -or [double]$row.longitude -gt 44.70) {
        throw "Coordinate outside declared broad Yerevan screening box: $($row.listing_id)"
    }
}
$destination = '44.512600,40.177600' # Declared point within Republic Square.
$manifest = @()
$results = @()
for ($start = 0; $start -lt $rows.Count; $start += 40) {
    $last = [Math]::Min($start + 39, $rows.Count - 1)
    $batch = @($rows[$start..$last])
    $coordinates = @($batch | ForEach-Object {
        ([double]$_.longitude).ToString('F6',[cultureinfo]::InvariantCulture) + ',' +
        ([double]$_.latitude).ToString('F6',[cultureinfo]::InvariantCulture)
    }) + @($destination)
    $originIndexes = (0..($batch.Count - 1)) -join ';'
    $baseUrl = 'https://router.project-osrm.org/table/v1/driving/' + ($coordinates -join ';')
    $responses = @{}
    foreach ($direction in @('outbound','return')) {
        $url = if ($direction -eq 'outbound') {
            $baseUrl + '?sources=' + $originIndexes + '&destinations=' + $batch.Count + '&annotations=distance,duration'
        } else {
            $baseUrl + '?sources=' + $batch.Count + '&destinations=' + $originIndexes + '&annotations=distance,duration'
        }
        $name = ('batch-{0:D3}-{1}.json' -f $start,$direction)
        $path = Join-Path $routeDirectory $name
        if (-not (Test-Path -LiteralPath $path)) {
            Invoke-WebRequest -Uri $url -OutFile $path -TimeoutSec 60 -MaximumRetryCount 1
            Start-Sleep -Seconds 1
        }
        $reply = Get-Content -LiteralPath $path -Raw | ConvertFrom-Json -Depth 50
        if ($reply.code -ne 'Ok') { throw "OSRM query failed: $name" }
        $responses[$direction] = $reply
        $manifest += [pscustomobject]@{
            file=$name; direction=$direction; url=$url
            retrieved_utc=(Get-Item -LiteralPath $path).LastWriteTimeUtc.ToString('o')
            sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
            data_version=$reply.data_version; listing_ids=@($batch.listing_id)
        }
    }
    for ($i = 0; $i -lt $batch.Count; $i++) {
        $out = $responses.outbound; $back = $responses.return
        $results += [pscustomobject]@{
            listing_id=$batch[$i].listing_id
            outbound_m=$out.distances[$i][0]; return_m=$back.distances[0][$i]
            outbound_seconds=$out.durations[$i][0]; return_seconds=$back.durations[0][$i]
            outbound_snap_m=$out.sources[$i].distance; return_snap_m=$back.destinations[$i].distance
            destination_snap_m=$out.destinations[0].distance
            route_kind='OSRM car-network estimate; no live traffic; no transit itinerary'
        }
    }
    Write-Host ("Routed origins: " + $results.Count + '/' + $rows.Count)
}
$results | Export-Csv -LiteralPath (Join-Path $routeDirectory 'routes.csv') -NoTypeInformation -Encoding utf8
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $routeDirectory 'manifest.json') -Encoding utf8
Write-Host 'Saved both directions; snap-distance and missing-route checks remain for the R analysis.'
