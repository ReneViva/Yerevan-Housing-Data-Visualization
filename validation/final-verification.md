# Final research and artifact verification

Completed 5 November 2026 under the user's standing continuation instruction.
The statistician accepted the descriptive scenario design before pricing results.
Independent QA subsequently checked source records, calculations, code and pages.
No remaining material defect was found in the reviewed scope.

| Check actually performed | Verified result |
|---|---|
| Housing snapshot | SHA256 matches retained acquisition metadata |
| Sample membership | Independently reconstructed 949 → 933 → 323 → 302 → 290 → 278 → 277 → 276; processed IDs match |
| Exclusions | Mixed offer 11834/geographic flags removed; possible signature record 12686 screened conservatively |
| Network evidence | All 14 cached hashes and every outward/return extracted value checked; final 276 origins complete, snaps within 250 m |
| Official sources | Nine snapshot hashes and rendered fare-text hash match; tariffs, units and gross wage definition checked |
| Independent arithmetic | All 22 budgets, 20 thresholds, 1584 household/heating/time rows, 66 travel rows and 10 transfer comparisons agree |
| Tests | Six launcher tests and financial helper tests exited 0; hand-derived and zero-time/additive/threshold identities pass |
| R execution | All 16 Rmd chunks rendered in a fresh --vanilla R 4.5.0 session; HTML generated |
| Figures | All six final PNGs inspected by coordinator and independently by QA; initial equality-line/legend/slice issues corrected |
| Word code | All 16 ordered labels, 394 numbered code paragraphs, code hashes and actual-result narratives match final Rmd |
| Word links | All 38 internal anchors resolve; manifest source/guide/results hashes current |
| Word appearance | Every individual native-size page PNG, 01–24, inspected by independent QA; representative pages also inspected by coordinator |
| PDF bounds | All 24 pages parsed; no text outside 12-point safe page boundaries |
| Source links | All 17 reference/documentation URLs HTTP 200; PSRC uses ordinary GET after HEAD rejection |
| HTML | Six embedded charts load; no unresolved inline R, missing images or console errors; desktop and mobile/reduced-motion DOM checks show no page overflow, with internal table scrolling |

Final independently reviewed hashes:

- Rmd: `1558e058659b3485a4f90e18b1207d395e6282bc59fee08c434c6f4c71573e30`
- DOCX: `44df5c72f1b57d1c7430b47b9f2b5d5ffc62163564c766743e8cef8f87993302`

Supporting result CSV/JSON, session information, manifest and URL checks remain
in the project. The direct-cost definition covers selected components only.

## Result and scientific limits

The primary sample contains 276 advertisements across 11 agency-labeled districts.
Kentron's median asking rent is 500000 AMD; other medians are 350000–400000 AMD.
Modeled winter utilities are 24769.36 AMD and half the hourly benchmark is
861.19318 AMD/hour. All ten noncentral examples are cheaper at baseline in each
mode. Exactly two selected grid rows reverse, both Davtashen public-transport
examples with two commuters, 26 days, full hourly benchmark and extra gas of
75/150 m³. These counts are not probabilities.

This does not establish representative citywide costs, causality, dwelling-quality
adjustment, observed bills/commutes, a universal geographic threshold, or statistical
significance. No p-values or population confidence intervals were fabricated.
Source selection, sparse groups, missing condition, approximate geography and
scenario assumptions remain material limitations disclosed in both documents.

## Technical limits and rendering fallback

The packaged renderer was attempted and exited 1 because soffice.exe was absent;
see packaged-renderer.log. An earlier combined official LibreOffice download/
extraction command was rejected by automatic tool review before dispatch. It was
not retried, and no installer was downloaded. The safe fallback used existing
Microsoft Word in a dedicated invisible, macro-disabled instance, opening only
our generated DOCX read-only without a recent-file entry, exporting an internal
PDF and quitting/releasing its own instance. Existing Poppler rendered all pages.
This is native Word/Poppler validation, not a successful LibreOffice render.
No R package or office software was installed.

Browser screenshot exports were denied by that tool's workspace policy and are
not claimed. HTML checks above are DOM checks; actual chart PNGs were inspected.
Six pre-existing package-build warnings were recorded in the final analysis
(the broader setup smoke used seven warning-emitting packages). Successful
execution is not comprehensive package-compatibility certification. Live new-agent
name registration and actual RStudio execution were not verified; existing agent
tools received role briefs. No remote publication, new account or global user
configuration change occurred. The project rubric, deadline, submission format
and AI policy remain unconfirmed and need instructor confirmation.
