"""
DataJam 2026 - static, slide-ready Vancouver maps (PNG).
Redraws the three folium maps in make_map.py without needing geopandas or
the raw Inside Airbnb files: polygons, values and listing coordinates are
read from the HTML files that make_map.py already produced.

Run:  python3 make_static_maps.py [folder_with_html_files] [output_folder]
Data: Inside Airbnb, Vancouver, 15 June 2026, CC BY 4.0.
"""
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from matplotlib.patches import Polygon

HERE = Path(__file__).resolve().parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE
MIN_ACTIVE = 30
CREDIT = "Data: Inside Airbnb, Vancouver, 15 June 2026, CC BY 4.0."
ASPECT = 1 / np.cos(np.radians(49.25))  # stretch x so Vancouver isn't squashed


def load_features(html_path):
    s = html_path.read_text(encoding="utf8")
    start = s.index("_add(", s.index("function geo_json_")) 
    start = s.index("_add({", start) + len("_add(")
    return json.JSONDecoder().raw_decode(s[start:])[0]["features"]


def load_points(html_path):
    s = html_path.read_text(encoding="utf8")
    start = s.index("L.heatLayer(") + len("L.heatLayer(")
    return np.array(json.JSONDecoder().raw_decode(s[start:].lstrip())[0])


def rings(geom):
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    return [np.array(p[0]) for p in polys]  # outer rings only


def _area_centroid(r):
    x, y = r[:, 0], r[:, 1]
    x1, y1 = np.roll(x, -1), np.roll(y, -1)
    cross = x * y1 - x1 * y
    a = cross.sum() / 2
    return abs(a), ((x + x1) * cross).sum() / (6 * a), ((y + y1) * cross).sum() / (6 * a)


def centroid(feature):
    """Area-weighted centroid of the largest outer ring."""
    _, cx, cy = max((_area_centroid(r) for r in rings(feature["geometry"])), key=lambda t: t[0])
    return cx, cy


def setup_axes(title, subtitle):
    fig, ax = plt.subplots(figsize=(10, 7.6), dpi=200)
    ax.set_aspect(ASPECT)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    fig.text(0.04, 0.955, title, fontsize=17, fontweight="bold", ha="left", va="top")
    fig.text(0.04, 0.905, subtitle, fontsize=10, ha="left", va="top", color="#444")
    return fig, ax


def draw_hoods(ax, feats, colours, edge="white", lw=0.8):
    patches, cols = [], []
    for f, c in zip(feats, colours):
        for r in rings(f["geometry"]):
            patches.append(Polygon(r, closed=True)); cols.append(c)
    ax.add_collection(PatchCollection(patches, facecolor=cols, edgecolor=edge, linewidth=lw))
    allp = np.vstack([r for f in feats for r in rings(f["geometry"])])
    ax.set_xlim(allp[:, 0].min() - 0.003, allp[:, 0].max() + 0.003)
    ax.set_ylim(allp[:, 1].min() - 0.003, allp[:, 1].max() + 0.003)


NUDGE = {"South Cambie": (-0.001, 0.006), "Riley Park": (0.006, 0.0),
         "Strathcona": (0.0, 0.0)}


def label_hoods(ax, feats, fmt=None, colours=None, hide_when=None):
    for i, f in enumerate(feats):
        x, y = centroid(f)
        dx, dy = NUDGE.get(f["properties"]["neighbourhood"], (0, 0))
        x, y = x + dx, y + dy
        c = colours[i] if colours is not None else "#ffffff"
        rgb = matplotlib.colors.to_rgb(c)
        txtcol = "white" if (0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]) < 0.5 else "#111"
        name = f["properties"]["neighbourhood"].replace("-", "-\n").replace(" ", "\n", 1)
        show_val = fmt is not None and not (hide_when and hide_when(f["properties"]))
        txt = f"{name}\n{fmt(f['properties'])}" if show_val else name
        ax.text(x, y, txt, ha="center", va="center", fontsize=5.8, color=txtcol, linespacing=1.05)


def footer(fig, extra=""):
    fig.text(0.04, 0.012, f"{CREDIT} Map: OpenStreetMap contributors.  {extra}",
             fontsize=7.5, color="#555")


