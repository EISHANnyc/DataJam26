import pandas as pd
from pathlib import Path

# Set the project paths
DATA_PATH = Path("Clean Data/listings_cleaned.csv")
OUTPUT_PATH = Path("Analysis/Outputs")

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Load the cleaned Airbnb listings
df = pd.read_csv(DATA_PATH)

print(f"Rows loaded: {len(df)}")

# Group property types into broader categories
property_type_mapping = {
    "Entire condo": "Apartment",
    "Entire rental unit": "Apartment",
    "Entire loft": "Apartment",
    "Entire serviced apartment": "Apartment",
    "Entire home": "House",
    "Entire townhouse": "Townhouse"
}

df["property_group"] = df["property_type"].map(property_type_mapping)

# Group listings by bedroom count
def group_bedrooms(bedrooms):
    if pd.isna(bedrooms):
        return None
    elif bedrooms == 0:
        return "Studio"
    elif bedrooms == 1:
        return "1 bedroom"
    elif bedrooms == 2:
        return "2 bedrooms"
    else:
        return "3+ bedrooms"

df["bedroom_group"] = df["bedrooms"].apply(group_bedrooms)

# Convert estimated revenue to numeric values
df["estimated_revenue_l365d"] = pd.to_numeric(
    df["estimated_revenue_l365d"], errors="coerce"
)

# Keep listings with a recognized property type and bedroom group
analysis_df = df.dropna(
    subset=["property_group", "bedroom_group", "estimated_revenue_l365d"]
).copy()

print(f"Listings included in analysis: {len(analysis_df)}")
print(f"Listings excluded: {len(df) - len(analysis_df)}")

print("\nProperty groups:")
print(analysis_df["property_group"].value_counts())

# Identify listings that may be actively operating
# This is a proxy, not confirmation that a listing is currently active
analysis_df["active_proxy"] = (
    (analysis_df["estimated_revenue_l365d"] > 0)
    & (analysis_df["number_of_reviews_ltm"] > 0)
)

print(
    "\nListings meeting active proxy:",
    analysis_df["active_proxy"].sum()
)

# Calculate revenue statistics by property type and bedroom group
revenue_by_type_beds = (
    analysis_df
    .groupby(["property_group", "bedroom_group"])
    ["estimated_revenue_l365d"]
    .agg(
        listing_count="count",
        median_revenue="median",
        mean_revenue="mean"
    )
    .reset_index()
)

# Calculate median revenue for all listings and active-proxy listings
revenue_comparison = (
    analysis_df
    .groupby("property_group")
    .apply(
        lambda group: pd.Series({
            "all_listings_median": group["estimated_revenue_l365d"].median(),
            "active_proxy_median": group.loc[
                group["active_proxy"], "estimated_revenue_l365d"
            ].median()
        }),
        include_groups=False
    )
    .reset_index()
)

# Save the analysis results
revenue_by_type_beds.to_csv(
    OUTPUT_PATH / "revenue_by_type_beds.csv",
    index=False
)

revenue_comparison.to_csv(
    OUTPUT_PATH / "revenue_comparison.csv",
    index=False
)

# Display results
print("\nRevenue by property type and bedroom group:")
print(revenue_by_type_beds.to_string(index=False))

print("\nRevenue comparison:")
print(revenue_comparison.to_string(index=False))

print("\nBedroom group counts:")
print(
    analysis_df["bedroom_group"]
    .value_counts()
    .reindex(
        ["Studio", "1 bedroom", "2 bedrooms", "3+ bedrooms"],
        fill_value=0
    )
)

print("\nRevenue analysis completed.")