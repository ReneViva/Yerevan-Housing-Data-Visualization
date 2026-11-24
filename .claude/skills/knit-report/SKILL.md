---
name: knit-report
description: Knit the Yerevan housing R Markdown report (HTML, PDF and six chart PNGs) with the project's pinned R 4.5.0 and Pandoc, check the outputs, and compare results with the archived baseline. Use after any change to the Rmd or data, before updating the Word companion, and before saying the report works.
---

# Knit the report

Rscript is not on PATH; `knit.ps1` uses the pinned paths from `CLAUDE.md`.

1. **Clean reproducibility check** (does not touch project files):

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .claude/skills/knit-report/knit.ps1 -Clean
   ```

   It copies only the Rmd and `data/` to a temp folder, knits HTML and PDF,
   checks for eight PNGs, and writes `results.json` there.

2. **Update the project outputs** (rewrites `outputs/` and `figures/`):

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .claude/skills/knit-report/knit.ps1
   ```

   Executed results go to `outputs/checks/results.json` (ignored by Git); the
   `update-companion` skill reads them.

3. **Look at the results, don't just trust the exit code.**
   - Open each PNG in `figures/` with Read: labels, units, legend, readability.
   - Check the takeaways in the HTML match the charts (they use inline R).
   - The PDF is A4 via XeLaTeX; confirm it has no overflowing text if layout changed.

## The archived-baseline check

`knit_and_check.R` stops if the 22 budgets, 20 break-even thresholds or 1,584
scenario rows differ from `_archive/previous-version/outputs/`. That is
intended: it protects the approved analysis. If the user **approves** a method
or data change, edit the comparison block in `knit_and_check.R` (and the
hard-coded chunk narratives in the same file) and say so in the report to the
user. Never edit `_archive/`.

## Failure notes

- TinyTeX auto-install is disabled on purpose. A missing LaTeX package needs the
  user's approval to install.
- The R PDF device can't draw Armenian/Cyrillic text; the report uses PNG charts
  for that reason. Keep `dev = "png"`.
