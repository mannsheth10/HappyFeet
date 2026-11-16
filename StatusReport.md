# Milestone 3 Status Report

Team: Mann Sheth, Vansh Patel, Jacob Drucker, Shuvam Sinha

Our project looks at whether counties with worse access to grocery stores have higher obesity and diabetes rates, and whether that still holds after accounting for income and poverty. So far we have downloaded and cleaned all three datasets, merged them into one file, and started looking at the data. The sections below go through each part of our [project plan](ProjectPlan.md).

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

## Merging the datasets

After the three datasets were cleaned, I wrote [integrate.py](scripts/integrate.py) to merge them using the FIPS code. The script makes sure each file has one row per county with a 5 digit FIPS code, then joins them together and adds a poverty rate column (people below poverty divided by total people counted). The merged file is [merged_county.csv](data/processed/merged_county.csv) and has 3,134 counties.

11 counties didn't show up in all three datasets, so they got dropped. These are listed in [merge_unmatched.csv](data/processed/merge_unmatched.csv). Most of them are the 9 Connecticut planning regions, since the Food Atlas still uses the old Connecticut counties. The other two are Loving County, TX (PLACES doesn't have it) and an old Alaska county code that the Atlas still uses.

## Early analysis

I also wrote [explore.py](scripts/explore.py) to get some basic stats and correlations before we start the actual regressions. The outputs are in the [results](results) folder.

Something we didn't expect: the overall low food access percentage has almost no correlation with obesity or diabetes (about -0.05). Income and poverty have much stronger relationships, for example poverty rate and diabetes have a correlation of 0.81. Low access for people without a car was the only food access variable with a moderate correlation (around 0.3 to 0.4). This means the second research question, whether food access still matters after controlling for income, is going to be really important.

We also compared the diabetes rate from PLACES with the diabetes rate from the Food Atlas, which we said we would do in our project plan. They only had a correlation of 0.52, so we decided to use the PLACES number since it's newer.

## Updated Timeline

- **Repository Setup**: Completed (Oct 16), Shuvam
- **Data Acquisition**: Completed (Nov 13), everyone did their own dataset
- **Data Cleaning and Integration**: Completed (Nov 15), cleaning by Jacob, Mann and Shuvam, merging by Vansh
- **Status Report (Milestone 3)**: Completed (Nov 16), all
- **Analysis and Visualization**: In progress, finishing by Nov 27, Vansh and Mann
- **Workflows and Reproducibility**: Not started, Dec 4, Jacob and Shuvam
- **Final Report**: Not started, Dec 11, all

Acquisition and cleaning took longer than we planned, so we pushed the analysis back from Nov 13 to Nov 27. The final deadline didn't change. For the analysis we still need to run the regressions and make a map of the counties that have low food access, high poverty and high obesity or diabetes.

## Changes to Our Project Plan

Our research question is the same. The main change is how we split up the work. Instead of two people downloading everything and two people cleaning everything, each person took one dataset and did both. Vansh then did the merging and the first analysis. We also ended up using OpenRefine for cleaning and saved the history files so the steps can be repeated. We dropped the obesity column from the Food Atlas because it was only reported by state, not by county.

## Milestone 2 Feedback

Our feedback asked whether data quality is consistent across counties, and told us to be specific about which parts of the Food Atlas we are using.

For the first point, we found that the data quality is not the same everywhere:

- PLACES is missing obesity and diabetes for every county in Kentucky and Pennsylvania, and food insecurity for every county in 11 states.
- About 900 counties are missing the grocery stores per 1,000 people number, and most of them are small counties.
- The PLACES numbers are estimates, and the estimates for small counties are less certain (their confidence intervals are wider).
- Some rural counties show 100% low food access because the Atlas uses a 10 mile distance in rural areas instead of 1 mile.

To deal with this, we will report how many counties are in each model, check whether the counties we drop are different from the ones we keep, and try controlling for state.

For the second point, these are the only Food Atlas variables we are using out of about 300:

- Percent of people with low access to a store (our main food access variable)
- Low access for low income people, households without a car, children, and seniors (for comparing groups in research question 3)
- Grocery stores per 1,000 people
- Adult diabetes rate (only to double check the PLACES diabetes numbers)

## Challenges

- Connecticut changed from counties to planning regions in 2022, but the Food Atlas still uses the old counties. We removed those rows and listed them in [fea_excluded.csv](data/processed/fea_excluded.csv).
- Each dataset was formatted differently. The Atlas had one row per variable instead of one per county, PLACES had confidence intervals stored as text, and the Census data used placeholder numbers like -666666666 for missing values. We fixed all of these in OpenRefine.
- A lot of data is missing in certain states (see the feedback section above). We can't fill it in, so we plan to be clear about which counties are included in each part of the analysis.
- Some files were uploaded to the wrong folders early on and had to be deleted and re-uploaded. The folders are organized now.

## Team Contributions

Each of us wrote and committed our own contribution summary:

- [Mann Sheth](cont_files/Mann_Sheth_StatusReport_Contribution.md)
- [Vansh Patel](cont_files/Vansh_Patel_StatusReport_Contribution.md)
- [Jacob Drucker](cont_files/Jacob_Drucker_StatusReport_Contribution.md)
- [Shuvam Sinha](cont_files/Shuvam_Sinha_StatusReport_Contribution.md)