def choropleth(feats, key, cmap_name, title, subtitle, cbar_label, outfile,
               grey_when=None, fmt=None, extra_note=""):
    cmap = plt.get_cmap(cmap_name)
    vals = np.array([f["properties"].get(key) if f["properties"].get(key) is not None
                     else np.nan for f in feats], dtype=float)
    greyed = np.array([bool(grey_when(f["properties"])) if grey_when else False for f in feats])
    vals_plot = np.where(greyed, np.nan, vals)
    norm = Normalize(np.nanmin(vals_plot), np.nanmax(vals_plot))
    colours = ["#d9d9d9" if np.isnan(v) else cmap(norm(v)) for v in vals_plot]
    fig, ax = setup_axes(title, subtitle)
    draw_hoods(ax, feats, colours)
    label_hoods(ax, feats, fmt, colours, grey_when)
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    cb = fig.colorbar(sm, ax=ax, shrink=0.55, pad=0.01)
    cb.set_label(cbar_label, fontsize=9)
    footer(fig, extra_note)
    fig.subplots_adjust(top=0.86, bottom=0.05, left=0.02, right=0.97)
    fig.savefig(OUT / outfile, facecolor="white")
    plt.close(fig)
    print("saved", outfile)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    feats = load_features(SRC / "revenue_map.html")
    print("neighbourhoods:", len(feats))

    # Map 1: where the listings are (share computed from the data, not typed in)
    tot = sum(f["properties"]["total_listings"] or 0 for f in feats)
    dt = next(f["properties"]["total_listings"] for f in feats if f["properties"]["neighbourhood"] == "Downtown")
    share = dt / tot
    choropleth(
        feats, "total_listings", "YlOrRd",
        "Where Vancouver's entire-home Airbnbs are",
        f"Entire-home listings per neighbourhood (min stay 30 nights or less). Downtown alone holds about {share:.0%} of all listings.",
        "Entire-home listings", "map1_listing_count.png",
        fmt=lambda p: f"{int(p['total_listings']):,}")

    # Map 2: where they earn (grey = too thin to trust)
    def _num(v):
        return 0 if v is None or v != v else v

    def thin(p):  # same rule as make_map.py: thin with OR without large operators
        return (_num(p.get("active_listings")) < MIN_ACTIVE
                or _num(p.get("active_no_big_host")) < MIN_ACTIVE)
    choropleth(
        feats, "median_revenue", "YlGn",
        "Where they earn: median estimated annual revenue",
        f"Per entire home with revenue > 0, CAD. Grey = fewer than {MIN_ACTIVE} earning listings, with or without large operators.",
        "Median estimated annual revenue (CAD)", "map2_median_revenue.png",
        grey_when=thin, fmt=lambda p: f"${p['median_revenue']/1000:.0f}k"
        if p.get("median_revenue") is not None else "",
        extra_note="Revenue is an Inside Airbnb estimate, gross, before costs.")

    # Map 3: density heatmap over neighbourhood outlines
    pts = load_points(SRC / "listing_density.html")
    fig, ax = setup_axes("Listing density: where Airbnbs cluster",
                         f"Each hexagon counts entire-home listings (n = {len(pts):,}), log colour scale so quieter areas stay visible.")
    draw_hoods(ax, feats, ["#f4f4f4"] * len(feats), edge="#bbbbbb", lw=0.6)
    hb = ax.hexbin(pts[:, 1], pts[:, 0], gridsize=55, cmap="inferno_r", mincnt=1, bins="log",
                   linewidths=0.1, alpha=0.85, extent=ax.get_xlim() + ax.get_ylim())
    cb = fig.colorbar(hb, ax=ax, shrink=0.55, pad=0.01)
    cb.set_label("Listings per cell (log10 scale)", fontsize=9)
    footer(fig)
    fig.subplots_adjust(top=0.86, bottom=0.05, left=0.02, right=0.97)
    fig.savefig(OUT / "map3_listing_density.png", facecolor="white")
    plt.close(fig)
    print("saved map3_listing_density.png")


if __name__ == "__main__":
    main()
