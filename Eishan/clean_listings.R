# ==============================================================================
# SFU DSSS DataJam 2026
# Task: Clean Inside Airbnb Vancouver (June 15, 2026) listings.csv.gz
# Eishan
# ==============================================================================

# 1. Load Required Libraries
library(tidyverse)

# Step 1: Loading raw listings data")

raw_listings <- read_csv("data/listings.csv.gz")
# nrow(raw_listings) 6509
# ncol(raw_listings) 90

# 2. Select the columns we need to keep
cols_to_keep <- c(
  "id", "name", "description",
  "hosts_time_as_user_years", "hosts_time_as_host_years", "host_location",
  "neighbourhood_cleansed", "property_type", "room_type",
  "accommodates", "bathrooms", "bedrooms", "beds", "amenities",
  "price", "price_quote_price_per_night", "minimum_nights",
  "availability_30", "availability_60", "availability_90", "availability_365",
  "number_of_reviews", "number_of_reviews_ltm", "reviews_per_month",
  "review_scores_rating", "review_scores_value",
  "license", "estimated_occupancy_l365d", "estimated_revenue_l365d"
)

df <- raw_listings %>% select(any_of(cols_to_keep))

# 3. Clean Data Types
# Cleaning data types
df_cleaned <- df %>%
  mutate(
    # Clean price: remove '$' and commas to convert to number
    price_clean = parse_number(price),
    
    # Ensure numeric types
    bedrooms_clean = as.numeric(bedrooms),
    minimum_nights = as.numeric(minimum_nights),
    estimated_occupancy_l365d = as.numeric(estimated_occupancy_l365d),
    estimated_revenue_l365d = as.numeric(estimated_revenue_l365d)
  )

# 4. Apply Business & Investment Filters
# Step 3: Applying Commercial Investment Filter
commercial_str <- df_cleaned %>%
  filter(
    # Filter 1:  NO private rooms or shared roomsy (So only Entire home/apt)
    room_type == "Entire home/apt",
    
    # Filter 2: True short-term rentals (<= 30 nights)
    ## In Vancouver, under 30 days is a short term rental, which is what our business is running
    minimum_nights <= 30,
    
    # Filter 3: Price limits (remove $0 listings and $2500+ outliers)
    price_clean >= 40 & price_clean <= 2500
  )

# Commercial STR listings after filtering:"
nrow(commercial_str)
nrow(commercial_str) / nrow(df_cleaned)
# 58% of original listings are left!

# 5. Generate Summary Table 1: Performance Across 22 Neighbourhoods
# Table 1: Top 10 Neighbourhoods by Listing Count
neighbourhood_summary <- commercial_str %>%
  group_by(neighbourhood = neighbourhood_cleansed) %>%
  summarize(
    total_listings = n(),
    median_nightly_price = round(median(price_clean, na.rm = TRUE), 2),
    mean_nightly_price = round(mean(price_clean, na.rm = TRUE), 2),
    avg_occupancy_days = round(mean(estimated_occupancy_l365d, na.rm = TRUE), 1),
    avg_annual_revenue = round(mean(estimated_revenue_l365d, na.rm = TRUE), 0)
  ) %>%
  arrange(desc(total_listings))

View(neighbourhood_summary)

# 6. Generate Summary Table 2: Performance by Neighbourhood x Bedrooms
# Table 2: Bedroom Performance in Core Target Neighbourhoods
target_neighbourhoods <- c("Downtown", "Shaughnessy", "Strathcona", "Oakridge", "Kitsilano", "Downtown Eastside", "Fairview")

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

View(bedroom_summary)

# 7. Export Clean Dataset
output_path <- "data/listings_cleaned.csv"
write_csv(commercial_str, output_path)
