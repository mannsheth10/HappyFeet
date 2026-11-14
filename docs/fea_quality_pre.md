# Introduction
After the script has pulled the raw data for the USDA Food Environment Atlas, it will undergo a preliminary assessment. This is used to assess the data under all 4 dimensions of data quality.


# Assessment

## Completeness

No null values in fips

No null values in fea_state_abbr

No null values in fea_county_name

3 null values in fea_pct_low_access_2019

3 null values in fea_pct_low_access_lowinc_2019

3 null values in fea_pct_low_access_no_car_2019

6 null values in fea_pct_low_access_children_2019

5 null values in fea_pct_low_access_seniors_2019

910 null values in fea_grocery_per_1k_2020

24 null values in fea_diabetes_pct_2019

The null values were originally coded as -9999 or -8888 in the Atlas and were replaced with blank cells.

## Consistency


All fips entries are 5 digits.
No duplicate fips entries.


fea_state_abbr has 50 entries (49 states + DC) after removing Connecticut.

Connecticut uses the old pre-2022 county codes (09001-09015), while the PLACES and ACS datasets use the new planning region codes (09110-09190). These 8 rows cannot be joined, so they were removed and listed in data/processed/fea_excluded.csv

Adult obesity is reported at the state level (the same value for every county in a state), so it was removed. We will cross-check PLACES with diabetes instead.

## Accuracy

All columns parse as numbers, and every percentage is between 0% and 100%. 

Grocery stores per 1,000 people ranges from 0.04 - 2.34, which is reasonable and has no negative values. 

The children and seniors low access percentages are often much higher than the total low access percentage (e.g., Holmes County, OH: 5% total vs. 89% children). According to the Atlas documentation, this is because they use different distance cutoffs: the total counts people more than 1 mile from a store in urban areas but more than 10 miles in rural areas, while children and seniors use 1 mile everywhere. These columns should not be compared directly with the total in rural counties. 

Kusilvak, AK has 0% total low access but 55% no car and low access. This is also due to the different cutoffs: the no car column counts housing units more than 1 mile from a store everywhere, while the total uses 10 miles in rural areas.

## Timeliness

Timeliness of the dataset has been recorded in data/raw/fea_manifest.json. The Atlas is the 2025 edition, but the low access and diabetes data are from 2019 and the grocery store data is from 2020, which is older than the PLACES and ACS data.
