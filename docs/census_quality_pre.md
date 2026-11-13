## Introduction

After the script pulls the raw census data, it will undergo a preliminary data assessment. This is used to assess the data under all 4 dimensions of data quality. 

## Assesment

## Accuracy: 

After looking at the data, we see that there are 52 total different state variables. This includes both the District of Columbia and Puerto Rico. Looking at the syntactic accuracy of the dataset, all counties and states appear to have reasonable names and are in letter form which fits these columns. Moving towards population, all of the variables are valid numbers ranging from 33-9,900,000 meaning this column is syntactically correct. Within the household income column, all values are valid numbers, however, one county has a negative median household income of -666666666  which is not possible and not syntactically correct. This value is likely used as a place holder for a value that was not able to be collected or is missing. With the people below the poverty line column, these are valid numbers and are syntactically correct. Finally, the state and county numbers are all valid codes and are syntactically correct. While we can not check the semantic accuracy of the data as we have no verifiable, alternative data, we performed logic tests to ensure that no data point was outrageously egregious and something that is not realistic. We checked that poverty numbers were 0 or above, people below poverty line values were not greater than the entire population of that county and income values were not extraordinarily high (greater than 250,000 dollars). Given these tests, we are moving forward with the assumption that the data is semantically correct. 

### Completeness:

All 50 states are represented in this dataset as well as Puerto Rico and the District of Columbia. There is one missing value in the data which is median household income of De Baca County in New Mexico that has a placeholder value of -666666666. Outside of this one datapoint, the columns are complete and all values are filled in indicating completeness. The sum of the rows equals 4,222 which is the total number of entries from the same source. Given this information, we can conclude that the data is complete. 

### Consistency: 

Looking at the data, all variables seem to be consistent. The state code is a 2 digit number (including leading zeroes) with the county code being a three digit number. When combined, this creates the FIPS code which is unique for each county and fits the 5 digit schema of a FIPS code. Looking at the 4 numerical variables, they all share the same schema with the idea that no negative numbers should be expected. Given this, there is 1 datapoint in the median household income column that breaks this schema with a value of -666666666. Outside of this, all numerical variables fit their respective schemas and the data is consistent with what we would expect. With the county name, all values are text and no numerical values were found which means it fits the text schema. For the state name, all values were text as well and were valid states in the US. Given this, we can conclude that the data is consistent with the exception of the one value from the median income. 

### Timeliness: 

This data was released in January of 2026, however it is from a 5 period ending in 2024. This data is outdated by over a year, however, for our analysis in 2024, the dataset will be able to give us accurate information from that time. Therefore, the data is not currently up to date with the current state of US counties, however, for our analysis, will be able to suffice.
