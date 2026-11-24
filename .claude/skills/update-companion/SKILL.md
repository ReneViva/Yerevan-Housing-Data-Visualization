---
name: update-companion
description: Rebuild Yerevan_Housing_Code_Companion.docx from the current Rmd so its chunk labels, order, code and six charts match exactly, then check the rendered pages. Use whenever Rmd code, chunk labels, charts or results change.
---

# Update the Word code companion

The Word guide must explain the **exact** Rmd code. Never retype code by hand.

1. Run `/knit-report` (default mode) first, so `figures/` and
   `outputs/checks/results.json` are current.
2. If chunks were added, removed, renamed or changed, edit
   `.claude/skills/update-companion/companion-guide.json`. It has one entry per
   chunk in Rmd order: `label`, `title`, `purpose`, optional `figure`, `blocks`
   (line ranges + plain-English explanations for a beginner), `expected`,
   `interpretation`, `hypothesis`. Line ranges count from 1 inside each chunk.
3. Validate without writing:

   ```powershell
   python .claude/skills/update-companion/build_companion.py --check-only
   ```

4. Build (overwrites the root `.docx` and writes `outputs/checks/companion-manifest.json`):

   ```powershell
   python .claude/skills/update-companion/build_companion.py
   ```

   The builder re-opens the saved file and fails if the Word code differs from
   the Rmd or if there aren't six images.

5. Check the pages visually. Export to PDF with Microsoft Word (the archived
   `_archive/revision-tools/render_word.ps1` shows a safe read-only method; copy
   its approach and send output to a temp folder, not `_archive/`), then read
   the PDF pages with the `anthropic-skills:pdf` skill or Read. Look for code
   overflowing, charts split from their headings, and unreadable text.

Report which checks ran. If page rendering wasn't possible, say so; don't
claim the Word layout was verified.
