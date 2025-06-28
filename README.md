title: "Population Data Analysis – Australian Bureau of Statistics"
description: >
  This Python project performs detailed statistical analysis on demographic datasets provided by the Australian Bureau of Statistics (ABS).
  It processes real-world population data and administrative area mappings to answer three key demographic research questions – entirely
  using built-in Python, without any external libraries.

files:
  - main.py: "Contains the full implementation to clean, validate, and analyze input CSVs."
  - SampleData_Areas.csv: "Sample dataset for area mappings"
  - SampleData_Populations.csv: "Sample dataset for population data"

objectives:
  - "Takes two CSV files as input: one for SA2 to SA3 area mappings, and one for SA2-level population distributions across age groups."
  - "Computes:"
  - "1. Largest population areas by age group at the state, SA3, and SA2 levels."
  - "2. SA3 areas with total population ≥150,000, along with the most populated SA2’s standard deviation."
  - "3. SA3 areas with ≥15 SA2s, identifying the SA2 pair with highest cosine similarity in age distribution."

features:
  - "🔍 Dynamic File Type Detection: Auto-identifies population vs area files regardless of input order."
  - "⚙️ No External Libraries: Fully implemented using core Python — no pandas, csv, or numpy."
  - "🧠 Advanced Statistics: Computes cosine similarity, standard deviation, and performs population aggregation."
  - "🔄 Robust Validation: Handles inconsistent files, empty cells, invalid types, duplicates, and mismatches."
  - "🧪 Debugging Commentary: Includes real-world debugging logs for transparency and learning."

sample_output:
  op1:
    "0-4": ["Western Australia", "Perth North", "Bayswater"]
    "5-9": ["Victoria", "South East", "Casey Central"]
  op2:
    "3":
      "30901": ["309021232", 172932, 2134.2401]
      "30902": ["309021100", 162482, 1982.4553]
  op3:
    "Melbourne - Inner East": ["Camberwell", "Hawthorn", 0.9987]

error_handling:
  - "Checks file extensions and order."
  - "Validates header format."
  - "Handles missing fields, empty lines, and inconsistent data."
  - "Removes duplicate rows and ensures consistent key matching."
  - "Returns empty outputs with console messages for critical issues."

lessons_debugging:
  - "Includes annotated debugging insights for common errors (e.g., wrong file order, duplicate rows, inconsistent values)."
  - "Documented within comments and the main() function."

usage: |
  python main.py <AreaFile.csv> <PopulationFile.csv>
  # Ensure both CSV files are formatted correctly, as shown in the provided samples.

author:
  name: "Nitya Rajender Arya"
  education: "Master's in Data Science"
  institution: "University of Western Australia"
  github: "https://github.com/nitya-s333"
