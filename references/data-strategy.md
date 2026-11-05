# Data strategy and methodological review milestone

5 November 2026. User standing authorization replaces B/C stop requests.
An independent statistician reviewed the pre-analysis plan and source metadata
before any housing-price results were calculated. Verdict: acceptable for a
descriptive agency snapshot plus conditional scenarios; not for population
significance tests, causal claims, or quality-adjusted rent estimates.

## Selected records and fixed eligibility

Use the frozen WSE.AM public catalogue factual extraction on 5 November 2026.
It contains 949 rental apartments, 933 tagged Yerevan. Source retrieval is an
observation of advertised availability, not verification that a unit remains
available or that the price was updated that day. Source creation dates are not
lease or price-update dates. Advertisements, not completed leases, are the units.
Source access and rights are documented in housing-discovery.md; no open-data
redistribution license was established. No personal contacts or images retained.

Primary screening: city tagged Yerevan, native AMD, two rooms, 45–75 square metres,
not source-flagged duplicate/part of a house, and furniture advertised. Exclude
known fallback Republic Square coordinates, explicitly named non-Yerevan town
cases, and ambiguous Avan-Arinj cases; do not silently reclassify these. Retain
one record per possible-property signature, selecting the most recently created
record by the source timestamp as a deterministic rule. This does not establish
that the selected record has a newer price or that a removed record is certainly
the same unit. Retain before/after counts and IDs in the exclusion log.

There are 302 native-AMD two-room/area candidates before furniture/geographic
screens, 278 after those screens, and 277 after conservative signature screening.
Use only route-complete, plausible-coordinate records for every primary rent and
budget comparison. Route completeness is checked without inspecting rents:
both directions available, nonnegative lengths/times, and origin snap <=250m
in each direction. The broad coordinate box is not an administrative boundary.
Districts are agency labels, not independently ground-truthed classifications.
Flag n<10 as sparse presentation, not a validity threshold. Keep all named
districts; do not pool every non-Kentron location as a geographic category.

Furniture is an advertised feature, not independently verified. Standardized
condition is missing; building type is partly missing and building year mostly
unusable. Area and rooms improve comparability without making units equivalent.
Show district area distributions. Do not claim quality adjustment.

## Evidence versus modeling

Verified official snapshots provide fare rules, electricity consumption bands,
gas tariff and 2026 no-change statement, 2026 water tariff, and Armstat annual
gross national wages through 2025. Tariff extraction is validated against retained
pages/rendered fare text. The 2025 wage benchmark is lagged and national, not a
2026 Yerevan renter's take-home wage. AMD-only selection avoids invented FX.

OSRM's public car-network table service supplies both outward and return route
distance and free-flow model duration to the declared Republic Square point
(longitude44.512600, latitude40.177600). Cache replies and request manifests.
No straight-line fallback is used; no live congestion or transit itinerary is
observed. Kentron homes retain their own nonzero journeys.

Baseline: two occupants, one commuter, 22 return-commute days per 30-day month.
Winter utilities: 150 day/50 night kWh,100m3 gas,8m3 water, equal across districts.
These consumption values are assumptions. Include electricity/gas/water only;
unobserved internet, building fees, waste, food and other spending are excluded.
Thus 'direct cost' refers to the selected housing-and-commuting components.
Heating is the gas component, never added again.

Transit: one boarding/leg; min(pay-per-ride,30-day pass), summed by commuter.
This is a specified short-horizon purchasing rule, not an all-ticket optimum.
Transit time scenario = two-way car-road km/12kmh*60 +30min for access/waiting.
It is not routed public transit. Car:60AMD/km operating allowance plus10000AMD
monthly destination parking per commuter; round-trip time=1.5*OSRM duration+10min.
These are declared assumptions and exclude full car ownership. Time value grid:
0%,25%,50%,100% of 2025 gross wage/(22*8 assumed paid hours). No lost earnings claim.

## Comparisons and robustness

Report empirical rent medians, IQRs and sample counts, not population intervals.
Model transparent district budgets with each district's sample-median rent and
median route inputs, common utilities and household assumptions. Label these
district archetypes, not median observed household bills or the median of summed
listing-level costs. Difference of medians is not a matched moving-household effect.
Use the same archetype consistently in direct, generalized and break-even outputs.

Competing signs: noncentral minus Kentron cost may be negative, zero or positive.
The predeclared two-sided null Delta=0 and alpha0.05 are documented but not tested:
convenience sampling, unverified dwelling independence, scenario outcomes and
few districts do not support the intended population inference. No manufactured
p-value or interval; IQRs show listing spread only. Regression is not necessary
to dress up missing condition information as adjustment.

Sensitivity: commuters1–2, days16/22/26, time fractions0/.25/.5/1, extra noncentral
winter gas0/75/150m3, public one/two boardings, car rates40/60/100AMD/km,
transit speeds8/12/16kmh with access/wait10/15/20min per leg. Also compare
longer-pass amortization as a separate commitment scenario, not a 30-day purchase.
Vary slow/fast modeled car congestion where useful. Explore central walking as
a separate comparator, using a stated walking-speed assumption rather than a
claimed observed walking route. No taxi or outside-town conclusion without data.

Break-even value = -direct difference/extra hours when direct difference<0 and
extra hours>0. Report already no cheaper, always cheaper over nonnegative time
values, or no time-value crossing as appropriate. A time-only break-even holds
other costs fixed; it is not a universal distance or congestion threshold.

Final route eligibility counts and monthly-rent semantics are checked before
conclusions. All actual numbers are produced by executed R. Rmd/Word labels,
code and result references must match; clean rendering and independent QA follow.

Completion update: all 277 routed origins passed the network checks. Public pages
confirmed monthly asking-price semantics; excluding mixed offer 11834 left 276
primary records. The statistician accepted the median-input budget definition
before pricing results. Full execution and independent artifact QA subsequently
passed; see validation/final-verification.md.
