# The Airbnb Vancouver Problem
## Business Case Brief · SFU DSSS DataJam 2026

Data-Driven Developments (DDD), a fictional private real estate fund, will put $10M CAD into BC short-term rental property. Your team recommends where, how many properties and what mix, then defends it to DDD's investment committee in 10 minutes.

---

### Sections
1. The Scenario (Page 2)
2. Background (Page 3)
3. Your Task (Page 4)
4. Data (Page 5)
5. Deliverables (Page 7)
6. How You Will Be Judged (Page 8)
7. What a Strong Pitch Looks Like (Page 9)
8. AI Use and Rules (Page 11)
9. Sources (Page 12)

---

### SECTION 1: The Scenario
You are an analytics consultancy retained by DDD. The fund has a $10M CAD mandate to deploy into BC short-term rental property, with a stated preference for Metro Vancouver. In 10 minutes you will present your recommendation to DDD's investment committee, who are also your judges. The committee does not want a model. They want a decision, a number and a reason to believe you.

| Item | Detail |
| :--- | :--- |
| **Client** | Data-Driven Developments (DDD), a fictional private real estate fund |
| **Mandate** | Deploy $10M CAD into BC short-term rental property |
| **Stated preference** | Metro Vancouver |
| **Properties operational** | January 1, 2027 |
| **Performance measured** | January 1, 2028 (the full 2027 calendar year) |
| **Your call** | Where, how many properties, what type and mix |
| **Central trade-off** | Few high-value properties vs. many modest ones |
| **Audience** | DDD's investment committee (the judges) |
| **Format** | **Preliminary round:** 7-minute pitch + 3-minute Q&A<br>**Final round:** 10-minute pitch + 5-minute Q&A |

- The mandate covers all of BC; Metro Vancouver is the fund's preference. A recommendation elsewhere should say why.
- **Simulation rule: ignore the principal residence requirement.** In real life, BC only allows short-term rentals in the host's own home (plus one secondary suite on the same property). That rule would stop an investor like DDD from buying properties just to rent them out short-term. For this case, assume the rule does not apply: DDD can buy properties purely to run as short-term rentals, and your job is to maximize the value of that investment. All other rules, such as business licences and provincial registration, still apply.

---

### SECTION 2: Background
This is the real-world regulatory context behind the data. For the simulation, the principal residence requirement is set aside (see The Scenario).

- **May 1, 2024:** BC's Short-Term Rental Accommodations Act (STRAA) took effect. Its principal residence requirement limits short-term rentals to the host's own home, plus at most one secondary suite or accessory dwelling on the same property. It applies in more than 60 BC communities, roughly those over 10,000 people. A separate investment property can no longer be run as a short-term rental.
- **2025:** The provincial registry went live, and platforms began validating registration numbers.
- **June 1, 2026:** Kelowna became the first municipality to opt out. A local government may request an exemption if its rental vacancy rate has been at or above 3% for two consecutive years. Kelowna's exemption is narrower than headlines suggest: it covers designated tourism zones and approved STR sub-zones, and local licensing and zoning still apply. The precedent is public, and the trigger is a published statistic.
- **Vancouver:** The requirement is fully in force. Operators need both a provincial registration number and a City of Vancouver business licence, shown on the listing, and platforms must remove listings without them. In April 2026 the City counted 4,969 active listings, 3,248 business licences and 69 licence suspensions.
- **From 2027:** The Province has moved the opt-out request deadline to Feb. 28 and the effective date to June 1. A request made after DDD's properties go live could therefore take effect partway through the measured year.
- **Regulatory timeline · 6 dates, 2024 to 2028:** An opt-out requested by Feb. 28, 2027 could take effect on June 1, five months into DDD's measured year.
- Listings and licences are not counted on the same basis, so any compliance rate you compute from them is an estimate.

---

### SECTION 3: Your Task
Your job is to answer a single question for DDD, backed by evidence: given what the data shows, where should DDD put its $10M CAD to maximize the value of the investment, and what are the biggest risks to that plan?

All teams work on the same challenge: deciding how DDD should invest its $10M. A complete recommendation covers:
- **Where:** which market or markets, and which neighbourhoods within them.
- **What:** property types, and the mix across them.
- **How many:** the number of properties, and where you land between few high-value and many modest ones.
- **Expected 2027 performance** with the assumptions behind it. Define your return metric and say why you chose it.
- **Uncertainty and risks:** the range around your number, the key risks, and how you would mitigate the most impactful ones.

