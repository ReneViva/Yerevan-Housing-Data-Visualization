# Read the openly accessible WSE catalogue once and retain analytical facts only.
# PowerShell uses the Windows HTTPS trust store; certificate checks stay enabled.
[CmdletBinding()]
param([string]$SnapshotDate = '2026-11-05')

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$rawDirectory = Join-Path $projectRoot 'data/raw'
$csvPath = Join-Path $rawDirectory "housing_wse_catalogue_facts_$SnapshotDate.csv"
$metadataPath = Join-Path $rawDirectory "housing_wse_metadata_$SnapshotDate.json"
$robotsPath = Join-Path $rawDirectory "housing_wse_robots_$SnapshotDate.txt"
$indexPath = Join-Path $rawDirectory "housing_wse_rent_index_$SnapshotDate.csv"
foreach ($target in @($csvPath, $metadataPath, $robotsPath, $indexPath)) {
    if (Test-Path -LiteralPath $target) { throw "Immutable snapshot already exists: $target. Choose a new SnapshotDate label." }
}
function Get-TextHash([string]$Text) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
    return [Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
}

$headers = @{ 'User-Agent' = 'AUA-DS116-academic-research/1.0 (public factual rental analysis)' }
$robotsUrl = 'https://wse.am/robots.txt'
$apiUrl = 'https://wse.am/api/properties'
$indexUrl = 'https://wse.am/indeks-arendy-erevana/2026-11.csv'
$robotsResponse = Invoke-WebRequest -Uri $robotsUrl -Headers $headers -TimeoutSec 30
if ($robotsResponse.Content -notmatch '(?m)^Allow: /api/properties\s*$') {
    throw 'The known explicit robots allowance is absent. Review source access before downloading.'
}
$response = Invoke-WebRequest -Uri $apiUrl -Headers $headers -TimeoutSec 45
$retrievedAt = [DateTimeOffset]::UtcNow.ToString('o')
$catalogue = @($response.Content | ConvertFrom-Json)
$rentApartments = @($catalogue | Where-Object { $_.transaction_type -eq 'rent' -and $_.property_type -eq 'apartment' })
if ($rentApartments.Count -eq 0) { throw 'No rental apartments returned; inspect the API rather than inventing records.' }
$coordinateCounts = @{}
foreach ($item in $rentApartments) {
    $key = "$($item.latitude)|$($item.longitude)"
    if (-not $coordinateCounts.ContainsKey($key)) { $coordinateCounts[$key] = 0 }
    $coordinateCounts[$key]++
}
$facts = foreach ($item in $rentApartments) {
    $features = @($item.features)
    # Addresses may contain building numbers. Keep only a redacted street label.
    $streetRedacted = [regex]::Replace([string]$item.street_name, '\d+[\p{L}]*(?:[/\\-]\d+[\p{L}]*)?', '[number]')
    $identity = (@($item.city, $item.district, $item.address, $item.area, $item.rooms, $item.floor) -join '|').ToLowerInvariant().Trim()
    $coordinateKey = "$($item.latitude)|$($item.longitude)"
    [pscustomobject][ordered]@{
        listing_id = $item.id
        source = 'WSE.AM'
        source_api_url = $apiUrl
        listing_url = "https://wse.am/en/snyat/$($item.url_slug)-$($item.id)"
        retrieved_at_utc = $retrievedAt
        observation_date = [DateTimeOffset]::Parse($retrievedAt).ToString('yyyy-MM-dd')
        source_created_at = $item.created_at
        price_observation_date = ''
        price_kind = 'advertised asking monthly rent'
        transaction_type = $item.transaction_type
        property_type = $item.property_type
        status = $item.status
        city_source = $item.city
        district_source = $item.district
        street_redacted = $streetRedacted
        latitude = $item.latitude
        longitude = $item.longitude
        area_m2 = $item.area
        rooms = $item.rooms
        bedrooms = $item.bedrooms
        floor = $item.floor
        total_floors = $item.total_floors
        building_type_source = $item.building_type
        year_built_source = $item.year_built
        is_new_building_source = $item.is_new_building
        price_original = $item.price
        currency_original = $item.currency
        source_price_usd = $item.price_usd
        is_duplicate_source = $item.is_duplicate
        is_part_of_house_source = $item.is_part_of_house
        furniture_feature_present = $features -contains 'Мебель'
        air_conditioning_feature_present = $features -contains 'Кондиционер'
        washing_machine_feature_present = $features -contains 'Стиральная машина'
        lift_feature_present = $features -contains 'Лифт'
        renovation_condition_observed = ''
        outside_town_name_flag = [bool]([string]$item.address -match 'Масис|Абовян|Дзорахбюр|Зовуни|Прошян|Птгни|Аштарак|Егвард|Джрвеж')
        arinj_border_name_flag = [bool]([string]$item.address -match 'Ариндж')
        repeated_centre_coordinate_flag = [bool]($item.latitude -eq 40.1776 -and $item.longitude -eq 44.5126)
        coordinate_repeat_count = $coordinateCounts[$coordinateKey]
        property_signature_sha256 = Get-TextHash $identity
    }
}
$facts = @($facts)
if (@($facts.listing_id | Select-Object -Unique).Count -ne $facts.Count) { throw 'Repeated listing IDs returned by source.' }
$facts | Export-Csv -LiteralPath $csvPath -NoTypeInformation -Encoding utf8
$robotsResponse.Content | Set-Content -LiteralPath $robotsPath -Encoding utf8 -NoNewline
Invoke-WebRequest -Uri $indexUrl -Headers $headers -TimeoutSec 30 -OutFile $indexPath
$eligible = @($facts | Where-Object { $_.status -eq 'active' -and $_.city_source -eq 'Ереван' -and $_.rooms -eq 2 -and $_.area_m2 -ge 45 -and $_.area_m2 -le 75 -and -not $_.is_duplicate_source -and -not $_.is_part_of_house_source })
$metadata = [ordered]@{
    publisher = 'WSE.AM real estate agency'
    source_api_url = $apiUrl
    source_catalogue_url = 'https://wse.am/en/apartments-for-rent-yerevan'
    retrieved_at_utc = $retrievedAt
    response_content_sha256_utf8 = Get-TextHash $response.Content
    saved_facts_sha256 = (Get-FileHash -LiteralPath $csvPath -Algorithm SHA256).Hash.ToLowerInvariant()
    total_api_objects = $catalogue.Count
    retained_rent_apartments_all_cities = $facts.Count
    retained_yerevan_rent_apartments = @($facts | Where-Object city_source -eq 'Ереван').Count
    preliminary_two_room_45_75_m2_yerevan_n = $eligible.Count
    preliminary_district_counts = @($eligible | Group-Object district_source | ForEach-Object { [ordered]@{ district_source = $_.Name; n = $_.Count } })
    source_created_at_min = ($facts.source_created_at | Sort-Object | Select-Object -First 1)
    source_created_at_max = ($facts.source_created_at | Sort-Object | Select-Object -Last 1)
    time_semantics = 'Retrieved active catalogue as published; created_at is a source field, not verified price-update or tenancy date. Price observation date is unknown.'
    extraction = 'One public API GET; retain rent apartment factual whitelist only. No descriptions, images, agent records, contacts or unredacted address/house numbers saved. All cities retained to support exclusions.'
    source_access = 'robots.txt explicitly allows /api/properties and AI crawlers. No login, tokens, CAPTCHA workaround, or disabled TLS checks.'
    rights = 'No open-data redistribution license established. Site footer reserves rights. Limited factual academic extraction with attribution; do not republish the catalogue or claim CC licensing.'
    robots_url = $robotsUrl
    privacy_url = 'https://wse.am/en/privacy'
    frozen_index_url = $indexUrl
    frozen_index_page_url = 'https://wse.am/en/indeks-arendy-erevana/2026-11'
    frozen_index_effective_date = '2026-11-01'
    frozen_index_warning = 'Agency aggregate medians by district/rooms, separate from listing sample. CSV also contains a later sale-price section; never parse it as rents.'
    price_usd_warning = 'source_price_usd is a website conversion, not a verified historical FX series. Use original AMD prices for primary analysis or independently document FX.'
    feature_warning = 'Feature presence is observed advertising text; absent feature does not establish absence of furnishing/equipment. Renovation condition is unknown.'
    coordinate_warning = 'Source coordinates may be approximate/geocoded/placeholder. Repeated centre coordinate is flagged; obvious non-Yerevan towns can be incorrectly tagged city/district. No point is independently ground-truthed.'
    signature_warning = 'Hashed source city/district/address/area/rooms/floor is a possible-property duplicate screen, not proof of distinct apartments. Several units at same building can legitimately share a signature.'
    sampling_warning = 'Single-agency convenience catalogue; not probability sampling, completed leases, or all Yerevan rentals. All counts are snapshot-specific.'
}
$metadata | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $metadataPath -Encoding utf8
Write-Output "Saved $($facts.Count) factual rental apartment records; preliminary comparable Yerevan sample n=$($eligible.Count)."
Write-Output $csvPath
