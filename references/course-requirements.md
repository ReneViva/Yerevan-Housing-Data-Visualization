# DS116 course evidence and open requirements

Checked **5 November 2026**, repository commit
`1a74f34584c85b08b0f9a87d055b663d209df9de`.

The user identified [ReneViva/DS116-Data-Visualization](https://github.com/ReneViva/DS116-Data-Visualization)
as the course source. Its [README](https://github.com/ReneViva/DS116-Data-Visualization/blob/1a74f34584c85b08b0f9a87d055b663d209df9de/README.md)
describes Dr. Habet Madoyan's AUA lecture notes/slides and gives lecture order
according to the syllabus. The repository itself does not contain a standalone
syllabus or establish this housing project's submission requirements.

## Inspection coverage

A separate read-only course audit inventoried all 11 topic folders and their
nested directories, retrieved all 17 Rmd sources and the README, and searched
for assignment, project, rubric, deadline, submission, citation, and AI-policy
instructions. There are 17 accompanying topic-level PDFs. Their visual renderings
and instructional images were not independently reviewed. No course code was
executed, course dataset downloaded, or research observation collected.

| Topic | Rmd count |
|---|---:|
| Intro to R | 1 |
| Introduction to ggplot2 | 2 |
| Single numeric variable | 5 |
| Multivariate numeric data | 1 |
| Categorical variables | 1 |
| Visualizing uncertainty | 2 |
| Colors | 1 |
| Principles of good visualization | 1 |
| Time series | 1 |
| Spatial visualization | 1 |
| PCA and clustering | 1 |

## Repository-verified teaching content

- [Intro to R](https://github.com/ReneViva/DS116-Data-Visualization/blob/1a74f34584c85b08b0f9a87d055b663d209df9de/DS116%20-%20Intro%20to%20R/DS%20116%20Intro%20to%20R.Rmd)
  teaches narrative plus executable R Markdown, labeled chunks, inline results,
  output formats, base `read.csv`, and dplyr verbs with `%>%`.
- [Multivariate numeric data](https://github.com/ReneViva/DS116-Data-Visualization/blob/1a74f34584c85b08b0f9a87d055b663d209df9de/DS116%20-%20Multivariate%20numeric%20data/DS%20116-Multivariate%20numeric%20data.Rmd)
  teaches scatterplots, linear smoothing, confidence bands, GGally, correlation,
  and hexagonal binning. These are examples, not mandatory project methods.
- [Uncertainty notes](https://github.com/ReneViva/DS116-Data-Visualization/blob/1a74f34584c85b08b0f9a87d055b663d209df9de/DS116%20-%20Visualiing%20Uncertainity/visualizing_uncertainty_extended.Rmd)
  cover confidence intervals, `t.test`, variability, and sample size. They explain
  that failing to reject a null does not establish equality. This does not make
  a t-test valid for an arbitrary housing dataset or modeled scenarios.
- [Visualization principles](https://github.com/ReneViva/DS116-Data-Visualization/blob/1a74f34584c85b08b0f9a87d055b663d209df9de/DS116%20-%20Principles%20of%20good%20visualizations/DS%20116%20-Principles%20of%20Good%20Visualization.Rmd)
  and [colors](https://github.com/ReneViva/DS116-Data-Visualization/blob/1a74f34584c85b08b0f9a87d055b663d209df9de/DS116%20-%20Colors/DS_116_Colors.Rmd)
  support meaningful labels, proportional graphics, restrained presentation,
  palettes matched to variables, and color-vision accessibility.
- [Spatial visualization](https://github.com/ReneViva/DS116-Data-Visualization/blob/1a74f34584c85b08b0f9a87d055b663d209df9de/DS116%20-%20Spatial%20Data%20Visualization/DS116%20Spatial%20data%20visualization.Rmd)
  teaches sf, coordinate systems, `st_read`, `st_transform`, and `geom_sf`.
  Mapping may justify sf later; it is not installed or required under A.
- [Income case study](https://github.com/ReneViva/DS116-Data-Visualization/blob/1a74f34584c85b08b0f9a87d055b663d209df9de/DS116%20-%20Single%20numeric%20variable/case-study-2007-income.Rmd)
  declares PDF and HTML and requests short interpretations. Other lecture files
  use Beamer/LaTeX; these templates do not mandate slides or PDF for our project.

## Requirements by authority

| Authority | What may currently be stated |
|---|---|
| Verified housing-project instructor requirements | No project-specific brief or rubric was found in this repository |
| Verified course content | R Markdown, ggplot2/dplyr, uncertainty, spatial plotting, and visualization principles are taught |
| User-reported previous homework practice | Executable Rmd plus PDF or HTML, readable labels, written findings, reproducible datasets; the reported Decoding the Gym assignment was not found here |
| User's housing-project requirements | Main explanatory Rmd plus chunk-matched educational DOCX, real evidence, geographic distinctions, separate cost outcomes, approval gates, beginner English and R explanations |
| Methodological recommendations | Provisional HTML rendering, base CSV import, ggplot2/dplyr, justified inference only, sensitivity and break-even analysis |
| Still needs instructor confirmation | Current project brief/rubric, deadline, length, submission format, required methods/packages, citation style, and AI-assistance policy |

Use a consistent reference format containing publisher, title, available dates,
URL, and access date; no mandatory APA/MLA style is established. Maintain the
AI assistance record and verify the student's understanding before submission.
The user confirmed beginner R experience and has not specified a deadline.

## Leads and cautions

Spatial teaching assets include a Yerevan districts shapefile bundle. Only file
names were inspected; provenance, license, dates, attributes, geometry, and
research suitability remain unverified. Do not copy or describe it as validated
research data before the approved discovery phase.

Some teaching chunks suppress warnings or show nonexecuted demonstrations.
Do not copy those choices into the analysis without justification. The income
example references a CSV absent from its folder inventory; lecture examples
have not been certified reproducible. Housing-project validation must be based
on its own executed code and available inputs.