The common dataset covers the City of Vancouver only, so a recommendation elsewhere needs outside data you can defend. Cross-market comparison is welcome where it earns its place, not as decoration.

---

### SECTION 4: Data
Every team works from the same Inside Airbnb Vancouver snapshot dated June 15, 2026. Anything you add must be public and defensible.

- **Source:** Inside Airbnb, Get the Data, Vancouver, 15 June 2026. Credit it on your slides:
  > `Data: Inside Airbnb, Vancouver, 15 June 2026, CC BY 4.0.`
- Use the detailed listings file (`listings.csv.gz`, about 75 columns), not the 18-column summary `listings.csv`. Inside Airbnb changes its columns over time, so run `df.columns` on your download and treat the data dictionary as a guide.

#### Files and joins
| File | One row per | Size | Joins on |
| :--- | :--- | :--- | :--- |
| `listings.csv.gz` (detailed) | Listing | ~5–6k rows, ~75 columns | `id` (hub) |
| `calendar.csv.gz` | Listing × night, 365 days ahead | ~2M rows | `listing_id` → `listings.id` |
| `reviews.csv.gz` | Review | ~300k+ rows | `listing_id` → `listings.id` |
| `neighbourhoods.geojson` | Neighbourhood polygon | small | `neighbourhood` → `listings.neighbourhood_cleansed` |

- `neighbourhoods.geojson` is under `/visualisations/` on the download page, not `/data/`.
- Coverage is the City of Vancouver only, across its 22 local planning areas. Burnaby, Richmond, Surrey and Kelowna are not in this snapshot.
- Earlier quarterly snapshots and Canada-wide regional archives are on the same download page.

#### Data notes
- Prices are stored as text everywhere they appear.
- An unavailable calendar night can be booked or blocked by the host; the data does not say which.
- Reviews are a proxy for stays, not a count of them.
- Estimated occupancy and revenue are Inside Airbnb estimates, not reported figures.
- `host_listings_count` is global; `calculated_host_listings_count` is this city only.
- Date formats differ across the three CSVs. Parse them explicitly.
- The data was scraped from Airbnb on one day; it is not an official or complete list of short-term rentals.

#### Supplementary datasets, staged for all teams
- **CMHC Rental Market Survey:**
  - Housing Market Information Portal: vacancy, average and median rents, turnover, and universe counts by zone.
  - Vacancy rates by rent quartile: vacancy by price tier, more useful than a headline rate for anything about market segments.
  - Rent quartiles: the rent distribution rather than just the average.
  - Number of units by building size: the rental universe, useful for sizing displacement effects.
  - Percentile rents for small centres: relevant if you look at smaller BC communities, which the legality constraint pushes toward.
- **Vancouver Open Data:** non-market housing data, subdivision category areas, and local area and zone boundaries.
- **Bring your own:** Source at least one more public dataset; there is no limit on how many you use. It must be free to access, with no paywall or login, so every team has equal access. A join you cannot defend is worse than no join.

---

### SECTION 5: Deliverables
Two things are due: a pitch (7 minutes in preliminary round, 10 minutes in final) and a GitHub repository that reproduces your numbers.
- **Pitch (.pptx):** 7 minutes plus 3 minutes Q&A in preliminary round; 10 minutes plus 5 minutes Q&A in final round. Lead with the recommendation, not the methodology. Mention your key decisions where they arise, and show your assumptions and how you validated your results. Put a decision log in the appendix that compiles your decisions (see How You Will Be Judged).
- **GitHub repository:** reproducible code that runs. A judge should be able to trace any number you present back to the line that produced it. The repo isn't scored; judges may use it to verify your numbers.
- Q&A runs very quickly. We recommend keeping your key assumptions and the reasoning behind them on a slide, so they are easy to refer back to when answering questions.

---

### SECTION 6: How You Will Be Judged
Judges score out of 30 on demonstrated evidence, not on how complex your methods are. Each requirement clearly shown earns 1 point; one that is absent, incorrect, or cannot be explained or defended earns 0. There are no partial points within an item.

