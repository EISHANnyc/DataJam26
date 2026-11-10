# DataJam 2026 — Team Meeting Notes
**Date:** November 9, 2026  
**Team Composition:** 4 Members (2 Statistics, 2 Computer Science)  

---

## 1. Meeting Overview & Agenda
* Brief alignment & prompt review
* The 5 core questions we must answer
* Division of roles & responsibilities
* Next milestones & deadlines

---

## 2. Discussion Notes (Live)
### Team Workflow & Collaboration Strategy:
* **Initial Team Effort (Data Cleaning):**
  * The team will first collaborate on **data cleaning** as a joint group effort across the datasets.
* **Independent Question Exploration:**
  * Rather than working on the 5 questions at the same time in a single group (which risks conflicting ideas and slowing progress), team members will explore and work on the questions **individually first**.
* **Cross-Validation & Synthesis:**
  * After individual drafts/solutions are built, the team will reconvene to exchange answers.
  * This creates a built-in **double-checking and triple-checking** process where teammates audit each other's assumptions, logic, and numbers to converge on the strongest final recommendation.

---

## 3. Team Member Dataset Ownership & Responsibilities
* **Eishan:** 
  * **Dataset:** `listings.csv.gz` (The primary Hub table).
  * **Role:** Filter and clean core listings, extract the 24 key variables (property types, bedrooms, nightly prices, occupancy, revenue), and generate `listings_cleaned.csv`.
* **Oliver:** 
  * **Datasets:** `calendar.csv.gz` and `reviews.csv.gz`.
  * **Role:** 
    1. Analyze forward `calendar.csv.gz` for monthly seasonality (summer peak vs. winter dip in availability and price).
    2. Filter `reviews.csv.gz` using the positive keyword dictionary to identify high-satisfaction property features and corroborate location picks.
* **Bhuvanesh:** 
  * **Datasets:** Supplementary CMHC datasets & CREA MLS acquisition data.
  * **Role:** Extract benchmark purchase prices (Apartments ~$688k, Townhouses ~$1.03M, Detached ~$1.82M from `CREA_MLS_HPI_Benchmarks.xlsx`) and use CMHC vacancy/rent data to justify the STR revenue premium over long-term leases.
* **Tory:** 
  * **Dataset:** `neighbourhoods.geojson` & `neighbourhoods.csv`.
  * **Role:** Spatial GIS mapping across Vancouver's 22 planning areas, preparing choropleth heatmap visualizations for the pitch deck.

---

## 4. File Schemas & Formatting (Calendar & Reviews)

### `calendar.csv.gz`
* **Columns:** `['listing_id', 'date', 'available', 'minimum_nights', 'maximum_nights']`
* **Key formatting notes:**
  * `listing_id`: Joins to `listings.id`.
  * `date`: YYYY-MM-DD format (June 15, 2026 to June 14, 2027).
  * `available`: `'t'` for available, `'f'` for unavailable/booked.

### `reviews.csv.gz`
* **Columns:** `['listing_id', 'id', 'date', 'reviewer_id', 'reviewer_name', 'comments']`
* **Key formatting notes:**
  * `listing_id`: Joins to `listings.id`.
  * `comments`: Raw text string of guest review feedback.

---

## 5. Review Sentiment Dictionary (Positive Value-Drivers)
Filter comments for these high-value keywords to identify what drives top guest willingness-to-pay:
* **Location & Walkability:** `"walkable"`, `"walking distance"`, `"location"`, `"skytrain"`, `"transit"`, `"seawall"`, `"restaurants"`, `"close to everything"`
* **Unit Quality & Views:** `"clean"`, `"spotless"`, `"view"`, `"modern"`, `"quiet"`, `"comfortable"`, `"balcony"`
* **Corporate / Business Travel:** `"fast wifi"`, `"desk"`, `"work"`, `"easy check-in"`, `"conference"`
* **Family / Group Appeal:** `"family"`, `"spacious"`, `"well equipped"`, `"kitchen"`, `"parking"`
* **Customer Loyalty / Superhost:** `"definitely stay again"`, `"highly recommend"`, `"perfect stay"`

---

## 6. Current Action Items Checklist
* [ ] **Eishan:** Run the cleaning script on `listings.csv.gz` (filter `Entire home/apt`, `minimum_nights <= 30`, clean prices) to produce the neighbourhood revenue table.
* [ ] **Oliver:** Pull monthly availability % from `calendar.csv.gz` and run the keyword search on `reviews.csv.gz`.
* [ ] **Bhuvanesh:** Finalize the purchase price denominator table from `CREA_MLS_HPI_Benchmarks.xlsx`.
* [ ] **Tory:** Load `neighbourhoods.geojson` into Python/R to test joining with neighbourhood names for mapping.
