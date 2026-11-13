# Tory: neighbourhood analysis, findings and decision log

DataJam 2026, Vancouver short-term rental case.
Data: Inside Airbnb, Vancouver, 15 June 2026, CC BY 4.0. Maps: OpenStreetMap contributors.
All figures below come from `make_map.py` run on `listings.csv.gz` and `neighbourhoods.geojson`.
Revenue is an Inside Airbnb **estimate** (gross, before costs), not reported income.

## 1. How to reproduce

1. Download `listings.csv.gz` (detailed) and `neighbourhoods.geojson` from insideairbnb.com/get-data (Vancouver, 15 June 2026). Put them in the repo's `Data/` folder or in `~/Downloads`. Do not commit them.
2. `python3 make_map.py` writes the summary CSVs and three interactive HTML maps next to the script.
3. `python3 make_static_maps.py` (run in the same folder) turns the HTML maps into slide-ready PNGs.

| Output | What it is |
|---|---|
| `neighbourhood_summary_python.csv` | Listings, earning listings, earning share, median and mean revenue per neighbourhood |
| `filter_steps_ranking.csv` | Neighbourhood rank after each cleaning step (decision-log evidence) |
| `sensitivity_big_hosts.csv` | Ranking with vs without hosts that have 20+ listings |
| `minnights_cutoff_test.csv` | Ranking if the minimum-stay cutoff were 7, 14, 30, 60, 89 (the legal line) or 90 nights |
| `bedroom_summary_python.csv` | City-wide 1, 2, 3 bedroom comparison |
| `neighbourhood_bedroom_summary.csv` | Neighbourhood by bedroom table, with a flag for cells under 30 listings |

## 2. Data pipeline (listing counts at each step)

| Step | Listings left |
|---|---|
| All listings in the file | 6,509 |
| Entire homes only | 5,322 |
| Minimum stay of 30 nights or less (drops 5 with no minimum stay recorded) | 3,901 |
| Price errors removed (over $5,000 a night) | 3,895 |

Revenue statistics use only listings with estimated revenue above 0 (3,250 of the 3,895, or about 83%).
Neighbourhoods: 24 polygon rows dissolve to 23 names because Strathcona appears twice in the geojson. The brief refers to 22 local planning areas, so the extra name should be explained if asked.

## 3. Decision log

### Decision 1: Entire homes only
- **What:** Dropped private rooms, shared rooms and hotel rooms (6,509 to 5,322).
- **Why:** DDD buys whole properties. A room inside someone's home is not something the fund can purchase and operate.
- **What changed:** The ranking reshuffled. Grandview-Woodland fell from 6th to 14th, West End from 14th to 20th, Dunbar Southlands rose from 22nd to 15th, Riley Park from 4th to 2nd.

### Decision 2: Exclude stays over 30 nights (`minimum_nights <= 30`)
- **What:** Removed 1,421 entire homes (27%): 1,416 with a minimum stay over 30 nights plus 5 with no minimum stay recorded. `<= 30` was also the team's agreed rule, and it matches the R code's `filter(minimum_nights <= 30)`, which drops missing values the same way.
- **Why:** A minimum stay over 30 nights is effectively a long-term rental, not the short-term product DDD is investing in. Keeping them understates what a short-term unit can earn.
- **What changed:** Downtown's median revenue went from about $46k to about $59k. Kitsilano rose from 6th to 3rd, Mount Pleasant from 19th to 9th, West End from 20th to 10th. Every neighbourhood's median rose, so some ranks fell (Downtown Eastside 3rd to 7th) because other areas gained more.
- **Tested alternatives (the cutoff does not matter):** at maximum stays of 7, 14, 30 and 60 nights the top five neighbourhoods are identical: Downtown (about $59-60k), Kitsilano ($48k), Riley Park ($46-47k), South Cambie ($45k) and Downtown Eastside ($44k). South Cambie is ranked in that test but is excluded from our recommendations under Decision 3.
- **Why not 90 nights (the legal line)?** BC's Short-Term Rental Accommodations Act defines a short-term rental as under 90 consecutive days, and Vancouver aligned its own definition on 8 October 2024 (some websites still show the old 30-day figure). In the data, only **1** entire home has a minimum stay of 31 to 89 nights, **1,314** require exactly 90 nights (legally long-term, so they are not short-term rentals) and 101 require more. So a cutoff of 30 and the legal cutoff of 89 give the same data, apart from that one listing.
- **What including the 90-night group would do:** Downtown's median falls to about $47k, Riley Park moves to 2nd and Kitsilano to 5th. Mount Pleasant drops from 7th to 20th and West End from 8th to 17th, so the legally long-term listings are concentrated in some areas and earn much less than genuine short stays. Leaving them in would distort the neighbourhood comparison.

### Decision 3: Do not rank neighbourhoods with fewer than 30 earning listings
- **What:** Greyed out and excluded Strathcona (14 earning listings), Fairview (18) and South Cambie (30 with all hosts, 29 without large operators).
- **Why:** Right after the minimum-nights filter, Strathcona jumped from 22nd to 1st and Fairview from 23rd to 4th. With so few listings, a handful of units decides the median, so those moves are noise. Fairview also had a $91,294-a-night price error and a cluster of low-priced listings from very large operators.
- **What changed:** Without this rule the "best neighbourhood" would be Strathcona, on 14 listings. With it, the reliable top tier is Downtown, Kitsilano and Riley Park.
- **Caveat:** 30 is a rule of thumb, not derived from the data. Raising it to 50 would also remove Shaughnessy (39) and Kerrisdale (47), neither of which is near the top, so the recommendation does not depend on the exact number.

