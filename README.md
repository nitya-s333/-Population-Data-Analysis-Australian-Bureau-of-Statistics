# 🧮 Population Data Analysis – Australian Bureau of Statistics

This Python project performs detailed statistical analysis on demographic datasets provided by the Australian Bureau of Statistics (ABS). It processes real-world population data and administrative area mappings to answer three key demographic research questions – entirely using built-in Python, without any external libraries.

  ---

  ## 📁 Files

  - `main.py` – Contains the full implementation to clean, validate, and analyze input CSVs.
  - Sample datasets:
    - `SampleData_Areas.csv`
    - `SampleData_Populations.csv`

  ---

  ## 🎯 Objectives

  The program takes two CSV files as input:
  - One with **SA2 to SA3 area mappings**
  - One with **SA2-level population distributions across age groups**

  It computes:
  1. **Largest population areas by age group** at the state, SA3, and SA2 levels.
  2. **SA3 areas with total population ≥150,000**, and the most populated SA2’s standard deviation.
  3. **SA3 areas with ≥15 SA2s**, finding the SA2 pair with highest cosine similarity of age distribution.

  ---

  ## 🛠️ Key Features

  - 🔍 **Dynamic File Type Detection**: Auto-identifies population vs area files regardless of input order.
  - ⚙️ **No External Libraries**: Fully implemented using core Python (e.g., `open`, `split`, `float`) — no `pandas`, `csv`, or `numpy`.
  - 🧠 **Advanced Statistics**: Calculates cosine similarity, standard deviation, and performs population aggregation by region.
  - 🔄 **Robust Validation**: Handles inconsistent files, empty cells, invalid types, duplicate rows, and non-matching keys.
  - 🧪 **Debugging Commentary**: Real-world debugging logs included for transparency and learning.

  ---

  ## 📊 Sample Output Structure

```

OP1 = {
"0-4": \["Western Australia", "Perth North", "Bayswater"],
"5-9": \["Victoria", "South East", "Casey Central"],
...
}

OP2 = {
"3": {
"30901": \["309021232", 172932, 2134.2401],
"30902": \["309021100", 162482, 1982.4553],
...
},
...
}

OP3 = {
"Melbourne - Inner East": \["Camberwell", "Hawthorn", 0.9987],
...
}

```

---

## 🚨 Error Handling

- Validates file extensions and uniqueness.
- Detects header structure and missing/empty fields.
- Filters out duplicate rows and misaligned entries between datasets.
- Returns clear console messages for all critical issues with structured empty outputs.

---

## 🧠 Lessons & Debugging Log

- **Issue 1**: Input file order mismatch resolved using column-based file identification.
- **Issue 2**: Duplicate rows caused by inconsistent formatting fixed via normalized comparison.
- **Issue 3**: Crashes from inconsistent return values in error branches fixed for reliability.

---

## 📎 Usage

Run the script using:

```

python main.py \<AreaFile.csv> \<PopulationFile.csv>

```

Ensure both CSV files are in the expected format as shown in sample files.

---

## 👤 Author

**Nitya Rajender Arya**  
Master's in Data Science  
University of Western Australia  
GitHub: [nitya-s333](https://github.com/nitya-s333)
```
