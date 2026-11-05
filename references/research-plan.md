# Research and implementation plan

Date: 5 November 2026. The user's instruction to continue until the end supplies
standing authorization for the remaining phases. B and C are documented review
milestones rather than additional stop requests. No public-source records had
been obtained when this plan was written.

## Research design and defaults

Question: for comparable long-term apartments, do rent savings relative to
central Yerevan exceed extra transport, utilities/heating, and optionally valued
commuting time? This is an associational market-and-scenario study, not a causal
estimate of what happens when a household moves. Primary unit: unique advertised
apartment, if verifiable listings are obtainable. Otherwise use a clearly labeled
district-level source comparison; never pretend aggregates are individual listings.

Use Republic Square as the common destination. Distinguish Kentron, named other
Yerevan administrative districts, and named towns outside the municipality. Begin
with Yerevan; include Abovyan/Masis only if comparable rent and journey evidence
exists. Do not treat outside Kentron as synonymous with peripheral or outside
Yerevan. No arbitrary straight-line distance becomes a network travel estimate.

Target long-term entire apartments with two rooms (one bedroom plus living room),
45–75 square metres, similar condition/furnishing where observed. Unknown
attributes remain unknown. Record exclusions and representativeness. Prefer a
single source/observation window to pooling incompatible markets. If these filters
leave insufficient support, explain any broader comparable sample before using it.
Aim for 150+ distinct observations with coverage outside Kentron; this is a
feasibility target, not a power calculation or a promise of representative sampling.
If only a small convenience sample can be obtained, descriptive conclusions and
scenario break-even calculations take priority over significance tests.

Baseline household: two adults sharing one apartment, one commuter, 22 commuting
days/month, one return trip/day. Report AMD/month. Core comparisons: public
transport and private car. Taxi is optional only with reproducible fare evidence.
Use source-period exchange rates if rents are in another currency; do not apply
an undocumented current rate to historical rents. The study's effective period is
the available rental observation window, not automatically the retrieval date.

Direct cost = rent + utilities (heating included once) + transport.
Generalized cost = direct cost + commuting hours times AMD/hour time value.
Use zero time value, and sensitivity at 25%, 50%, and 100% of a clearly defined
net/gross hourly wage benchmark; if no suitable wage is verified, label an explicit
AMD/hour scenario grid as assumptions. Wage averages are not each renter's income.
The no-time scenario equals direct cost. Uniform verified tariffs do not establish
geographic differences in consumption. Use equal apartment utility consumption
as baseline unless differential evidence exists, then transparent winter/efficiency
stress scenarios. Modeled bills and journey times are never actual household bills
or observed peak travel times. Do not infer a universal distance threshold if the
data only permit a conditional time or rent-saving threshold.

## Numbered execution plan

| Step and objective | Owner | Inputs and actions | Output and completion criterion | Dependency and authorization |
|---|---|---|---|---|
| 1 Define question/scope | Coordinator | Brief and course evidence; lock outcomes, destination and households | This plan, with assumptions stated | Completed under standing authorization |
| 2 Challenge hypotheses | Statistician | Plan; define competing explanations and estimands before results | Written methodological review, corrections applied | 1; standing authorization |
| 3 Discover rental evidence | Researcher | Public Armenian/market/archived open sources; inspect records, access rights and timestamps | Obtained records or explicit evidence gap; no invented sample | 1; standing authorization, no bypass/manual survey |
| 4 Verify transport evidence | Coordinator/researcher | Municipality, official operators, public network sources; check fares, validity and modes | Dated source records and observed-versus-modeled journey definitions | 1; standing authorization |
| 5 Verify utilities/wages/FX | Coordinator | Official regulator, utilities, Armstat/CBA; inspect actual tables and units | Source register, verified constants, explicit scenario inputs | 1; standing authorization |
| 6 Define geographic comparisons | Coordinator/statistician | Observed locations; administrative names and central destination | Named comparable groups, outside-municipality exclusion/extension justified | 3–5; standing authorization |
| 7 Freeze data strategy | Statistician | Discovery inventory, completeness, duplicates, sample support | Milestone C memo with final estimands, exclusions, methods and limits | 2–6; independent review required, user pause waived |
| 8 Clean/validate evidence | Coordinator | Immutable raw records and source ledger | Reproducible processed data, exclusion/missingness/duplicate log | 7; standing authorization |
| 9 Model commuting costs | Coordinator | Fare rules, mode assumptions, travel evidence, household grid | No double counting; direct costs/time by mode with units | 7–8; standing authorization |
| 10 Model heating/utilities | Coordinator | Tariffs, apartment characteristics, consumption scenarios | Monthly/winter utility assumptions clearly separated from observations | 7–8; standing authorization |
| 11 Estimate comparisons | Coordinator/statistician | Approved sample, models and assumptions | Effect estimates; CIs/p-values only if justified, otherwise explanatory omission | 7–10; standing authorization |
| 12 Visualize and test robustness | Coordinator | Executed estimates, mode/household/time/utility grids | Approximately 5–7 strong charts with readable labels and limitations | 11; standing authorization |
| 13 Author main Rmd | Coordinator | Actual executed results and references | One Rmd with required explanation structure for every substantive chunk, clean HTML render | 8–12; standing authorization |
| 14 Author Word companion | Coordinator | Extracted final chunk code and results, bundled document tooling | One DOCX with matching labels/order/code, meaningful block explanations and references | 13; standing authorization, renderer must work |
| 15 Independently verify | QA | Final files, source records, formulas, rendered pages | Numerical and code-matching checks; clean R execution; every Word page inspected | 13–14; standing authorization |
| 16 Deliver conditional conclusions | Coordinator | QA evidence and limitations | Two principal files plus rendered analysis, concise completion note, disclosed gaps | 15; no external publication |

