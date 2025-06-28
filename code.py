"""
Student Name: Nitya Rajender Arya
Student ID: 24155608
"""

def main(csvfile_1, csvfile_2):

    # Step 1: Initialize empty dictionaries for outputs OP1, OP2, OP3
    op1 = {}  # Dictionary for largest populations per age group
    op2 = {}  # Nested dictionary for SA3 areas with population >= 150000
    op3 = {}  # Dictionary for SA3 areas with >= 15 SA2 areas and max cosine similarity

    try:
        # Step 2: Validate inputs before opening files
        
        if not (isinstance(csvfile_1, str) and isinstance(csvfile_2, str)):
            print("Invalid CSV headers: missing required columns")
            return {}, {}, {}

        if not (csvfile_1.lower().endswith('.csv') and csvfile_2.lower().endswith('.csv')):
            print("Input files must have .csv extension")
            return {}, {}, {}
        
        if csvfile_1.lower() == csvfile_2.lower():
            print("Input files must be different")
            return {}, {}, {}

        with open(csvfile_1, 'r') as f1:
            area_lines = f1.readlines()
        with open(csvfile_2, 'r') as f2:
            pop_lines = f2.readlines()
            
        if not area_lines or not pop_lines:
            print("Either one or both of the input files are empty")
            return {}, {}, {}

    except FileNotFoundError:
        print(f"{csvfile_1} or {csvfile_2} or both files do not exist")
        return {}, {}, {}
    except IOError:
        print("An error occurred while reading the input files")
        return {}, {}, {}
    
    # Step 3: Validate that files are not empty
    if not area_lines or not pop_lines:
        print("One or both of the input files are empty")
        return {}, {}, {}
    
    # Step 4: Parse headers from both files
    area_headers = area_lines[0].strip().split(',')
    pop_headers = pop_lines[0].strip().split(',')

    #Step 5: Detect which file is area file and which is population file

    area_headers = area_lines[0].strip().split(',')
    pop_headers = pop_lines[0].strip().split(',')

    def is_area_file(headers):
        h = [col.strip().lower() for col in headers]
        return 'sa3 name' in h and 'sa2 name' in h

    def is_population_file(headers):
        h = [col.strip().lower() for col in headers]
        return any(col.startswith('age ') for col in h) and 'area_code_level2' in h

    if is_area_file(area_headers) and is_population_file(pop_headers):
        # Files already correct
        pass
    elif is_area_file(pop_headers) and is_population_file(area_headers):
        # Swap files and headers
        area_lines, pop_lines = pop_lines, area_lines
        area_headers, pop_headers = pop_headers, area_headers
    else:
        print("Unable to determine which file is area or population data")
        return {}, {}, {}

    # Step 6: Identify relevant columns in area file

    state_code_col = state_name_col = sa3_code_col = sa3_name_col = sa2_code_col = sa2_name_col = None

    for i, h in enumerate(area_headers):
        h = h.lower()
        if h == 's_t code':
            state_code_col = i
        elif h == 's_t name':
            state_name_col = i
        elif h == 'sa3 code':
            sa3_code_col = i
        elif h == 'sa3 name':
            sa3_name_col = i
        elif h == 'sa2 code':
            sa2_code_col = i
        elif h == 'sa2 name':
            sa2_name_col = i

    # Step 7: Identify relevant columns in population file

    sa2_code_pop_col = None
    age_cols = []

    for i, h in enumerate(pop_headers):
        h = h.lower()
        if h == 'area_code_level2':
            sa2_code_pop_col = i
        elif h.startswith('age '):
            age_str = h[4:].replace(' and over', '-None')
            age_cols.append((i, age_str))

    # Step 8: Validate all required columns found

    if None in (state_code_col, state_name_col, sa3_code_col, sa3_name_col, sa2_code_col, sa2_name_col, sa2_code_pop_col) or not age_cols:
        print("Invalid CSV headers")
        return {}, {}, {}
    
    # Step 9: Parse area data
    
    # Step 9.1: Initialize dictionary for area data {sa2_code: (state_code, state_name, sa3_code, sa3_name, sa2_name)}
    areas = {}  
    # Step 9.2: Init9alize dictionary to map SA3 to SA2 areas {sa3_code: [(sa2_code, sa2_name)]}
    sa3_to_sa2 = {}  
    # Step 9.3: Initialize set to track duplicate rows
    seen_sa2_1 = set()
    dup_sa2_1 = set()
    # Step 9.4: Iterate through data rows (skip header)
    max_index = max(state_code_col, state_name_col, sa3_code_col, sa3_name_col, sa2_code_col, sa2_name_col)
    for line in area_lines[1:]:
        row = line.strip().split(',')
        if len(row) <= max_index:
            continue
        sa2_code=row[sa2_code_col].lower()
        if sa2_code in seen_sa2_1:
            dup_sa2_1.add(sa2_code)
            continue
        seen_sa2_1.add(sa2_code)
        
        try:
            state_code = row[state_code_col].lower()
            state_name = row[state_name_col].lower()
            sa3_code = row[sa3_code_col].lower()
            sa3_name = row[sa3_name_col].lower()
            sa2_code = row[sa2_code_col].lower()
            sa2_name = row[sa2_name_col].lower()
            # Step 9.5: Skip rows with empty fields
            if not all([state_code, state_name, sa3_code, sa3_name, sa2_code, sa2_name]):
                continue
            # Step 9.6: Store area data in dictionary
            areas[sa2_code] = (state_code, state_name, sa3_code, sa3_name, sa2_name)
            if sa3_code not in sa3_to_sa2:
                # Step 9.7: Initialize SA3 entry if not present
                sa3_to_sa2[sa3_code] = []
                # Step 9.8: Map SA2 code and name to SA3
            sa3_to_sa2[sa3_code].append((sa2_code, sa2_name))
        except IndexError:
            print("Invalid data format in area_file: missing columns in a row")
            return {},{},{}
        except TypeError:
            print("Invalid data format in area_file: unexpected type while processing a row")
            return {},{},{}
        
    # Step 10: Parse populations data
    
    # Step 10.1: Initialize dictionary for population data {sa2_code: {age_group: population}}
    populations = {}
    # Step 10.2: Initialize set to track duplicate rows
    seen_sa2_2 = set()
    dup_sa2_2= set()
    # Step 10.3: function to validate a population row 
    def is_valid_population_row(row, age_cols):
        for col_idx, _ in age_cols:
            if col_idx >= len(row):
                return False
            val = row[col_idx].strip()
            if val == '':
                return False
            try:
                f = float(val)
                if f < 0:
                    return False
            except ValueError:
                return False
        return True
    # Step 10.4: Iterate through data rows (skip header)
    for line in pop_lines[1:]:
        row = line.strip().split(',')
        if len(row) <= max([sa2_code_pop_col] + [i for i, _ in age_cols]):
            continue
        # Step 10.5: Get SA2 code from row
        sa2_code = row[sa2_code_pop_col].lower()
        if sa2_code not in areas:
            continue
        if sa2_code in seen_sa2_2:
            dup_sa2_2.add(sa2_code)
            continue
        # Step 10.6: Validate population row before processing
        if not is_valid_population_row(row, age_cols):
            continue
        seen_sa2_2.add(sa2_code)
        
        # Step 10.7: Attempt to parse population data
        try:
            populations[sa2_code] = {}
            for col_idx, age_group in age_cols:
                pop = row[col_idx]
                # Step 10.8: Check for invalid population
                if pop.strip() == '':
                    return {},{},"Invalid data in population_file: empty population field"
                value = float(pop)
                if value < 0:
                    return {},{}, "Invalid data in population_file: negative population value"
                populations[sa2_code][age_group] = value
        except (IndexError, ValueError, TypeError):
            print("Invalid data in population_file: error while reading population values")
            return {},{},{}
    
    # Remove invalid corresponding rows
    # Step 11: Keep only SA2 codes that exist in both areas and populations
    duplicated_sa2s=dup_sa2_1 | dup_sa2_2
    valid_codes = (set(areas.keys()) & set(populations.keys())) - duplicated_sa2s

    # Step 11.1: Remove SA2 entries from areas that don't have population data
    new_areas = {}
    for sa2_code, data in areas.items():
        if sa2_code in valid_codes:
            new_areas[sa2_code] = data
    areas = new_areas

    # Step 11.2: Remove SA2 entries from populations that don't have area data
    new_populations = {}
    for sa2_code, data in populations.items():
        if sa2_code in valid_codes:
            new_populations[sa2_code] = data
    populations = new_populations

    # Step 11.3: For each SA3 area, remove SA2 entries that aren't valid
    new_sa3_to_sa2 = {}
    for sa3_code, sa2_list in sa3_to_sa2.items():
        new_list = []
        for sa2_code, sa2_name in sa2_list:
            if sa2_code in valid_codes:
                new_list.append((sa2_code, sa2_name))
        new_sa3_to_sa2[sa3_code] = new_list
    sa3_to_sa2 = new_sa3_to_sa2

    # Step 11.4: If there's no valid data left, return an error message
    if not areas or not populations:
        print("No valid data available after filtering")
        return {},{},{}
    
    # Step 12: Compute OP1 - Largest populations per age group
    # Step 12.1: Iterate through each age group from age_cols
    for _, age_group in age_cols:
        state_pops = {}
        sa3_pops = {}
        sa2_pops = {}

        # Step 12.2: To get aggregate populations per area level iterate through SA2 codes and their population data
        for sa2_code, pops in populations.items():
            if age_group not in pops:
                continue
            pop = pops[age_group]
            # Step 12.3: Get population for current age group
            state_code, state_name, sa3_code, sa3_name, sa2_name = areas[sa2_code]
            # Step 12.4: Extract area details (state code, name, SA3 code, name, SA2 name)
            state_pops[state_code] = state_pops.get(state_code, 0) + pop
            sa3_pops[sa3_code] = sa3_pops.get(sa3_code, 0) + pop
            sa2_pops[sa2_code] = pop

        # Step 13: Define a function to find max with tie-break
        def max_with_tiebreak(d):
            max_pop = -1
            max_key = None
            for k, v in d.items():
                # Step 13.1: Update max if value is higher or equal with lower key
                if v > max_pop or (v == max_pop and (max_key is None or k < max_key)):
                    max_pop = v
                    max_key = k
            # Step 13.2: Return key with max population
            return max_key
        # Step 13.3: Find codes with max populations using tie-breaking
        max_state_code = max_with_tiebreak(state_pops)
        max_sa3_code = max_with_tiebreak(sa3_pops)
        max_sa2_code = max_with_tiebreak(sa2_pops)

        #13.4:Validate max codes
        if max_state_code and max_sa3_code and max_sa2_code:
            # areas[sa2_code] = (state_code, state_name, sa3_code, sa3_name, sa2_name)
            # We need names for max_state_code, max_sa3_code, and max_sa2_code
            # To get state_name for max_state_code:
            max_state_name = None
            for v in areas.values():
                # Step 13.5: Update max if value is higher or equal with lower key
                if v[0] == max_state_code:
                    max_state_name = v[1]
                    break
            # Step 13.6: To get sa3_name for max_sa3_code:
            max_sa3_name = None
            for v in areas.values():
                if v[2] == max_sa3_code:
                    max_sa3_name = v[3]
                    break
            # Step 13.7: For SA2, we can get name directly:
            max_sa2_name = areas[max_sa2_code][4]
            op1[age_group] = [max_state_name, max_sa3_name, max_sa2_name]
            
        # Step 14: Compute OP2 – SA3 areas with population >= 150000
        # Step 14.1: Aggregate total population per SA3, grouped by state
        state_sa3_pops = {}
        for sa2_code, pops in populations.items():
            state_code, _, sa3_code, _, _ = areas[sa2_code]
            total_pop = sum(pops.values())
            if state_code not in state_sa3_pops:
                state_sa3_pops[state_code] = {}
            state_sa3_pops[state_code][sa3_code] = state_sa3_pops[state_code].get(sa3_code, 0) + total_pop

        # Step 14.2: For each qualifying SA3, find the SA2 with the highest population and compute its standard deviation
        for state_code in sorted(state_sa3_pops.keys()):
            op2[state_code] = {}
            for sa3_code, total_pop in state_sa3_pops[state_code].items():
                if total_pop < 150000:
                    continue  # Skip SA3s below threshold

                # Step 14.3: Find SA2 with highest total population in this SA3
                max_sa2_pop = -1
                max_sa2_code = None
                for sa2_code, _ in sa3_to_sa2.get(sa3_code, []):
                    if sa2_code in populations:
                        sa2_total = sum(populations[sa2_code].values())
                        if (
                            sa2_total > max_sa2_pop or
                            (sa2_total == max_sa2_pop and (max_sa2_code is None or sa2_code < max_sa2_code))
                        ):
                            max_sa2_pop = sa2_total
                            max_sa2_code = sa2_code

                # Step 14.4: Calculate standard deviation of age distribution in that SA2
                if max_sa2_code:
                    pops = [populations[max_sa2_code][age] for _, age in age_cols if age in populations[max_sa2_code]]
                    if len(pops) > 1:
                        mean = sum(pops) / len(pops)
                        variance = sum((x - mean) ** 2 for x in pops) / (len(pops) - 1)
                        std_dev = variance ** 0.5
                    else:
                        std_dev = 0.0

                    # Step 14.5: Store results as [SA2 code, total pop, std dev]
                    op2[state_code][sa3_code] = [
                        max_sa2_code,
                        int(max_sa2_pop) if max_sa2_pop.is_integer() else round(max_sa2_pop, 4),
                        round(std_dev, 4)
                    ]

            # Step 14.6: Sort SA3s by descending total population within each state
            op2[state_code] = dict(sorted(op2[state_code].items(), key=lambda x: x[1][1], reverse=True))

        # Step 15: Compute OP3 – SA3 areas with ≥ 15 SA2s and highest cosine similarity between SA2s
        op3_temp = {}

        # Step 15.1: Process each SA3 with at least 15 SA2 regions
        for sa3_code, sa2_list in sa3_to_sa2.items():
            if len(sa2_list) < 15:
                continue  # Skip SA3s with fewer than 15 SA2s

            max_sim = -1
            best_pair = None

            # Step 15.2: Sort SA2s in SA3 alphabetically by name for tie-breaking
            sa2_list.sort(key=lambda x: x[1])

            # Step 15.3: Compare each pair of SA2s in this SA3
            for i in range(len(sa2_list)):
                for j in range(i + 1, len(sa2_list)):
                    sa2_code1, sa2_name1 = sa2_list[i]
                    sa2_code2, sa2_name2 = sa2_list[j]

                    if sa2_code1 not in populations or sa2_code2 not in populations:
                        continue

                    # Step 15.4: Skip if any population is 0 to avoid division by zero
                    total1 = sum(populations[sa2_code1].values())
                    total2 = sum(populations[sa2_code2].values())
                    if total1 == 0 or total2 == 0:
                        continue

                    # Step 15.5: Normalize both SA2 vectors and compute cosine similarity
                    vec1 = []
                    vec2 = []
                    for _, age in age_cols:
                        p1 = populations[sa2_code1].get(age, 0) / total1
                        p2 = populations[sa2_code2].get(age, 0) / total2
                        vec1.append(p1)
                        vec2.append(p2)

                    dot = sum(a * b for a, b in zip(vec1, vec2))
                    norm1 = sum(a * a for a in vec1) ** 0.5
                    norm2 = sum(b * b for b in vec2) ** 0.5
                    sim = dot / (norm1 * norm2) if norm1 and norm2 else 0.0

                    # Step 15.6: Update best match if similarity is higher or ties alphabetically earlier
                    if sim > max_sim:
                        max_sim = sim
                        best_pair = (sa2_name1, sa2_name2, sim)
                    elif sim == max_sim:
                        if best_pair is None or (sa2_name1, sa2_name2) < (best_pair[0], best_pair[1]):
                            best_pair = (sa2_name1, sa2_name2, sim)

            #Step 15.7: Save best pair and similarity under the SA3 name
            if best_pair:
                sa3_name = areas[sa2_list[0][0]][3].strip()  # Get SA3 name from first SA2
                op3_temp[sa3_name] = [
                    best_pair[0],
                    best_pair[1],
                    round(best_pair[2], 4)
                ]

        # Step 15.8: Sort final OP3 dictionary alphabetically by SA3 name
        op3 = op3_temp

    return op1, op2, op3

