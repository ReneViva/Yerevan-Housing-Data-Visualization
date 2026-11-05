"""Author the single self-contained analysis Rmd and its matching teaching guide."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
guides = []
parts = [r'''---
title: "Does Cheaper Housing Make Life More Expensive?"
subtitle: "Yerevan asking rents and conditional commuting and winter utility costs"
date: "5 November 2026"
output:
  html_document:
    toc: true
    toc_depth: 2
    number_sections: false
    code_folding: show
    self_contained: true
    theme: readable
    highlight: textmate
    mathjax: null
---

<style>
table { display: block; max-width: 100%; overflow-x: auto; }
pre { max-width: 100%; overflow-x: auto; }
img { max-width: 100%; height: auto; }
</style>

## Introduction

A lower advertised rent may leave more money for other needs. A longer commute
can consume some of that saving through transport spending and time. This study
asks whether those extra costs outweigh the saving for comparable rental choices
in Yerevan. The answer is allowed to be either yes or no.

We study **advertisements from one agency**, not actual signed leases or a random
sample of households. The main comparison uses two-room apartments, 45–75 m²,
advertised as furnished. Room and area filters improve comparability; missing
renovation and energy-efficiency information prevents a quality-adjusted claim.

For each named district we construct an **example monthly budget** from its
sample-median asking rent, median round-trip road distance, and median route
duration. These medians may describe different apartments. The result is a
modeled district budget, not an observed household bill or the median of summed
apartment-level costs. Kentron is the central-area comparator; its homes still
have their own journeys to the common destination, Republic Square.

### Research question and competing hypotheses

Does rent saved relative to Kentron exceed additional transport, selected
utilities, and optionally valued commuting time? For each named comparison,
define Delta as its modeled cost minus Kentron's. Negative Delta means the
comparison is cheaper under that scenario; positive Delta means it is dearer.
The competing possibilities are Delta < 0, Delta = 0, and Delta > 0.

An inferential null would be H0: Delta = 0, versus H1: Delta is not zero,
with alpha = 0.05 fixed before results. **We do not run a population hypothesis
test here.** One agency's convenience catalogue, uncertain dwelling independence,
and constructed budgets do not justify the intended citywide p-values or
confidence intervals. This is a descriptive and sensitivity study. A p-value,
even if available, would not establish causation or prove a hypothesis.

### Two outcomes and their limits

- **Direct selected cost:** asking rent + modeled electricity, gas and water +
  modeled commuting spending, in AMD per household per 30-day month.
- **Generalized selected cost:** direct selected cost + modeled commuting hours
  multiplied by an assumed AMD/hour value of time.

These are selected housing-and-commuting components, not a complete living-cost
index. Food, internet, waste charges, building fees, moving costs, deposits,
health costs and full car ownership are outside the measured model. Heating is
included once through gas. Valued time is an opportunity-cost scenario, not an
extra cash payment or a verified loss of earnings. A zero time value must give
exactly the direct-cost outcome.

### Sources and what they can establish

| Evidence | Coverage and use | Important limitation |
|---|---|---|
| [WSE.AM catalogue](https://wse.am/en/apartments-for-rent-yerevan) and public API | Active catalogue retrieved 5 November 2026; asking prices, rooms, area, advertised furniture, district labels and approximate coordinates | Single agency; availability and last price-update date unverified; no open redistribution license established |
| [Yerevan transport](https://transport.yerevan.am/) | Public fare table inspected in the rendered official page | Fares do not provide observed trip times or household spending |
| [Electric Networks of Armenia](https://www.ena.am/Info.aspx?id=11&lang=2) | Standard household day/night tariffs by monthly consumption band | Tariffs are observed; our consumption amounts are assumptions |
| [PSRC gas decision](https://www.psrc.am/contents/newsPress/gas-tariff-22) and [2026 statement](https://psrc.am/contents/page/posts/natural-gas-tariffs-for-residents-will-stay-unchanged) | Standard gas rate and confirmation of unchanged resident payments from August 2026 | Household consumption and heating efficiency are not observed |
| [Veolia Djur](https://www.veolia.am/en/news/2026-drinking-water-tariff-consumers-will-not-increase) | Standard 2026 metered water/wastewater rate | Assumed household use; excludes special eligibility |
| [Armstat wages](https://sdg.armstat.am/8-5-1-a-iframe/) | 2025 national gross monthly wage, used only as a time-value benchmark | Lagged national gross mean, not a renter's net wage |
| [OSRM](https://project-osrm.org/docs/v26.5.0/http) using OpenStreetMap | Two-way car-network distance and free-flow model duration, queried 5 November 2026 | Approximate origins, no live traffic and no transit itinerary |

All sources were accessed on 5 November 2026. Raw factual extracts, hashes,
retrieval metadata and route replies are retained separately from processed
tables. Only analytical housing fields were extracted; contacts, images, owner
names and full address numbers were excluded. Source robots explicitly permits
the public API, but that is not an open-data license. Do not republish the catalogue
as an openly licensed dataset. The frozen 1 November agency district index is
retained as separate context and is **not pooled** into this later listing sample.

The geography is **named agency-labeled Yerevan districts**. Outside Kentron does
not mean outside Yerevan. Abovyan and Masis are not compared: adequate matched
town samples and journeys were not established. One Masis listing mislabeled as
Kentron is excluded. District labels and origin coordinates are not ground-truthed
administrative boundaries. No map is used to suggest precision we do not have.

## Reproducible analysis

Run this file from the project root using the verified R launcher. It reads local
snapshots and makes no network requests during rendering. It needs the existing
ggplot2, dplyr, tidyr, knitr, scales and jsonlite packages. No package is installed
automatically. All substantive analysis chunks run; no result is supplied by
invented example observations.
''']


def chunk(label, title, objective, what, blocks, expected, interpretation, hypothesis, why):
    lines = []
    documented = []
    for code, explanation in blocks:
        if lines:
            lines.append("")
        start = len(lines) + 1
        lines.extend(code.strip("\n").splitlines())
        documented.append({"start": start, "end": len(lines), "explanation": explanation})
    code = "\n".join(lines)
    guides.append(dict(label=label, title=title, objective=objective, what=what,
                       why=why, expected=expected, interpretation=interpretation,
                       hypothesis=hypothesis, blocks=documented))
    parts.append(f'''\n### Chunk {len(guides)} — {title}

**Research objective:** {objective}

**What this code does:** {what}

**Code:**

```{{r {label}}}
{code}
```

**Expected output:** {expected}

**Actual result:** `r chunk_results[["{label}"]]`

**Interpretation:** {interpretation}

**Connection to our hypothesis:** {hypothesis}
''')


chunk("setup", "Prepare a clean and documented R session",
      "Make the analysis repeatable and identify the software actually used.",
      "Loads installed packages, sets readable plotting defaults, and records existing package-build warnings.", [
    (r'''options(stringsAsFactors = FALSE, scipen = 999)
packages <- c("ggplot2", "dplyr", "tidyr", "knitr", "scales", "jsonlite")
setup_warnings <- character()
for (package in packages) {
  withCallingHandlers(
    suppressPackageStartupMessages(library(package, character.only = TRUE)),
    warning = function(w) {
      if (grepl("was built under R version", conditionMessage(w))) {
        setup_warnings <<- c(setup_warnings, conditionMessage(w))
        invokeRestart("muffleWarning")
      }
    }
  )
}''', "Load only installed dependencies. The handler records the known package-build warnings instead of filling the report with repeated messages; other warnings remain visible. No package is downloaded."),
    (r'''knitr::opts_chunk$set(echo = TRUE, message = FALSE, warning = TRUE,
                      fig.width = 9, fig.height = 5.5, dpi = 140,
                      fig.align = "center", out.width = "100%")
dir.create("outputs/figures", recursive = TRUE, showWarnings = FALSE)
theme_set(theme_minimal(base_size = 12))
set.seed(116)
money <- scales::label_number(accuracy = 1, big.mark = ",")
chunk_results <- list()
software <- data.frame(package = packages,
                       version = sapply(packages, function(p) as.character(packageVersion(p))))
rownames(software) <- NULL
knitr::kable(software)
chunk_results[["setup"]] <- paste("R", getRversion(), "loaded", length(packages),
                                 "packages; recorded", length(setup_warnings), "package-build warnings.")''', "Set a consistent chart style and seed for reproducible point jitter, create output folders, and list actual package versions. The seed affects visual jitter, not rental observations or scenario assumptions.")
], "A package-version table and a recorded environment status, without installing anything.",
      "The verified executable is R 4.5.0. Some existing packages were built under a newer patch release; their warnings are preserved in the final environment record. Successful execution of this report does not certify every possible package operation.",
      "This establishes a reproducible environment; it supplies no evidence about housing costs.",
      "Use the course's familiar packages and preserve environment warnings transparently.")

chunk("load-evidence", "Read the frozen evidence",
      "Identify the observations and official facts available for this study.",
      "Reads the agency facts, two-direction route results, tariff extraction and Armstat wage series from relative paths.", [
    (r'''raw <- read.csv("data/raw/housing_wse_catalogue_facts_2026-11-05.csv",
                fileEncoding = "UTF-8", check.names = FALSE)
routes <- read.csv("data/raw/routes_2026-11-05/routes.csv", fileEncoding = "UTF-8")
tariffs <- read.csv("data/raw/official/tariffs.csv", fileEncoding = "UTF-8")
wages <- read.csv("data/raw/official/wage.csv", fileEncoding = "UTF-8")
raw$listing_id <- as.character(raw$listing_id)
routes$listing_id <- as.character(routes$listing_id)
flag <- function(x) tolower(as.character(x)) %in% c("true", "1")''', "Read preserved files, make join IDs the same type, and interpret both textual and numeric source flags. Loading uses no live API, so future catalogue changes cannot silently alter these results."),
    (r'''stopifnot(!anyDuplicated(raw$listing_id), !anyDuplicated(routes$listing_id))
stopifnot(all(raw$price_original > 0), all(raw$area_m2 > 0))
stopifnot(all(raw$transaction_type == "rent"), all(raw$property_type == "apartment"))
evidence_counts <- data.frame(evidence = c("Retained rental facts", "Source-tagged Yerevan", "Routed origins"),
                              rows = c(nrow(raw), sum(raw$city_source == "Ереван"), nrow(routes)))
knitr::kable(evidence_counts)
chunk_results[["load-evidence"]] <- sprintf("Read %s rental facts, including %s tagged Yerevan, and %s network origins.",
                                           nrow(raw), sum(raw$city_source == "Ереван"), nrow(routes))''', "Check unique source IDs, positive basic quantities and rental-apartment tags. These checks detect some errors; unique IDs alone do not prove distinct dwellings.")
], "A small evidence-count table; invalid IDs or quantities stop execution.",
      "The raw facts include other room counts, currencies and locations so exclusions remain auditable. The source's active status is catalogue status, not confirmation of immediate vacancy. Creation dates are not verified price-update dates.",
      "These are usable advertised market records, but their existence does not establish the research conclusion.",
      "Frozen local inputs and explicit checks are simpler and more reproducible than downloading during rendering.")

chunk("screen-listings", "Select comparable advertised apartments",
      "Reduce obvious differences in rooms, area, currency, furnishing and geography before comparing prices.",
      "Applies predeclared screens, removes known ambiguous geography and one mixed-term offer, and conservatively screens possible duplicates.", [
    (r'''yerevan <- raw %>% filter(city_source == "Ереван")
room_area <- yerevan %>% filter(rooms == 2, area_m2 >= 45, area_m2 <= 75)
candidates <- room_area %>%
  filter(currency_original == "AMD", !flag(is_duplicate_source),
         !flag(is_part_of_house_source))
furnished <- candidates %>% filter(flag(furniture_feature_present))
located <- furnished %>%
  filter(!flag(repeated_centre_coordinate_flag), !flag(outside_town_name_flag),
         !flag(arinj_border_name_flag), between(latitude, 40.05, 40.30),
         between(longitude, 44.35, 44.70))''', "Limit the primary design to two rooms, the fixed size band, original AMD quotes and advertised furniture. Exclude flagged placeholders, town mismatches and boundary-ambiguous cases. The coordinate box is a broad error screen, not proof of district membership."),
    (r'''long_term <- located %>% filter(listing_id != "11834")
selected <- long_term %>%
  arrange(desc(source_created_at), desc(listing_id)) %>%
  distinct(property_signature_sha256, .keep_all = TRUE)
sample_flow <- data.frame(
  stage = c("All retained rental facts", "Tagged Yerevan", "Two rooms and 45–75 m2", "Native AMD, whole unit",
            "Furniture advertised", "Geographic screen", "Mixed-term offer excluded", "Possible duplicate screen"),
  n = c(nrow(raw), nrow(yerevan), nrow(room_area), nrow(candidates),
        nrow(furnished), nrow(located), nrow(long_term), nrow(selected)))
knitr::kable(sample_flow)
chunk_results[["screen-listings"]] <- sprintf("The fixed screens retain %s advertised-furnished apartments from %s native-AMD candidates.",
                                            nrow(selected), nrow(candidates))''', "Exclude ID11834 because its public page offers daily as well as long-term availability. Source page labels support monthly asking-price interpretation for the rental category. Keep one record per possible-property signature using a deterministic creation-date order; this is a conservative screen, not proof that two ads are the same dwelling.")
], "A sequential sample-flow table with all denominators visible.",
      "Absent furniture features mean unknown, not proven unfurnished. The signature screen removes a possible duplicate; distinct units can share building characteristics. Renovation remains unobserved, so the selected apartments are only partially comparable. Some ads have future or limited availability.",
      "This reduces several alternative explanations for rent differences, while leaving important quality and selection bias unresolved.",
      "Original AMD quotes avoid undocumented currency conversion; transparent narrow screens are preferable to unsupported quality adjustment.")

chunk("network-sample", "Check both directions of each journey",
      "Use network distances without silently replacing missing journeys with straight-line distance.",
      "Joins cached car-network outputs, checks both directions and snap distances, and fixes one primary analytical sample.", [
    (r'''joined <- selected %>% left_join(routes, by = "listing_id")
joined <- joined %>% mutate(
  route_valid = !is.na(outbound_m) & !is.na(return_m) &
    !is.na(outbound_seconds) & !is.na(return_seconds) &
    outbound_m >= 0 & return_m >= 0 & outbound_seconds >= 0 & return_seconds >= 0 &
    outbound_snap_m <= 250 & return_snap_m <= 250)
analysis <- joined %>% filter(route_valid) %>%
  mutate(round_trip_km = (outbound_m + return_m) / 1000,
         round_trip_freeflow_minutes = (outbound_seconds + return_seconds) / 60)
route_audit <- joined %>% group_by(district_source) %>%
  summarise(selected = n(), excluded_route = sum(!route_valid | is.na(route_valid)), .groups = "drop")
stopifnot(!anyDuplicated(analysis$listing_id), all(analysis$round_trip_km > 0))''', "Require route outputs and origin snapping within250m in each direction. Add outward and return lengths/times before converting metres to kilometres and seconds to minutes; one-way streets can make the two legs different."),
    (r'''district_names <- c("Кентрон" = "Kentron", "Арабкир" = "Arabkir", "Ачапняк" = "Ajapnyak",
  "Давташен" = "Davtashen", "Канакер-Зейтун" = "Kanaker-Zeytun", "Малатия-Себастия" = "Malatia-Sebastia",
  "Нор Норк" = "Nor Nork", "Норк-Мараш" = "Nork-Marash", "Шенгавит" = "Shengavit",
  "Эребуни" = "Erebuni", "Аван" = "Avan")
analysis$district <- unname(district_names[analysis$district_source])
stopifnot(!anyNA(analysis$district), "Kentron" %in% analysis$district)
write.csv(analysis, "data/processed/analysis_listings.csv", row.names = FALSE, fileEncoding = "UTF-8")
exclusions <- raw %>% select(listing_id, district_source, rooms, area_m2, currency_original) %>%
  mutate(in_primary_sample = listing_id %in% analysis$listing_id)
write.csv(exclusions, "data/processed/sample_membership.csv", row.names = FALSE, fileEncoding = "UTF-8")
knitr::kable(route_audit)
chunk_results[["network-sample"]] <- sprintf("The route-complete primary sample contains %s listings in %s agency-labeled districts; %s selected origins failed route checks.",
                                          nrow(analysis), n_distinct(analysis$district), nrow(selected) - nrow(analysis))''', "Translate source district labels for presentation and preserve both the analytical table and a membership log. Every primary rent and budget comparison uses this same sample, avoiding hidden denominator changes.")
], "A district route-exclusion table and reproducible processed files.",
      "OSRM supplies a car-road model, not measured peak travel. Approximate listing points and agency district tags remain uncertain even after snapping. Public-transport times below are separate road-distance-based assumptions, not these car durations relabeled as transit.",
      "The route inputs allow conditional commuting comparisons, but do not prove actual daily travel burdens.",
      "Two-direction cached network queries preserve road structure and provide an explicit missingness rule.")

chunk("district-summary", "Summarize rent and remaining comparability",
      "Describe how the selected advertisements differ across named districts.",
      "Calculates counts, rent spread, area spread and medians of already-summed round-trip road inputs.", [
    (r'''districts <- analysis %>% group_by(district) %>% summarise(
  n = n(), rent = median(price_original), rent_q1 = quantile(price_original, 0.25),
  rent_q3 = quantile(price_original, 0.75), area = median(area_m2),
  area_q1 = quantile(area_m2, 0.25), area_q3 = quantile(area_m2, 0.75),
  round_trip_km = median(round_trip_km),
  freeflow_minutes = median(round_trip_freeflow_minutes),
  missing_building = sum(is.na(building_type_source) | building_type_source == ""), .groups = "drop") %>%
  arrange(rent)
district_order <- districts$district
district_labels <- setNames(paste0(districts$district, " (n=", districts$n, ")"), districts$district)
summary_display <- districts %>% select(district, n, rent, rent_q1, rent_q3, area, area_q1, area_q3)
knitr::kable(summary_display, digits = 0, col.names = c("District", "n", "Rent AMD", "Rent Q1", "Rent Q3", "Area m2", "Area Q1", "Area Q3"))''', "Group by each named district and calculate sample medians and quartiles. Quartiles describe the middle half of these advertisements; they are not confidence intervals. Check area differences inside the allowed band rather than claiming all apartments are identical."),
    (r'''central_rent <- districts$rent[districts$district == "Kentron"]
chunk_results[["district-summary"]] <- sprintf("Kentron's sample-median asking rent is %s AMD. District sample sizes range from %s to %s; %s districts have fewer than 10 records.",
  money(central_rent), min(districts$n), max(districts$n), sum(districts$n < 10))''', "Record the central comparison and sparse-group warning for the executed narrative. The fewer-than-ten flag is a presentation caution, not a formal statistical cutoff.")
], "A rent-and-area summary table, with sample counts for each district.",
      "Unobserved renovation and partially missing building type remain competing explanations. Higher district rent can reflect location, quality, building mix or agency selection. The table is descriptive and cannot separate those effects.",
      "Rent savings are one side of the hypothesis; this table alone cannot determine whether commuting costs outweigh them.",
      "Medians are readable and less sensitive to extreme advertisements; showing IQRs and area spread prevents a misleading single-number comparison.")

chunk("rent-distribution", "Visualize the asking-rent distributions",
      "See both the rent differences and the variation hidden by district medians.",
      "Draws horizontal boxplots and individual advertisement points, with sample counts in district labels.", [
    (r'''rent_plot <- ggplot(analysis, aes(x = price_original, y = factor(district, levels = district_order))) +
  geom_boxplot(fill = "#D9E6EC", outlier.shape = NA, width = 0.55) +
  geom_jitter(height = 0.12, width = 0, alpha = 0.3, size = 1.1, color = "#244A60") +
  scale_y_discrete(labels = district_labels) +
  scale_x_continuous(labels = label_number(scale = 0.001, suffix = "k")) +
  labs(title = "Asking rents differ, and each district has substantial spread",
       subtitle = "Two rooms, 45–75 m², furniture advertised; one agency snapshot",
       x = "Advertised monthly rent (AMD)", y = NULL,
       caption = "Boxes show listing quartiles, not confidence intervals.\nSource: WSE.AM, 5 November 2026.")
rent_plot
ggsave("outputs/figures/rent-distribution.png", rent_plot, width = 9, height = 6.4, dpi = 160)
chunk_results[["rent-distribution"]] <- sprintf("The chart displays all %s primary advertisements; Kentron's median is %s AMD and the lowest district median is %s AMD.",
  nrow(analysis), money(central_rent), money(min(districts$rent)))''', "Map AMD rent to the horizontal axis and named districts to the vertical axis. Boxes and points show sample spread; transparent jitter separates overlapping points without changing the rent values. Save the same plot used in the report.")
], "One distribution chart, not a predicted price pattern.",
      "Overlapping distributions mean a household could find an unusually cheap central listing or an expensive noncentral one. District median differences are not guarantees for a specific available apartment.",
      "This tests the descriptive premise of cheaper rents away from the central comparator, not the full hidden-cost claim.",
      "A distribution chart preserves heterogeneity that a bar chart of medians would hide.")

chunk("rent-and-journey", "Compare rents with the road-journey model",
      "Explore whether lower asking rents accompany longer modeled car-network journeys.",
      "Plots individual rents against half of each two-way free-flow duration, highlighting Kentron.", [
    (r'''journey_plot <- ggplot(analysis, aes(x = round_trip_freeflow_minutes / 2, y = price_original,
                                      color = district == "Kentron")) +
  geom_point(alpha = 0.5, size = 1.7) +
  scale_color_manual(values = c("FALSE" = "#25718B", "TRUE" = "#B75F28"),
                     labels = c("Other named Yerevan districts", "Kentron"), name = NULL) +
  scale_y_continuous(labels = label_number(scale = 0.001, suffix = "k")) +
  labs(title = "Rent and modeled road time are only part of the comparison",
       x = "Mean of outward and return free-flow car minutes", y = "Advertised monthly rent (AMD)",
       caption = "OSRM road model, not observed congestion or public-transit time. No causal fit or confidence band.") +
  theme(legend.position = "bottom")
journey_plot
ggsave("outputs/figures/rent-journey.png", journey_plot, width = 9, height = 5.3, dpi = 160)
chunk_results[["rent-and-journey"]] <- sprintf("The plotted mean-leg free-flow estimates range from %.1f to %.1f minutes in the selected sample.",
  min(analysis$round_trip_freeflow_minutes / 2), max(analysis$round_trip_freeflow_minutes / 2))''', "Use actual listing rents and cached route-model outputs. Half the round-trip duration is an average of the two legs, not an assumption that the legs match. Color highlights the central comparator without pooling other districts for estimation.")
], "A scatterplot showing the observed asking-price and modeled-route combinations.",
      "The plot can suggest an association, but does not control dwelling quality or validate peak commuting times. It cannot establish that distance caused a rent reduction.",
      "Even an apparent rent–journey tradeoff needs the cost model to assess whether savings survive.",
      "A scatterplot makes variation visible without implying an unsupported regression or population test.")

chunk("scenario-inputs", "Separate verified tariffs from assumed consumption",
      "Define an explicit winter-month household and time-value benchmark.",
      "Uses official tariff facts while keeping consumption, working hours and travel assumptions visible.", [
    (r'''rates <- setNames(tariffs$value, tariffs$parameter)
wage_2025 <- wages$Value[wages$Year == 2025]
stopifnot(length(wage_2025) == 1)
paid_hours_assumed <- 22 * 8
hourly_benchmark <- wage_2025 / paid_hours_assumed
time_fractions <- c(0, 0.25, 0.5, 1)
half_time_value <- 0.5 * hourly_benchmark
days <- 22
commuters <- 1
utility_parts <- data.frame(component = c("Electricity: 150 day + 50 night kWh", "Gas: 100 m3", "Water: 8 m3"),
  amd = c(150 * rates["electric_day_low"] + 50 * rates["electric_night_low"],
          100 * rates["gas_per_1000m3"] / 1000, 8 * rates["water_per_m3"]))
utilities <- sum(utility_parts$amd)
knitr::kable(utility_parts, digits = 2)''', "Read verified rates, select the2025 gross national wage, and divide it by an assumed176 paid hours. Compute winter electricity/gas/water costs from declared usage. Electricity uses the tariff band for200kWh total, not a progressive first-block calculation."),
    (r'''time_value_table <- data.frame(fraction_of_gross_hourly_benchmark = time_fractions,
                               amd_per_hour = time_fractions * hourly_benchmark)
knitr::kable(time_value_table, digits = 2)
chunk_results[["scenario-inputs"]] <- sprintf("The modeled winter utilities total %s AMD. Armstat's 2025 gross wage is %s AMD/month; the assumed hourly benchmark is %.2f AMD and its half-value is %.2f AMD/hour.",
  money(utilities), money(wage_2025), hourly_benchmark, half_time_value)''', "Show zero, quarter, half and full benchmark values. None is an observed willingness to pay or renter wage; zero time value remains a separate cash-cost comparison.")
], "A modeled utility-cost table and a wage-based time-value scenario table.",
      "Equal consumption makes baseline utility costs equal across districts. That is an assumption, not evidence that bills are geographically equal. The model excludes internet, building fees and other unsupported charges, and represents a winter month rather than an annual average.",
      "This prevents a hidden heating difference from being invented and lets the importance of time depend on explicit assumptions.",
      "Observed unit tariffs and modeled quantities must remain distinguishable so readers can replace assumptions with their own.")

helper_code = (ROOT / "scripts/cost-model.R").read_text(encoding="utf-8")
helper_blocks = [(block, explanation) for block, explanation in zip(helper_code.strip().split("\n\n"), [
    "Choose pay-per-ride or one30-day pass per commuter. Multiply two directions by return-commute days and boardings once. This does not optimize all quarterly or annual ticket products.",
    "Multiply already-summed road kilometres by days, the operating allowance and independent commuters, then add each commuter's assumed destination parking. Zero commuting days incur no modeled parking subscription.",
    "Convert already-round-trip minutes to household monthly hours; the two legs have already been added, so there is no further factor of two.",
    "Add housing/utilities, transport and the optional value of commuting hours. When the time value is zero the last term vanishes exactly.",
    "Calculate a positive time-value crossing only if the comparison is directly cheaper and takes more time. Return missing for other cases so they receive their own interpretation rather than a misleading negative or infinite threshold."
])]
helper_blocks.append((r'''chunk_results[["cost-functions"]] <- "Five small functions define the fare cap, marginal driving cost, monthly hours, generalized cost and positive break-even value."''', "Record which financial operations were defined; these functions do not themselves contain housing observations."))
chunk("cost-functions", "Define the financial calculations", "Translate the economic model into short reusable R functions.",
      "Defines five transparent calculations, using named units and special-case handling.", helper_blocks,
      "Function definitions; numerical behavior is checked later against hand-calculated cases.",
      "Private-car costs are a marginal operating scenario, not depreciation, financing, insurance or an observed fuel bill. Two-commuter car scenarios assume independent journeys/vehicles; shared-car savings are not modeled.",
      "These calculations operationalize both outcomes without double-counting transport or time.",
      "Small named functions keep repeated sensitivity calculations consistent while retaining beginner-readable arithmetic.")

chunk("district-budgets", "Build consistent district budget examples",
      "Compare direct and generalized selected costs under identical household rules.",
      "Applies each mode to the district median inputs and compares every example with the same-mode Kentron example.", [
    (r'''public <- districts %>% mutate(mode = "Public transport",
  transport = transit_cost(days, commuters, 1, rates["fare_single"], rates["fare_30day"]),
  round_trip_minutes = round_trip_km / 12 * 60 + 2 * 15)
car <- districts %>% mutate(mode = "Private car",
  transport = car_cost(round_trip_km, days, commuters, 60, 10000),
  round_trip_minutes = freeflow_minutes * 1.5 + 2 * 5)
budgets <- bind_rows(public, car) %>% mutate(
  hours = monthly_hours(round_trip_minutes, days, commuters),
  direct = rent + utilities + transport,
  generalized_half = generalized_cost(rent, utilities, transport, hours, half_time_value))''', "Construct a public-road-distance scenario at12km/h plus15minutes access/wait per leg, and a car scenario at1.5times free-flow duration plus5minutes per leg. Both use each district's own journeys. The car allowance is60AMD/km plus10000AMD parking per commuter; these values are assumptions."),
    (r'''central <- budgets %>% filter(district == "Kentron") %>%
  select(mode, central_rent = rent, central_transport = transport,
         central_direct = direct, central_hours = hours, central_generalized = generalized_half)
comparisons <- budgets %>% left_join(central, by = "mode") %>% mutate(
  rent_saved = central_rent - rent,
  extra_transport = transport - central_transport,
  direct_difference = direct - central_direct,
  extra_hours = hours - central_hours,
  generalized_difference = generalized_half - central_generalized)
knitr::kable(budgets %>% select(district, mode, rent, transport, hours, direct, generalized_half), digits = 0)
cheaper_half <- comparisons %>% filter(district != "Kentron") %>% group_by(mode) %>%
  summarise(cheaper = sum(generalized_difference < 0), comparisons = n(), .groups = "drop")
chunk_results[["district-budgets"]] <- paste("At half the hourly benchmark, cheaper non-Kentron district examples:",
  paste0(cheaper_half$mode, " ", cheaper_half$cheaper, "/", cheaper_half$comparisons, collapse = "; "), ".")''', "Match central comparisons by mode and calculate rent saved, extra spending and extra hours. These are differences between modeled district examples, not paired moving-household effects. Summarize the executed sign comparisons without a significance test.")
], "A table of district examples for both modes, showing direct and time-valued outcomes separately.",
      "A flat city fare can leave monetary transit spending unchanged even when travel takes longer. The central comparator also has transport costs and time. Medians of rent, road length and road time need not come from the same apartment, so this is not a median observed total budget.",
      "Negative cost differences contradict the strong claim that savings always disappear; positive differences support it only for the stated district example and scenario.",
      "One explicit archetype makes additive cost differences and break-even equations exactly consistent.")

chunk("cost-visuals", "Show costs and the rent-saving tradeoff",
      "Make clear how much of the rent saving is consumed by modeled extra transport and time.",
      "Plots direct versus generalized examples and compares rent saved with extra commuting burden.", [
    (r'''cost_long <- budgets %>% select(district, mode, direct, generalized_half) %>%
  pivot_longer(c(direct, generalized_half), names_to = "outcome", values_to = "amd")
cost_plot <- ggplot(cost_long, aes(x = amd, y = factor(district, levels = district_order), color = outcome)) +
  geom_point(size = 2.4, position = position_dodge(width = 0.35)) +
  facet_wrap(~mode, nrow = 1) +
  scale_color_manual(values = c("direct" = "#25718B", "generalized_half" = "#B75F28"),
    labels = c("Direct selected cost", "Including time at half benchmark"), name = NULL) +
  scale_x_continuous(labels = label_number(scale = 0.001, suffix = "k")) +
  labs(title = "Adding time changes the comparison without changing the rent",
       subtitle = "Modeled district budgets; one commuter, 22 days, equal winter consumption",
       x = "AMD per household per modeled month", y = NULL) + theme(legend.position = "bottom")
cost_plot
ggsave("outputs/figures/modeled-costs.png", cost_plot, width = 10, height = 6.3, dpi = 160)''', "Reshape only the two outcomes into a plotting table; these extra rows are not new observations. Use a separate panel for each transport mode and label both outcomes explicitly."),
    (r'''tradeoff <- comparisons %>% filter(district != "Kentron") %>%
  mutate(extra_commuting = extra_transport + extra_hours * half_time_value)
tradeoff_plot <- ggplot(tradeoff, aes(x = rent_saved, y = extra_commuting, color = mode)) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "grey45") +
  geom_point(size = 2.5) +
  scale_color_manual(values = c("Private car" = "#B75F28", "Public transport" = "#25718B")) +
  scale_x_continuous(labels = label_number(scale = 0.001, suffix = "k")) +
  scale_y_continuous(labels = label_number(scale = 0.001, suffix = "k")) +
  coord_equal(xlim = c(0, 165000), ylim = c(0, 165000)) +
  labs(title = "Below the dashed line, rent savings exceed extra commuting burden",
       subtitle = "Time valued at half the gross hourly benchmark; utility consumption held equal",
       x = "Rent saved relative to Kentron (AMD/month)", y = "Extra transport + valued time (AMD/month)", color = NULL,
       caption = "Each point is a named district–mode example; see the preceding table for names and values.") +
  theme(legend.position = "bottom")
tradeoff_plot
ggsave("outputs/figures/savings-tradeoff.png", tradeoff_plot, width = 10, height = 6.1, dpi = 160)
chunk_results[["cost-visuals"]] <- sprintf("The tradeoff chart contains %s named district–mode examples; %s lie below the equality line at the half-benchmark time value.",
  nrow(tradeoff), sum(tradeoff$extra_commuting < tradeoff$rent_saved))''', "The equality line is an algebraic reference, not a fitted trend. Below it, rent saving exceeds extra transport and valued time. Equal axes preserve an honest visual comparison; the preceding district table identifies every point without overlapping text labels.")
], "Two complementary figures: budget levels and saving-versus-extra-cost comparisons.",
      "The dashed line explains the model's decision rule. It does not estimate a causal relationship. A point below the line can still reverse under a larger time value, greater heating use or different commuting assumptions.",
      "These charts directly assess the conditional hidden-cost claim and show which component changes the answer.",
      "Use budget levels and one explicit equality comparison instead of redundant bar charts.")

chunk("break-even", "Calculate conditional time-value thresholds",
      "Find where the district example stops being cheaper as commuting time becomes more valuable.",
      "Computes positive break-even values and plots cost differences across a continuous time-value range.", [
    (r'''thresholds <- comparisons %>% filter(district != "Kentron") %>% mutate(
  value_of_time_threshold = break_even_value(direct_difference, extra_hours),
  threshold_status = case_when(
    direct_difference >= 0 & extra_hours >= 0 ~ "No saving at zero time value",
    direct_difference < 0 & extra_hours <= 0 ~ "Cheaper for all nonnegative time values",
    direct_difference >= 0 & extra_hours < 0 ~ "May become cheaper as time value rises",
    TRUE ~ "Positive break-even time value"))
knitr::kable(thresholds %>% select(district, mode, direct_difference, extra_hours,
                                  value_of_time_threshold, threshold_status), digits = 1)
curve <- merge(comparisons %>% filter(district != "Kentron"),
               data.frame(time_value = seq(0, 10000, by = 100)), by = NULL) %>%
  mutate(cost_difference = direct_difference + extra_hours * time_value)''', "Use the exact direct-cost difference and extra household hours from the same archetype. Missing thresholds are interpreted by direction of costs/time, rather than displayed as misleading negative or infinite solutions. The plotted 0–10000 AMD/hour range is a scenario axis, not an observed wage distribution."),
    (r'''threshold_plot <- ggplot(curve, aes(x = time_value, y = cost_difference, color = district)) +
  geom_hline(yintercept = 0, linetype = "dashed") + geom_line(linewidth = 0.7) +
  facet_wrap(~mode, nrow = 1) +
  scale_color_viridis_d(option = "turbo", end = 0.9) +
  scale_y_continuous(labels = label_number(scale = 0.001, suffix = "k")) +
  labs(title = "A break-even value is conditional on the household and mode",
       subtitle = "Negative difference means cheaper than the same-mode Kentron example",
       x = "Assumed value of commuting time (AMD/hour)", y = "Cost difference from Kentron (AMD/month)", color = "District") +
  theme(legend.position = "bottom", legend.text = element_text(size = 8))
threshold_plot
ggsave("outputs/figures/time-thresholds.png", threshold_plot, width = 11, height = 6.5, dpi = 160)
finite_thresholds <- thresholds$value_of_time_threshold[is.finite(thresholds$value_of_time_threshold)]
chunk_results[["break-even"]] <- if (length(finite_thresholds)) sprintf("%s examples have a positive time-value threshold; the smallest is %.0f AMD/hour. Other examples require their stated special-case interpretation.",
  length(finite_thresholds), min(finite_thresholds)) else "No positive threshold exists for the selected examples under the baseline model."''', "Plot each named comparison as its own line. The crossing is a model threshold under fixed other costs; no citywide distance threshold is inferred. Save exactly the plotted figure.")
], "A threshold table and a cost-difference curve, including no-crossing cases.",
      "Time value, not physical distance alone, determines these crossings. Car costs and journeys vary together, so a universal kilometre threshold is unsupported. A threshold outside the plotted range still exists algebraically when the table reports it.",
      "This identifies when the hidden-cost claim can become true under changed preferences rather than presuming one answer for every household.",
      "A simple additive model permits an exact, understandable break-even equation without statistical theatre.")

chunk("sensitivity", "Vary household, heating and travel assumptions",
      "Check whether the conclusion depends on a narrow choice of assumptions.",
      "Builds household/wage/heating scenarios and separately changes transit access, transfers and driving costs.", [
    (r'''scenario_grid <- expand.grid(commuters = c(1, 2), days = c(16, 22, 26),
  fraction = time_fractions, extra_gas = c(0, 75, 150))
scenario_rows <- merge(budgets %>% select(district, mode, rent, round_trip_km, freeflow_minutes),
                       scenario_grid, by = NULL) %>% mutate(
  transport = ifelse(mode == "Public transport",
    transit_cost(days, commuters, 1, rates["fare_single"], rates["fare_30day"]),
    car_cost(round_trip_km, days, commuters, 60, 10000)),
  minutes = ifelse(mode == "Public transport", round_trip_km / 12 * 60 + 30, freeflow_minutes * 1.5 + 10),
  hours = monthly_hours(minutes, days, commuters),
  utility_scenario = utilities + ifelse(district == "Kentron", 0, extra_gas * rates["gas_per_1000m3"] / 1000),
  total = rent + utility_scenario + transport + hours * fraction * hourly_benchmark)
scenario_central <- scenario_rows %>% filter(district == "Kentron") %>%
  select(mode, commuters, days, fraction, extra_gas, reference_total = total)
scenario_rows <- scenario_rows %>% left_join(scenario_central,
  by = c("mode", "commuters", "days", "fraction", "extra_gas")) %>% mutate(delta = total - reference_total)''', "Cross declared assumptions, not sampled households. Extra gas is imposed only on noncentral examples as a stress test, not estimated from district location. Match each example to Kentron with exactly the same mode/household/time assumptions."),
    (r'''stress <- scenario_rows %>% filter(commuters == 2, days == 26, extra_gas == 150, district != "Kentron")
stress_plot <- ggplot(stress, aes(x = factor(fraction, levels = time_fractions),
  y = factor(district, levels = district_order), fill = delta)) +
  geom_tile(color = "white") +
  geom_text(aes(label = round(delta / 1000), color = delta < -90000), size = 3) +
  scale_color_manual(values = c("FALSE" = "black", "TRUE" = "white"), guide = "none") +
  facet_wrap(~mode, nrow = 1) +
  scale_fill_gradient2(low = "#246A82", mid = "#F5F4EF", high = "#B55B32", midpoint = 0,
                       limits = c(-150000, 150000), breaks = c(-150000, 0, 150000),
                       labels = label_number(scale = 0.001, suffix = "k")) +
  labs(title = "A two-commuter winter stress can change the answer",
       subtitle = "26 days; +150 m³ gas outside Kentron; cell values are AMD thousands",
       x = "Fraction of gross hourly wage benchmark", y = NULL, fill = "Difference") +
  theme(legend.position = "bottom")
stress_plot
ggsave("outputs/figures/sensitivity.png", stress_plot, width = 10, height = 6.4, dpi = 160)''', "Display one explicit stress slice, with a diverging color scale centered at zero. The cells are modeled differences, not probabilities or independent observations. Negative cells indicate a cheaper district example."),
    (r'''travel_grid <- data.frame(travel_case = c("Faster", "Baseline", "Slower"),
  public_speed = c(16, 12, 8), wait_per_leg = c(10, 15, 20),
  congestion = c(1, 1.5, 2), car_per_km = c(40, 60, 100))
travel_sensitivity <- merge(budgets %>% select(district, mode, rent, round_trip_km, freeflow_minutes),
                            travel_grid, by = NULL) %>% mutate(
  minutes = ifelse(mode == "Public transport", round_trip_km / public_speed * 60 + 2 * wait_per_leg,
                   freeflow_minutes * congestion + 10),
  transport = ifelse(mode == "Public transport", transit_cost(22, 1, 1, rates["fare_single"], rates["fare_30day"]),
                    car_cost(round_trip_km, 22, 1, car_per_km, 10000)),
  total = rent + utilities + transport + monthly_hours(minutes, 22, 1) * half_time_value)
travel_central <- travel_sensitivity %>% filter(district == "Kentron") %>%
  select(mode, travel_case, central_total = total)
travel_sensitivity <- travel_sensitivity %>% left_join(travel_central, by = c("mode", "travel_case")) %>%
  mutate(delta = total - central_total)
transfer_test <- comparisons %>% filter(mode == "Public transport", district != "Kentron") %>%
  mutate(two_boarding_delta = direct_difference + transit_cost(22, 1, 2, rates["fare_single"], rates["fare_30day"]) -
           transit_cost(22, 1, 1, rates["fare_single"], rates["fare_30day"]) + extra_hours * half_time_value)
commitment_pass_month <- rates["fare_365day"] / 12
dearer_grid <- sum(scenario_rows$delta[scenario_rows$district != "Kentron"] > 0)
chunk_results[["sensitivity"]] <- sprintf("Computed %s household/heating/time scenario rows and %s travel-sensitivity rows; %s noncentral grid rows are dearer than Kentron. This grid count is not a probability. Two boardings cost %s AMD per commuter under the 30-day rule; the annual pass amortizes to %s AMD/month but requires a different commitment.",
  nrow(scenario_rows), nrow(travel_sensitivity), dearer_grid, money(transit_cost(22, 1, 2, rates["fare_single"], rates["fare_30day"])), money(commitment_pass_month))''', "Check paired fast/base/slow road-based travel assumptions and car allowances. Separately test two boardings outside Kentron, with the central comparator kept at one, so a flat fare does not silently hide transfer spending. Annual-pass amortization is reported separately because paying yearly is not the same30-day purchasing strategy.")
], "A sensitivity heatmap and retained scenario/travel tables, without interpreting grid size as sample size.",
      "The grid exposes dependence on time, workers and heating. It does not assign probabilities to scenarios. Two-car cases assume separate commuting vehicles; shared rides could lower costs. Real traffic, timetables, taxi fares, social discounts and every possible household are not observed or exhaustively modeled.",
      "A finding that reverses in plausible scenarios supports a conditional recommendation; it cannot justify a universal claim about peripheral living.",
      "Separate uncertainty in assumptions from variation between rental ads; neither is a manufactured sampling confidence interval.")

chunk("robustness", "Check aggregation and the narrower area band",
      "Assess whether a different summary construction changes the comparison.",
      "Calculates listing-level modeled totals as an alternative summary and reports rent-only summaries for a narrower area band.", [
    (r'''individual_public <- analysis %>% mutate(mode = "Public transport",
  modeled_transport = transit_cost(22, 1, 1, rates["fare_single"], rates["fare_30day"]),
  modeled_minutes = round_trip_km / 12 * 60 + 30)
individual_car <- analysis %>% mutate(mode = "Private car",
  modeled_transport = car_cost(round_trip_km, 22, 1, 60, 10000),
  modeled_minutes = round_trip_freeflow_minutes * 1.5 + 10)
individual_totals <- bind_rows(individual_public, individual_car) %>% mutate(
  modeled_total = price_original + utilities + modeled_transport +
    monthly_hours(modeled_minutes, 22, 1) * half_time_value)
alternative <- individual_totals %>% group_by(district, mode) %>%
  summarise(median_listing_model_total = median(modeled_total), .groups = "drop")
alternative_central <- alternative %>% filter(district == "Kentron") %>%
  select(mode, alternative_central = median_listing_model_total)
aggregation_check <- alternative %>% left_join(alternative_central, by = "mode") %>%
  mutate(alternative_difference = median_listing_model_total - alternative_central) %>%
  left_join(comparisons %>% select(district, mode, generalized_difference), by = c("district", "mode")) %>%
  mutate(sign_changed = sign(alternative_difference) != sign(generalized_difference))
knitr::kable(aggregation_check %>% filter(district != "Kentron") %>%
  select(district, mode, generalized_difference, alternative_difference, sign_changed), digits = 0)''', "Calculate a modeled total for each advertisement before taking its district median. Compare the sign with the primary median-input archetype. These totals are still hypothetical budgets, not observed household bills; the exercise tests aggregation sensitivity."),
    (r'''narrow_area <- analysis %>% filter(area_m2 >= 55, area_m2 <= 65) %>% group_by(district) %>%
  summarise(n = n(), median_rent = median(price_original), .groups = "drop")
knitr::kable(narrow_area, digits = 0)
chunk_results[["robustness"]] <- sprintf("Changing to medians of listing-level modeled totals changes %s noncentral mode-comparison signs. The 55–65 m² rent-only subset contains %s listings; its counts differ from the primary sample.",
  sum(aggregation_check$sign_changed[aggregation_check$district != "Kentron"]), sum(narrow_area$n))''', "Show a narrower55–65m² rent-only check with its own counts. Do not silently substitute these rents into the primary budget or imply that absent/very small districts have reliable estimates.")
], "An aggregation-sensitivity table and a clearly separate narrower-band rent table.",
      "If signs remain unchanged, that supports stability to this particular summary choice, not robustness to unobserved renovation, agency selection or real congestion. A narrow size band can greatly reduce district support.",
      "This checks whether the conditional finding is an artifact of one aggregation rule while acknowledging remaining confounding.",
      "A direct alternative-summary check is more honest than attaching unjustified inferential precision to convenience data.")

chunk("validation", "Verify formulas and study boundaries",
      "Ensure reported conclusions follow from executed calculations.",
      "Runs hand-calculated cost checks, algebraic identities, sample checks and break-even substitution.", [
    (r'''stopifnot(transit_cost(22, 1, 1, 150, 9000) == 6600)
stopifnot(transit_cost(22, 1, 2, 150, 9000) == 9000)
stopifnot(car_cost(10, 22, 1, 60, 10000) == 23200)
stopifnot(monthly_hours(60, 22, 1) == 22)
stopifnot(isTRUE(all.equal(utilities, 24769.36)))
stopifnot(all(generalized_cost(budgets$rent, utilities, budgets$transport, budgets$hours, 0) == budgets$direct))
stopifnot(all(abs(comparisons$direct_difference - (-comparisons$rent_saved + comparisons$extra_transport)) < 0.000001))
positive_crossings <- thresholds %>% filter(is.finite(value_of_time_threshold))
stopifnot(all(abs(positive_crossings$direct_difference +
                   positive_crossings$extra_hours * positive_crossings$value_of_time_threshold) < 0.000001))''', "Check literal hand-derived examples, the winter utility sum, the zero-time identity, the rent-saving identity, and zero generalized difference at each positive crossing. A small numerical tolerance handles floating-point arithmetic."),
    (r'''stopifnot(all(analysis$currency_original == "AMD"), all(analysis$rooms == 2),
          all(between(analysis$area_m2, 45, 75)), all(flag(analysis$furniture_feature_present)),
          !any(analysis$listing_id %in% c("11834", "14196", "12868", "10570")))
stopifnot(all(is.finite(budgets$direct)), all(budgets$hours >= 0))
chunk_results[["validation"]] <- "All executed sample, fare, utility, zero-time, additive-cost and positive-crossing checks passed. These checks do not validate source representativeness or unobserved quality."''', "Ensure excluded IDs remain excluded and every primary observation obeys the declared selection rule. Only claim these executed checks passed; they do not certify the website's coordinates or all economic assumptions.")
], "Execution continues only if all stated checks pass; otherwise rendering stops.",
      "Numerical correctness and scientific validity are different. Correct arithmetic cannot repair a nonrepresentative sample or turn modeled utility use into observed spending. Independent QA also checks the source/code/document correspondence.",
      "This protects the link between evidence and conclusions without claiming more validity than the study design permits.",
      "Hand-derived examples and algebraic invariants can catch double-counting and unit mistakes with no additional test packages.")

references = [
    dict(title="WSE.AM rental catalogue and public property API", publisher="WSE.AM", date="Snapshot 2026-11-05", url="https://wse.am/en/apartments-for-rent-yerevan", accessed="2026-11-05"),
    dict(title="Public property API access rules", publisher="WSE.AM", date="Accessed 2026-11-05", url="https://wse.am/robots.txt", accessed="2026-11-05"),
    dict(title="Unified public transport ticket comparison", publisher="Yerevan Municipality", date="2025 onward", url="https://transport.yerevan.am/", accessed="2026-11-05"),
    dict(title="Household electricity tariffs", publisher="Electric Networks of Armenia", date="2022 rates with 2025 amendments", url="https://www.ena.am/Info.aspx?id=11&lang=2", accessed="2026-11-05"),
    dict(title="Natural gas tariff decision", publisher="Public Services Regulatory Commission", date="2022-03-01", url="https://www.psrc.am/contents/newsPress/gas-tariff-22", accessed="2026-11-05"),
    dict(title="Resident gas tariffs unchanged from August 2026", publisher="Public Services Regulatory Commission", date="2026", url="https://psrc.am/contents/page/posts/natural-gas-tariffs-for-residents-will-stay-unchanged", accessed="2026-11-05"),
    dict(title="2026 drinking water tariff", publisher="Veolia Djur", date="2025-11-26", url="https://www.veolia.am/en/news/2026-drinking-water-tariff-consumers-will-not-increase", accessed="2026-11-05"),
    dict(title="Water tariff units and metering FAQ", publisher="Veolia Djur", date="2025 tariff description", url="https://www.veolia.am/en/consumers/frequently-asked-questions", accessed="2026-11-05"),
    dict(title="SDG8.5.1.a average monthly nominal wages and metadata", publisher="Armstat", date="Data updated 2026-06-10; observation 2025", url="https://sdg.armstat.am/8-5-1-a-iframe/", accessed="2026-11-05"),
    dict(title="OSRM HTTP API table service", publisher="Project OSRM", date="v26.5.0 documentation", url="https://project-osrm.org/docs/v26.5.0/http", accessed="2026-11-05"),
    dict(title="OpenStreetMap data attribution and license", publisher="OpenStreetMap contributors", date="Accessed 2026-11-05", url="https://www.openstreetmap.org/copyright", accessed="2026-11-05"),
    dict(title="DS116 lecture materials", publisher="Habet Madoyan, American University of Armenia", date="Repository commit 1a74f34584c85b08b0f9a87d055b663d209df9de", url="https://github.com/ReneViva/DS116-Data-Visualization/tree/1a74f34584c85b08b0f9a87d055b663d209df9de", accessed="2026-11-05"),
    dict(title="ggplot2 reference", publisher="ggplot2 authors", date="Installed version recorded in report", url="https://ggplot2.tidyverse.org/reference/", accessed="2026-11-05"),
    dict(title="dplyr reference", publisher="dplyr authors", date="Installed version recorded in report", url="https://dplyr.tidyverse.org/reference/", accessed="2026-11-05"),
    dict(title="knitr documentation", publisher="Yihui Xie and contributors", date="Installed version recorded in report", url="https://yihui.org/knitr/", accessed="2026-11-05"),
]
(ROOT / "references/reference-list.json").write_text(json.dumps(references, indent=2), encoding="utf-8")

chunk("export-results", "Save the executed results and provenance",
      "Keep the Word companion and final conclusions tied to this exact executed analysis.",
      "Exports tables, actual-result narratives, references and environment information for verification and documentation.", [
    (r'''write.csv(districts, "outputs/district-summary.csv", row.names = FALSE)
write.csv(sample_flow, "outputs/sample-flow.csv", row.names = FALSE)
write.csv(route_audit, "outputs/route-audit.csv", row.names = FALSE, fileEncoding = "UTF-8")
write.csv(comparisons, "outputs/baseline-comparisons.csv", row.names = FALSE)
write.csv(thresholds, "outputs/break-even.csv", row.names = FALSE)
write.csv(scenario_rows, "outputs/sensitivity.csv", row.names = FALSE)
write.csv(travel_sensitivity, "outputs/travel-sensitivity.csv", row.names = FALSE)
write.csv(aggregation_check, "outputs/aggregation-check.csv", row.names = FALSE)
write.csv(narrow_area, "outputs/narrow-area-rents.csv", row.names = FALSE)
write.csv(transfer_test, "outputs/transfer-sensitivity.csv", row.names = FALSE)
capture.output(sessionInfo(), file = "outputs/session-info.txt")
chunk_results[["export-results"]] <- "Saved the executed summary, exclusion-flow, baseline, threshold, sensitivity and robustness tables, package session information, and matching Word-companion result narratives."''', "Write supporting results with row names disabled so no artificial observation column is introduced. These are supporting reproducibility files, not extra principal deliverables. Record the actual R session."),
    (r'''results <- list(chunks = chunk_results,
  summary = list(sample_n = nrow(analysis), districts_n = nrow(districts),
    kentron_rent_amd = central_rent, modeled_winter_utilities_amd = utilities,
    wage_2025_gross_amd = wage_2025, hourly_benchmark_amd = hourly_benchmark,
    half_time_value_amd = half_time_value, cheaper_half = cheaper_half,
    dearer_scenario_rows = dearer_grid,
    aggregation_sign_changes = sum(aggregation_check$sign_changed[aggregation_check$district != "Kentron"]),
    sample_kind = "Single-agency convenience advertisements; not representative households",
    cost_kind = "Modeled district budgets built from sample medians and declared assumptions",
    p_values = "Not estimated: intended population inference unsupported",
    confidence_intervals = "Not estimated; IQRs describe observed listing spread"),
  references = jsonlite::fromJSON("references/reference-list.json", simplifyVector = FALSE),
  software = software, package_build_warnings = setup_warnings)
jsonlite::write_json(results, "outputs/results.json", pretty = TRUE, auto_unbox = TRUE)
knitr::kable(cheaper_half)''', "Export actual values and per-chunk narratives for the code companion. Explicitly state why p-values and population intervals were not estimated; no missing significance result is replaced with a fabricated one.")
], "Supporting CSV/JSON/session files and a final conditional sign-count table.",
      "The Word builder reads these executed narratives and extracts the code from this Rmd, reducing the chance of mismatched values or chunk names. Re-render this analysis before rebuilding the companion after any substantive change.",
      "This preserves an auditable path from source records through calculations to the stated conclusion.",
      "Use one executed source of results and one source of chunk code rather than manually maintaining conflicting documents.")

parts.append(r'''
## Statistical interpretation

No population p-values or confidence intervals are reported. The advertised
properties were not randomly sampled from Yerevan's rental stock, source IDs do
not establish independent dwellings, and most cost inputs are modeled. Repeating
a property across modes or time values creates scenarios, not additional data.
The boxplot IQR is observed listing spread, not uncertainty about a population
median. A bootstrap of this agency catalogue would not remove its selection bias.

If a representative, independently sampled dataset became available, the analysis
would need an explicit estimand and sampling/clustering design before selecting
a test. A p-value would measure incompatibility with that model's null, not the
probability that the hypothesis is true. A95% confidence interval would describe
a procedure's long-run coverage under its assumptions, not a95% chance that a
fixed parameter lies in the computed interval. Statistical significance would
not establish a practically important or causal effect. Here, model differences
and sensitivity checks answer the defensible descriptive question.

## Conditional conclusions and recommendations

The executed comparison at half the gross hourly benchmark is:

`r paste0(cheaper_half$mode, ": ", cheaper_half$cheaper, " of ", cheaper_half$comparisons, " non-Kentron district examples are cheaper than Kentron.", collapse = " ")`

This applies to **one commuter,22 commuting days, the stated winter consumption
and travel assumptions, and this agency's selected advertisements**. It does not
mean that the same number of districts is cheaper for every renter or that any
district is statistically proven cheaper. Direct and generalized costs must be
read separately; the zero-time scenario remains the direct selected-cost outcome.

At the baseline settings, the lowest modeled generalized example is
`r budgets$district[budgets$mode == "Public transport"][which.min(budgets$generalized_half[budgets$mode == "Public transport"])]`
for public transport and
`r budgets$district[budgets$mode == "Private car"][which.min(budgets$generalized_half[budgets$mode == "Private car"])]`
for private car. These are conditional example rankings, not guaranteed available
apartments or a citywide optimal-location recommendation. Sparse districts deserve
particular caution.

`r if (all(cheaper_half$cheaper == cheaper_half$comparisons)) "The baseline model does not support the blanket claim that lower noncentral rents are necessarily erased by the selected extra costs." else "The baseline model gives a conditional mixture of cheaper and dearer district examples."`
In the chosen household/heating/time grid, `r dearer_grid` noncentral rows reverse
to a higher cost than Kentron. This count describes the chosen grid, not the
likelihood that a household will face higher costs. The sensitivity figure shows
the specified two-commuter winter stress comparison.

A household can use the comparison by obtaining an actual rent quote, checking
the condition and heating system, timing its own outward and return commute,
and replacing our assumptions with its own fare/pass choice, driving costs and
time value. Lower rent is financially advantageous when it exceeds the extra
cash costs; it remains advantageous in generalized terms only when it also
compensates for the household's value of additional time. The break-even table
and sensitivity chart show where that conditional answer can reverse.

## Limitations

- One agency's active catalogue is a convenience snapshot. It may overrepresent
  certain prices, districts, building types or clients. Asking rent is not agreed
  rent; creation date is not a known price-update date, and active ads can have
  future or restricted availability.
- Furniture is advertised, renovation is unstandardized, and building details
  are incomplete. Area differences remain inside the size band. Neither narrow
  filtering nor the robustness checks makes this a causal or quality-adjusted
  estimate.
- District tags and coordinates may be approximate. Known placeholders, explicit
  town mismatches and ambiguous border cases were removed; remaining points were
  not ground-truthed. Public road routes use OpenStreetMap contributors' data,
  with cached OSRM model outputs, not live congestion or a transit timetable.
- Winter consumption, access/waiting, congestion, marginal car costs and time
  values are assumptions. Full car ownership, shared-car commuting, actual taxi
  fares, summer/annual-average energy use and unsupported budget components are
  outside the model. Longer ticket commitments and eligible discounts can differ.
- The2025 national gross wage is a benchmark, not a2026 personal net wage.
  Heating stress is not a measured geographic effect. No universal distance
  threshold, municipality-external comparison, or population significance claim
  is supported.
- Changing the aggregation to medians of listing-level modeled totals changed
  `r sum(aggregation_check$sign_changed[aggregation_check$district != "Kentron"])`
  comparison signs; this is one limited robustness check, not complete immunity
  to bias or changed assumptions.

## Reproducibility and academic transparency

The main source is this single Rmd. Supporting data, acquisition scripts, source
metadata, frozen route replies, output tables and validation records remain in
the project. A separate Word companion explains the same chunks and exact code.
The report does not require a live website connection to re-run.

This work used Codex for source discovery, code, analysis explanations, and
verification, with independent methodological and QA reviews. Sources and all
numerical statements must be checked, and the student should independently
understand and explain the work. The repository's lecture examples do not
establish the instructor's AI policy or this project's submission rubric; those
remain to be confirmed before submission. The course's familiar ggplot2/dplyr
patterns guide the code; advanced methods were not added solely for appearance.

Existing package-build warnings recorded in this run:

`r if (length(setup_warnings)) paste(unique(setup_warnings), collapse = "; ") else "None captured."`

## References

''')
for ref in references:
    parts.append(f'- {ref["publisher"]}. {ref["date"]}. [{ref["title"]}]({ref["url"]}). Accessed {ref["accessed"]}.\n')
parts.append("\nR package versions are listed in the setup table; full session details are saved in outputs/session-info.txt.\n")
# Improve prose spacing without changing any executable code or line references.
replacements = {"A95%": "A 95%", "a95%": "a 95%", "The2025": "The 2025",
                "a2026": "a 2026", "a2025": "a 2025", "commuter,22": "commuter, 22"}
def normalize_prose(text):
    text = re.sub(r"\b(the|The|assumed|for|within|one|same|at|plus|is|narrower|ID)(?=\d)", r"\1 ", text)
    return re.sub(r"(\d)(?=(?:AMD|kWh|km|m²|m3|m³|minutes|hours)\b)", r"\1 ", text)

report = "\n".join(parts)
for old, new in replacements.items():
    report = report.replace(old, new)
in_code = False
report_lines = []
for line in report.splitlines():
    if line.startswith("```"):
        in_code = not in_code
    report_lines.append(line if in_code or line.startswith("```") else normalize_prose(line))
report = "\n".join(report_lines) + "\n"
for guide in guides:
    for field in ("objective", "what", "why", "expected", "interpretation", "hypothesis"):
        for old, new in replacements.items():
            guide[field] = guide[field].replace(old, new)
        guide[field] = normalize_prose(guide[field])
    for block in guide["blocks"]:
        block["explanation"] = normalize_prose(block["explanation"])
(ROOT / "Yerevan_Housing_Research.Rmd").write_text(report, encoding="utf-8")
(ROOT / "references/chunk-guide.json").write_text(json.dumps(guides, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Authored one main Rmd and {len(guides)} matching chunk guides.")