| Category | Points | Judges look for |
| :--- | :--- | :--- |
| **1. Data Understanding** | 5 | The business problem, the dataset and its source, relevant variables, data-quality checks, and stated limitations |
| **2. Analysis & Validation** | 6 | The approach and why it fits, steps from data to results, quantitative evidence, a validation or sanity check, and uncertainty |
| **3. Decision Log & Justification** | 9 | Three decisions, each scored on what was decided, why, and what changed as a result |
| **4. Insights & Recommendations** | 6 | Two distinct data-backed findings, recommendations tied to them, next steps, expected 2027 performance, and a range with key risks and mitigation |
| **5. Presentation & Communication** | 4 | A clear narrative, accurate visuals, finishing on time, and understanding shown in Q&A |
| **Total** | **30** | |

#### Details on Decision Log:
The decision log is the largest category (9 points). Document three meaningful analytical or business decisions in a decision log in your presentation's appendix, and mention the key ones in the pitch where they arise. Each earns:
- 1 point for identifying it
- 1 point for justifying it with evidence or a comparison of alternatives
- 1 point for explaining how it affected your findings or recommendation and defending that in Q&A.
*(Saying "we removed outliers" earns 1 of 3. Showing why those values should go, and how removing them changed your results, earns the other 2. Other acceptable decisions include choosing a metric or model, handling missing values, changing the scope, prioritizing a recommendation, or choosing between business alternatives.)*

Simple methods can earn full marks. Machine learning and other advanced techniques do not score extra. A simple, well-justified and validated method can take every point.

---

### SECTION 7: What a Strong Pitch Looks Like
A strong pitch opens with the answer, then shows just enough evidence for the committee to believe your answer. This is a suggested shape, not a required one:
1. **The recommendation:** where, how many, what property mix, and the expected 2027 result with its range.
2. **The problem and the data:** what DDD is deciding, what the snapshot covers, what you cleaned or excluded, and what you joined in.
3. **The evidence:** what the Vancouver data shows, and what that implies for your picks.
4. **Your key decisions:** mention each where it shapes the story: what you chose, why, and what it changed.
5. **Risks and mitigation:** your assumptions, how you validated, the key risks, and how you would mitigate the most impactful ones.
6. **Next steps:** what DDD should do first, and how it would know the plan is working.

#### What tends to earn points:
- Finding something the data supports that is not obvious.
- Quantifying the recommendation and attaching honest uncertainty to it.
- Naming the biggest risks and how you would mitigate them.
- Saying "we tested that and it didn't hold" out loud.

#### What tends to lose points:
- A tour of your exploratory analysis.
- Correlation presented as a causal claim.
- Charts without a decision attached.
- A model with a good metric and no business consequence.
- Precision the data cannot support. If you report a figure to two decimal places, be ready to defend both.

#### Presentation checklist:
- Business problem and objective.
- Overview of the dataset, and the important cleaning or preparation steps.
- Analytical approach and supporting evidence.
- Key decisions mentioned where they arise, with their reasoning and impact, and a decision log compiling them in the appendix.
- Data-supported insights and actionable recommendations.
- Relevant assumptions, limitations and validation.
- Disclosure of material AI assistance, if applicable, and how you checked important AI-assisted outputs.

---

### SECTION 8: AI Use and Rules
- AI tools are allowed, and they raise the bar rather than lower it. When every team can produce a competent analysis in an afternoon, what sets you apart is knowing why your approach is right, what it assumes, where it breaks and what you rejected.
- You are responsible for the accuracy of your work, and for explaining and defending your methods and decisions.
- **Disclose material AI assistance** in the pitch, and explain how you checked the important AI-assisted outputs.
- AI use itself earns or loses no points. Being unable to explain your own analysis does.
- Judges will pick claims from your pitch and ask you to defend them. "The model chose that" is not a defence.

#### Rules and conduct
- All data must be public. Nothing behind a paywall or login, and no scraping.
- Credit Inside Airbnb on your slides, using: `Data: Inside Airbnb, Vancouver, 15 June 2026, CC BY 4.0.`
- Do not identify or contact individual hosts. Never show real licence numbers, host names or listing URLs.
- Compliance rates you compute from the license field are estimates from imperfect data. Present them that way.
- If the brief is unclear, ask. A judge would rather clarify it than watch you build the wrong thing.

---

### SECTION 9: Sources
- BC Government news release, April 17, 2026: communities covered, the 3% vacancy test, and the 2027 opt-out dates.
- City of Kelowna, Short-term rentals: where Kelowna's requirement still applies.
- Inside Airbnb, Get the Data: the Vancouver snapshot.
- The case dates (January 1, 2027 and 2028), Vancouver's April 2026 licence counts, and the staged datasets come from the DataJam 2026 planning document.
