# AI assistance record

The DS116 instructor's AI policy has not been confirmed. This record keeps AI
use transparent. It does not claim permission under course policy.

## 5–6 November 2026: OpenAI Codex

The student supplied the research brief, the DS116 course repository and the
known requirements from previous homework. Codex planned the study, collected
public data (WSE.AM listings, OSRM routes, official tariffs, Armstat wages),
obtained an independent statistical review, wrote and executed the R Markdown,
built the Word companion, simplified the report into six charts at the
student's request, and published the repository. Independent QA agents checked
the calculations, code matching and rendered pages. The full original record is
in `_archive/previous-version/references/ai-assistance.md`, and verification
evidence is in `_archive/`.

## 24 November 2026: moved to Claude Code

At the student's request, Claude (Anthropic) reviewed the whole project and
replaced the Codex configuration with Claude Code equivalents:

- `AGENTS.md` became `CLAUDE.md`, with the DS116 course scope and the known
  instructor requirements made explicit.
- `.codex/agents/` (researcher, statistician) became `.claude/agents/`, plus a
  chart reviewer and a QA verifier.
- Project skills in `.claude/skills/` for knitting the report, rebuilding the
  Word companion and checking course scope. The companion builder and render
  checks were copied from `_archive/revision-tools/`, which is unchanged.

No analysis, data, chart or result was changed in this step.

## 24 November 2026: Yandex Taxi data, tidier report, taxi comparison

At the student's request, Claude:

- found and saved the taxi and traffic data (`data/taxi_tariffs.csv`,
  `data/traffic_score_weekday.csv`, `data/traffic_benchmarks.csv`). Hourly
  Yandex prices are not published. The traffic curve was read from a Yandex
  chart image; how each number was made is in
  `data/raw/taxi_traffic_2026-11-24/README.md`;
- proposed the traffic equation (k = 0.13), calibrated on the mayor's figure
  and checked against Numbeo. The student chose to use it for both car and taxi;
- rewrote the Rmd in the style of the DS116 lecture files. It removed custom
  CSS, tidyr, waterfall and dumbbell charts, and other code outside the course.
  Before adding the taxi, it checked that the tidy version gave exactly the same
  numbers as the approved version;
- added the taxi mode, two new charts and an updated conclusion. Bus results
  still match the archived analysis exactly; car and taxi results were checked
  by an independent hand calculation from the CSVs;
- ran an independent chart review and statistical review (Claude agents), and
  rebuilt the Word companion from the Rmd.

Car results changed on purpose: the car now uses the same traffic model as the
taxi instead of "1.5 × empty-road time".

## Before submission

The student should be able to explain the code, methods and results
independently, and should confirm the instructor's project and AI-assistance
rules.
