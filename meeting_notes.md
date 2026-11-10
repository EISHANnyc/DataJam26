# DataJam 2026 — Team Meeting Notes
**Date:** November 9, 2026  

---

## 1. Meeting Overview & Agenda
* prompt review
* The 5 core questions we must answer
* Division of roles & responsibilities
* Next things to do & deadlines

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

## 3. Team Member Action Items (Agreed)
* **Eishan:** Clean `listings.csv.gz` to find average prices across neighbourhoods and average cost based on how many bed/bathrooms.
* **Oliver:** Use `reviews.csv.gz` (and calendar) to create a library of listing IDs with good / bad reviews (create a dictionary of good / bad words, filter the comments, and group by listing ID).
* **Bhuvanesh:** Look through supplementary datasets and outside sources to identify what is missing/needed, determine how to link datasets together, and find average purchase prices for property types (using the CREA benchmark data).
* **Tory:** Look through `neighbourhoods.geojson` and `neighbourhoods.csv` to see if we can make a visual map of target areas or a heatmap of neighbourhoods where Airbnbs are located.

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
