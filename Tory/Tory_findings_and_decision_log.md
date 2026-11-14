# Tory: neighbourhood analysis, findings and decision log

DataJam 2026, Vancouver short-term rental case. Data: Inside Airbnb, Vancouver, 15 June 2026, CC BY 4.0. Maps: OpenStreetMap contributors. All figures come from `make_map.py` run on `listings.csv.gz` and `neighbourhoods.geojson`. Revenue is an Inside Airbnb estimate (gross, before costs), not reported income.

## 1. How to reproduce
1. Download `listings.csv.gz` (detailed) and `neighbourhoods.geojson` from insideairbnb.com/get-data (Vancouver, 15 June 2026). Put them in the repo's `Data/` folder or `~/Downloads`. Do not commit them.
2. `python3 make_map.py` writes the summary CSVs and three interactive HTML maps next to the script.
3. `python3 make_static_maps.py` (same folder) turns the maps into slide PNGs.

| Output | What it is |
|---|---|
| neighbourhood_summary_python.csv | Listings, earning listings, earning share, median/mean revenue per neighbourhood |
| filter_steps_ranking.csv | Neighbourhood rank after each cleaning step (decision-log evidence) |
| sensitivity_big_hosts.csv | Ranking with vs without hosts that have 20+ listings |
| minnights_cutoff_test.csv | Ranking if the minimum-stay cutoff were 7, 14, 30, 60 or 90 nights |
| bedroom_summary_python.csv | City-wide 1, 2, 3 bedroom comparison |
| neighbourhood_bedroom_summary.csv | Neighbourhood by bedroom table, flag for cells under 30 listings |

## 2. Data pipeline
| Step | Listings left |
|---|---|
| All listings in the file | 6,509 |
| Entire homes only | 5,322 |
| Minimum stay of 30 nights or less | 3,906 |
| Price errors removed (over $5,000 a night) | 3,900 |

Note: 5 of these 3,900 entire homes have no minimum_nights value. The 30-night filter removes only values above 30, so it keeps them. The cutoff test (`minnights_cutoff_test.csv`) uses `<= n`, which drops them, so it shows 3,895 listings at 30 nights instead of 3,900. The top three are the same either way.

Revenue statistics use only listings with estimated revenue above 0 (3,255 of 3,900, about 84%). 24 polygon rows dissolve to 23 names because Strathcona appears twice in the geojson; the brief says 22 local planning areas, so be ready to explain the extra name.

## 3. Decision log

### Decision 1: Entire homes only
- **What:** Dropped private, shared and hotel rooms (6,509 to 5,322).
- **Why:** DDD buys whole properties; a room inside someone's home can't be purchased and operated.
- **What changed:** Ranking reshuffled. Grandview-Woodland 6th to 14th, West End 14th to 20th, Dunbar Southlands 22nd to 15th, Riley Park 4th to 2nd.

### Decision 2: Exclude stays over 30 nights (minimum_nights <= 30)
- **What:** Removed 1,416 entire homes (27%). Also the team's agreed rule.
- **Why:** A minimum stay over 30 nights is effectively a long-term rental, not the short-term product DDD is buying. Keeping them understates what a short-term unit can earn.
- **What changed:** Downtown median about $46k to about $59k. Kitsilano 6th to 3rd, Mount Pleasant 19th to 9th, West End 20th to 10th (ranks here are out of all 23 areas, including thin ones). Every median rose, so some ranks fell (Downtown Eastside 3rd to 7th) because others gained more.
- **Tested alternatives:** `minnights_cutoff_test.csv` re-ranks neighbourhoods (those with 30+ earning listings) at cutoffs of 7, 14, 30, 60 and 90 nights. Downtown, Kitsilano and Riley Park are the top three at 7, 14, 30 and 60 nights, with identical order. The data is split into two groups: only about 1 entire home has a minimum stay between 31 and 60 nights (3,895 to 3,896 listings), so any cutoff from 30 to 60 gives the same answer. Going to 90 nights adds back about 1,300 long-stay listings (5,210 total) and changes the picture: Kitsilano falls from 2nd to 5th and Mount Pleasant from 7th to 20th. That cutoff is not a short-term rental product, so we rejected it. Conclusion: the 30-night rule is not a knife-edge, and the top three do not depend on the exact cutoff.

