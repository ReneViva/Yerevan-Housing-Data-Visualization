# Taxi and traffic source snapshots (24 November 2026)

Raw pages saved with `curl` on 24 November 2026 for the Yandex Taxi comparison.
They are immutable evidence for the tidy CSVs in `data/`. `SHA256SUMS.txt`
holds their hashes. robots.txt was checked for every site; all pages used are
allowed. No logins, API keys or paid services were used. One site (arkatelecom.am)
answered with a bot challenge; it was not bypassed and no copy was kept.

## What exists and what does not

- **Hourly Yandex Taxi prices for Yerevan: not published.** Yandex shows a
  price only for one requested ride at one moment. Surge multipliers are not
  published.
- **Yandex Go fare rules for Yerevan: published.** A ride costs a minimum price
  (covers the first 1 km and 2.5 min), then a price per km and per minute. So
  price depends on distance **and** on time in traffic.
- **Yerevan traffic by time of day: published only as Yandex's 0–10 traffic
  score** (an index, not a speed). TomTom's Traffic Index does not include
  Yerevan (its city page returns 404).

## Files

| File | Source | Used for |
|---|---|---|
| `yandex_tariff_index.html` and `yandex_tariff_<slug>.html` (7 classes) | Yandex Go official Yerevan fare pages | `data/taxi_tariffs.csv` |
| `yandex_chart_1593694571_1039495.jpg` | Yandex chart "Change of traffic score during a working day, February 2020", published by Mediamax (1 July 2020) | `data/traffic_score_weekday.csv` |
| `yandex_chart_1593694571_6223199.jpg` | Yandex chart of the average score during the 2020 quarantine | context only |
| `mediamax_jams_launch_ru.html` | Mediamax, 27 March 2018: Yandex launches the traffic score in Yerevan | `data/traffic_benchmarks.csv` |
| `mediamax_jams_covid_ru.html` | Mediamax, 1 July 2020: interview with Yandex analyst Leonid Mednikov | `data/traffic_benchmarks.csv`, chart images |
| `yandex_jams_method.html` | Yandex, "How Yandex Traffic works" | method note below |
| `numbeo_traffic_yerevan.html` | Numbeo, Traffic in Yerevan (48 contributors, updated 16 Nov 2026) | `data/traffic_benchmarks.csv` |
| `pan_mayor_traffic_en.html` | PAN.am, 12 Oct 2026: Yerevan Mayor Tigran Avinyan on traffic | `data/traffic_benchmarks.csv` |

## How the tidy files were made

- `taxi_tariffs.csv`: numbers copied from the seven city service-class pages.
  The City to City class (pickup-fee structure, for trips between cities) was
  left out. All Yerevan districts in the study are inside the city, so the
  **city** rates apply. The page states: values are **maximums** ("not more
  than"); surge, demand and density **multipliers are not included**; the final
  price is **rounded up to a multiple of 100 AMD**; a pickup fee may be added;
  "rates are valid until 24.11.2026" (the page shows the retrieval date).
- `traffic_score_weekday.csv`: the 07:00–22:00 weekday line was **digitized**
  from the chart's pixels at 15-minute steps. Gridlines were found at
  49 px per score point and the x-axis spans 07:00–22:00; values were rounded
  to 0.1. Spot checks against the chart and the analyst's text: score ≈ 2 before
  08:00, ≈ 6 at 08:45, ≈ 7.8 at 18:30. This is **February 2020**, before the
  pandemic and before later road changes. Hours before 07:00 and after 22:00
  are not covered.
- `traffic_benchmarks.csv`: individual facts from the articles and Numbeo,
  one per row, with source and period.

## Limits to keep in mind

- Yandex defines the score from how much longer fixed city routes take than
  their free-flow reference time, but it **does not publish a formula** turning
  a score into extra minutes. Any score-to-time conversion is an assumption.
  The mayor's 2026 figure (rush-hour bus trips take 70–80% longer) is the best
  available anchor.
- Numbeo values are self-reported perceptions from 48 people, not measurements.
- The study's road distances and free-flow minutes per listing are already in
  `data/rentals.csv` (OSRM), so a taxi fare can be modeled per listing.
- **Rights:** these are publishers' copyrighted pages and images. They are kept
  as evidence; do not republish them publicly without checking. Numbeo has its
  own data license. The `.html` and `.jpg` copies are therefore kept only on
  the local computer (ignored by Git); this README and `SHA256SUMS.txt` are
  public so the files can be re-checked.
