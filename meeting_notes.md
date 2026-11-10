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
  * **Role:** Filter and clean core listings, extract key variables (property types, bedrooms, nightly prices, occupancy, revenue), and generate `listings_cleaned.csv`.
* **Oliver:** 
  * **Datasets:** `calendar.csv.gz` and `reviews.csv.gz`.
  * **Role:** Analyze daily forward calendar for seasonal price variations (summer peak vs. winter dip) and analyze historical reviews as a proxy for completed guest stays.
* **Bhuvanesh:** 
  * **Datasets:** Supplementary CMHC datasets & missing acquisition data.
  * **Role:** Evaluate CMHC rental market surveys (vacancy rates by quartile, median rents vs. STR revenue), and integrate CREA MLS property acquisition benchmark prices.
* **Tory:** 
  * **Dataset:** `neighbourhoods.geojson` & `neighbourhoods.csv`.
  * **Role:** Explore spatial/GIS mapping across Vancouver's 22 planning areas, determine boundary overlays, and prepare choropleth heatmap visualizations for the pitch deck.
