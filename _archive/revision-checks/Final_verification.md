# Simplified visual report verification

Verified on 6 November 2026. Research snapshot remains 5 November 2026.

- Six questions now use boxplots, a commute dumbbell, stacked cash budgets,
  an explanatory savings waterfall, a sensitivity heatmap and break-even dots.
  Selection reasons are in references/Sources_and_method.md.
- The editable Rmd contains nine chunks and 168 executable code lines, down
  from approximately 394. It imports only four flat CSVs from data/.
- Fresh isolated R --vanilla execution of the YAML Knit function generated
  HTML, PDF and six PNGs from only the Rmd and four CSVs. No acquisition or
  development script was needed. Source inspection found no network operation.
- Executed comparisons match the archived baseline within 0.000001 AMD:
  22 budgets, 20 thresholds and all 1584 scenario rows. The 276-record sample
  is unchanged. Independent QA reproduced the new waterfall accounting and
  checked all boxplot medians and modeled mode comparisons.
- The waterfall explicitly selects Davtashen because it contains the smallest
  remaining baseline saving. Car saving is 76171.568 AMD; public transport
  saving is 81093.676 AMD. It does not depict every district as that example.
- HTML was rendered and inspected using Playwright at 1365 by 900 and 390 by
  844. First image starts at 297 and 368 CSS pixels respectively. Desktop
  chart width is 980 pixels. Both views have no horizontal page overflow.
  Six images load, code starts folded and all three optional notes start shut.
- Keyboard interaction opened and closed code and native details. The code
  button has a visible solid 3-pixel focus outline. Bootstrap folding needs
  its transition to finish before another toggle. No custom motion is used.
  The only final HTTP console error was the preview server's missing favicon;
  no report-script errors were observed. Impeccable detection returned [].
- The 8-page A4 XeLaTeX report and all six PNGs were visually inspected.
  The Windows R character locale is set only in the R process. A separate
  Cyrillic fixture rendered correctly using the report's PNG plus XeLaTeX
  route. The default R PDF graphics device failed that fixture, explaining
  why the report deliberately uses PNG charts. Armenian PDF text is not claimed
  as independently verified.
- Native Microsoft Word exported the companion using a dedicated invisible
  instance and read-only document open. Poppler generated all 17 page PNGs.
  All pages were visually inspected; reflowed pages were reinspected after
  fixes, and unchanged page hashes checked. Body text is 11pt and code 10pt;
  text was not reduced to meet the page target. Exact Word code matches all
  168 source lines and nine labels; embedded image hashes match six final PNGs.
- verify_artifacts.py confirms all 122 archived original hashes, every ZIP
  member, and the old Rmd/Word/HTML Git blobs under before-visual-simplification.
  No research evidence was deleted. The original recent PDF settings remain
  in that preserved Rmd. No remote publication occurred.

The current existing R, RStudio Pandoc, TinyTeX, Word and bundled Python were
used. A first PDF attempt caused TinyTeX to auto-install the missing nameref
support package before failing on a Windows image path; subsequent analysis
explicitly disables automatic TeX package installation. No R package or office
renderer was installed for this revision. Earlier failed renderer attempts and
acquisition details remain archived.

The course project rubric, submission deadline and instructor AI policy remain
unconfirmed; the active source note distinguishes these from user preferences.
