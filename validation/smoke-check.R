# Setup diagnostics only. No research observations or conclusions are created.
options(warn = 1)

packages <- c("ggplot2", "dplyr", "tidyr", "stringr", "rmarkdown",
              "knitr", "scales", "jsonlite")
package_warnings <- character()
for (package in packages) {
  withCallingHandlers(
    suppressPackageStartupMessages(library(package, character.only = TRUE)),
    warning = function(w) {
      package_warnings <<- c(package_warnings, conditionMessage(w))
    }
  )
}
# Keep pre-existing package-build warnings visible, but treat subsequent chart
# and rendering warnings as failures rather than silently accepting missing text.
options(warn = 2)
stopifnot(as.character(getRversion()) == "4.5.0")
stopifnot(rmarkdown::pandoc_available())

smoke_directory <- file.path("validation", ".setup-smoke")
dir.create(smoke_directory, recursive = TRUE, showWarnings = FALSE)
smoke_directory <- normalizePath(smoke_directory, winslash = "/")

armenian_labels <- c("\u0535\u0580\u0587\u0561\u0576",
                     "\u053f\u0565\u0576\u057f\u0580\u0578\u0576")
stopifnot(all(validUTF8(armenian_labels)))
label_check <- data.frame(label = armenian_labels, x = 1:2, y = c(1, 1))
chart <- ggplot2::ggplot(label_check, ggplot2::aes(x = x, y = y, label = label)) +
  ggplot2::geom_text(family = "sans", size = 8) +
  ggplot2::xlim(0.3, 2.7) +
  ggplot2::ylim(0.5, 1.5) +
  ggplot2::labs(title = "Armenian font rendering check",
                subtitle = "Setup fixture only; no research observations") +
  ggplot2::theme_void(base_family = "sans") +
  ggplot2::theme(plot.title = ggplot2::element_text(size = 18),
                 plot.subtitle = ggplot2::element_text(size = 12))
chart_path <- file.path(smoke_directory, "utf8-labels.png")
ggplot2::ggsave(chart_path, chart, width = 8, height = 3, dpi = 150,
                device = "png", type = "cairo", bg = "white")
stopifnot(file.info(chart_path)$size > 0)

# Keep the diagnostic Rmd temporary; the main research Rmd is gated by C.
input_path <- file.path(smoke_directory, "setup-smoke.Rmd")
writeLines(c(
  "---",
  'title: "Checkpoint A rendering check"',
  "output:",
  "  html_document:",
  "    self_contained: true",
  "    theme: null",
  "    mathjax: null",
  "---", "",
  "This is a setup diagnostic, not a housing research report.", "",
  "```{r setup-label-image, echo=TRUE}",
  'knitr::include_graphics("utf8-labels.png")',
  "```"
), input_path, useBytes = TRUE)
html_path <- rmarkdown::render(input_path, quiet = TRUE,
                              envir = new.env(parent = baseenv()),
                              encoding = "UTF-8")
stopifnot(file.exists(html_path), file.info(html_path)$size > 0)
unlink(input_path)

diagnostics <- list(
  purpose = "Checkpoint A nonresearch setup smoke check",
  checked_at = format(Sys.time(), tz = "Asia/Yerevan", usetz = TRUE),
  r_version = R.version.string,
  r_home = R.home(),
  library_paths = .libPaths(),
  locale = Sys.getlocale(),
  pandoc_version = as.character(rmarkdown::pandoc_version()),
  package_versions = setNames(lapply(packages, function(p) {
    as.character(utils::packageVersion(p))
  }), packages),
  package_loading_warnings = package_warnings,
  armenian_utf8_valid = all(validUTF8(armenian_labels)),
  chart = chart_path,
  html = html_path,
  visual_inspection = "Not performed by this script; see validation/setup-status.md for independent image review",
  research_data_collected = FALSE
)
jsonlite::write_json(diagnostics, file.path(smoke_directory, "diagnostics.json"),
                     pretty = TRUE, auto_unbox = TRUE)
cat("PASS: package loading, UTF-8 string checks, PNG generation, HTML rendering.\n")
cat("Visual inspection still required.\n")
cat("HTML:", html_path, "\n")
