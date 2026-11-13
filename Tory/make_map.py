"""
DataJam 2026 - Vancouver short-term rental maps
Data: Inside Airbnb, Vancouver, 15 June 2026, CC BY 4.0.

Run:  python3 make_map.py
Needs: neighbourhoods.geojson and listings.csv.gz. The script looks in the
repo's Data/ folder (any subfolder) first, then in ~/Downloads. Both files come
from insideairbnb.com/get-data (Vancouver, 15 June 2026).
Outputs (same folder as this script):
  listing_count_map.html, revenue_map.html, listing_density.html,
  neighbourhood_summary_python.csv, bedroom_summary_python.csv,
  sensitivity_big_hosts.csv, filter_steps_ranking.csv
"""
from pathlib import Path

import folium
import geopandas as gpd
import pandas as pd
from folium.plugins import HeatMap

OUT = Path(__file__).resolve().parent
REPO = OUT.parent


def find_data(name):
    """Find an input file in <repo>/Data (any subfolder), else in ~/Downloads."""
    data_dir = REPO / "Data"
    if data_dir.exists():
        hits = sorted(data_dir.rglob(name))
        if hits:
            return hits[0]
    in_downloads = Path.home() / "Downloads" / name
    if in_downloads.exists():
        return in_downloads
    raise FileNotFoundError(
        f"Could not find {name}. Put it in the repo's Data/ folder or in ~/Downloads "
        "(download from insideairbnb.com/get-data, Vancouver, 15 June 2026).")


CENTER = [49.2527, -123.1207]
MIN_ACTIVE = 30  # grey out areas with fewer earning listings than this

# 1. Neighbourhood shapes (merge the duplicate Strathcona polygons)
hoods = gpd.read_file(find_data("neighbourhoods.geojson"))
print("polygon rows before dissolve:", len(hoods))
hoods = hoods.dissolve(by="neighbourhood", as_index=False)
print("neighbourhoods after dissolve:", len(hoods))  # expect 23

# 2. Listings
raw = pd.read_csv(find_data("listings.csv.gz"))
print("\nall listings:", len(raw))  # expect 6509
print(raw["room_type"].value_counts())

