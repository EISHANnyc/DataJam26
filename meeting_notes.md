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

## 3. Agreed Action Items & Ownership
* [x] **Core Missing Data Identified:**
  * **Property Sale / Acquisition Prices:** Real estate benchmark purchase prices for 1-bed/2-bed condos and townhomes across Vancouver submarkets (needed to calculate how many units $10M buys and the Cap Rate).
  * **Operating Costs:** Fixed expense modeling (Airbnb platform fee, property management, strata/HOA fees, property tax, licensing).
* [x] **Decision Log Entry Formulated (Decision #2):**
  * **Topic:** Modeling Operating Costs via Fixed Benchmark Percentages.
  * **What:** Assume fixed industry-standard percentages for operating expenses rather than arbitrary flat dollar amounts.
  * **Why:** Turnkey property management (15%–18%) and Airbnb host fees (3%) scale dynamically with revenue; strata and taxes scale with property assessed value.
* [ ] **Next Step (Data Cleaning):** Filter and prune `listings.csv.gz` to the essential columns and commercially viable rows.
