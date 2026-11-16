# WHERE? 
## Where are we buying properties (In what neighbourhoods? Downtown? Kitsilano? Fairview?)
# Step 1:   Calculate revenue per available night across all neighbourhoods
# Step 2:   Find high demand zones using calendar (ID) and vacancy and find out which neighbourhoods are booked and what isn't
# Step 3:   Analyze differences in the different seasons (What houses and areas have less availability (more used) throughout the year)
# Step 4:   Compare with alternative BC markets and justify why Metro Vancouver remains the agency's risk-adjusted pick
# Step 5:   What houses? We know Where, but what types of houses??
# =====================================================================================================================================

library(tidyverse)
library(httr2)

df <- read_csv("Data/Clean Data/listings_cleaned.csv")

# calculate revenue per availalbe night
df_revPar <- df |>
  mutate(
    occupancy_rate = (estimated_occupancy_l365d / 365) * 100,
    revpar = (price_clean * estimated_occupancy_l365d) / 365
  )
neighbourhood_revpar <- df_revPar |> 
  group_by(neighbourhood = neighbourhood_cleansed) |> 
  summarize(
    active_properties = n(),
    median_nightly_price = round(median(price_clean, na.rm = TRUE), 0),
    avg_occupancy_pct = round(mean(occupancy_rate, na.rm = TRUE), 1),
    median_revpar = round(median(revpar, na.rm = TRUE), 0),
    mean_revpar = round(mean(revpar, na.rm = TRUE), 0),
    avg_annual_revenue = round(mean(estimated_revenue_l365d, na.rm = TRUE), 0)
  ) |> 
  arrange(desc(mean_revpar))


print(neighbourhood_revpar)
# Top neighbourhoods with highest revpar: Downtown, Shaughnessy, Oakridge, Strathcona
# Shaugnessy and Oakridge have an avg occupancy of 20%... (empty 80% of the year)
# Why not Strathcona? High occupancy %, high average revpar, high avg annual revenue..
## Because it only has 14 active properties. 
# Kitsilano (6) and Fairview (5) have higher occupancy rates
# Downtown makes $160 per day and is in use 31% of the year

# Find high demand zones
df_demand <- df |> 
  mutate(
    booked_pct_30d = round((30 - availability_30) / 30 * 100, 1),
    booked_pct_90d = round((90 - availability_90) / 90 * 100, 1),
    booked_pct_365d = round((365 - availability_365) / 365 * 100, 1),
  )

# what % of houses are booked in the next x days
neighbourhood_demand <- df_demand |> 
  group_by(neighbourhood = neighbourhood_cleansed) |> 
  summarize(
    active_properties = n(),
    median_nightly_price = round(median(price_clean, na.rm = TRUE), 0),
    avg_booked_30d_pct   = round(mean(booked_pct_30d, na.rm = TRUE), 1),
    avg_booked_90d_pct   = round(mean(booked_pct_90d, na.rm = TRUE), 1),
    avg_booked_365d_pct  = round(mean(booked_pct_365d, na.rm = TRUE), 1),
    # Recent review amounts
    avg_reviews_past_year = round(mean(number_of_reviews_ltm, na.rm = TRUE), 1)
  ) |>
  # Focus on neighbourhoods with inventory (at least 20 properties)
  filter(active_properties >= 20) |>
  arrange(desc(avg_booked_30d_pct))


print(neighbourhood_demand, n = 23)

# High demand places are Kitsilano, having an avg of 63% of the next 30 days booked, with Shaugnessy around 57%
# When we look at the 90 and 365 days, most are 30-60% booked
## *** It says that an unavailable calendar can be 'booked' or 'blocked' by the host (so we should only do 30-90 days, not full year )

# Let's compare it to alternative BC markets! 
# AKA Why we are choosing Vancouver
# Bhuvanesh's clean data
cmhc_rentals <- read_csv("Data/Clean Data/RentalMarketStatistics_clean.csv")

suburb_comparison <- cmhc_rentals |>
  filter(zone %in% c("Downtown", "Kitsilano/Point Grey", "West End/Stanley Park", 
                     "Surrey", "North Burnaby", "New Westminster", "Richmond")) |>
  mutate(
    monthly_rent = average_rent,
    annual_long_term_rent = monthly_rent * 12,
    vacancy_pct = as.numeric(vacancy_rate_percent)
  ) |>
  select(zone, vacancy_pct, monthly_rent, annual_long_term_rent) |>
  arrange(vacancy_pct)