"""
Debugging Documentation:

Issue 1 (Date: May 18, 2025):
- Error Description:
    My code crashed with the error as ValueError: Too many values to unpack.
- Erroneous Code Snippet:
    area_headers = csvfile_1[0].strip().split(',')
    pop_headers = csvfile_2[0].strip().split(',')
    # Assumed csvfile_1 was area file without checking headers
- Test Case:
    main('SampleData_Populations.csv', 'SampleData_Areas.csv')
    # csvfile_1 contains population data, csvfile_2 contains area data
- Reflection:
   I initially assumed that the input files would always be provided in a fixed order — with the population data file first and the area data file second. Because of
   this assumption, my code failed when I tried to run it with the files in reverse order. The crash occurred because my program tried to parse the headers without checking
   which file was which, leading to incorrect logic being applied to the wrong data. To fix this, I implemented checks using is_area_file and is_population_file functions.
   These functions first examine the column headers in each file to determine which one contains area data and which one contains population data. Based on that identification,
   the program assigns the correct roles to the files and proceeds with the appropriate logic. This change allowed my code to handle input files in any order, improving its robustness.
   From this, I learned the importance of validating assumptions about input and designing programs to be flexible when handling external data to avoid unexpected crashes.


Issue-2 (Date: May 19, 2025)
- Error Description:  
    Got duplicate rows in the output even after writing the code to remove them.  
- Erroneous Code Snippet:  
if row not in seen_rows:  
    seen_rows.add(row)  
    valid_rows.append(row)  
- Test Case:  
    main('DuplicateTest_Areas.csv', 'ValidPopulations.csv')
# I created these 2 files 'DuplicateTest_Areas.csv', 'ValidPopulations.csv' for testing my code.
# Duplicate area rows like ['502011003', '502011000', 'Busselton', 'Rural West'] still appeared twice  
- Reflection:  
The error occurred because rows from the CSV contained inconsistent whitespace and case, causing direct list comparisons to fail when detecting duplicates. I realized that
comparing raw lists was not correct, so I normalized each row by stripping whitespace and converting values to a consistent case before converting them to tuples for comparison.
This debugging taught me that data normalization is essential to ensure accurate duplicate detection and reliable data processing.


Issue 3 (Date: May 20, 2025)
-Error Description:  
    The program crashed without showing any error message, even though I had written code to display a message when invalid input files were given (like a .txtx file instead of .csv).
    This happened even though I was using try-except blocks to catch errors.

-Erroneous Code Snippet:   
    try:
        if not (isinstance(csvfile_1, str) and isinstance(csvfile_2, str)):
            return ("Invalid CSV headers: missing required columns")
        if not (csvfile_1.lower().endswith('.csv') and csvfile_2.lower().endswith('.csv')):
            return ("Input files must have .csv extension")
        if csvfile_1.lower() == csvfile_2.lower():
            return ("Input files must be different")
-Test Case:  
    main('not_a_csv.txt', 'valid_populations.csv')

-Reflection:  
    The error occurred because I didn’t return all three expected outputs when handling invalid input with a try-except block. This caused the program to crash later
    during unpacking. I realized that every branch of the main() function, including error-handling cases, must return the same structured output. This debugging process
    taught me the importance of consistent return values to avoid silent failures and ensure the program behaves reliably under all conditions.
"""

