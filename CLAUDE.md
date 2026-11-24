# Yerevan housing project — instructions for Claude

This project is worked on with **Claude Code**. It was started with OpenAI Codex
on 5–6 November 2026; on 24 November 2026 the user moved it to Claude. Codex
files were replaced by this file, `.claude/agents/` and `.claude/skills/`.
Anything under `_archive/` that mentions Codex is historical evidence: leave it
unchanged.

## 1. Course scope comes first

This is a project for **DS116 Data Visualization** (Dr. Habet Madoyan, American
University of Armenia). The course materials are in the user's GitHub repo
[ReneViva/DS116-Data-Visualization](https://github.com/ReneViva/DS116-Data-Visualization)
(last checked at commit `1a74f34`, 25 Oct 2026). Before changing the analysis,
check whether that repo has new commits or an assignment brief.

Every change must serve **data visualization**: a clear question, a chart that
answers it, and a short written takeaway. Statistics and cost modeling exist to
support the charts, not to replace them. The user said: "It's a data
visualization course … we care about charts, statistics", not walls of numbers.
Do not grow the project into an economics model or a software tool.

Prefer techniques taught in the course topics:

| Course topic | What it supports here |
|---|---|
| Intro to R | R Markdown, labeled chunks, inline results, `read.csv`, dplyr with `%>%` |
| Introduction to ggplot2 | Layered ggplot2 charts, facets, scales, labels |
| Single numeric variable | Histograms, density, boxplots, QQ plots, distribution summaries |
| Categorical variables | Bar charts, ordered categories, proportions |
| Multivariate numeric data | Scatterplots, trend lines, GGally, correlation, hexbin |
| Visualizing uncertainty | Confidence intervals, variability, sample size, `t.test` (only when valid) |
| Colors | Palettes matched to the variable type, colour-vision accessibility |
| Principles of good visualization | Honest proportions, meaningful labels, restrained design |
| Time series | Only if a real time dimension is added |
| Spatial visualization | `sf`, `geom_sf`, coordinate systems; the repo has `Yerevan-Districts.zip` (provenance and license still unverified) |
| PCA and clusters | Only if clearly justified by the question |

Course examples are teaching material, not mandatory methods. A new package
(for example `sf` for a district map) needs the user's approval before install.

## 2. Instructor requirements: confirmed vs. not confirmed

No project brief, rubric or deadline was found in the course repo. Keep these
categories separate and never invent a missing academic rule.

- **From previous DS116 homework (reported by the user, e.g. "Decoding the
  Gym"):** an executable `.Rmd`; a rendered PDF or HTML; code that runs from
  start to end; clear chart titles, axis labels and legends; short written
  interpretations of findings; dataset files organized so the report reproduces.
- **Packages used in the course:** ggplot2, dplyr, GGally, hexbin. No official
  mandatory list for this project. Prioritize ggplot2 and dplyr.
- **Citation style:** not confirmed. Cite every dataset and method source with
  publisher, title, dates, URL and access date in one consistent format. Do not
  assume APA or MLA.
- **AI policy:** not confirmed. Keep AI assistance transparent, verify all
  generated analysis and citations, and make sure the student can explain the
  code. Flag academic-integrity concerns before submission.
- **Still needs instructor confirmation:** project rubric, deadline, length,
  submission format, required methods, citation style and AI policy.

## 3. The user's own requirements

- Two principal deliverables: the root **`Yerevan_Housing_Research.Rmd`** and
  the root **`Yerevan_Housing_Code_Companion.docx`**. HTML and PDF in
  `outputs/` are for reading.
- Simple academic English for a beginner R student at AUA.
- The report reads as **question → chart → short bold Answer**, in the style of
  the professor's lecture Rmd files: plain YAML, one setup chunk, `library()`,
  `read.csv`, one `+` per ggplot line, short plain comments, blank lines between
  steps. No custom CSS, HTML wrappers, tidyr or other packages outside the course
  unless the user approves. Checks live in `.claude/skills/knit-report/`, not in
  the student Rmd.
- The Rmd reads only flat CSVs in `data/` and calculates every result itself.
  `knitr` saves the charts to `figures/` through `fig.path` (8 charts).
- Three commuting modes (since 24 Nov 2026): public transport, private car and
  Yandex Taxi (Comfort; Start in one comparison chart). Car and taxi share the
  traffic model `t = free-flow × (1 + 0.13 × (score − 2))`; trips at 08:45 and
  18:30. Surge and the score-to-minutes conversion are labeled assumptions.
- Charts should be varied and chosen for what best explains the data (current
  set: boxplots, line chart by hour, grouped bars, stacked bars, grouped bars for
  the focus district, small-multiple lines for surge, heatmap, dot plot). Reasons
  are in `references/Sources_and_method.md`.
- The Word companion explains the exact chunks in the same order, includes every
  chart, and its code must be **extracted from the Rmd**, never retyped.
- Use real data. Never claim a hypothesis is proven only because a p-value is
  significant.

## 4. Research rules

- Question: does rent saved farther from central Yerevan outweigh extra
  transport, commuting time, heating and utilities? Treat it as falsifiable;
  cheaper peripheral housing may stay cheaper overall. No causal claims.
- Keep Kentron, other Yerevan districts and places outside the municipality
  distinct. The shared destination is Republic Square.
- Direct monthly cost = rent + utilities (heating counted once, through gas) +
  transport. Generalized cost = direct cost + monetary value of commuting time.
  Report both, including a zero time-value case. No double counting.
- Separate asking rents from transactions, observations from assumptions, and
  network journeys from straight-line distance.
- Never invent observations, impute without an approved method, or fabricate
  p-values. Scenario grids are not independent households. Quartiles describe
  ads; they are not confidence intervals.
- Small districts (n < 10) must stay marked as sparse.

## 5. Data rights and privacy

The WSE.AM catalogue has **no established redistribution license**; robots.txt
permission is not a license. Keep only factual fields, no contacts, photos or
descriptions. The repository is public (authorized by the user on 6 Nov 2026),
so do not add more raw third-party data to it without asking. Keep credentials,
`.RData` and `.Rhistory` out of Git.

## 6. Files and tools

| Path | Contents |
|---|---|
| `Yerevan_Housing_Research.Rmd` | Main report, 10 chunks, 8 charts |
| `Yerevan_Housing_Code_Companion.docx` | Chunk-by-chunk Word guide |
| `data/` | `rentals.csv` (276 ads), `tariffs.csv`, `wages.csv`, `sources.csv`; added 24 Nov 2026 for the taxi comparison: `taxi_tariffs.csv`, `traffic_score_weekday.csv`, `traffic_benchmarks.csv` |
| `data/raw/taxi_traffic_2026-11-24/` | Raw snapshots, hashes and provenance for the taxi/traffic files. Copyrighted pages: check before publishing. |
| `figures/`, `outputs/` | Generated by Knit |
| `references/Sources_and_method.md` | Active source and method note |
| `_archive/` | Previous version, raw downloads, scripts, checks. **Preserve byte-for-byte.** Git tag `before-visual-simplification` must not be rewritten. |

Environment: R 4.5.0 at `D:\Softwares\Applications\R\R-4.5.0\bin\Rscript.exe`
(not on PATH), RStudio Pandoc at
`D:\Softwares\Applications\RStudio\resources\app\bin\quarto\bin\tools`,
TinyTeX/XeLaTeX for the PDF, Python 3.12 with python-docx, Microsoft Word for
checking the companion. Packages: ggplot2, dplyr, tidyr, scales, rmarkdown,
knitr. Do not install software or packages without the user's approval. Keep
`options(tinytex.install_packages = FALSE)`.

Project skills (in `.claude/skills/`):
- `/knit-report`: render HTML, PDF and figures in a clean R session and check them.
- `/update-companion`: rebuild the Word guide from the Rmd and check that it matches.
- `/course-scope-check`: review a change or the whole report against DS116.

Project agents (in `.claude/agents/`), all advisory:
- `researcher`: Armenian housing, transport and utility sources.
- `statistician`: independent methodological challenge.
- `chart-reviewer`: chart choice, readability and fit with DS116.
- `qa-verifier`: independent numerical, execution, citation and artifact checks.

Useful installed Claude skills: `dataviz` (chart design), `data:statistical-analysis`,
`data:validate-data`, `anthropic-skills:docx` and `anthropic-skills:pdf`,
`engineering:debug`, `code-review`. Spawn agents only when the user asks
or the task truly needs an independent review. Don't repeat an investigation.

## 7. Verification before saying "done"

- Knit in a clean session (`/knit-report`). Numbers in the text must come from
  executed inline R, not typed by hand.
- Look at every chart: title or question, axis labels, units (AMD, minutes),
  legend, readable text, colour-blind-safe colours.
- If code changed, rebuild and check the Word companion (`/update-companion`)
  and inspect its pages.
- Report only checks that were actually run, with their results and limits.

## 8. Approvals

- Ask before: changing the research question, scope or method; collecting new
  data; installing software or packages; adding services or credentials;
  committing; pushing to GitHub.
- The user has authorized the public repo
  `ReneViva/Yerevan-Housing-Data-Visualization`. Each push still needs a yes.
- Update the AI assistance note (`references/AI_assistance.md`) when Claude
  makes substantive changes.
