# Yerevan housing and commuting costs

Completed DS116 research using 276 screened advertisements from one agency across
11 named Yerevan districts. The results are conditional modeled budgets, not
representative household spending or causal effects.

## Deliverables

- `Yerevan_Housing_Research.Rmd`: one complete executable analysis with 16 explained
  chunks, actual results, six charts, sensitivity analysis and references.
- `outputs/Yerevan_Housing_Code_Companion.docx`: the 24-page educational companion,
  containing the exact numbered code, logical-block explanations, executed results
  and working links in the same chunk order.
- `outputs/Yerevan_Housing_Research.html`: self-contained rendered analysis.

Under baseline assumptions all ten non-Kentron district examples remain cheaper
in each mode. Two cases reverse within the chosen household/heating/time grid.
These are conditional scenarios, not probabilities or citywide findings.

## Reproduce

Open `YerevanHousing.Rproj` for editing. From PowerShell 7 at the project root:

```powershell
.\scripts\run-r.ps1 -RArguments @('scripts/render-analysis.R')
.\scripts\run-r.ps1 -RArguments @('validation/test-cost-model.R')
```

The launcher uses verified R 4.5.0 and RStudio Pandoc 3.10 at their existing
D-drive paths. For another computer supply `-RscriptPath` and `-PandocDirectory`.
It preserves arguments and exit status, starts at the project root, and changes
locale/Pandoc variables only in the child process. Code uses `--vanilla`; RStudio's
own selected executable is not controlled by the project file. Streams are printed
when R finishes. Default version and help commands also work.

The Rmd makes no network requests during execution. Keep the local `data/` and
`references/` files with it. Installed dependencies are ggplot2, dplyr, tidyr,
knitr, scales and jsonlite; versions/build warnings are recorded in the report
and `outputs/session-info.txt`. No package installation is automatic.

After a substantive change, re-render Rmd, then rebuild the Word companion:

```powershell
& 'C:\Users\Raven\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 scripts/build-companion.py
```

The builder checks chunk order, explanation coverage, actual-result narratives,
and exact saved DOCX code, then emits a hash manifest. Update the chunk guide when
changing code. Optional `scripts/build-analysis.py` generates the Rmd and guide
from one authoring source; running it replaces manual edits to those two files.
Choose the authoring path deliberately and preserve changes.

Final visual validation used existing native Microsoft Word in a dedicated
invisible, macro-disabled instance, opening only our DOCX read-only, followed by
Poppler. `scripts/render-companion.ps1` reproduces internal QA PDF/page images.
The packaged LibreOffice renderer lacks soffice; no office suite was installed.
Re-render and inspect pages after layout or content changes.

## Evidence

Raw source facts, official snapshots, source metadata, semantic checks and cached
route replies are in `data/raw/`; executed sample and membership log are in
`data/processed/`. Supporting results/charts/JSON are in `outputs/`. Plans, course
requirements, source discovery, reviewed strategy, chunk guide and AI assistance
record are in `references/`. Actual verification evidence is in `validation/`.

Source acquisition uses normal TLS and public access without bypassing controls.
The agency has not established an open-data redistribution license. Contacts,
images and descriptions were omitted; public listing URLs may contain address
slugs. Do not republish the catalogue as open data. Git has no remote.

See `references/dataset-discovery.md` and `validation/final-verification.md` for
coverage and limitations. The user's standing continuation instruction superseded
B/C pauses; the plan and independent strategy review remain recorded milestones.
The project rubric, deadline, submission format and AI policy still require
instructor confirmation. HTML is a provisional rendered submission option.
