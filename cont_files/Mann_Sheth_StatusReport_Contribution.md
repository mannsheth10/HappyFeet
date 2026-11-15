## Mann Sheth Status Report Contribution 

For our project milestone 3, I created a Python script [scripts\acquire_places.py] which pulled county-level data from the CDC PLACES 2025 county release (dataset i46a-9kgh), with age-adjusted health estimates for every U.S. county. It saved the data in [data\raw\places_county_2025.csv] and provided a manifest report alongside it in (data\raw\places_manifest.json).

From here, I performed a data assessment of the raw PLACES data, which can be found in (docs\places_quality_pre.md). Once I made my assessment, I cleaned the data and prepared it to be merged alongside the other datasets so we would be able to answer our research question. This involved removing columns that were not needed for our analysis, as well as ensuring that the columns I decided to keep were in the proper data type format. This cleaned data can be found at (data\processed\places_county_2025_clean.csv).

I then wrote the PLACES data acquisition status report detailing the dataset and the steps I took to clean it. The 3 cleaned datasets were then passed off to Vansh, who handled the merging and exploratory analysis of our merged dataset.

The Census data acquisition report, project timeline, and changes to our project plan can all be found in [ProjectPlan.md](ProjectPlan.md).