## Candidate sources and acquisition risks

Armstat, Cadastre, Yerevan Municipality, PSRC, CBA, official utilities/operators,
public housing listings or properly documented open rental datasets, and OSM are
leads only. Verify URLs, actual records, variables, units/dates, geographic/sample
coverage, access restrictions/licensing, and reproducibility before recommending
them. Prefer direct lawful downloads. Preserve source snapshots and retrieval
metadata; never bypass CAPTCHAs or logins. No paid API or new external account.
Public availability alone is not a redistribution license. Store only analytical
listing fields, not phone numbers, owners' names or photographs. If redistribution
is unclear, retain a small factual research extraction with citations and note the
restriction instead of claiming an open-data license.

Listing selection, duplicate advertisements, unobserved quality and inaccurate
locations are major risks. Maps/routes may be approximate and not live congested
journeys. Tariffs can change or depend on packages, eligibility and validity.
Record years and scenario dates separately. If observed heating or commute data
are absent, use labeled scenarios and do not invent location effects.

## Hypotheses, statistics and charts

Define Delta as adjusted cost for a named noncentral comparison minus Kentron.
Competing possibilities are Delta < 0, = 0, or > 0. For any valid inferential
comparison use a two-sided null Delta = 0 at alpha 0.05, with effect sizes and
intervals; positive Delta supports the narrower hidden-cost claim. Rents may
decline while total costs still remain lower away from Kentron. Pre-specify any
secondary rent-versus-journey association separately. Statistical significance
does not establish causality, practical importance, or a universal recommendation.

Choose descriptive summaries, matching/regression, conditional bootstrap or
permutation inference only after seeing the sample structure, not its preferred
conclusion. Few geographic clusters or a tiny purposive sample may preclude
meaningful p-values. Repeated mode/wage scenarios do not enlarge the sample.
Report modeled scenario ranges separately from sampling uncertainty. A break-even
curve is algebra from assumptions, not proof that an empirical crossing exists.

Prioritize a rent/comparability chart, direct-cost composition, generalized cost
by mode, rent-savings versus extra-cost chart, and sensitivity/break-even chart.
Add a map and statistical interval plot only when the data justify them. Avoid
redundant plots or maps suggesting precise locations from district-only evidence.

## Documents, verification and delivery

Main Rmd: title/context, question/hypotheses, source quality, geography/households,
data preparation, exploratory plots, separate cost outcomes, justified inference,
sensitivity, conditional conclusion, limitations and references. Every substantive
chunk has the full user-required explanation structure; numerical narratives use
executed objects/inline R rather than hand-entered outcomes.

Word: cover, navigable contents, overview/methods/sources, explanations in identical
chunk order, extracted numbered code, meaningful line/block explanations, expected
versus actual results, statistical/visualization guidance, limitations and references.
Use a restrained academic layout. Inspect all rendered pages, not just text XML.

Tests cover missing/duplicate/invalid values, currencies and geography, manual
formula spot-checks, zero-time identity, commuting-count scaling, no double counting,
break-even substitution and chart/source consistency. Execute from a clean R session
with relative paths. Compare Word code text/hash and chunk identifiers against the
final Rmd. Verify cited source URLs and disclose failures. No slides or additional
long user-facing report. Supporting discovery/strategy/QA logs remain in project.

Current instructor submission specifications and AI policy remain unconfirmed.
Use transparent AI documentation and beginner explanations; do not claim course
permission. Deadline is unspecified. HTML is the provisional rendered output.
