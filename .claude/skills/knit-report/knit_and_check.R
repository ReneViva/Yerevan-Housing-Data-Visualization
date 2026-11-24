# Knit the report and write executed results for the Word companion.
# Usage (from a folder holding the Rmd and data/):
#   Rscript --vanilla knit_and_check.R <project-root> <results.json>
args <- commandArgs(trailingOnly = TRUE)
root <- normalizePath(args[1], winslash = "/")
results_path <- args[2]
if (.Platform$OS.type == "windows") invisible(Sys.setlocale("LC_CTYPE", "English_United States.utf8"))
options(tinytex.install_packages = FALSE, warn = 1)

# Render both formats; the HTML run keeps its objects for checking.
report <- new.env()
rmarkdown::render("Yerevan_Housing_Research.Rmd", output_format = "html_document",
  output_dir = "outputs", envir = report, encoding = "UTF-8", quiet = TRUE)
# LaTeX must run next to figures/, so render the PDF here and then move it.
pdf <- rmarkdown::render("Yerevan_Housing_Research.Rmd", output_format = "pdf_document",
  envir = new.env(), encoding = "UTF-8", quiet = TRUE)
stopifnot(file.copy(pdf, "outputs/Yerevan_Housing_Research.pdf", overwrite = TRUE))
invisible(file.remove(pdf))
r <- report

# ---- Internal checks (moved here from the student Rmd) ----
stopifnot(nrow(r$rentals) == 276, !anyDuplicated(r$rentals$listing_id))
stopifnot(all(r$rentals$rooms == 2), all(r$rentals$area_m2 >= 45 & r$rentals$area_m2 <= 75))
stopifnot(isTRUE(all.equal(as.numeric(r$utilities), 24769.36)))
stopifnot(all(abs(r$budgets$direct - (r$budgets$rent + r$utilities + r$budgets$transport)) < 1e-6))
stopifnot(all(abs(r$noncentral$direct_difference +
  r$noncentral$extra_hours * r$thresholds$break_even) < 1e-6, na.rm = TRUE))

# ---- Archived baseline (approved analysis of 5-6 Nov 2026) ----
# Public transport did not change, so its rows must match exactly.
# Car time changed on purpose (shared traffic model, 24 Nov 2026); taxi is new.
arch <- function(f) read.csv(file.path(root, "_archive/previous-version/outputs", f))
pt <- "Public transport"
check <- merge(r$comparisons[r$comparisons$mode == pt, ], arch("baseline-comparisons.csv"),
  by = c("district", "mode"))
stopifnot(nrow(check) == 11)
stopifnot(all(abs(check$direct.x - check$direct.y) < 1e-6))
stopifnot(all(abs(check$with_time - check$generalized_half) < 1e-6))
stopifnot(all(abs(check$saving + check$generalized_difference) < 1e-6))
check_threshold <- merge(r$thresholds[r$thresholds$mode == pt, ], arch("break-even.csv"),
  by = c("district", "mode"))
stopifnot(nrow(check_threshold) == 10)
stopifnot(all(abs(check_threshold$break_even - check_threshold$value_of_time_threshold) < 1e-6))
new_scenarios <- r$scenarios[r$scenarios$mode == pt, ]
names(new_scenarios)[names(new_scenarios) == "workers"] <- "commuters"
names(new_scenarios)[names(new_scenarios) == "workdays"] <- "days"
check_grid <- merge(new_scenarios, arch("sensitivity.csv"),
  by = c("district", "mode", "commuters", "days", "fraction", "extra_gas"))
stopifnot(nrow(check_grid) == 792, all(abs(check_grid$saving + check_grid$delta) < 1e-6))
stopifnot(nrow(r$scenarios) == 2376, nrow(r$budgets) == 33)

