# Sources and method

The full source list, with publishers, links and access dates, is in
**data/sources.csv** and in the report's reference list.

## Data

- **data/rentals.csv**: 276 cleaned asking rents from WSE.AM, downloaded on
  5 November 2026. Two rooms, 45–75 m², furniture advertised, priced in AMD. Each
  row has the road distance and empty-road driving time to Republic Square and
  back (OSRM, OpenStreetMap). The original 949-record extraction and screening
  evidence are in **_archive/previous-version**. Public access is not a
  redistribution licence.
- **data/tariffs.csv**: official electricity, gas, water and bus-fare facts.
- **data/wages.csv**: Armstat's average gross monthly wage; 2025 is used to value
  time.
- **data/taxi_tariffs.csv**: Yandex Go's official Yerevan rates for seven classes,
  24 November 2026. The report uses Comfort, and Start for comparison.
- **data/traffic_score_weekday.csv**: Yandex's 0–10 weekday traffic score,
  07:00–22:00, read at 15-minute steps from a Yandex chart for February 2020.
- **data/traffic_benchmarks.csv**: published traffic facts (Yandex, the Yerevan
  mayor, Numbeo).

Raw pages and how each taxi and traffic number was made are in
**data/raw/taxi_traffic_2026-11-24/README.md**.

## Method in short

- Districts are compared with Kentron, with Republic Square as the shared
  destination.
- **Direct monthly cost** = rent + winter bills (heating counted once, as gas)
  + transport. **Cost including time** adds commuting hours × a value of time.
- **Bus:** 12 km/h on the road route + 15 minutes per trip; the cheaper of single
  tickets or a 30-day pass.
- **Road traffic (car and taxi):** time = empty-road time ×
  (1 + 0.13 × (Yandex score − 2)). Trips leave at 08:45 (score 5.9) and 18:30
  (score 7.8). Yandex does not publish how its score turns into minutes. The 0.13
  gives about +75% at the evening peak, which matches the mayor's "70–80% longer
  at rush hour" (October 2026). Numbeo users' car commutes (about 27 km/h against
  42 km/h on empty roads) give the same stretch.
- **Car:** traffic time + 5 minutes parking per trip; 60 AMD/km plus 10,000 AMD
  parking a month.
- **Taxi:** Yandex fare per trip = minimum price (covers 1 km and 2.5 min) +
  price per km + price per minute, × surge, rounded up to the next 100 AMD. These
  rules are from Yandex's fare page; the rates are maximums and exclude surge.
  Waiting 3 minutes for the car counts as time, not money.
- Each district budget combines the district's median rent and median route.
  It is an example, not a real household bill.
- No p-values: the ads are one agency's catalogue, not a random sample, and the
  scenarios are not independent households.

## Why these charts

| Question | Chart | Reason |
|---|---|---|
| Where is rent cheaper? | Boxplots | Show medians, spread and overlap of the ads |
| How does traffic change the trip? | Line chart by hour | Shows the Yandex traffic curve turned into minutes |
| How long is the commute? | Grouped bars | Compare bus, car and taxi in each district |
| What does a month cost? | Stacked bars, one panel per mode | Show rent, bills and transport adding up |
| How much saving is left? | Grouped bars for the closest case | Show rent saved, extra costs and what remains |
| Start or Comfort, with surge? | Small multiples of lines | Show when, if ever, the taxi saving reaches zero |
| When can the answer change? | Heatmap | Compare a heavy winter across values of time |
| When would the saving disappear? | Dot plot | Compare break-even values of time with the wage |

All charts use ggplot2 techniques from the DS116 lectures.

## Course requirements

The DS116 course repository and the original course audit are in
**_archive/previous-version/references/course-requirements.md**. The project
rubric, deadline and the instructor's AI policy still need confirmation before
submission. AI assistance is recorded in **references/AI_assistance.md**.