raw["price_num"] = pd.to_numeric(
    raw["price"].astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce")


def summarise(df):
    """One row per neighbourhood. Revenue stats use listings with estimated revenue > 0."""
    active = df[df["estimated_revenue_l365d"] > 0]
    counts = df.groupby("neighbourhood_cleansed").agg(
        total_listings=("id", "count"), median_price=("price_num", "median"))
    rev = active.groupby("neighbourhood_cleansed").agg(
        active_listings=("id", "count"),
        median_revenue=("estimated_revenue_l365d", "median"),
        mean_revenue=("estimated_revenue_l365d", "mean"))
    return (counts.join(rev).reset_index()
            .rename(columns={"neighbourhood_cleansed": "neighbourhood"}))


# 3. FILTER STEPS (decision log): apply one filter at a time and record the
#    neighbourhood ranking after each, so each decision's effect is isolated.
steps = {"1_all_rooms": raw.copy()}

# Step 2: entire homes only (DDD buys whole properties)
listings = raw[raw["room_type"] == "Entire home/apt"].copy()
steps["2_entire_homes"] = listings.copy()

# Step 3: minimum stay over 30 nights is a long-term rental, not a short-term one
long_stay = listings["minimum_nights"] > 30
print("entire homes with minimum_nights > 30 (removed):", int(long_stay.sum()))
listings = listings[~long_stay].copy()
steps["3_min_nights_30"] = listings.copy()

# Step 4: nightly prices above $5,000 are data errors (e.g. one Fairview listing at
#         $91,294/night). Missing prices are kept so listing counts stay complete;
#         they drop out of the revenue stats anyway because revenue is not > 0.
bad_price = listings["price_num"] > 5000
print("price errors removed (>$5,000/night):", int(bad_price.sum()))
listings = listings[~bad_price].copy()
steps["4_price_errors"] = listings.copy()
after = summarise(listings)

print("\nlistings remaining after each step:")
for k, d in steps.items():
    print(f"  {k}: {len(d)}")

ladder = None
for k, d in steps.items():
    s = summarise(d)[["neighbourhood", "median_revenue"]].rename(
        columns={"median_revenue": f"median_rev_{k}"})
    s[f"rank_{k}"] = s[f"median_rev_{k}"].rank(ascending=False)
    ladder = s if ladder is None else ladder.merge(s, on="neighbourhood")
names = list(steps)
for a, b in zip(names[:-1], names[1:]):
    ladder[f"move_{b[0]}"] = ladder[f"rank_{a}"] - ladder[f"rank_{b}"]  # + = moved up
ladder["earning_listings_final"] = ladder["neighbourhood"].map(
    after.set_index("neighbourhood")["active_listings"])
rank_cols = ["neighbourhood"] + [f"rank_{k}" for k in names] + ["earning_listings_final"]
print("\nRANKING AFTER EACH FILTER STEP (1 = highest median revenue)")
print(ladder[rank_cols].sort_values(f"rank_{names[-1]}").round(0).to_string(index=False))
ladder.round(0).to_csv(OUT / "filter_steps_ranking.csv", index=False)

# 3c. SENSITIVITY: does the ranking change without large operators?
#     Cutoffs 10 / 20 / 50 are all tried so the 20 is not an arbitrary pick.
for cutoff in (10, 20, 50):
    n_big = int((listings["calculated_host_listings_count"] >= cutoff).sum())
    print(f"hosts with {cutoff}+ Vancouver listings: {n_big} entire homes")
no_big = summarise(listings[listings["calculated_host_listings_count"] < 20])
sens = after[["neighbourhood", "active_listings", "median_revenue"]].merge(
    no_big[["neighbourhood", "active_listings", "median_revenue"]],
    on="neighbourhood", suffixes=("_all", "_no_big_host"))
sens["rank_all"] = sens["median_revenue_all"].rank(ascending=False)
sens["rank_no_big_host"] = sens["median_revenue_no_big_host"].rank(ascending=False)
sens["rank_change"] = sens["rank_all"] - sens["rank_no_big_host"]
print("\nSENSITIVITY: all hosts vs hosts with fewer than 20 listings")
print(sens.sort_values("rank_all").round(0).to_string(index=False))
sens.round(0).to_csv(OUT / "sensitivity_big_hosts.csv", index=False)

# 3d. MIN-NIGHTS CUTOFF TEST: is the 30-night rule driving the result?
def trusted_rank(df):
    s = summarise(df)
    s = s[s["active_listings"].fillna(0) >= MIN_ACTIVE]
    return s.set_index("neighbourhood")["median_revenue"].rank(ascending=False, method="min")


base = steps["2_entire_homes"]
base = base[~(base["price_num"] > 5000)]
cuts = (7, 14, 30, 60, 90)
cut = pd.DataFrame({f"rank_le_{n}": trusted_rank(base[base["minimum_nights"] <= n])
                    for n in cuts}).sort_values("rank_le_30")
cut.to_csv(OUT / "minnights_cutoff_test.csv")
print("\nMIN-NIGHTS CUTOFF TEST (rank among neighbourhoods with 30+ earning listings)")
print("entire homes kept at each cutoff:",
      {n: int((base["minimum_nights"] <= n).sum()) for n in cuts})
print(cut.to_string())
print("Top 3 at each cutoff:")
for c in cut.columns:
    print(" ", c, cut[c].nsmallest(3).index.tolist())

summary = after.merge(
    no_big[["neighbourhood", "active_listings"]].rename(
        columns={"active_listings": "active_no_big_host"}),
    on="neighbourhood", how="left")
summary["earning_share"] = summary["active_listings"] / summary["total_listings"]
print("earning share overall:", round(summary["active_listings"].sum() / summary["total_listings"].sum(), 3))
summary.round(0).assign(earning_share=summary["earning_share"].round(3)).to_csv(
    OUT / "neighbourhood_summary_python.csv", index=False)

gdf = hoods.merge(summary, on="neighbourhood", how="left")
print("\nunmatched names:", gdf[gdf["total_listings"].isna()]["neighbourhood"].tolist())  # expect []
gdf["thin"] = ((gdf["active_listings"].fillna(0) < MIN_ACTIVE)
               | (gdf["active_no_big_host"].fillna(0) < MIN_ACTIVE))
print("greyed out (fewer than", MIN_ACTIVE, "earning listings, with or without large operators):",
      gdf[gdf["thin"]]["neighbourhood"].tolist())

# 4. Bedroom mix (entire homes, 1-3 bedrooms, all of Vancouver)
active_homes = listings[(listings["estimated_revenue_l365d"] > 0)
                        & (listings["bedrooms"].between(1, 3))]
bed = (active_homes.groupby("bedrooms")
       .agg(earning_listings=("id", "count"),
            median_price=("price_num", "median"),
            median_revenue=("estimated_revenue_l365d", "median"))
       .reset_index())
bed.round(0).to_csv(OUT / "bedroom_summary_python.csv", index=False)
print("\nBedroom mix (entire homes, earning listings):")
print(bed.round(0).to_string(index=False))

# 4b. Neighbourhood x bedroom table (flag cells with fewer than MIN_ACTIVE listings)
nb = (active_homes.groupby(["neighbourhood_cleansed", "bedrooms"])
      .agg(earning_listings=("id", "count"),
           median_price=("price_num", "median"),
           median_revenue=("estimated_revenue_l365d", "median"))
      .reset_index().rename(columns={"neighbourhood_cleansed": "neighbourhood"}))
nb["enough_data"] = nb["earning_listings"] >= MIN_ACTIVE
nb.round(0).to_csv(OUT / "neighbourhood_bedroom_summary.csv", index=False)

# 5. Maps
bounds = gdf.total_bounds
fit = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]


