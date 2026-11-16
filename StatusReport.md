# HappyFeet: Milestone 3 Status Report

**Team:** Mann Sheth, Vansh Patel, Jacob Drucker, Shuvam Sinha
**Research question:** Do counties with worse access to grocery stores have higher rates of adult obesity and diabetes, and does that relationship hold after controlling for income and poverty? (See [ProjectPlan.md](ProjectPlan.md).)

## Task Overview

| Task (from [ProjectPlan.md](ProjectPlan.md)) | Status | Main artifacts |
|---|---|---|
| Repository setup | Completed | `data/raw`, `data/processed`, `scripts`, `docs`, `results` |
| Data acquisition | Completed | [acquire_census.py](scripts/acquire_census.py), [acquire_places.py](scripts/acquire_places.py), [acquire_fea.py](scripts/acquire_fea.py), manifests in [data/raw](data/raw) |
| Data quality pre-assessment | Completed | [census_quality_pre.md](docs/census_quality_pre.md), [places_quality_pre.md](docs/places_quality_pre.md), [fea_quality_pre.md](docs/fea_quality_pre.md) |
| Data cleaning | Completed | [data/processed](data/processed), [OpenRefine histories](data/openrefine_history) |
| Data integration | Completed | [integrate.py](scripts/integrate.py), [merged_county.csv](data/processed/merged_county.csv) |
| Analysis and visualization | In progress | [explore.py](scripts/explore.py), [results](results) |
| Workflow and reproducibility | Not started | [requirements.txt](requirements.txt) |
| Final report | Not started | |

## Census data acquisition status report

