# Sources and method

The complete source list, including publishers, URLs, dates and access dates,
is in **data/sources.csv** and the report's optional reference list.

**data/rentals.csv** contains 276 already-cleaned native-AMD advertisements
from WSE.AM, downloaded on 5 November 2026. They advertise two rooms, 45–75 m²
and furniture, with usable road-route inputs. This file preserves the selected
IDs, rents and route values from the previous analysis. The original 949-record
extraction, screening decisions, duplicate/exclusion evidence and OSRM responses
remain in **_archive/previous-version**. Collection and source-access records
remain there too. Public access does not establish a redistribution license.

**data/tariffs.csv** holds the verified electricity, gas, water and public-fare
facts. **data/wages.csv** contains Armstat's annual wage series; the model uses
the 2025 national gross wage as a time-value benchmark. These source facts do
not measure a household's consumption or take-home pay.

The analysis compares named districts within Yerevan with Kentron and uses
Republic Square as its shared destination. Outside Kentron does not mean
outside the municipality. Road inputs are model outputs; public-transport
speed, waiting, traffic adjustment, consumption, workdays, car costs and the
value of time are explicit assumptions. The report separates cash costs from
costs including time. Heating is counted once through gas.

Each district budget combines medians of separate components; it is not the
median of observed household bills. The sample is one agency's catalogue,
not random sampling or verified completed leases. Small samples are marked.
Quartiles describe the advertisements; they are not confidence intervals.
Scenario counts are not probabilities. Unsupported population p-values are
omitted. The full household/heating/time grid and primary calculations remain
consistent with the previous version; supplementary investigations are archived.

The pinned DS116 course repository and the original course audit are preserved
in **_archive/previous-version/references/course-requirements.md**. Requirements
from previous homework remain distinct from confirmed project instructions.
The executable Rmd and Word companion are the student's requested deliverables;
HTML and PDF are supplied for reading. The project rubric, deadline and
instructor's AI policy still require confirmation before submission.

AI assisted research, code, writing and checking. The student should understand
and independently explain the analysis. No missing academic rule is assumed.

## Why these charts

| Question | Chart | Reason |
|---|---|---|
| Where is rent cheaper? | Boxplots | Show medians, variation and overlap across the observed advertisements |
| How much longer is the commute? | Dumbbell | Connect the two modeled mode times for each district |
| What does the budget include? | Stacked bars | Show the three cash components and their total |
| How much saving remains? | Waterfall | Show how extra transport and valued time reduce the initial rent saving |
| When can the answer change? | Heatmap | Compare stated time-value assumptions within one stress scenario |
| When would saving disappear? | Dot plot | Compare all district–mode thresholds with the wage benchmark |

The waterfall transparently selects the district containing the smallest
remaining baseline saving. It explains that example; the calculations and
written takeaway still cover all 20 noncentral district–mode comparisons.
