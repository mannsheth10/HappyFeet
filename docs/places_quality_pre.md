# Introduction
Once the script has pulled the raw data for the PLACES dataset, it will undergo a prelimiary assement. This assesment is to examine how the dataset fares under all four dimensions of a quality dataset.

# Assesment

## Completeness
No null values in FIPS
No null values in StateAbbr
No null values in CountyName
No null values in TotalPop
No null values in TotalPop18Plus
187 null values in Adjusted Obesity Data
844 null values in Adjusted Food Insecurity Data
187 null values in Adjusted Diabetes Data

## Consistency
All FIPS entries are 5 digits
No duplicate FIPS entries
StateAbbr column has exactly 51 entries (50 states + DC)
Connecticut uses the updated FIPS digit codes post-2018

Overall, this dataset has very consistent values within all of the columns that we need to use for analysis. This facet of the dataset did not require any further cleaning, and will make it easy to join the dataset with the other two.

## Accuracy 
The Adjusted Obesity Data percentages range from 17% - 55%, which is within a reasonable range and does not have any values that fail to parse.
The Adjusted Food Insecurity Data percentages range from 5% - 47%, which is on the lower range, but seems reasonable since food insecurity is a more rare condition than insecurity.
The Adjusted Diabetes Data percentages range from 6% - 24%, which is within a reasonable range and does not have any values that fail to parse.

## Timeliness
Timeliness of the dataset has been recorded in data/places_manifest.json
