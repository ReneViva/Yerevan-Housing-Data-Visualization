# Housing dataset discovery and validation

Researcher audit, 5 November 2026. This is a source/quality record, not a cost
analysis or a claim about which location is cheaper overall.

## Selected evidence

| Dataset | Direct source | Variables and coverage | Status | Recommendation and limitations |
|---|---|---|---|---|
| WSE.AM active long-term apartment catalogue factual extraction | https://wse.am/api/properties | Listing ID, original asking price/currency, rooms, area, source city/district, coordinates, floor, building/new-build fields, advertised feature indicators and source creation timestamp | Downloaded and validated as a factual snapshot: 949 rental apartments; 933 source-tagged Yerevan | Primary source. A single-agency convenience catalogue, not executed leases or a representative Yerevan sample. Unknown condition; inaccurate geography and possible duplicates need exclusions/checks. |
| WSE.AM November 2026 rent index | https://wse.am/indeks-arendy-erevana/2026-11.csv | Frozen district/room medians in AMD and USD, as of 1 November 2026; includes a separate later sale-price section | Downloaded; CSV contents inspected against publisher's methodology page | Aggregate fallback/context only. Do not pool with individual listings or treat cells as household observations. Units and source date differ from current catalogue snapshot. |
| YerevanEstate segment rental-yield API | https://www.yerevanestate.am/en/ai | Public aggregate rental/sale metrics for specified building and renovation segments; individual listing access requires Premium | Accessible public documentation and an example aggregate response inspected; no research file acquired | Alternative aggregate lead only. Reported sample definitions mix sale/rent context and need investigation before use. No Premium account or connector created. |
| glenstorm/rent_in_armenia_git2 | https://github.com/glenstorm/rent_in_armenia_git2 | Scraper/dashboard source code, repository root inspected | Candidate, unsuitable as an already-available validated dataset | No downloadable research records identified in inspected root. Did not run source scraper or assume collection rights. |
| izirento/izirento-armenia-rent-index | https://github.com/izirento/izirento-armenia-rent-index | Rent/landlord rules compilation, as described in repository inventory | Candidate, not individual apartment rental evidence | Not a substitute for comparable listing observations. |

Publisher: WSE.AM, a private real estate agency. Primary source context:
https://wse.am/en/apartments-for-rent-yerevan . Asking monthly rents are published
in a catalogue that distinguishes `rent`, `daily_rent`, and `sale`. Extraction
kept only `rent` plus `apartment`; houses, land, commercial space, daily rentals
and sale objects were excluded. Source `active` is the agency's assertion, not
independent confirmation that a unit remains available.

Snapshot obtained at **2026-11-05T14:57:52.1641557Z**. API had 1,808 objects of all
types. Retained rental apartment source creation timestamps range from 3 June to
5 November 2026. **Creation timestamp is not the price-update, lease-signing, or
price-observation date.** This study may describe the active catalogue as
published at retrieval, rather than historical rents on each creation date.

## Acquisition and retained files

- `scripts/acquire-housing.ps1`: one public catalogue GET, plus robots and the
  published frozen-index download. Uses normal Windows HTTPS validation; no
  tokens, browser session, proxy rotation, login or CAPTCHA workaround.
- `data/raw/housing_wse_catalogue_facts_2026-11-05.csv`: immutable whitelisted
  factual extraction of all 949 long-term rental apartments, including other
  source cities so subsequent scope exclusions can be reproduced.
- `data/raw/housing_wse_metadata_2026-11-05.json`: source/retrieval/selection
  metadata, full-response UTF-8 content hash and saved CSV hash.
- `data/raw/housing_wse_robots_2026-11-05.txt`: preserved access rules.
- `data/raw/housing_wse_rent_index_2026-11-05.csv`: publisher's frozen index file,
  not mixed into the individual apartment sample.

Rereading the frozen files does not require a network connection. Reacquisition
requires PowerShell 7 and changes the live population. The script refuses to
overwrite an existing snapshot; a new label is required for a different snapshot.
No package was installed. Python's bundled HTTPS trust store rejected an expired
certificate on this site; normal `Invoke-WebRequest` using Windows trust worked.
Certificate validation was never disabled.

### Access and reuse boundaries

The inspected https://wse.am/robots.txt explicitly allows `/api/properties` and
AI crawlers. The public site includes an AI-context file. Access is reproducible
without authentication. The only linked policy located was the privacy policy
at https://wse.am/en/privacy ; it does not establish an open-data license.
The catalogue footer reserves rights. **Robots allowance is not a redistribution
license or legal opinion.** This is a limited factual academic extraction with
attribution; do not republish the full catalogue or claim a CC/open-data license.

No descriptions, photographs, contact names, phone numbers, messaging handles,
agent records, or unredacted street/building numbers are saved. Street labels
replace numeric tokens with `[number]`. Source URLs retain their public slugs so
records can be traced. A one-way property signature is calculated before address
redaction to screen for possible repeated units. Exact addresses are not retained.
Coordinates are source-advertised locations, not independently verified homes.

## Preliminary comparable sample and checks

