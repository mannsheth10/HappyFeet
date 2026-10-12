## Overview:


Dataset Information:

County Based Health Statistics (Data Set 1): Our first dataset is a dataset provided by Data.gov and provides health statistics of different communities across the United States. The data provides health information on 3,143 different counties in all 50 states and the District of Columbia and provides different health statistics about the specific county. The provided information highlights statistics on different health diagnoses like high blood pressure, obesity, diabetes, cancer, and more. These statistics are presented on a county by county basis and give insight as to the percentage of people in an area with different health problems. With this information, we hope to determine the percentage of people who are obese or have diabetes and use this information in unison with the other datasets to answer our research question. Each county has a unique Federal Information Processing Code, also known as a FIPS code. This code is unique to every county in America and can be used as a unique identifier for every county. More information as well as a the downloadable file of the data can be found here: https://data.cdc.gov/500-Cities-Places/PLACES-County-Data-GIS-Friendly-Format-2025-releas/i46a-9kgh/data_preview

County Based Food Access (Data Set 2): Our next dataset is provided by the U.S. Department of Agriculture. In this dataset, each observation is a different county and provides us information on the food environment within that county. It provides 3,145 observations of different counties and shares information as to the demographics of that area as well as statistics about the access that residents of that county have to different types of food. Alongside traditional demographic data, it provides information on different groups of people’s access to food like children, elderly, people without cars, overall food access and more. This information can be used to determine the access of people in certain counties to food and can be compared to the other datasets by utilizing the FIPS Code to answer our research question. More information as well as a download to the data can be found here: https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation-downloads

County Based Income Level (Data Set 3): The last dataset we will be utilizing is provided by Census.gov. In this dataset, we get access to economic and resident income data of 3,199 different counties throughout the country. In this data, it provides information from 2020-2024 as to the poverty levels grouped by age and median household income alongside additional statistics of income allowing us to get an understanding of the income level of people in this specific county. By using this data, we will be able to see the average income of households in a specific county and compare it to data about health and access to food in other datasets to answer our research question. For each observation, a FIPS code is available allowing us to use this data in unison with the other datasets. For more information about this dataset as well as directions to access an API for this data can be found here: https://www.census.gov/data/developers/data-sets/acs-5year.html


Unique Identifier: For all datasets, they provide a FIPS code for each county. A FIPS code also known as a  Federal Information Processing Code is unique and standardized code to each county and can be used to match each observation to an observation found in a different dataset. This is how we will join datasets together and is our unique identifier. 










## Project Timeline:

### 1. Repository Setup
**Description:**
- Create folders for raw data, processed data, Python filtering scripts, and results
- Create a documentation Markdown file tracking our progress

**Date:** October 16

**Team Member:** Shuvam

### 2. Data Acquisition
**Description:**
- Download the CDC PLACES county data, USDA Food Environment Atlas data, and Census ACS 5-year data
- Document the data links, release versions, download dates, and checksums

**Date:** October 23

**Team Members:** Vansh, Mann

### 3. Data Cleaning and Integration
**Description:**
- Standardize county FIPS codes across all datasets
- Handle missing values
- Select key variables from each dataset
- Confirm a common key links all datasets, then join them on that key

**Date:** November 6

**Team Members:** Jacob, Shuvam

### 4. Plan Update and Status Report (Milestone 3)
**Description:**
- Revise ProjectPlan.md based on feedback
- Summarize progress and update the timeline
- Create the status report release for Milestone 3

**Date:** November 13

**Team Members:** All

### 5. Analysis and Visualization
**Description:**
- Run descriptive statistics, correlations, and regression models to test whether food access explains obesity and diabetes rates
- Create relevant plots

**Date:** November 13

**Team Members:** Vansh, Mann

### 6. Workflows and Reproducibility
**Description:**
- Write a script that automates the pipeline (acquire, clean, integrate, analyze) so it runs with one command
- Add instructions for reproducing the results and other relevant documentation

**Date:** December 4

**Team Members:** Jacob, Shuvam

### 7. Final Report and Submission
**Description:**
- Write a final report with findings and limitations
- Review as a group and submit

**Date:** December 11

**Team Members:** All

## Constraints:
The main constraint that we want to discuss is the overlap between data sources and the possible limitations of the underlying models these data sources use. The PLACES County Health Dataset uses a model to estimate the obesity rates – this model is a statistical model that uses age, race, sex, education, and the share of the country below 150% of the poverty line to predict what the obesity rate in that county would be. Thus, we need to make sure to clarify that this dataset uses estimates from a model, and when we are controlling for these variables in our other data sets, we need to make sure we are not double counting variables such as income and education. The USDA Food Atlas Dataset also has its own columns for obesity, diabetes, and income levels. We want to cross-reference these numbers with the model that the PLACES dataset uses to make sure the model is accurate – if it is accurate, it will ensure that all counties have data for obesity and other health issues, even if any physical data has not been collected. Another constraint is the difference of formatting in all of the datasets we have chosen. The PLACES dataset is simply one CSV file, with each row providing data for one county. The Food Atlas dataset comes as an Excel workbook, or a zipped file containing many CSV files. Since the Census ACS Dataset comes from an API, the data will be returned as a JSON file where every value is a “text” type by default. Converting these datasets to standardize their file types and data types will potentially be time consuming and could delay our progress.

## Gaps:
Since we are only halfway through the semester, there are a couple of gaps in our Project Plan that we feel will be resolved as we continue learning more on this topic. These are our most distinct analysis gaps:

When it comes to data quality, we don’t know how to measure the accuracy of the obesity model of the PLACES dataset when there is no “true” value of obesity for us to compare to. The model outputs a 95% confidence interval for each estimate, so we wanted to understand how to correctly use this confidence interval in our analyses.

We also want to understand how to go about cleaning the values in our dataset to account for factors such as extreme outliers and missing values. We have already seen that some counties have a lot of missing data, and we want to understand how much data needs to be missing before we can make the decision to drop the row/column. We know there are different scripts for data cleaning, but want to make sure we are using the right software.

We have also started learning about the reproducibility and provenance of datasets and want to understand how to provide people with everything they need to replicate our repo exactly. A lot of the data we use is updated very frequently by the government, and we are worried that our data will become outdated and unavailable for download. We want to understand how to collect and store the exact datasets we used, and how we need to record exactly where each file came from.

