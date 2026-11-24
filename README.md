# Yerevan housing and commuting costs

DS116 Data Visualization project at the American University of Armenia.

**Question:** someone works in the centre of Yerevan. Is it cheaper to rent in
Kentron, or in another district and commute by bus, by car or by Yandex Taxi?

[R Markdown source](Yerevan_Housing_Research.Rmd) ·
[Word code companion](Yerevan_Housing_Code_Companion.docx) ·
[PDF report](outputs/Yerevan_Housing_Research.pdf)

Download the repository and open `outputs/Yerevan_Housing_Research.html` to read
the report. Use **Code** to show the code behind a chart.

## Run it

Open **YerevanHousing.Rproj** in RStudio, open **Yerevan_Housing_Research.Rmd**
and click **Knit**. RStudio makes the HTML next to the Rmd and saves the eight
charts in **figures/**. Choose *Knit to PDF* for the PDF version.

Needed: R with ggplot2, dplyr, rmarkdown and knitr; RStudio's Pandoc; a LaTeX
installation (TinyTeX) for the PDF. No internet connection is needed.

## Files

| Folder | What it contains |
|---|---|
| data | CSV inputs: rentals with road routes, tariffs, wages, Yandex taxi rates, Yandex traffic score, traffic facts, sources |
| data/raw | Saved source pages for the taxi and traffic data, with notes on how each number was made |
| figures | The eight charts, made by Knit |
| outputs | The rendered HTML and PDF |
| references | Sources and method, and the AI assistance record |
| _archive | The previous versions, original records, scripts and checks |
| .claude | Claude Code agents and skills used to maintain the project (see CLAUDE.md) |

The 276 advertisements are one agency's sample. Rents are observed asking
prices; travel times, taxi fares and household costs are modeled examples.

The first version is saved in Git as `before-visual-simplification` (`abcf7d5`)
and in `_archive/previous-version`.

Public repository: [ReneViva/Yerevan-Housing-Data-Visualization](https://github.com/ReneViva/Yerevan-Housing-Data-Visualization).