def blank_map(zoom=11):
    m = folium.Map(location=CENTER, zoom_start=zoom, tiles="OpenStreetMap")
    m.fit_bounds(fit)
    return m


def hover_layer(fields):
    return folium.GeoJson(
        gdf, style_function=lambda x: {"fillOpacity": 0, "weight": 0},
        tooltip=folium.GeoJsonTooltip(fields=fields))


# Map A: listing count (entire homes)
mA = blank_map()
folium.Choropleth(
    geo_data=gdf.__geo_interface__, data=gdf,
    columns=["neighbourhood", "total_listings"],
    key_on="feature.properties.neighbourhood",
    fill_color="YlOrRd", legend_name="Entire-home listings",
).add_to(mA)
hover_layer(["neighbourhood", "total_listings", "median_price"]).add_to(mA)
mA.save(OUT / "listing_count_map.html")

# Map B: median estimated annual revenue (grey = too few earning listings)
gdf["map_value"] = gdf["median_revenue"].where(~gdf["thin"])
mB = blank_map()
folium.Choropleth(
    geo_data=gdf.__geo_interface__, data=gdf,
    columns=["neighbourhood", "map_value"],
    key_on="feature.properties.neighbourhood",
    fill_color="YlGn", nan_fill_color="lightgrey",
    legend_name="Median estimated annual revenue per entire home (CAD). Grey = under 30 earning listings (with or without large operators)",
).add_to(mB)
hover_layer(["neighbourhood", "total_listings", "active_listings",
             "active_no_big_host", "median_price", "median_revenue"]).add_to(mB)
mB.save(OUT / "revenue_map.html")

# Map C: density heatmap (entire homes)
mC = blank_map(12)
HeatMap(listings[["latitude", "longitude"]].dropna().values.tolist(), radius=8).add_to(mC)
mC.save(OUT / "listing_density.html")

print("\nSaved to", OUT)
print("Credit on slides: Data: Inside Airbnb, Vancouver, 15 June 2026, CC BY 4.0. Map: OpenStreetMap contributors.")
