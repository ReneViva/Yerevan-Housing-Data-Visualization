---
name: course-scope-check
description: Check a proposed change, or the whole Yerevan housing report, against the DS116 Data Visualization course (AUA, Dr. Habet Madoyan) and the instructor requirements known so far. Use before adding charts, methods, packages or sections, and before submission.
---

# Course scope check

1. **Check the course repo for anything new.** Compare the latest commit of
   `ReneViva/DS116-Data-Visualization` with `1a74f34` (recorded in `CLAUDE.md`):

   ```powershell
   curl.exe -s "https://api.github.com/repos/ReneViva/DS116-Data-Visualization/commits?per_page=5"
   ```

   If there are new commits, read what changed. Look especially for a project
   brief, rubric, deadline, submission format, citation style or AI policy. A
   new rule from the instructor overrides the defaults in `CLAUDE.md`; tell the
   user and update `CLAUDE.md` section 2.

2. **Score the change or report** against this list. Mark each item
   pass / needs work / not applicable:

   - It is about **visualizing** data: each section is a question, a chart and a
     short takeaway. No new section is mainly tables or numbers.
   - The technique belongs to a course topic (ggplot2, distributions,
     categorical, multivariate, uncertainty, colours, principles, time series,
     spatial, PCA/clusters). Name the topic.
   - Built with ggplot2 + dplyr; any other package is justified and approved.
   - Titles, axis labels with units, legends, captions; colour-blind-safe palette.
   - Written interpretation of findings, not only plots.
   - Runs from start to end; the Rmd reads only `data/`; HTML/PDF render.
   - Sources cited consistently (publisher, title, date, URL, access date).
   - Statistics are honest: no fabricated p-values, observed vs. modeled is
     labeled, small samples are marked.
   - Beginner-friendly English and code; the Word companion still matches.
   - AI assistance is documented in `references/AI_assistance.md`.

3. **Report** a short table of results, then the top changes needed. Keep the
   project in scope: suggest removing or simplifying work that does not help a
   DS116 reader understand the charts.

Do not treat course lecture examples as mandatory methods, and do not invent
rules the instructor has not given. Keep "confirmed", "from previous homework",
"student's preference" and "still unconfirmed" separate.
