title: "🧮 Population Data Analysis – Australian Bureau of Statistics"
description: >
  A Python-based project that performs statistical analysis on demographic datasets from the Australian Bureau of Statistics (ABS).
  The project answers key research questions using raw CSV inputs and built-in Python—without relying on external libraries like pandas or numpy.

files:
  - main.py: Full implementation for reading, cleaning, validating, and analyzing the input data.
  - SampleData_Areas.csv: Sample CSV file containing SA2-to-SA3 area mappings.
  - SampleData_Populations.csv: Sample CSV file with population data distributed by age groups.

objectives:
  - Analyze two CSV datasets: area mapping and population distribution by age.
  - Determine the region with the largest population per age group at state, SA3, and SA2 levels.
  - Identify SA3 areas with total population ≥ 150,000, and compute standard deviation of the most populated SA2.
  - Find SA3 regions with ≥ 15 SA2s and the SA2 pair with the highest cosine similarity of age distribution.

features:
  - Dynamic file role detection regardless of input order.
  - No external libraries: entirely built with Python built-ins like open, split, and float.
  - Calculates cosine similarity, standard deviation, and aggregates population across levels.
  - Handles invalid input formats, missing data, duplicate SA2 rows, and unmatched keys robustly.
  - Includes a documented debug log with real-life errors and resolutions.

output_examples:
```
  OP1:
    "0-4": ["Western Australia", "Perth North", "Bayswater"]
    "5-9": ["Victoria", "South East", "Casey Central"]
  OP2:
    "3":
      "30901": ["309021232", 172932, 2134.2401]
      "30902": ["309021100", 162482, 1982.4553]
  OP3:
    "Melbourne - Inner East": ["Camberwell", "Hawthorn", 0.9987]
```
error_handling:
  - Validates file extensions and uniqueness.
  - Detects header structure and missing/empty fields.
  - Filters out duplicate rows and misaligned entries between datasets.
  - Returns clear console messages for all critical issues with structured empty outputs.

debugging_documentation:
  - Issue 1: Input file order mismatch resolved using column-based file identification.
  - Issue 2: Duplicate rows caused by inconsistent formatting fixed via normalized comparison.
  - Issue 3: Crashes from inconsistent return values in error branches fixed for reliability.

usage: >
  Run the script using:
  ```
  `python main.py <AreaFile.csv> <PopulationFile.csv>`
  ```
  Ensure files follow the format shown in the sample datasets provided.

author:
  name: "Nitya Rajender Arya"
  role: "Master’s in Data Science"
  institution: "University of Western Australia"
  github: "https://github.com/nitya-s333"

