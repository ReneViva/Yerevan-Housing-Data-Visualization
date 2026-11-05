# Development verification only; the main Rmd does not source this file.
options(warn = 1)
report <- new.env()
rmarkdown::render("Yerevan_Housing_Research.Rmd", output_format = "html_document",
  output_dir = "outputs", intermediates_dir = tempdir(), envir = report,
  encoding = "UTF-8", quiet = TRUE)
rmarkdown::render("Yerevan_Housing_Research.Rmd", output_format = "pdf_document",
  output_dir = "outputs", intermediates_dir = tempdir(), envir = new.env(),
  encoding = "UTF-8", quiet = TRUE)

old <- read.csv("_archive/previous-version/outputs/baseline-comparisons.csv")
check <- merge(report$comparisons, old, by = c("district", "mode"))
stopifnot(nrow(check) == 22)
stopifnot(all(abs(check$direct.x - check$direct.y) < 0.000001))
stopifnot(all(abs(check$with_time - check$generalized_half) < 0.000001))
stopifnot(all(abs(check$saving + check$generalized_difference) < 0.000001))
old_threshold <- read.csv("_archive/previous-version/outputs/break-even.csv")
check_threshold <- merge(report$thresholds, old_threshold, by = c("district", "mode"))
stopifnot(all(abs(check_threshold$break_even - check_threshold$value_of_time_threshold) < 0.000001))
old_scenarios <- read.csv("_archive/previous-version/outputs/sensitivity.csv")
new_scenarios <- report$scenarios
names(new_scenarios)[names(new_scenarios) == "workers"] <- "commuters"
names(new_scenarios)[names(new_scenarios) == "workdays"] <- "days"
check_grid <- merge(new_scenarios, old_scenarios,
  by = c("district", "mode", "commuters", "days", "fraction", "extra_gas"))
stopifnot(nrow(check_grid) == 1584, all(abs(check_grid$saving + check_grid$delta) < 0.000001))

chunks <- list(
  prepare = sprintf("Loaded four CSVs: %s cleaned advertisements, %s tariff facts, %s wage years and %s source entries.",
    nrow(report$rentals), nrow(report$tariffs), nrow(report$wages), nrow(report$sources)),
  rent = sprintf("The sample has %s districts. Kentron's median is %s AMD; the other district medians range from %s to %s AMD.",
    nrow(report$districts), report$districts$rent[report$districts$district == "Kentron"],
    min(report$districts$rent), max(report$districts$rent[report$districts$district != "Kentron"])),
  commute = sprintf("The modeled one-way times range from %.1f to %.1f minutes across the district–mode examples. These are scenario estimates, not observed commutes.",
    min(report$travel$trip_minutes / 2), max(report$travel$trip_minutes / 2)),
  budgets = sprintf("Winter utilities total %.2f AMD. The half-wage time value is %.2f AMD/hour. The stacked chart contains 22 modeled district–mode cash budgets.",
    report$utilities, report$time_value),
  savings = sprintf("All %s noncentral district–mode examples remain cheaper than Kentron; monthly savings range from %.0f to %.0f AMD. The waterfall follows %s: %.0f AMD left for the car example and %.0f AMD for public transport.",
    report$cheaper, min(report$noncentral$saving), max(report$noncentral$saving),
    report$focus_district, report$focus$saving[report$focus$mode == "Private car"],
    report$focus$saving[report$focus$mode == "Public transport"]),
  stress = sprintf("The complete grid contains %s scenario rows. Exactly %s noncentral rows become more expensive; this is a grid count, not a probability. The displayed heavy-winter slice has one negative-saving cell.",
    nrow(report$scenarios), report$reversals),
  threshold = sprintf("All 20 examples have positive time-value thresholds. The lowest is %.0f AMD/hour, compared with the gross benchmark of %.0f AMD/hour.",
    report$lowest_threshold, report$hourly),
  checks = "The 276-row sample, unique IDs, room/area limits, utility sum, direct-cost identity and break-even substitution all passed. Separate verification also matched every baseline and sensitivity result against the archived version.",
  references = sprintf("Printed %s source entries read from data/sources.csv. Dataset and model sources are retained with dates and links.", nrow(report$sources)))
jsonlite::write_json(list(chunks = chunks,
  summary = list(sample_n = nrow(report$rentals), district_n = nrow(report$districts),
    utilities = report$utilities, half_time_value = report$time_value,
    cheaper_examples = report$cheaper, reversal_rows = report$reversals),
  budgets = report$comparisons, thresholds = report$thresholds),
  "_archive/revision-checks/results.json", pretty = TRUE, auto_unbox = TRUE)
cat("PASS: HTML and PDF rendered; 22 budgets, 20 thresholds and 1584 scenario rows match the previous version.\n")
