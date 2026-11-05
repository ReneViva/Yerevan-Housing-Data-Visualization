# Dataset discovery and selection

Retrieved and checked 5 November 2026. Reference links were checked again at the
end: all 17 returned HTTP 200. PSRC rejects HEAD but ordinary GET succeeded.

| Dataset and direct link | Variables and coverage | Quality and limitation | Status and recommendation |
|---|---|---|---|
| [WSE public API](https://wse.am/api/properties) | 1808 source objects; factual extraction of 949 rental apartments, 933 tagged Yerevan; asking rent, currency, rooms, area, district, features, coordinates, IDs and creation dates | One-agency convenience catalogue; unstandardized condition and approximate geography; no open redistribution license | Downloaded and validated. Primary sample: 276 records. Immutable CSV/hash retained |
| [WSE frozen November index](https://wse.am/indeks-arendy-erevana/2026-11.csv) | Agency aggregate rent medians by district/rooms, frozen 1 November; a later section contains sale prices | Different aggregation/date; source methodology not independently reconstructed | Downloaded and inspected. Context only; not pooled into listing analysis |
| [Official city fares](https://transport.yerevan.am/) | 150 AMD/boarding, 9000 AMD/30-day pass, 90000 AMD/annual pass | Rates, not journeys. Raw HTML is a shell; rendered fare text was saved | Downloaded and validated. Use declared 30-day purchasing strategy |
| [ENA tariffs](https://www.ena.am/Info.aspx?id=11&lang=2) | Household day/night rates by monthly consumption band | Consumption and actual bills are unobserved; standard eligibility only | Downloaded and validated. Apply the 200 kWh band to explicit baseline usage |
| [PSRC gas rate](https://www.psrc.am/contents/newsPress/gas-tariff-22) and [2026 confirmation](https://psrc.am/contents/page/posts/natural-gas-tariffs-for-residents-will-stay-unchanged) | 143700 AMD/1000 m³; unchanged resident payments from August 2026 | No heating consumption or efficiency observations | Downloaded and validated. Consumption remains a winter scenario |
| [Veolia 2026](https://www.veolia.am/en/news/2026-drinking-water-tariff-consumers-will-not-increase) and [units](https://www.veolia.am/en/consumers/frequently-asked-questions) | 200.42 AMD/m³ standard metered water plus wastewater, including VAT | Actual use absent; nonmetered/vulnerable rules differ | Downloaded and validated. Explicit 8 m³ assumption |
| [Armstat CSV](https://armstat.github.io/sdg-data-armenia/prod/en/headline/8-5-1-a.csv) and [metadata](https://sdg.armstat.am/8-5-1-a-iframe/) | 2015–2025 national gross nominal wage; 2025 = 303140 AMD/month | National pretax mean, not current personal net income; paid hours assumed | Downloaded and validated. Time-value benchmark only |
| [OSRM API definition](https://project-osrm.org/docs/v26.5.0/http) | 277 origins in both directions to Republic Square; 14 cached network-response batches | Car model using OSM, not live traffic or transit; original network-data version not returned | Downloaded and validated. All 276 primary records have complete routes; no straight-line fallback |

The official tariff extraction has 11 fact rows; Armstat has 11 annual records.
Monthly rent semantics were checked against three eligible pages, a daily-rent
comparator and a mixed-offer page. Mixed offer 11834 was excluded conservatively.
Known placeholders, a Masis mismatch and Avan-Arinj ambiguities were screened.
Possible-property signature record 12686 was removed. This does not prove all
remaining advertisements represent independent dwellings.

The course's district shapefile remains a candidate requiring provenance,
licensing, date, geometry and attribute checks. It was not downloaded as research
evidence and does not ground-truth labels. Cadastre transaction rents,
representative utility bills, measured peak journeys, usable transit routing,
taxi quotations and matched Abovyan/Masis samples were not obtained. This is not
a claim that such sources cannot exist. No observations substitute for these gaps.

Access and rights are detailed in housing-discovery.md and source metadata.
Robots permission is not an open-data license. Contacts, images and descriptions
were omitted; retained public listing URLs may contain address slugs, so the
extraction is not fully anonymized. Do not republish it as openly licensed data.
