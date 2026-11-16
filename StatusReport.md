# Milestone 3 Status Report

Team: Mann Sheth, Vansh Patel, Jacob Drucker, Shuvam Sinha

Our project is looking at if counties with worse access to grocery stores also have higher obesity and diabetes rates and if that is still true once you account for income and poverty. So far all three datasets are downloaded and cleaned. We merged them into one file and started looking at the data. Below we go through each part of our [project plan](ProjectPlan.md).

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

Once everyone finished cleaning their dataset I wrote [integrate.py](scripts/integrate.py) to merge them on the FIPS code. It checks that every file has one row per county and that the FIPS codes are 5 digits. Then it joins all three together. I also had it make a poverty rate column by dividing the number of people below poverty by the total number of people counted. The merged file is [merged_county.csv](data/processed/merged_county.csv) and it has 3,134 counties.

11 counties weren't in all three datasets so they got dropped, these are in [merge_unmatched.csv](data/processed/merge_unmatched.csv). Nine of them are Connecticut planning regions because the Food Atlas still has the old Connecticut counties. PLACES doesn't have Loving County in Texas. The last one is an old Alaska county code that only the Atlas still uses.

## Early analysis

Before doing the actual regressions I wrote [explore.py](scripts/explore.py) to get some basic stats and correlations. Everything it makes is saved in the [results](results) folder.

One thing we didn't expect was that the overall low food access percent had pretty much no correlation with obesity or diabetes, it was around -0.05. Income and poverty were a lot stronger. Poverty rate and diabetes had a correlation of 0.81 for example. The only food access variable that had a moderate correlation was low access for people without a car which was around 0.3 to 0.4. So our second research question about whether food access still matters after controlling for income is going to be really important.

Our project plan said we would compare the diabetes rate from PLACES to the one from the Food Atlas so we did that too. The correlation was only 0.52. We're going with the PLACES number because its the newer one.

## Updated Timeline

- **Repository Setup**: Completed on Oct 16 by Shuvam
- **Data Acquisition**: Completed on Nov 13, everyone did their own dataset
- **Data Cleaning and Integration**: Completed on Nov 15. Jacob, Mann and Shuvam cleaned and Vansh did the merging
- **Status Report for Milestone 3**: Completed on Nov 16 by all of us
- **Analysis and Visualization**: In progress, should be done by Nov 27, Vansh and Mann
- **Workflows and Reproducibility**: Not started yet, due Dec 4, Jacob and Shuvam
- **Final Report**: Not started yet, due Dec 11, all of us

Getting and cleaning the data took longer then we thought it would. Because of that we moved analysis from Nov 13 to Nov 27 but the final deadline is the same. We still have to run the regressions. We also want to make a map showing which counties have low food access and high poverty and high obesity or diabetes all at once.

## Changes to Our Project Plan

The research question didn't change. What did change is how we split the work. Originally two people were going to download everything and the other two would clean it. We ended up having each person take one dataset and do both parts for it, then Vansh did the merging and the first analysis. Cleaning was done in OpenRefine and we saved the history files so someone else can redo the same steps. We also got rid of the obesity column from the Food Atlas since it was only reported by state and not by county.

## Milestone 2 Feedback

We got asked whether the data quality is consistent across counties. We were also told to be more specific about what parts of the Food Atlas we are actually using.

For the first part we found the quality is definitely not the same everywhere:

- PLACES has no obesity or diabetes data for any county in Kentucky or Pennsylvania. Food insecurity is missing for every county in 11 states.
- Around 900 counties don't have the grocery stores per 1,000 people number and most of those are small counties.
- The PLACES numbers are estimates and for small counties the confidence intervals are a lot wider so those are less certain.
- Some rural counties have 100% low food access. That happens because the Atlas uses 10 miles as the cutoff for rural areas but 1 mile for cities.

Our plan for this is to report how many counties go into each model and to check if the counties we drop are different from the ones we keep. We're also going to try controlling for state.

For the second part, out of the roughly 300 variables in the Food Atlas these are the only ones we use:

- Percent of people with low access to a store, which is our main food access variable
- Low access for low income people, households with no car, kids and seniors so we can compare groups for research question 3
- Grocery stores per 1,000 people
- Adult diabetes rate, but only to double check the PLACES diabetes numbers

## Challenges

- In 2022 Connecticut switched from counties to planning regions but the Food Atlas still uses the old counties. We took those rows out and listed them in [fea_excluded.csv](data/processed/fea_excluded.csv).
- Every dataset was formatted differently. The Atlas had a row for each variable instead of a row for each county. PLACES stored the confidence intervals as text. In the Census data missing values were filled with placeholder numbers like -666666666. All of this got fixed in OpenRefine.
- Some states are missing a lot of data like we talked about in the feedback section. There's no way for us to fill that in so we're going to be upfront about which counties are in each part of the analysis.
- Early on a few files got uploaded to the wrong folders and we had to delete them and upload them again. Everything is organized now.

## Team Contributions

Everyone wrote and committed their own contribution summary:

- [Mann Sheth](cont_files/Mann_Sheth_StatusReport_Contribution.md)
- [Vansh Patel](cont_files/Vansh_Patel_StatusReport_Contribution.md)
- [Jacob Drucker](cont_files/Jacob_Drucker_StatusReport_Contribution.md)
- [Shuvam Sinha](cont_files/Shuvam_Sinha_StatusReport_Contribution.md)