print(suburb_comparison)


# step 5
df_properties <- df |> 
  mutate(
    property_category = case_when(
      str_detect(property_type, regex("condo|apartment|loft", ignore_case = TRUE)) ~ "Apartment",
      str_detect(property_type, regex("townhouse", ignore_case = TRUE)) ~ "Townhouse",
      str_detect(property_type, regex("house|villa|bungalow", ignore_case = TRUE)) ~ "Single Family",
      TRUE ~ "Apartment"
    ),
    benchmark_price = case_when(
      property_category == "Apartment"     ~ 688100,
      property_category == "Townhouse"     ~ 1031200,
      property_category == "Single Family" ~ 1820900
    ),
    gross_yield_pct = round((estimated_revenue_l365d / benchmark_price ) * 100, 2),
    booked_pct_30d = round((30 - availability_30) / 30 * 100, 1),
    booked_pct_90d = round((90 - availability_90) / 90 * 100, 1)
  )

property_comparison <- df_properties |> 
  group_by(property_category) |> 
  summarize(
    total_listings = n(),
    avg_annual_revenue = round(mean(estimated_revenue_l365d, na.rm = TRUE), 0),
    benchmark_price = first(benchmark_price),
    avg_gross_yield_pct = round(mean(gross_yield_pct, na.rm = TRUE), 2)
  ) |> 
  arrange(desc(avg_gross_yield_pct))

print(property_comparison)


# We find that apartments generate a 6.63% yield ($45k in revenue on a $688.1k apartment cost)
# A single family house only generates a 2.18% yield ($39k on a $1.8209M house)

# now we should compare bedrooms (1 vs 2 vs 3) for apartments!
bedroom_comparison <- df_properties |> 
  filter(property_category == "Apartment", bedrooms_clean %in% c(1,2,3)) |> 
  group_by(bedrooms = bedrooms_clean) |> 
  summarize(
    active_properties   = n(),
    median_nightly_price = round(median(price_clean, na.rm = TRUE), 0),
    avg_booked_30d_pct  = round(mean(booked_pct_30d, na.rm = TRUE), 1),
    avg_booked_90d_pct  = round(mean(booked_pct_90d, na.rm = TRUE), 1),
    avg_annual_revenue  = round(mean(estimated_revenue_l365d, na.rm = TRUE), 0),
    avg_gross_yield_pct = round(mean(gross_yield_pct, na.rm = TRUE), 2)
  ) |> 
  arrange(bedrooms)
print(bedroom_comparison)

# 1-Bedroom units have the highest occupancy throughout the year (117/365)
# 2-Bedroom units generate higher revenue ($45.3k) and 6.58% yield
# We should focus on a 60/40 mix of 2-Bedroom and 1-Bedroom units


# now we should combine both the Where and the What houses
core_neighbourhoods <- c("Downtown", "Kitsilano", "West End", "Mount Pleasant", "Fairview")

where_and_what <- df_properties |> 
  filter(
    neighbourhood_cleansed %in% core_neighbourhoods,
    property_category == "Apartment",
    bedrooms_clean %in% c(1,2)
  ) |> 
  group_by(neighbourhood = neighbourhood_cleansed, bedrooms = bedrooms_clean) |>
  summarize(
    active_properties   = n(),
    median_nightly_rate = round(median(price_clean, na.rm = TRUE), 0),
    avg_annual_revenue  = round(mean(estimated_revenue_l365d, na.rm = TRUE), 0),
    avg_gross_yield_pct = round(mean(gross_yield_pct, na.rm = TRUE), 2),
    .groups = "drop"
  ) |>
  arrange(desc(avg_gross_yield_pct))

print(where_and_what)

# This tells us that we get the highest avg yield is a 2 bedroom house in Downtown, and the next leading ones
# are 1 and 2 bedrooms in Kitsilano at a ~7.3% average yield, with a 1 bedroom Downtown falling right behind at 7.14%

# Verdict: We should have a 60/40 split of 1 and two bedrooms in downtown and Kitsilano
# 60%: Downtown (8 units): 5 2-bedroom apartments, 3 1-bedroom apartments
# 40%: Kitsilano (5 units): 3-2bedroom apartments, 2-1bedroom apartments