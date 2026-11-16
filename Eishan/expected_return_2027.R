# How much actual profit does the $10M fund make in 2027, and what are all the expenses?

# Take our $711,889 gross revenue from the 13 units
# Subtract real-world Vancouver operating expenses (Airbnb fee, property management, strata fees, city licences, property taxes, insurance, maintenance)
# Calculate Net Operating Income
# Calculate our official return metric: Net Cap Rate = 4.08% on the $10M fund
# Build an honest Bear / Base / Bull scenario range so the judges see we prepared for market downturns or tourism booms

library(tidyverse)

total_capital <- 10000000
deployed_capital <- 13 * 728000
cash_reserve <- total_capital - deployed_capital

gross_revenue <- 711889

opex_breakdown <- tibble(
  expense_name = c(
    "AirBnb Platform fee (3%)",
    "Property Management (15%)",
    "Strata Fees ($450/unit)",
    "Property Taxes and Vancouver Licenses",
    "Utilities and Insurance ($250/month/unit)",
    "Maintenance Reserve (4%)"
  ),
  cost = c(
    .03 * gross_revenue,
    .15 * gross_revenue,
    13 * 450 * 12,
    13 * (688100 * .0028 + 1000),
    13 * 250 * 12,
    .04 * gross_revenue
  )
)
print(opex_breakdown)

total_opex <- sum(opex_breakdown$cost)
total_opex


net_operating_income <- gross_revenue - total_opex
net_cap_rate_fund <- round((net_operating_income / total_capital) * 100, 2)

net_cap_rate_deployed <- round((net_operating_income / deployed_capital) * 100, 2)

pro_forma_table <- tibble(
  `Financial Line Item` = c(
    "Gross Rental Revenue (13 units)",
    "Total OPEX",
    "-------------------------------",
    "Net Operating Income",
    "Net Cap Rate (on $10M Fund)",
    "Net Cap Rate (on $9.46M Deployed"
  ),
  `2027 Projection` = c(
    paste0("$", format(round(gross_revenue), big.mark = ",")),
    paste0("-$", format(round(total_opex), big.mark = ",")),
    "-------------------",
    paste0("$", format(round(net_operating_income), big.mark = ",")),
    paste0(net_cap_rate_fund, "%"),
    paste0(net_cap_rate_deployed, "%")
  )
)

print(pro_forma_table)

# we make 4.08% on the full $10m, but since we only put in $9.46m, we make 4.31% on that

# now we should include uncertainty
# - fixed costs stay the same ($)
# - Variable costs (airBnb + Management, Maintenance = 22%)

fixed_opex <- (13*450*12) + (13 * (688100 * .0028 + 1000)) + (13*250*12)

scenario_analysis <- tibble(
  scenario = c(
    "Bear Case (-15% Tourisim, fewer bookings)",
    "Base Case (+-0% Expected Performance)",
    "Bull Case ( +15% Tourism, more bookings)"
  ),
  gross_rev = c(
    gross_revenue * .85,
    gross_revenue,
    gross_revenue * 1.15
  )
) |> 
  mutate(
    variable_opex = .22 * gross_rev,
    total_costs = round(variable_opex + fixed_opex),
    net_income = round(gross_rev - total_costs),
    net_cap_rate = round((net_income / total_capital) * 100, 2)
  )

scenario_table <- scenario_analysis |> 
  transmute(
    Scenario = scenario,
    `Gross Revenue` = paste0("$", format(round(gross_rev), big.mark = ",")),
    `Total Costs (OPEX)` = paste0("-$", format(total_costs, big.mark = ",")),
    `Net Profit` = paste0("$", format(net_income, big.mark = ",")),
    `Net Cap Rate` = paste0(net_cap_rate, "%")
  )
View(scenario_table)