Before inspecting rent outcomes, the specified eligibility screen is: source city
Yerevan, active, long-term entire apartment, exactly two total rooms, 45–75 m2,
not source-flagged duplicate/part-of-house. This gives **323 distinct listing IDs**.
Use native AMD-priced listings for the primary analysis: **302**, excluding 21
USD-priced observations without introducing a foreign-exchange assumption.

| Source district | AMD observations before geography/deduplication review | Distinct coordinate pairs | Repeated fallback-centre coordinates |
|---|---:|---:|---:|
| Kentron | 101 | 86 | 3 |
| Arabkir | 80 | 66 | 2 |
| Ajapnyak (source spelling Achapnyak) | 27 | 22 | 2 |
| Malatia-Sebastia | 20 | 20 | 0 |
| Nor Nork | 17 | 15 | 2 |
| Avan | 15 | 14 | 0 |
| Kanaker-Zeytun | 11 | 10 | 0 |
| Davtashen | 10 | 10 | 0 |
| Shengavit | 8 | 7 | 1 |
| Erebuni | 7 | 6 | 0 |
| Nork-Marash | 6 | 6 | 0 |

These are preliminary counts, not final analytical sample sizes. Nubarashen has
no observation meeting this screen. City/district labels remain publisher fields
until geography review; do not conflate other districts with outside Yerevan.

### Monthly price and long-term category confirmation

Follow-up public-page checks are recorded in
`data/raw/housing_monthly_semantics_2026-11-05.txt`. IDs 14552, 14529 and 14394
have an explicit long-term deal label and monthly price-period title. The general
rental landing page says rent is paid monthly and typical leases are 6–12 months.
A daily comparator (13697) is instead API-classified `daily_rent` and its page
labels its price per day/night. Thus source `rent` has corroborated monthly,
long-term-category semantics; it is not merely an unexplained API token.

However, ID **11834** (two rooms, 60 m2, AMD) explicitly offers both daily and
long-term rental. Its displayed price is explicitly monthly. A follow-up
in-memory description keyword screen identified this and five-room ID 12292;
the latter is already ineligible. Conservative exclusion of 11834 or a separate
mixed-offer sensitivity is recommended. Keyword screening does not certify all
other offers as exclusive long-term leases. Advertised future availability and
bounded lease periods also occur. Describe the variable as **advertised monthly
asking rent in the agency's long-term category**, with realized duration,
availability and lease conditions unverified. No new primary cost analysis was
performed, and the original immutable factual snapshot was not changed.

- All 302 preliminary AMD records have coordinates and district labels. This
  establishes completeness, not positional accuracy. Ten share the exact point
  **40.1776, 44.5126**, across five source districts. This strongly suggests a
  fallback/geocoding location; flag these points rather than treating them as
  verified journeys. Other coordinates also repeat, sometimes plausibly within
  a building. Coordinate spread varies within districts rather than every record
  having one district centroid.
- ID **14196** says Masis in its source address but city Yerevan/district Kentron,
  and uses that fallback point. Exclude this obvious municipal mismatch from the
  Yerevan comparison; never recode it into a valid Masis comparative sample.
- IDs **12868** and **10570** mention Avan-Arinj. Their border location needs a
  municipal/boundary check; the name alone does not establish outside-Yerevan
  status.
- IDs **14490** and **12686** share source city/district/address, area, rooms,
  floor and coordinates. They are a potential duplicate pair, not proven to be
  the same apartment; document any conservative deduplication and sensitivity.
  Different units at a building can legitimately share these attributes.
- Source duplicate flags are false for every retained record. This does not
  prove uniqueness. `is_part_of_house_source` is numeric `0`; duplicate and
  feature fields may be textual booleans after CSV import. Parse both formats.
- No nonpositive rent appears in all 949 retained records. No inference about
  plausible market bounds was imposed during acquisition.
- Among the 302 candidates, 290 advertise furniture. The other 12 are **not
  established unfurnished**. Every record lacks a standardized observed
  renovation/condition value; 74 lack a building-type value; 298 have no usable
  positive year-built value. New-building indicator is advertised for 161.
  Matching on unobserved condition is impossible; do not imply quality equivalence.
- `source_price_usd` is retained only for provenance. It is the website's
  conversion, not an independently verified historical exchange rate; primary
  native AMD rents avoid relying on it.

The hash signature is a possible-property screening aid. Do not use the redacted
street label itself as a duplicate key, since many distinct buildings share it.

## Verification actually performed

API HTTP 200 and returned schema inspected. Catalogue and robots HTTP 200 checked.
A constructed retained listing URL was requested and returned HTTP 200. CSV
parsed, record counts/ID uniqueness/eligibility/currency/geographic flags and
missingness checked. Saved CSV SHA256 matches metadata. A second invocation
correctly rejected overwriting before network requests, and the raw hash stayed
unchanged. No rent-cost analysis, inference or claim of representative sampling
was performed by this researcher.

Frozen-index methodology at
https://wse.am/en/indeks-arendy-erevana/2026-11 says records are asking prices,
daily rentals and other property types excluded, duplicates counted once, medians
shown only for cells with at least five listings, and values frozen. Its CSV has
two separate sections: rent medians and sale prices. The source uses 360.14 AMD
per USD for that issue. These agency assertions were read, not independently
reconstructed from the current, later catalogue.