### Decision 4 (smaller): Remove nightly prices above $5,000
- **What:** Removed 6 entire homes. **Why:** they are data errors (for example one listing at $91,294 a night inflated a neighbourhood mean about tenfold). **What changed:** medians barely move, but Fairview and Riley Park swap 4th and 5th place after the minimum-nights filter. Fairview is excluded anyway, so no recommendation changes. This is the least important decision, so say so honestly if asked.

## 4. Findings

### Finding 1: Three neighbourhoods are clearly strongest, and the result holds up when tested
Median estimated annual revenue per earning entire home (all hosts, final data):

| Neighbourhood | Earning listings | Median revenue |
|---|---|---|
| Downtown | 804 | about $59k |
| Kitsilano | 223 | about $48k |
| Riley Park | 164 | about $46k |
| Downtown Eastside | 291 | about $44k |
| Hastings-Sunrise | 177 | about $42k |

- **Validation:** Excluding hosts with 20+ Vancouver listings leaves Downtown, Kitsilano and Riley Park in the same positions. "We tested whether large operators drive this, and they don't."
- **Exception:** Mount Pleasant drops from 9th to 14th without large operators, so it is not a safe pick.
- **Present as tiers, not exact ranks.** The 4th to 8th places move by a few positions depending on assumptions. Round to the nearest $1k.

### Finding 2: Whether bigger units pay depends on the neighbourhood
City-wide, bigger units look like a poor deal. Median annual revenue by bedrooms (earning entire homes):

| Bedrooms | Earning listings | Median nightly price | Median annual revenue |
|---|---|---|---|
| 1 | 1,222 | $342 | $41.1k |
| 2 | 1,159 | $419 | $41.4k |
| 3 | 505 | $514 | $44.6k |

City-wide, a 3-bedroom earns only about 9% more than a 1-bedroom while charging about 50% more per night. Revenue divided by price gives roughly 120, 99 and 87 booked nights a year (a back-of-envelope ratio of medians, based on Inside Airbnb's own estimates), so larger units book fewer nights.

**That city-wide pattern hides big differences between neighbourhoods** (`neighbourhood_bedroom_summary.csv`, medians, earning listings in brackets):

| Neighbourhood | 1 bedroom | 2 bedrooms | 3 bedrooms |
|---|---|---|---|
| Downtown | $52.3k (360) | $63.1k (298) | $68.2k (110) |
| Kitsilano | $50.3k (73) | $48.5k (90) | $38.4k (34) |
| Riley Park | $44.9k (53) | $45.9k (60) | $31.4k (34) |
| Downtown Eastside | $40.9k (159) | $41.1k (96) | too few (19) |
| Hastings-Sunrise | $33.2k (57) | $39.0k (68) | too few (29) |

- **Downtown rewards size:** a 2-bedroom earns about 21% more than a 1-bedroom and a 3-bedroom about 30% more.
- **Kitsilano and Riley Park do not:** a 1-bedroom earns as much as a 2-bedroom, and 3-bedrooms earn less (those 3-bedroom groups are small, 34 listings each).
- **The right size therefore depends on where DDD buys, and on what each size costs.** A Downtown 2-bedroom is only a better investment than a 1-bedroom if it costs less than about 21% more. Only the purchase prices (Bhuvanesh's CREA table) can settle that, and they need to be by area and bedroom count.
- **Means are well above medians in Downtown** (the 3-bedroom mean is about $84k against a median of $68k) because a few listings earn a lot. Use medians for expected revenue, and treat the means as the optimistic tail.
- **Do not build a plan on groups under 30 listings** (the `enough_data` flag marks them).

## 5. Risk flag for the investment model: not every listing earns

About 83% of entire homes (3,250 of 3,895) have revenue above 0. In Downtown it is about 86% and in Kitsilano about 83%. Of the roughly 17% without revenue, 562 listings (about 14%, or one in seven) have an estimated revenue of exactly zero and 83 (about 2%) have no estimate at all.
Revenue medians and averages in this folder are **conditional on earning something.** A newly bought unit has roughly a one in seven chance of looking like a listing with zero estimated revenue, plus a small chance of having no estimate. Any expected-return figure should either multiply by the earning share or explain why a professionally run unit would do better. Applying about 85% to a 13-unit Downtown/Kitsilano portfolio moves a ~4.1% net cap rate to roughly 3.2%. That figure is my own calculation from the team's pro forma, so rerun it in the team's code before using it.

## 6. Limitations
- One-day scrape. Not an official or complete list of short-term rentals.
- Revenue and occupancy are Inside Airbnb estimates, not reported figures. An unavailable calendar night may be booked or blocked, and the data does not say which.
- Medians describe existing, established listings. A new unit in 2027 may take time to build reviews.
- Neighbourhood by bedroom groups can be small. Use the `enough_data` flag.
- Listings and licences are not counted on the same basis, so any compliance rate is an estimate.

## 7. Cross-check list for the team
- Does `clean_listings.R` apply the same filters (entire homes, `minimum_nights <= 30`, price errors)? Our final count is 3,895 listings.
- Are the per-unit revenues in Q3 means or medians, and do they include zero-revenue listings? His inputs sit close to our **medians**, not our means: Downtown 2-bed $62,647 vs our median $63,092, Kitsilano 1-bed $50,535 vs $50,293, Kitsilano 2-bed $50,010 vs $48,518, and Downtown 1-bed $49,153 vs $52,290 (6% lower). Ask which filters he used, especially for Downtown 1-bed.
- Do the Q3/Q4 revenue totals trace to one source, rather than a typed-in number?
- Are purchase prices set by neighbourhood and bedroom count, or is one price used for every unit?

## 8. AI assistance (for the pitch disclosure)
An AI assistant (Claude) helped write and debug `make_map.py` and `make_static_maps.py`, and drafted this document. Every number here was checked against the script output. Anyone presenting these figures should be able to explain how they were produced.
