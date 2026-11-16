"""First-pass exploratory analysis of the merged county dataset.

This is groundwork for the Analysis and Visualization task, not the final models:
descriptive statistics, a correlation matrix, and a few plots that tell us whether
the relationships in our research questions are worth modelling.

Input:  data/processed/merged_county.csv  (made by scripts/integrate.py)
Output: results/descriptive_stats.csv
        results/correlations.csv
        results/fig_low_access_vs_health.png
        results/fig_diabetes_places_vs_fea.png
        results/fig_correlation_heatmap.png

Run from the repository root:  python scripts/explore.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
MERGED = ROOT / "data" / "processed" / "merged_county.csv"
RESULTS = ROOT / "results"

# Variables tied to our research questions, with short labels for tables and plots.
VARS = {
    "places_obesity_pct": "Obesity % (PLACES)",
    "places_diabetes_pct": "Diabetes % (PLACES)",
    "places_food_insecurity_pct": "Food insecurity % (PLACES)",
    "fea_pct_low_access_2019": "Low access %",
    "fea_pct_low_access_lowinc_2019": "Low access, low income %",
    "fea_pct_low_access_no_car_2019": "Low access, no car %",
    "fea_pct_low_access_children_2019": "Low access, children %",
    "fea_pct_low_access_seniors_2019": "Low access, seniors %",
    "fea_grocery_per_1k_2020": "Grocery stores per 1k",
    "acs_median_household_income": "Median household income",
    "acs_poverty_rate_pct": "Poverty rate %",
}


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    df = pd.read_csv(MERGED, dtype={"fips": str})
    data = df[list(VARS)]

    # Descriptive statistics, plus how many counties are missing each variable.
    stats = data.describe().T
    stats.insert(0, "missing", data.isna().sum())
    stats.index = [VARS[c] for c in stats.index]
    stats.round(3).to_csv(RESULTS / "descriptive_stats.csv")

    # Pearson and Spearman correlations (pairwise, so missing values only drop that pair).
    pearson = data.corr(method="pearson")
    spearman = data.corr(method="spearman")
    rows = []
    for outcome in ["places_obesity_pct", "places_diabetes_pct"]:
        for x in VARS:
            if x == outcome:
                continue
            rows.append(
                {
                    "outcome": VARS[outcome],
                    "variable": VARS[x],
                    "pearson_r": round(pearson.loc[outcome, x], 3),
                    "spearman_rho": round(spearman.loc[outcome, x], 3),
                    "n": int(data[[outcome, x]].dropna().shape[0]),
                }
            )
    pd.DataFrame(rows).to_csv(RESULTS / "correlations.csv", index=False)

    # Figure 1: low food access vs obesity and diabetes (Research Question 1).
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, outcome in zip(axes, ["places_obesity_pct", "places_diabetes_pct"]):
        sub = df[["fea_pct_low_access_2019", outcome]].dropna()
        ax.scatter(sub.iloc[:, 0], sub.iloc[:, 1], s=6, alpha=0.35)
        r = pearson.loc[outcome, "fea_pct_low_access_2019"]
        ax.set_xlabel("Population with low access to a store (%)")
        ax.set_ylabel(VARS[outcome])
        ax.set_title(f"{VARS[outcome]} vs low access (r = {r:.2f}, n = {len(sub)})")
    fig.tight_layout()
    fig.savefig(RESULTS / "fig_low_access_vs_health.png", dpi=150)
    plt.close(fig)

    # Figure 2: the two diabetes estimates against each other. Our plan said we would
    # cross-check the PLACES model estimates against the Atlas figures.
    sub = df[["fea_diabetes_pct_2019", "places_diabetes_pct"]].dropna()
    r = sub.corr().iloc[0, 1]
    fig, ax = plt.subplots(figsize=(5.5, 5))
    ax.scatter(sub.iloc[:, 0], sub.iloc[:, 1], s=6, alpha=0.35)
    lo, hi = sub.min().min(), sub.max().max()
    ax.plot([lo, hi], [lo, hi], color="grey", lw=1, ls="--", label="y = x")
    ax.set_xlabel("Adult diabetes % (Food Environment Atlas, 2019)")
    ax.set_ylabel("Adult diabetes % (PLACES, 2025 release)")
    ax.set_title(f"Diabetes estimates by source (r = {r:.2f}, n = {len(sub)})")
    ax.legend()
    fig.tight_layout()
    fig.savefig(RESULTS / "fig_diabetes_places_vs_fea.png", dpi=150)
    plt.close(fig)

    # Figure 3: correlation heatmap of all analysis variables.
    labels = [VARS[c] for c in VARS]
    fig, ax = plt.subplots(figsize=(9, 7.5))
    im = ax.imshow(pearson.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(labels)), labels, rotation=45, ha="right")
    ax.set_yticks(range(len(labels)), labels)
    for i in range(len(labels)):
        for j in range(len(labels)):
            v = pearson.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7,
                    color="white" if abs(v) > 0.6 else "black")
    fig.colorbar(im, ax=ax, label="Pearson r")
    ax.set_title("Correlations between analysis variables")
    fig.tight_layout()
    fig.savefig(RESULTS / "fig_correlation_heatmap.png", dpi=150)
    plt.close(fig)

    print(pd.DataFrame(rows).to_string(index=False))
    print(f"\nPLACES vs Atlas diabetes: r = {r:.3f}, n = {len(sub)}")


if __name__ == "__main__":
    main()
