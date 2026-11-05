# Yerevan housing research project

## Approved work and approval gates

### Current standing authorization

On 2026-11-05, after setup, the user instructed "dont stop continue until the
end". This supersedes the earlier B/C pause requirements below: proceed through
planning, lawful public-source acquisition, independent methodological review,
R analysis, document creation, and validation without requesting another phase
approval. Record the B/C decisions and limitations as review milestones. Use
judgment for unspecified study assumptions and disclose them. Do not fabricate
data or inference, publish externally, bypass restrictions, or create paid
accounts/services. Prefer existing packages and project-local tools. Historical
checkpoint notes below describe the original process, not the current permission.

- Checkpoint A setup was approved on 2026-11-05. Only project instructions,
  two agent definitions, local Git, R tooling, and nonresearch smoke checks
  are authorized at this stage.
- Checkpoint B is not approved. Do not collect housing, transport, utility,
  wage, routing, or other research data before the user approves the full plan.
  Reading the user-provided DS116 course repository is authorized separately.
- Checkpoint C is not approved. After B, discover and inspect candidate data,
  then obtain the user's approval of the final data and analytical strategy
  before generating the principal research R Markdown or Word companion.
- Manual data collection, changes to the approved scope or methodology,
  new services/authentication, and software installation require explicit
  authorization. Do not bypass CAPTCHAs, access controls, or source restrictions.
- A statistician reviews the approach before implementation. Agent reviews
  are advisory and do not replace the user's B or C approval.
- Continue planning after setup; stop at the user's research approval gates.

## Research and evidence

- Working question: does rent saved farther from central Yerevan outweigh
  additional transport, commuting-time, heating, and utility costs?
- Treat this as a falsifiable hypothesis. Cheaper peripheral housing may remain
  cheaper overall. Do not assume a desired conclusion or claim causation.
- Keep outside Kentron, peripheral Yerevan, and outside the Yerevan municipality
  distinct. Define a central destination and geographic comparisons explicitly.
- Direct monthly cost = rent + utilities (including heating once) + transport.
- Generalized monthly cost = direct monthly cost + monetary commuting-time cost.
  Report these separately; include a zero time-value scenario. Do not double-count.
- Separate asking rents from transactions, observations from assumptions, and
  network journeys from straight-line distance. Compare equivalent properties
  and households. Record seasonal and transport-mode differences.
- Preserve immutable raw inputs separately from processed data. Record source
  URLs, publisher, dates, units, coverage, access method, transformations,
  duplicate handling, limitations, and measured versus modeled status.
- Say data is found only when relevant records have been obtained and checked.
  Never invent observations, impute without an approved method, or fabricate
  p-values. Scenario grids are not independently sampled households.
- Establish estimands, hypotheses, inference assumptions, and alpha before
  inspecting main results. Use effect sizes and confidence intervals where
  valid; explain when inference is unsupported. Sensitivity analyses should
  expose dependence on household, travel, wage, and consumption assumptions.

## R and educational outputs

- Use beginner-friendly R, prioritizing ggplot2 and dplyr. Reuse installed
  packages; justify additions. Do not install any package under setup approval.
- Use relative project paths. The launcher pins the verified local R 4.5.0
  executable, supplies Pandoc, and sanitizes only the child process locale.
  It uses --vanilla and does not automatically load .Rprofile or renv.
- Final principal files are one executable .Rmd and one .docx code companion.
  A rendered HTML or PDF is provisional pending project submission instructions.
- Each substantive Rmd chunk needs a descriptive title and unique label,
  research objective, what the code does, executable code, expected output type
  without predicted findings, actual result, interpretation, and connection
  to the hypothesis.
- The Word companion follows identical chunk order and identifiers. Extract
  code from the final Rmd rather than maintaining a divergent copy. Explain
  meaningful lines/blocks, method choice, actual outputs, limitations, and sources.
- Use simple academic English, consistent citations, working source links,
  and readable chart titles, axes, legends, and units. Do not invent citation rules.
- Review references/course-requirements.md for confirmed versus provisional
  requirements. The student is a beginner in R; the deadline is not specified.
- Record AI assistance transparently in references/ai-assistance.md; the
  instructor's AI policy remains unconfirmed unless course evidence establishes it.

## Roles and verification

- Coordinator owns approvals, R implementation, visualization, and teaching text.
- Researcher combines source discovery and Armenian housing/transport expertise.
- Statistician independently challenges assumptions and analytical validity.
- Reuse qa_verifier for independent numerical, execution, citation, and artifact
  checks. Do not create six agents or repeat the same investigation unnecessarily.
- No new MCP, plugin, credential, global config, or remote repository is authorized.
  No project .codex/config.toml is required. Keep agent definitions advisory;
  instructions alone are not enforced read-only permissions.
- Verify numerical claims against executed code, render the final Rmd in a clean
  session, validate units/missing values/duplicates/geography, and inspect charts.
- Match Word code/chunks to the final Rmd and visually inspect all rendered pages.
  The DOCX renderer currently lacks a located LibreOffice executable. Do not
  claim Word validation or install a renderer under A.
- Report checks actually performed, changes, limitations, evidence, and next
  approval. Smoke fixtures are not research data or final deliverables.

The user's global personal working preferences also apply. Use relevant installed
skills; preserve unrelated work and never publish externally without approval.
