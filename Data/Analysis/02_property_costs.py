
import pandas as pd
from pathlib import Path

# Set the project paths
OUTPUT_PATH = Path("Analysis/Outputs")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Set the available investment budget
BUDGET = 10_000_000

# Set the property tax rate
PROPERTY_TAX_RATE = 0.00336394


# Calculate BC Property Transfer Tax
def calculate_ptt(price):
    if price <= 0:
        raise ValueError("Property price must be greater than zero.")

    tax = 0

    tax += min(price, 200_000) * 0.01

    if price > 200_000:
        tax += (min(price, 2_000_000) - 200_000) * 0.02

    if price > 2_000_000:
        tax += (price - 2_000_000) * 0.03

    if price > 3_000_000:
        tax += (price - 3_000_000) * 0.02

    return tax


# Set property purchase price assumptions
# GVR prices are benchmark prices, not guaranteed purchase prices.
# GVR Average is a simple midpoint of East and West benchmarks.
property_prices = {
    "Apartment": {
        "GVR East": 635_100,
        "GVR West": 751_400,
        "GVR Average": (635_100 + 751_400) / 2
    },
    "House": {
        "GVR East": 1_610_700,
        "GVR West": 2_899_700,
        "GVR Average": (1_610_700 + 2_899_700) / 2
    }
}


# Calculate acquisition costs for each property type and GVR price scenario
results = []

for property_type, scenarios in property_prices.items():
    for scenario, purchase_price in scenarios.items():

        ptt = calculate_ptt(purchase_price)

        # Acquisition cost includes purchase price and PTT only.
        # It excludes legal fees, inspections, furnishing and setup.
        all_in_cost = purchase_price + ptt

        affordable_units = int(BUDGET // all_in_cost)

        deployed_capital = affordable_units * all_in_cost

        remaining_budget = BUDGET - deployed_capital

        results.append({
            "property_type": property_type,
            "scenario": scenario,
            "purchase_price": purchase_price,
            "ptt": ptt,
            "all_in_cost_per_property": all_in_cost,
            "affordable_units": affordable_units,
            "deployed_capital": deployed_capital,
            "remaining_budget": remaining_budget
        })


# Create the results table
property_costs = pd.DataFrame(results)

# Save the results
property_costs.to_csv(
    OUTPUT_PATH / "property_costs.csv",
    index=False
)

# Display the results
print("\nProperty acquisition costs:")
print(property_costs.to_string(index=False))

print("\nProperty cost analysis completed.")