### Decision 3: Do not rank neighbourhoods with fewer than 30 earning listings
- **What:** Greyed out Strathcona (14 earning), Fairview (18), South Cambie (30 with all hosts, 29 without large operators).
- **Why:** Right after the minimum-nights filter, Strathcona jumped 22nd to 1st and Fairview 23rd to 4th. With so few listings a handful of units sets the median, so those moves are noise. Fairview also had a $91,294-a-night price error and a cluster of cheap listings from very large operators (likely, not proven).
- **What changed:** Without the rule the "best neighbourhood" would be Strathcona on 14 listings. With it, the reliable top tier is Downtown, Kitsilano, Riley Park (1st to 3rd among areas with enough data). South Cambie sits 4th at exactly 30 earning listings with all hosts but 29 without large operators, so it is greyed out as borderline.
- **Caveat:** 30 is a rule of thumb, not derived from data. Raising it to 50 would also remove Shaughnessy (39) and Kerrisdale (47), neither near the top, so the recommendation doesn't depend on the exact number.

### Decision 4 (smaller): Remove nightly prices above $5,000
- **What:** Removed 6 entire homes (data errors, e.g. one at $91,294 a night inflated a neighbourhood mean about tenfold).
- **What changed:** Medians barely move; Fairview and Riley Park swap 4th and 5th after the min-nights filter. Fairview is excluded anyway, so no recommendation changes. Least important decision; say so if asked.

## 4. Findings

### Finding 1: Three neighbourhoods are clearly strongest, and it holds up when tested
| Neighbourhood | Earning listings | Median revenue |
|---|---|---|
| Downtown | 806 | about $59k |
| Kitsilano | 223 | about $48k |
| Riley Park | 164 | about $46k |
| Downtown Eastside | 292 | about $44k |
| Hastings-Sunrise | 177 | about $42k |

- **Validation:** Excluding hosts with 20+ Vancouver listings leaves Downtown, Kitsilano and Riley Park in the same positions.
- **Exception:** Mount Pleasant drops from 9th to 14th without large operators, so it's not a safe pick.
- Present as tiers, not exact ranks (4th to 8th move by a few places). Round to the nearest $1k.

### Finding 2: Bigger units charge more but earn only slightly more
| Bedrooms | Earning listings | Median nightly price | Median annual revenue |
|---|---|---|---|
| 1 | 1,223 | $342 | $41.1k |
| 2 | 1,163 | $419 | $41.2k |
| 3 | 505 | $514 | $44.6k |

- Revenue / price gives roughly 120, 98 and 87 booked nights a year (ratio of medians, rough).
- A 3-bedroom earns about 8% more than a 1-bedroom. Unless it costs under about 8% more to buy, return per dollar is worse. Points toward more, smaller units, but only purchase prices (Bhuvanesh's CREA table) can settle it.
- City-wide median mixes locations; check `neighbourhood_bedroom_summary.csv` before relying on it.

## 5. Risk flag: not every listing earns
About 83.5% of entire homes (3,255 of 3,900) have revenue above 0. Downtown 806 of 939 (86%), Kitsilano 223 of 268 (83%). Medians here are conditional on earning something, so a new unit has roughly a one-in-six chance of looking like a non-earner. Any expected-return figure should multiply by the earning share or explain why a professionally run unit does better. Applying about 85% to a 13-unit Downtown/Kitsilano portfolio moves a ~4.1% net cap rate to roughly 3.2% (my own calculation from the team's pro forma; rerun it in the team's code before using it).

## 6. Limitations
- One-day scrape; not an official or complete list of short-term rentals.
- Revenue and occupancy are Inside Airbnb estimates. An unavailable night may be booked or blocked; the data doesn't say which.
- Medians describe established listings; a new 2027 unit may take time to build reviews.
- Neighbourhood by bedroom groups can be small; use the `enough_data` flag.
- Listings and licences aren't counted on the same basis, so any compliance rate is an estimate.

## 7. Cross-check list for the team
- Does `clean_listings.R` apply the same filters (entire homes, minimum_nights <= 30, price errors)? Final count should be 3,900.
- Are the Q3 per-unit revenues means or medians, and do they include zero-revenue listings?
- Do the Q3/Q4 revenue totals trace to one source rather than a typed-in number?
- Are purchase prices set by neighbourhood and bedroom count, or one price for every unit?

## 8. AI assistance (for the pitch disclosure)
An AI assistant (Claude) helped write and debug `make_map.py` and `make_static_maps.py` and drafted this document. Every number was checked against script output. Anyone presenting these figures should be able to explain how they were produced.
