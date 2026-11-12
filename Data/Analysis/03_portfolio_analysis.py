
import pandas as pd
from pathlib import Path

# Set the project paths
OUTPUT_PATH = Path("Analysis/Outputs")

# Set the investment assumptions
BUDGET = 10_000_000
PLATFORM_FEE = 0.155
PROPERTY_TAX_RATE = 0.00336394

# Set management fee scenarios
MANAGEMENT_FEES = {
    "Best": 0.15,
    "Base": 0.22,
    "Worst": 0.30
}

# Load the revenue analysis results
revenue_comparison = pd.read_csv(
    OUTPUT_PATH / "revenue_comparison.csv"
)

# Load the property acquisition costs
property_costs = pd.read_csv(
    OUTPUT_PATH / "property_costs.csv"
)

# Check that the required columns are available
required_revenue_columns = {
    "property_group",
    "all_listings_median",
    "active_proxy_median"
}

required_cost_columns = {
    "property_type",
    "scenario",
    "purchase_price",
    "ptt",
    "all_in_cost_per_property"
}

if not required_revenue_columns.issubset(revenue_comparison.columns):
    raise ValueError("Revenue comparison file is missing required columns.")

if not required_cost_columns.issubset(property_costs.columns):
    raise ValueError("Property costs file is missing required columns.")


# Calculate the estimated contribution from one property
# This is partial operating income, not full NOI
def calculate_unit_income(revenue, purchase_price, management_fee):
    return (
        revenue * (1 - PLATFORM_FEE - management_fee)
        - purchase_price * PROPERTY_TAX_RATE
    )


# Evaluate all possible apartment and house combinations
def analyse_portfolios(price_scenario, revenue_basis, management_scenario):

    management_fee = MANAGEMENT_FEES[management_scenario]

    # Select the appropriate revenue estimates
    revenue_column = (
        "all_listings_median"
        if revenue_basis == "all"
        else "active_proxy_median"
    )

    # Get the revenue assumptions by property type
    revenue_data = revenue_comparison.set_index("property_group")

    apartment_revenue = revenue_data.loc[
        "Apartment", revenue_column
    ]

    house_revenue = revenue_data.loc[
        "House", revenue_column
    ]

    if pd.isna(apartment_revenue) or pd.isna(house_revenue):
        raise ValueError("Missing revenue estimate for a property type.")

    # Get the acquisition prices for the selected GVR scenario
    scenario_costs = property_costs[
        property_costs["scenario"] == price_scenario
    ].set_index("property_type")

    if not {"Apartment", "House"}.issubset(scenario_costs.index):
        raise ValueError(
            f"Missing apartment or house costs for {price_scenario}."
        )

    apartment_price = scenario_costs.loc[
        "Apartment", "purchase_price"
    ]

    apartment_ptt = scenario_costs.loc[
        "Apartment", "ptt"
    ]

    house_price = scenario_costs.loc[
        "House", "purchase_price"
    ]

    house_ptt = scenario_costs.loc[
        "House", "ptt"
    ]

    apartment_cost = apartment_price + apartment_ptt
    house_cost = house_price + house_ptt

    # Calculate estimated income per property
    apartment_income = calculate_unit_income(
        apartment_revenue,
        apartment_price,
        management_fee
    )

    house_income = calculate_unit_income(
        house_revenue,
        house_price,
        management_fee
    )

    results = []

    # Test every feasible combination of apartments and houses
    max_apartments = int(BUDGET // apartment_cost)
    max_houses = int(BUDGET // house_cost)

    for apartments in range(max_apartments + 1):
        for houses in range(max_houses + 1):

            total_properties = apartments + houses

            if total_properties == 0:
                continue

            deployed_capital = (
                apartments * apartment_cost
                + houses * house_cost
            )

            if deployed_capital > BUDGET:
                continue

            remaining_budget = BUDGET - deployed_capital

            # Calculate total estimated partial operating income
            total_income = (
                apartments * apartment_income
                + houses * house_income
            )

            # Calculate the share of income from the largest property type
            property_type_incomes = []

            if apartments > 0:
                property_type_incomes.append(
                    apartments * apartment_income
                )

            if houses > 0:
                property_type_incomes.append(
                    houses * house_income
                )

            largest_type_income = max(property_type_incomes)

            largest_type_share = (
                largest_type_income / total_income * 100
                if total_income > 0
                else float("nan")
            )

            largest_type = (
                "Apartment"
                if apartments * apartment_income >= houses * house_income
                else "House"
            )

            # Calculate yield on deployed acquisition capital
            yield_on_deployed = (
                total_income / deployed_capital
                if deployed_capital > 0
                else 0
            )

            results.append({
                "price_scenario": price_scenario,
                "revenue_basis": revenue_basis,
                "management_scenario": management_scenario,
                "apartments": apartments,
                "houses": houses,
                "total_properties": total_properties,
                "partial_operating_income": total_income,
                "deployed_capital": deployed_capital,
                "remaining_budget": remaining_budget,
                "yield_on_deployed": yield_on_deployed,
                "largest_property_type": largest_type,
                "largest_property_type_income": largest_type_income,
                "largest_property_type_share_pct": largest_type_share
            })

    return pd.DataFrame(results)


# Run the portfolio analysis using GVR Average pricing only
all_results = []

for revenue_basis in ["all", "active"]:

    for management_scenario in MANAGEMENT_FEES:

        results = analyse_portfolios(
            "GVR Average",
            revenue_basis,
            management_scenario
        )

        all_results.append(results)


# Combine all results
portfolio_results = pd.concat(
    all_results,
    ignore_index=True
)

# Save the portfolio results
portfolio_results.to_csv(
    OUTPUT_PATH / "portfolio_all_combinations.csv",
    index=False
)


# Display the top 10 GVR Average portfolios using all listings
# and base management
gvr_base = portfolio_results[
    (portfolio_results["revenue_basis"] == "all")
    & (portfolio_results["management_scenario"] == "Base")
].copy()

gvr_base = gvr_base.sort_values(
    "partial_operating_income",
    ascending=False
)

print("\nTop 10 GVR Average portfolios:")
print(
    gvr_base.head(10).to_string(index=False)
)


# Display the best portfolio for each revenue and management scenario
print("\nBest GVR Average portfolio by scenario:")

gvr_best = (
    portfolio_results
    .sort_values(
        "partial_operating_income",
        ascending=False
    )
    .groupby(
        ["revenue_basis", "management_scenario"],
        as_index=False
    )
    .first()
)

print(gvr_best.to_string(index=False))


# Display the number of feasible portfolios
print("\nNumber of feasible GVR Average portfolios:")
print(len(portfolio_results))

print("\nPortfolio analysis completed.")
