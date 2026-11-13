## Jacob Drucker Status Report Contribution 
In my role, I created a Python script ([scripts/acquire_census.py](scripts/acquire_census.py)) which pulled county-level data from the U.S. Census Bureau. This obtained five-year average Census data from every county in the U.S., alongside other metrics. It saved the data in [data/raw/acs5_county_2024.csv](data/raw/acs5_county_2024.csv) and provided a manifest report alongside it ([data/raw/acs5_manifest.json](data/raw/acs5_manifest.json)).

From here, I performed a data assessment of the raw Census data, which can be found in [docs/census_quality_pre.md](docs/census_quality_pre.md). Once I made my assessment, I cleaned the data and prepared it to be merged alongside the other datasets so we would be able to answer our research question. This cleaned data can be found at [data/processed/county_income_2024_cleaned.csv](data/processed/county_income_2024_cleaned.csv).

I then wrote the Census data acquisition status report detailing the dataset and the steps I took to clean it. I also updated our project timeline and the dates by which our next tasks should be completed. Finally, I documented the changes we needed to make to our project plan, as well as how we incorporated the feedback given after our initial project plan report.

The Census data acquisition report, project timeline, and changes to our project plan can all be found in [ProjectPlan.md](ProjectPlan.md).
