# ==============================================================================
# SFU DSSS DataJam 2026 - Data Cleaning Pipeline
# Task: Clean Inside Airbnb Vancouver (June 15, 2026) listings.csv.gz
# Author: Eishan (Data Lead)
# ==============================================================================

# 1. Load Required Libraries
suppressPackageStartupMessages({
  library(tidyverse)
})

cat("=== Step 1: Loading raw listings data ===\n")
raw_path <- "data/listings.csv.gz"
if (!file.exists(raw_path)) {
  stop("Could not find data/listings.csv.gz. Make sure working directory is DataJam26.")
}

raw_listings <- read_csv(raw_path, show_col_types = FALSE)
cat("Loaded raw dataset:", nrow(raw_listings), "rows and", ncol(raw_listings), "columns.\n\n")

# 2. Select the 24 Essential Columns Agreed by Team
cols_to_keep <- c(
  "id", "name", "description",
  "hosts_time_as_user_years", "hosts_time_as_host_years", "host_location",
  "neighbourhood_cleansed", "property_type", "room_type",
  "accommodates", "bathrooms", "bathrooms_text", "bedrooms", "beds", "amenities",
  "price", "price_quote_price_per_night", "minimum_nights",
  "availability_30", "availability_60", "availability_90", "availability_365",
  "number_of_reviews", "number_of_reviews_ltm", "reviews_per_month",
  "review_scores_rating", "review_scores_value",
  "license", "estimated_occupancy_l365d", "estimated_revenue_l365d"
)

df <- raw_listings %>% select(any_of(cols_to_keep))

# 3. Clean Data Types
cat("=== Step 2: Cleaning Data Types ===\n")
df_cleaned <- df %>%
  mutate(
    # Clean price: strip '$' and commas to convert to numeric
    price_clean = parse_number(price),
    
    # Extract numeric bathroom count from bathrooms_text (e.g. '1.5 baths' -> 1.5)
    bathrooms_clean = coalesce(as.numeric(bathrooms), parse_number(bathrooms_text)),
    
    # Ensure numeric types
    bedrooms_clean = as.numeric(bedrooms),
    minimum_nights = as.numeric(minimum_nights),
    estimated_occupancy_l365d = as.numeric(estimated_occupancy_l365d),
    estimated_revenue_l365d = as.numeric(estimated_revenue_l365d)
  )

# 4. Apply Business & Investment Filters
cat("=== Step 3: Applying Commercial Investment Filters ===\n")
commercial_str <- df_cleaned %>%
  filter(
    # Filter 1: Commercial assets only (Entire home/apt)
    room_type == "Entire home/apt",
    
    # Filter 2: True short-term rentals (<= 30 nights)
    minimum_nights <= 30,
    
    # Filter 3: Price bounds (remove $0 test listings and extreme $2500+ outliers)
    price_clean >= 40 & price_clean <= 2500
  )

cat("Commercial STR listings after filtering:", nrow(commercial_str), 
    paste0("(", round(nrow(commercial_str)/nrow(raw_listings)*100, 1), "% of total)\n\n"))

# 5. Generate Summary Table 1: Performance Across 22 Neighbourhoods
cat("=== Table 1: Top 10 Neighbourhoods by Listing Count ===\n")
neighbourhood_summary <- commercial_str %>%
  group_by(neighbourhood = neighbourhood_cleansed) %>%
  summarise(
    total_listings       = n(),
    median_nightly_price = round(median(price_clean, na.rm = TRUE), 2),
    mean_nightly_price   = round(mean(price_clean, na.rm = TRUE), 2),
    avg_occupancy_days   = round(mean(estimated_occupancy_l365d, na.rm = TRUE), 1),
    avg_annual_revenue   = round(mean(estimated_revenue_l365d, na.rm = TRUE), 0)
  ) %>%
  arrange(desc(total_listings))

print(head(neighbourhood_summary, 10))

# 6. Generate Summary Table 2: Performance by Neighbourhood x Bedrooms
cat("\n=== Table 2: Bedroom Performance in Core Target Submarkets ===\n")
target_neighbourhoods <- c("Downtown", "West End", "Kitsilano", "Mount Pleasant", "Downtown Eastside")

bedroom_summary <- commercial_str %>%
  filter(
    neighbourhood_cleansed %in% target_neighbourhoods,
    bedrooms_clean %in% c(1, 2, 3)
  ) %>%
  group_by(neighbourhood = neighbourhood_cleansed, bedrooms = bedrooms_clean) %>%
  summarise(
    total_listings       = n(),
    median_nightly_price = round(median(price_clean, na.rm = TRUE), 2),
    avg_annual_revenue   = round(mean(estimated_revenue_l365d, na.rm = TRUE), 0),
    .groups = "drop"
  ) %>%
  arrange(neighbourhood, bedrooms)

print(bedroom_summary)

# 7. Export Clean Dataset
output_path <- "data/listings_cleaned.csv"
write_csv(commercial_str, output_path)
cat("\n=== Successfully saved cleaned dataset to", output_path, "===\n")
