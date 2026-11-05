# Checkpoint A setup status

Historical setup record. The user later authorized continuation through the end;
see final-verification.md for completed research and artifact checks.

Date: **5 November 2026**, Asia/Yerevan.

## Approval and changes

The user approved the six Checkpoint A setup actions and separately requested
inspection of the DS116 course repository. Project instructions, two advisory
agent definitions, a minimal RStudio project, an R launcher, verification scripts,
course evidence, and an AI assistance record were created. Empty data and output
directories contain only Git placeholders. Local Git uses branch main, with no
remote and no commits yet. No global configuration, package installation, plugin,
MCP registration, external account, or research collection was performed.

## Executed verification

| Check | Result and evidence |
|---|---|
| R launcher integration tests | Six real-process tests cover default/version/help calls, literal arguments/spaces/quotes/empty string, project working directory, clean locale/Pandoc, stdout/stderr, R failure exit status, and missing R/Pandoc paths; see test_launcher.py |
| Installed R | R 4.5.0 executed; no fallback to R 4.3.3 |
| Package loading | ggplot2 4.0.3, dplyr 1.2.1, tidyr 1.3.2, stringr 1.6.0, rmarkdown 2.32, knitr 1.52, scales 1.4.0, jsonlite 2.0.0 loaded |
| Pandoc | Existing RStudio Pandoc 3.10 discovered by child R |
| Locale | Child R used English_United States.utf8; inherited C.UTF-8 warnings absent |
| Font fixture | PNG generated and visually inspected; Armenian labels Երևան and Կենտրոն are readable |
| R Markdown | Temporary nonresearch Rmd rendered successfully to self-contained HTML, then source removed |
| Browser check | Chrome opened the generated HTML; embedded image loaded at 1200 by 450 pixels, document title/text correct, no horizontal overflow at the inspected viewport |
| Agent definitions | Both TOML files parsed successfully with name, description, and developer_instructions; no model/permission/service overrides |
| Git hygiene | No remote; setup artifacts ignored; raw and processed data directories remain empty except .gitkeep |
| DOCX prerequisite | Packaged renderer and Python/Poppler dependencies exist; no located LibreOffice executable; no DOCX generated or rendered |

Generated diagnostic JSON, HTML, and PNG are under ignored
`validation/.setup-smoke/`. Successful smoke rendering does not validate future
research models, data quality, inference, or final documents.

## Limitations and pending work

- Seven installed packages emitted existing warnings that they were built under
  R 4.5.3. The R 4.5.0 package-loading, chart, and HTML checks completed successfully.
  Warnings are visible and recorded in diagnostics.json. This is not a claim of
  comprehensive package compatibility; no upgrade or reinstall was performed.
- The RStudio project controls editing/workspace settings, not RStudio's chosen
  R executable or environment. The launcher is the verified execution path.
- Agent TOML parsing is verified; live registration of the two new role names
  in an already-running Codex session has not been established. Existing agent
  tools can receive the corresponding brief; reload the project if needed later.
  Their instructions do not enforce read-only tool permissions.
- No formal syllabus, housing-project brief/rubric, deadline, required citation
  style, or AI policy was found in the inspected course source. See the separate
  requirements record for the distinction between instruction and examples.
- LibreOffice was not found on PATH or in the previously checked locations. This
  is not an exhaustive claim that it is absent everywhere on the computer. Its
  discovery or installation remains a prerequisite before DOCX visual QA.
- Independent setup QA completed; the initial launcher finding was corrected
  and independently reverified. No material issue remains in the reviewed scope.
- Checkpoint B and C remain unapproved. No research Rmd or Word companion exists.

Next: prepare the research plan using the inspected course evidence and resolve
material research-scope choices. Obtain B approval before dataset discovery and C
approval before analytical implementation. Do not finalize submission requirements
without the project brief or explicit acknowledgment that they remain provisional.

## QA review history

Independent QA reproduced a bug in the first implementation: prepending
`--vanilla` before `--version` made the documented default command fail with
"file name is missing". Regression tests reproduced default, explicit version,
and help failures before the correction. The launcher now leaves informational
flags first (they exit without starting an R session) and retains `--vanilla`
for code execution. All six tests passed in the coordinator's subsequent run.
Independent re-verification passed all six tests with exit 0 and confirmed the
documented no-argument launcher reports Rscript 4.5.0 with exit 0. This supersedes
the initial finding. The final QA verdict found no remaining material issue in
the reviewed setup scope.

The first independent review also reran the earlier four tests and smoke check,
inspected the Armenian PNG, and confirmed with a same-process probe that the
parent environment is unchanged. Both TOMLs and local Git/data boundaries were
checked. No other material issue was identified in that review. Actual RStudio,
new role-name registration, browser, Word/PDF rendering, and external course-source
claims were not independently tested by that reviewer.