# ---- Hand calculation of car and taxi, straight from the CSVs ----
raw <- read.csv("data/rentals.csv")
tx  <- read.csv("data/taxi_tariffs.csv")
sc  <- read.csv("data/traffic_score_weekday.csv")
s_am <- sc$yandex_score[sc$time == "08:45"]; s_pm <- sc$yandex_score[sc$time == "18:30"]
stopifnot(s_am == 5.9, s_pm == 7.8)
for (d in unique(raw$district)) {
  km1 <- median(raw$round_trip_km[raw$district == d]) / 2
  ff1 <- median(raw$freeflow_minutes[raw$district == d]) / 2
  t_am <- ff1 * (1 + 0.13 * (s_am - 2)); t_pm <- ff1 * (1 + 0.13 * (s_pm - 2))
  fare <- function(cls, tmin) {
    row <- tx[tx$service_class == cls, ]
    ceiling((row$minimum_price_amd + row$city_amd_per_km * max(km1 - 1, 0) +
             row$city_amd_per_min * max(tmin - 2.5, 0)) / 100) * 100
  }
  b <- r$budgets[r$budgets$district == d, ]
  stopifnot(abs(b$transport[b$mode == "Taxi (Comfort)"] - 22 * (fare("Comfort", t_am) + fare("Comfort", t_pm))) < 1e-6)
  stopifnot(abs(b$trip_minutes[b$mode == "Private car"] - (t_am + t_pm + 10)) < 1e-6)
  stopifnot(abs(b$trip_minutes[b$mode == "Taxi (Comfort)"] - (t_am + t_pm + 6)) < 1e-6)
  stopifnot(abs(b$transport[b$mode == "Private car"] - (2 * km1 * 22 * 60 + 10000)) < 1e-6)
}
# ---- Actual results, one sentence per chunk, for the Word guide ----
f0 <- function(x) format(round(x), big.mark = ",")
chunks <- list(
  setup = "Sets chunk options: code is shown, charts are 9 by 5.5 inches and saved as PNG files in figures/.",
  load = sprintf("Loaded %s ads, %s tariff facts, %s wage years, %s taxi classes and %s traffic times. Winter bills total %s AMD a month; time is valued at %s AMD an hour; traffic scores are %s at 08:45 and %s at 18:30.",
    nrow(r$rentals), nrow(r$tariffs), nrow(r$wages), nrow(r$taxi), nrow(r$traffic),
    format(round(r$utilities, 2), big.mark = ","), format(round(r$time_value, 2), nsmall = 2),
    r$score_morning, r$score_evening),
  rent = sprintf("The sample has %s districts. Kentron's median is %s AMD; the other district medians range from %s to %s AMD.",
    nrow(r$districts), f0(r$rent_kentron), f0(min(r$districts$rent)),
    f0(max(r$districts$rent[r$districts$district != "Kentron"]))),
  traffic = sprintf("Road time is multiplied by 1.00 at 07:00 and by %.2f at 18:30. Avan's one-way drive grows from %.1f to %.1f minutes.",
    1 + 0.13 * (r$score_evening - 2),
    r$by_hour$road_minutes[r$by_hour$district == "Avan" & r$by_hour$time == "07:00"],
    r$by_hour$road_minutes[r$by_hour$district == "Avan" & r$by_hour$time == "18:30"]),
  commute = sprintf("Modeled one-way times range from %.1f to %.1f minutes across %s district-mode rows. These are scenario estimates, not timed journeys.",
    min(r$travel$trip_minutes / 2), max(r$travel$trip_minutes / 2), nrow(r$travel)),
  budgets = sprintf("The chart shows %s monthly budgets. A daily Comfort taxi costs %s to %s AMD a month.",
    nrow(r$budgets), f0(min(r$budgets$taxi_cost)), f0(max(r$budgets$taxi_cost))),
  savings = sprintf("%s of %s district-mode examples stay cheaper than Kentron; savings range from %s to %s AMD a month. The focus district is %s.",
    r$cheaper, nrow(r$noncentral), f0(min(r$noncentral$saving)), f0(max(r$noncentral$saving)), r$focus_district),
  taxi_classes = sprintf("Comfort costs %s AMD a month more than Start on average. Compared with Kentron by bus, the lowest saving in the surge range is %s AMD a month.",
    f0(r$class_gap), f0(min(r$surge_grid$saving))),
  stress = sprintf("The grid has %s combinations outside Kentron. %s of them are more expensive than Kentron (%s with a taxi); this is a count of what-if cases, not a probability.",
    nrow(r$outside), r$reversals, sum(r$outside$saving < 0 & r$outside$mode == "Taxi (Comfort)")),
  threshold = sprintf("The lowest break-even value is %s AMD an hour, compared with the average wage of %s AMD an hour. %s taxi examples have no break-even because the taxi is faster than the bus from Kentron.",
    f0(r$lowest_threshold), f0(r$hourly), r$no_break_even))

dir.create(dirname(results_path), recursive = TRUE, showWarnings = FALSE)
jsonlite::write_json(list(chunks = chunks,
  summary = list(sample_n = nrow(r$rentals), district_n = nrow(r$districts),
    utilities = r$utilities, half_time_value = r$time_value,
    cheaper_examples = r$cheaper, reversal_rows = r$reversals),
  budgets = r$comparisons, thresholds = r$thresholds),
  results_path, pretty = TRUE, auto_unbox = TRUE)
cat("PASS: rendered; internal checks pass; public transport matches the archive (11 budgets, 10 thresholds, 792 scenarios); car and taxi match hand calculations in all 11 districts.\n")