The data come from the U.S. Census Bureau’s [American Community Survey (ACS) 2020–2024 5-year estimates](https://www.census.gov/data/developers/data-sets/acs-5year.html), pulled at the county level through the Census API. A Python script ([acquire_census.py](scripts/acquire_census.py)) saved the raw response in [acs5_county_2024.csv](data/raw/acs5_county_2024.csv) and wrote a manifest with the source URL, the query, the download time, the row count, and a SHA-256 checksum ([acs5_manifest.json](data/raw/acs5_manifest.json)). The request covered county, county code, state, state code, total population, median household income, the number of people for whom poverty status was determined, and the number of people below the poverty level. These are the data points that are important for our analysis and allow us to join this dataset with the other two.

### Census data cleaning

Cleaning was done in OpenRefine on a copy of the raw file. When downloading, leading zeros were kept, and a five-digit FIPS column was built by joining the two-digit state code to the three-digit county code (for example, 01 + 001 for Autauga County, Alabama). The combined name field was split into separate county and state name columns, the numerical columns were converted from text to numbers, and the columns were renamed to lowercase snake case. The Census placeholder value -666666666 found in the median income value for De Baca County, New Mexico was replaced with a blank cell. From here, all Puerto Rico counties were removed from the dataset leaving us with a total of 3,144 rows. The final file was exported as a CSV to [county_income_2024_cleaned.csv](data/processed/county_income_2024_cleaned.csv) and checked to confirm that FIPS was a unique, five-character text, with one row per county.

## PLACES data acquisition status report

The data come from the Centers for Disease Control and Prevention's [Local Data for Better Health, County Data, 5-Year Release](https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-County-Data-20/swc5-untb/about_data), pulled at the county level without any API needed. A Python script ([acquire_places.py](scripts/acquire_places.py)) saved the raw response in [places_county_2025.csv](data/raw/places_county_2025.csv) and wrote a manifest with the source URL, the query, the download time, the row count, and a SHA-256 checksum ([places_manifest.json](data/raw/places_manifest.json)). The request covered county, county code, state, state code, total population, total population over 18-years-old, rate of obesity, rate of food insecurity, and rate of diabetes. These are the data points that are important for our analysis and allow us to join this dataset with the other two.

### PLACES data cleaning

Cleaning was done in OpenRefine on a copy of the raw file, and the steps are saved in [places_operations.json](data/openrefine_history/places_operations.json). When downloading, leading zeros were kept, and the FIPS code of each county was already accurately reported, with no joining needed. The first step was to remove columns that were not needed for our analysis, such as data on other health issues (arthritis, blood pressure, cancer, etc.). Afterwards, the remaining diabetes, food insecurity, and obesity columns had a Confidence Interval column that needed cleaning. Before, each column listed the upper and lower bound of the confidence interval, such as "(12.13, 40.02)". This was formatted as a text block, which made it difficult to interpret, so I split these into two columns, one for the lower bound and one for the upper bound. I then took all of the columns that needed to be expressed as a number and converted them all using the "transformation" feature in OpenRefine. The final file was exported as a CSV to [places_county_2025_clean.csv](data/processed/places_county_2025_clean.csv).

## Food Environment Atlas data acquisition status report

The data comes from the U.S. Department of Agriculture Economic Research Service's [Food Environment Atlas (2025 edition)](https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation-downloads), downloaded at the county level as a zipped set of CSV files with no API key needed. I wrote a Python script ([acquire_fea.py](scripts/acquire_fea.py)) that saved the raw download as [fea_county_2025.zip](data/raw/fea_county_2025.zip) and wrote a manifest with the source page, the download URL, the download time, the file size, the list of files in the zip, and a SHA-256 checksum ([fea_manifest.json](data/raw/fea_manifest.json)). The zip contains StateAndCountyData.csv, which holds every indicator in the Atlas, along with a variable list and a ReadMe. From the roughly 300 indicators, we used the percentage of the population with low access to a store, along with low access for low-income residents, households without a car, children, and seniors, plus grocery stores per 1,000 people and the adult diabetes rate. These are the data points that are important for our analysis, and the county FIPS code allows us to join this dataset with the others.

### Food Environment Atlas data cleaning

I cleaned the dataset in OpenRefine using a copy of the raw file, and saved my work in the file [fea_operations.json](data/openrefine_history/fea_operations.json). The raw file is in a long format with 957,753 rows, one row per county per variable, so the first step was to keep only the rows for the 8 variables we needed. The file was then pivoted with OpenRefine's key-value columnize feature so that each variable became its own column, leaving one row per county, instead of there being one row per variable for each county. Adult obesity was removed because it is only reported at the state level, not the county level (all counties in the same state had the same value). The Atlas placeholder values -9999 and -8888 were replaced with blank cells so it wouldn't affect numerical summaries, and the columns were converted from text to numbers and renamed to a standardized format that we previously determined. The 8 Connecticut counties were removed because the Atlas still uses Connecticut's old county codes, while the PLACES and ACS data use the 9 planning regions that replaced them in 2022, so they could not be joined. The Connecticut rows are listed in [fea_excluded.csv](data/processed/fea_excluded.csv). The final file was exported as a CSV to [fea_clean.csv](data/processed/fea_clean.csv) and checked to confirm that FIPS was a unique, five-character text, with one row for each of the 3,136 counties.

## Data integration status report

[integrate.py](scripts/integrate.py) checks that FIPS is a unique five-digit code in each cleaned file, adds an `acs_` prefix to the Census columns, derives a poverty rate, and inner-joins the three files into [merged_county.csv](data/processed/merged_county.csv) (**3,134 counties, 27 columns**; counts in [merge_summary.json](data/processed/merge_summary.json)). Eleven counties are dropped and listed in [merge_unmatched.csv](data/processed/merge_unmatched.csv): 9 Connecticut planning regions (not in the Atlas), Loving County, TX (not published by PLACES), and Valdez-Cordova, AK (split in 2019; only the Atlas still uses it).

## Exploratory analysis

[explore.py](scripts/explore.py) writes [descriptive statistics](results/descriptive_stats.csv), [correlations](results/correlations.csv) and three figures. The overall low-access share barely correlates with obesity (r = -0.06) or diabetes (r = -0.05) ([figure](results/fig_low_access_vs_health.png)), low access without a car does moderately (r = 0.31 and 0.41), and poverty and income correlate most strongly (poverty vs diabetes r = 0.81; [heatmap](results/fig_correlation_heatmap.png)). This makes Research Question 2, whether food access matters after controlling for income, central to the regressions. The PLACES and Atlas diabetes estimates agree only moderately (r = 0.52, [figure](results/fig_diabetes_places_vs_fea.png)), so we use PLACES as the outcome and the Atlas figure as a robustness check.

## Updated Timeline

| # | Task | Status | Planned date | Revised date | Team members |
|---|---|---|---|---|---|
| 1 | Repository setup | Completed | Oct 16 | Oct 16 | Shuvam |
| 2 | Data acquisition | Completed | Oct 23 | Nov 13 | Vansh, Mann (scripts written by each dataset's owner) |
| 3 | Data cleaning and integration | Completed | Nov 6 | Nov 15 | Jacob, Shuvam, Mann (cleaning); Vansh (integration) |
| 4 | Plan update and status report (Milestone 3) | Completed | Nov 13 | Nov 16 | All |
| 5 | Analysis and visualization | In progress (exploratory analysis done) | Nov 13 | Nov 27 | Vansh, Mann |
| 6 | Workflow and reproducibility | Not started | Dec 4 | Dec 4 | Jacob, Shuvam |
| 7 | Final report and submission | Not started | Dec 11 | Dec 11 | All |

Remaining for Task 5: regression models for Research Questions 1–3 (with income and poverty as controls), the subgroup comparison for Question 3, and a county map for Question 4. Task 6 will chain the acquisition scripts, the OpenRefine histories, `integrate.py` and the analysis scripts into one run-all script or Snakemake workflow. [requirements.txt](requirements.txt) now includes pandas and matplotlib for the new scripts.

## Changes to Our Project Plan

The research question is unchanged. Changes so far:

- **Each dataset owner acquired and cleaned their own source**, instead of splitting acquisition and cleaning between pairs. Vansh took over integration and exploratory analysis.
- **Analysis moved from Nov 13 to Nov 27** because acquisition and cleaning took longer than planned. The final deadline is unchanged.
- **Cleaning used OpenRefine** with saved operation histories, answering the tool question in our plan's Gaps section.
- **Atlas obesity was dropped** because it is state-level, so PLACES is our only obesity source.
- **Acquisition scripts record provenance** (URL, download time, SHA-256), addressing our concern about government data changing.

## Response to Milestone 2 Feedback

The feedback asked whether data quality is consistent across counties and jurisdictions, and which parts of the Food Environment Atlas we use.

### 1. Data quality varies across counties and states

Measured in [merged_county.csv](data/processed/merged_county.csv):

- **Missing data clusters by state.** PLACES has no obesity or diabetes estimates for Kentucky or Pennsylvania (187 counties) and no food insecurity estimates for 11 states (844 counties). Grocery stores per 1,000 is missing for 908 mostly small counties (median population 7,854 vs 25,909 overall).
- **Precision depends on county size.** The median obesity confidence interval is 16.7 points wide in the smallest quarter of counties and 11.4 in the largest.
- **Jurisdictions differ between sources** in Connecticut, Alaska and Loving County, TX (see integration above).
- **Rural measures differ.** 48 rural counties report 100% low access because the Atlas uses a 10-mile rural cutoff versus 1 mile in urban areas.

In the analysis we will report the number of counties in each model, compare dropped and kept counties on income, poverty and access, control for state, and rerun the main models weighted by population and without the least precise counties.

### 2. Food Environment Atlas variables we use

We keep 7 of the roughly 300 indicators. Restaurants, food prices, assistance programs and similar indicators are outside our question about physical access to grocery stores.

| Atlas code | Column | Used for |
|---|---|---|
| `PCT_LACCESS_POP19` | `fea_pct_low_access_2019` | Main access measure (Q1, Q2) |
| `PCT_LACCESS_LOWI19` | `fea_pct_low_access_lowinc_2019` | Subgroups (Q3); low-income counties (Q2) |
| `PCT_LACCESS_HHNV19` | `fea_pct_low_access_no_car_2019` | Subgroups (Q3) |
| `PCT_LACCESS_CHILD19` | `fea_pct_low_access_children_2019` | Subgroups (Q3) |
| `PCT_LACCESS_SENIORS19` | `fea_pct_low_access_seniors_2019` | Subgroups (Q3) |
| `GROCPTH20` | `fea_grocery_per_1k_2020` | Alternative access measure (Q1) |
| `PCT_DIABETES_ADULTS19` | `fea_diabetes_pct_2019` | Cross-check of PLACES diabetes only |

## Challenges and How We Are Addressing Them

1. **Connecticut county codes** don't match across sources. *Resolved:* excluded the 8 old counties ([fea_excluded.csv](data/processed/fea_excluded.csv)); noted as a limitation.
2. **Inconsistent formats:** long-format Atlas data, text confidence intervals in PLACES, and placeholder codes (-666666666, -9999, -8888). *Resolved* in OpenRefine.
3. **Missing data clusters by state.** *Plan:* the steps in the feedback response above.
4. **Low-access subgroup measures use different distance cutoffs** than the total. *Plan:* compare subgroups only with each other and add a rural/urban indicator.
5. **Repository clean-up:** early uploads went to wrong folders. *Resolved:* the layout is now `data/raw` → `data/processed` → `results`.

## Team Contributions

Each team member wrote and committed their own summary.

### Vansh Patel

I merged the cleaned datasets ([integrate.py](scripts/integrate.py)), wrote the exploratory analysis ([explore.py](scripts/explore.py), [results](results)), and measured how data quality varies across counties to answer our Milestone 2 feedback. In this report I wrote the task overview, integration, analysis, feedback and challenges sections and the timeline table. Full summary: [Vansh_Patel_StatusReport_Contribution.md](cont_files/Vansh_Patel_StatusReport_Contribution.md).

### Other team members

- [Mann Sheth](cont_files/Mann_Sheth_StatusReport_Contribution.md)
- [Jacob Drucker](cont_files/Jacob_Drucker_StatusReport_Contribution.md)
- [Shuvam Sinha](cont_files/Shuvam_Sinha_StatusReport_Contribution.md)
