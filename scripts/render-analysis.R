# Execute the complete main document from a fresh launcher process.
options(warn = 1)
rmarkdown::render("Yerevan_Housing_Research.Rmd", output_dir = "outputs",
                  quiet = FALSE, envir = new.env(), encoding = "UTF-8")
