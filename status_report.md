
## Census data acquisition status report

The data come from the U.S. Census Bureau’s [American Community Survey (ACS) 2020–2024 5-year estimates](https://www.census.gov/data/developers/data-sets/acs-5year.html), pulled at the county level through the Census API. A Python script ([acquire_census.py](scripts/acquire_census.py)) saved the raw response in [acs5_county_2024.csv](data/raw/acs5_county_2024.csv) and wrote a manifest with the source URL, the query, the download time, the row count, and a SHA-256 checksum ([acs5_manifest.json](data/raw/acs5_manifest.json)). The request covered county, county code, state, state code, total population, median household income, the number of people for whom poverty status was determined, and the number of people below the poverty level. These are the data points that are important for our analysis and allow us to join this dataset alongside the other 3.

### Census data cleaning

Cleaning was done in OpenRefine on a copy of the raw file. When downloading, leading zeros were kept, and a five-digit FIPS column was built by joining the two-digit state code to the three-digit county code (for example, 01 + 001 for Autauga County, Alabama). The combined name field was split into separate county and state name columns, the numerical columns were converted from text to numbers, and the columns were renamed to lowercase snake case. The Census placeholder value -666666666 found in the median income value for De Baca County, New Mexico was replaced with a blank cell. From here, all Puerto Rico counties were removed from the dataset leaving us with a total of 3,144 rows. The final file was exported as a CSV to [county_income_2024_cleaned.csv](data/processed/county_income_2024_cleaned.csv) and checked to confirm that FIPS was a unique, five-character text, with one row per county.

## PLACES data acquisition status report

The data come from the Centers for Disease Control and Prevention's [Local Data for Better Health, County Data, 5-Year Release](https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-County-Data-20/swc5-untb/about_data), pulled at the county level without any API needed. A Python script ([acquire_places.py](scripts/acquire_places.py)) saved the raw response in [places_county_2025.csv](data/raw/places_county_2025.csv) and wrote a manifest with the source URL, the query, the download time, the row count, and a SHA-256 checksum ([places_manifest.json](data/raw/places_manifest.json)). The request covered county, county code, state, state code, total population, total population over 18-years-old, rate of obesity, rate of food insecurity, and rate of diabetes. These are the data points that are important for our analysis and allow us to join this dataset alongside the other 3.

### PLACES data cleaning

Cleaning was done in OpenRefine on a copy of the raw file. When downloading, leading zeros were kept, and the FIPS code of each county was already accurately reported, with no joining needed. The first step was to remove columns that were not needed for our analysis, such as data on other health issues (arthritis, blood pressure, cancer, etc.). Afterwards, the reminaing diabetes, food insecurity, and obesity columns had a Confidence Interval column that needed cleaning. Before, each column listed the upper and lower bound of the confidence interval, such as "(12.13, 40.02)". This was formatted as a text block, which made it difficult to interpret, I decided to split these into two columns, one for the lower bound and one for the upper bound. I then took all of the columns that needed to be expressed as a number and converted them all using the "transformation" feature in OpenRefine. The final file was exported as a CSV to [data/processed/places_county_2025_clean.csv](data/processed/places_county_2025_clean.csv).

## Food Environment Atlas data acquisition status report

The data comes from the U.S. Department of Agriculture Economic Research Service's [Food Environment Atlas (2025 edition)](https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation-downloads), downloaded at the county level as a zipped set of CSV files with no API key needed. I wrote a Python script ([acquire_fea.py](https://github.com/mannsheth10/HappyFeet/blob/main/scripts/acquire_fea.py)) that saved the raw download as [fea_county_2025.zip](https://github.com/mannsheth10/HappyFeet/blob/main/data/raw/fea_county_2025.zip) and wrote a manifest with the source page, the download URL, the download time, the file size, the list of files in the zip, and a SHA-256 checksum ([fea_manifest.json](https://github.com/mannsheth10/HappyFeet/blob/main/data/raw/fea_manifest.json)). The zip contains StateAndCountyData.csv, which holds every indicator in the Atlas, along with a variable list and a ReadMe. From the roughly 300 indicators, we used the percentage of the population with low access to a store, along with low access for low-income residents, households without a car, children, and seniors, plus grocery stores per 1,000 people and the adult diabetes rate. These are the data points that are important for our analysis, and the county FIPS code allows us to join this dataset with the others.

## Food Environment Atlas data cleaning

I cleaned the dataset in OpenRefine using a copy of the raw file, and saved my work in the file [fea_operations.json](https://github.com/mannsheth10/HappyFeet/blob/main/data/openrefine_history/fea_operations.json). The raw file is in a long format with 957,753 rows, one row per county per variable, so the first step was to keep only the rows for the 8 variables we needed. The file was then pivoted with OpenRefine's key-value columnize feature so that each variable became its own column, leaving one row per county, instead of there being one row per variable for each county. Adult obesity was removed because it is only reported at the state level, not the county level (all counties in the same state had the same value). The Atlas placeholder values -9999 and -8888 were replaced with blank cells so it wouldn't affect numerical summaries, and the columns were converted from text to numbers and renamed to a standardized format that we previously determined. The 8 Connecticut counties were removed because the Atlas still uses Connecticut's old county codes, while the PLACES and ACS data use the 9 planning regions that replaced them in 2022, so they could not be joined. The Connecticut rows are listed in [fea_excluded.csv](https://github.com/mannsheth10/HappyFeet/blob/main/data/processed/fea_excluded.csv). The final file was exported as a CSV to [fea_clean.csv](https://github.com/mannsheth10/HappyFeet/blob/main/data/processed/fea_clean.csv) and checked to confirm that FIPS was a unique, five-character text, with one row for each of the 3,136 counties. 

## Updated Timeline 

# Project Timeline and Milestones

## Repository Setup <span> </span> — Completed
- **Description:**
  - Create folders for raw data, processed data, Python filtering scripts, and results.
  - Create a documentation Markdown file outlining project progress.
- **Date:** October 16
- **Team Members:** Shuvam

## Data Acquisition — Completed
- **Description:**
  - Download the CDC PLACES county data, USDA Food Environment Atlas data, and Census ACS 5-year data.
  - Document data links, release versions, download dates, and checksums.
- **Date:** October 23
- **Team Members:** Vansh, Mann

## Data Cleaning and Integration — Completed
- **Description:**
  - Standardize data using county FIPS codes.
  - Handle missing values.
  - Select key variables from each dataset.
  - Ensure there is a common key linking all datasets and join datasets based on this key.
- **Date:** November 6
- **Team Members:** Jacob, Shuvam

## Plan Update and Status Report (Milestone 3) — Completed
- **Description:**
  - Summarize project progress.
  - Update the project timeline.
  - Create the Milestone 3 status report.
- **Date:** November 13
- **Team Members:** All

## Analysis and Visualization — Upcoming
- **Description:**
  - Run descriptive statistics, correlations, and regression models to test whether food access explains obesity and diabetes rates.
  - Create relevant plots and visualizations.
- **Date:** November 27
- **Team Members:** Vansh, Mann

## Workflows and Reproducibility — Upcoming
- **Description:**
  - Write a script automating the pipeline (acquisition, cleaning, integration, and analysis) so it runs with one command.
  - Provide instructions for reproducing the results.
  - Add relevant documentation.
- **Date:** December 4
- **Team Members:** Jacob, Shuvam

## Final Report and Submission — Upcoming
- **Description:**
  - Write a final report outlining findings and limitations.
  - Review the report as a group.
  - Submit the completed project.
- **Date:** December 11
- **Team Members:** All

## Changes to Our Project Plan and Incorporated Feedback

No overall changes to our project plan were needed for this submission. Our initial project plan remains the same, and our research goal is unchanged.

When acquiring our data, we made sure to pull only the necessary data points and exclude information that was not imperative to our analysis. This involved selecting only a few relevant columns from the extensive Census and Food Environment Atlas datasets. By doing so, we ensured that our merged dataset contains only the information necessary to address our research question.

After evaluating the data quality of each dataset, we concluded that they have reasonably similar levels of data quality. Additionally, we verified that the FIPS codes (the identifiers used to merge the datasets) are accurate and consistent across all three datasets. This allows us to accurately integrate the data while ensuring that each county's corresponding variables are uniquely associated with the correct county.

Overall, our project plan remains unchanged, and analyzing the integrated dataset to address our research question is our next step. After incorporating the feedback received and completing this milestone, we are confident that we can use our analysis to answer our research question as thoroughly as possible.
