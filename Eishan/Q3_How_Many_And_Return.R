library(tidyverse)

df <- read_csv("Data/Clean Data/listings_cleaned.csv")

# Question 3: how many?
# Source: CREA benchmark for detached homes is $1.82M, but in luxury Westside areas (Shaughnessy,
# Point Grey), benchmark single-family homes sell for $2.5M+ (CMHC price percentiles data)

total_capital <- 10000000

# Strategy A
# Buy 4 Single-Family Detached Luxury Homes in Westside / Shaughnessy

luxury_price_per_unit <- 2500000   # $2.5M per luxury home ($10M total / $2.5M = 4 houses)
luxury_unit_count     <- round(total_capital / luxury_price_per_unit) # 4 units

# Average annual revenue for single-family homes
# detached houses in Vancouver averaged $39,783)
luxury_avg_annual_rev <- 39783     

strat_a_total_rev   <- luxury_unit_count * luxury_avg_annual_rev # 4 * $39,783 = $159,132
strat_a_gross_yield <- (strat_a_total_rev / total_capital) * 100 # Only 1.59% return on $10M

# Risk: What happens if JUST ONE property has zero bookings
# (If 1 out of 4 houses is empty or has issues, we lose 1/4 of all our money)
strat_a_shock_loss_pct <- (1 / luxury_unit_count) * 100  # 25% revenue lost!



# STRATEGY B: 
# 13 Units: 8 Downtown + 5 Kitsilano (1 and 2 bedroom)
# Budget breakdown per unit:
# $688,100 purchase (from Bhuvanesh's CREA apartment benchmark) 
# + $40,000 extra costs (BC Property Transfer Tax is ~$12k, legal fees ~$2.5k, and furnishing/smart locks is ~$25k)
# Total cost = ~$728,000 per apartment
condo_budget_per_unit <- 728000
condo_unit_count      <- floor(total_capital / condo_budget_per_unit) # 13 units ($10M / $728k = 13.7)

# 13-unit portfolio from average revenues:
# (These 4 revenue numbers are the exact averages from our where_and_what table in script 1)
# - 5 Downtown 2-Bed:   $62,647 each
# - 3 Downtown 1-Bed:   $49,153 each
# - 3 Kitsilano 2-Bed:  $50,010 each
# - 2 Kitsilano 1-Bed:  $50,535 each

portfolio_units <- tribble(
  ~neighbourhood, ~bedrooms, ~units, ~unit_cost, ~annual_rev_per_unit,
  "Downtown",     2,         5,      728000,     62647,
  "Downtown",     1,         3,      728000,     49153,
  "Kitsilano",    2,         3,      728000,     50010,
  "Kitsilano",    1,         2,      728000,     50535
)

# Calculate totals
strat_b_portfolio <- portfolio_units |>
  mutate(
    total_cost    = units * unit_cost,
    total_revenue = units * annual_rev_per_unit
  )

strat_b_total_cost    <- sum(strat_b_portfolio$total_cost)       # ~$9.46M (leaving ~$540k cash reserve!)
strat_b_total_rev     <- sum(strat_b_portfolio$total_revenue)    # ~$711,889
strat_b_gross_yield   <- (strat_b_total_rev / total_capital) * 100 # 7.12% return on $10M

# Downside Risk: What happens if 1 property is vacant?
# (If 1 out of 13 apartments is empty, we only lose 1/13 of our money)
strat_b_shock_loss_pct <- (1 / condo_unit_count) * 100           # Only 7.7% revenue lost!


# Comparison table
comparison_summary <- tibble(
  Metric = c(
    "Strategy Name",
    "Number of Properties",
    "Asset Type",
    "Capital Deployed",
    "Cash Reserve Buffer",
    "Total Expected Revenue (Gross)",
    "Gross Yield on $10M",
    "Downside Shock (If 1 Unit Fails)"
  ),
  `Strategy A (Luxury)` = c(
    "A few luxury houses",
    "4 Homes",
    "Single-Family Detached",
    "$10,000,000",
    "$0",
    paste0("$", format(round(strat_a_total_rev), big.mark = ",")),
    paste0(round(strat_a_gross_yield, 2), "%"),
    paste0("-", round(strat_a_shock_loss_pct, 1), "% of fund revenue")
  ),
  `Strategy B (Your Portfolio)` = c(
    "Lots of apartments",
    "13 Condos",
    "1-Bed & 2-Bed Apartments",
    paste0("$", format(round(strat_b_total_cost), big.mark = ",")),
    paste0("$", format(round(total_capital - strat_b_total_cost), big.mark = ",")),
    paste0("$", format(round(strat_b_total_rev), big.mark = ",")),
    paste0(round(strat_b_gross_yield, 2), "%"),
    paste0("-", round(strat_b_shock_loss_pct, 1), "% of fund revenue")
  )
)

print(comparison_summary)

