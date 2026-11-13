# Introduction
Once the script has pulled the raw data for the PLACES dataset, it will undergo a prelimiary assement. This assesment is to examine how the dataset fares under all four dimensions of a quality dataset.

# Assesment

## Completeness
- No null values in FIPS
- No null values in StateAbbr
- No null values in CountyName
- No null values in TotalPop
- No null values in TotalPop18Plus
- 187 null values in Adjusted Obesity data
- 844 null values in Food Insecurity
- 187 null values in Diabetes

## Consistency
- All FIPS entries are 5 digits
- No duplicate FIPS entries
- StateAbbr column has exactly 51 entries (50 states + DC)
- Connecticut uses the updated FIPS digit codes post-2018

## Accuracy 

## Timeliness
