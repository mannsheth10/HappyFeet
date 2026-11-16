"""Merge the three cleaned county datasets on the five-digit FIPS code.

Inputs (from data/processed/):
    places_county_2025_clean.csv   CDC PLACES health estimates
    fea_clean.csv                  USDA Food Environment Atlas
    county_income_2024_cleaned.csv Census ACS 2020-2024 income and poverty

Outputs:
    data/processed/merged_county.csv      one row per county found in all three
    data/processed/merge_unmatched.csv    counties dropped by the inner join, with the reason
    data/processed/merge_summary.json     row counts and checks, for the status report

Run from the repository root:  python scripts/integrate.py
"""
from pathlib import Path
import json

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"


def load(name: str) -> pd.DataFrame:
    # Read FIPS as text so leading zeros (e.g. 01001) survive.
    df = pd.read_csv(PROCESSED / name, dtype={"fips": str})
    assert df["fips"].str.fullmatch(r"\d{5}").all(), f"{name}: FIPS not 5 digits"
    assert not df["fips"].duplicated().any(), f"{name}: duplicate FIPS"
    return df


def main() -> None:
    places = load("places_county_2025_clean.csv")
    fea = load("fea_clean.csv")
    acs = load("county_income_2024_cleaned.csv")

    # Give the Census columns the same source prefix the other two datasets use,
    # and derive a poverty rate (people below poverty / people with poverty status determined).
    acs = acs.rename(
        columns={
            "county_name": "acs_county_name",
            "state_name": "acs_state_name",
            "total_population": "acs_population",
            "median_household_income": "acs_median_household_income",
            "poverty_status": "acs_poverty_universe",
            "income_below_poverty": "acs_below_poverty",
        }
    ).drop(columns=["state", "county"])
    acs["acs_poverty_rate_pct"] = (
        acs["acs_below_poverty"] / acs["acs_poverty_universe"] * 100
    ).round(2)

    # Record which counties each join would drop before doing it.
    sources = {"places": set(places.fips), "fea": set(fea.fips), "acs": set(acs.fips)}
    all_fips = set().union(*sources.values())
    unmatched = []
    for fips in sorted(all_fips):
        missing = [k for k, v in sources.items() if fips not in v]
        if missing:
            unmatched.append({"fips": fips, "missing_from": ";".join(missing)})
    unmatched = pd.DataFrame(unmatched)

    merged = places.merge(fea, on="fips", how="inner", validate="one_to_one").merge(
        acs, on="fips", how="inner", validate="one_to_one"
    )

    # Put identifiers first, then a single state/county label.
    merged.insert(1, "state_abbr", merged.pop("places_state_abbr"))
    merged.insert(2, "county_name", merged.pop("places_county_name"))
    merged = merged.drop(columns=["fea_state_abbr", "fea_county_name", "acs_county_name"])
    merged = merged.sort_values("fips").reset_index(drop=True)

    assert merged["fips"].is_unique

    merged.to_csv(PROCESSED / "merged_county.csv", index=False)
    unmatched.to_csv(PROCESSED / "merge_unmatched.csv", index=False)

    summary = {
        "rows_in": {"places": len(places), "fea": len(fea), "acs": len(acs)},
        "rows_merged": len(merged),
        "columns_merged": merged.shape[1],
        "unmatched_counties": len(unmatched),
        "missing_values": {c: int(n) for c, n in merged.isna().sum().items() if n},
    }
    (PROCESSED / "merge_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
