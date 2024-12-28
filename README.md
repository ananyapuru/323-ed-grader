# Ed Discussion Parsing and CSV Export

This repository contains two Python files (`scraper.py` and `utils.py`) that parse an Ed Discussion JSON export for a class (CPSC 323 in this example, but this can be used for any Ed class), count the number of verified/endorsed contributions by user, and optionally output the results to a CSV file.

---

## How It Works

1. **Data Input**

   - The JSON file is specified by `DATA_FILE_NAME` in `scraper.py` (default: `cpsc323_ed_fall24.json`).
   - Each top-level item in the JSON is considered a thread (e.g., post, question, announcement).
   - We inspect:
     - The main body of each thread
     - All comments nested within that thread
     - Any “answers” nested within that thread

2. **Verification/Endorsement Rules**

   - An item is considered “verified/endorsed” if either:
     - It has `endorsed: true`
     - **Or** it has more than 100 characters *and* does not contain any question marks, based on the special rule included.

3. **User Identification**

   - We track users by their `name` (from `user["name"]`), defaulting to `"unknown name"` if missing (although this should never be the case!)

4. **Nested Comments**

   - The script recursively parses comments so that all levels of nested discussion are considered.

5. **Output**

   - The final output is printed to the terminal, showing each user and their verified/endorsed count, sorted in descending order.
   - It also writes a CSV file named `verified_endorsed_counts.csv` with two columns: `Contributor` and `Verified/Endorsed Count`.
   - Uncomment (in `scraper.py`) the optional `group_by_count` code if you want to see how many users fit each count bracket.

---

## File Descriptions

- **`utils.py`**  
  Contains the core functions for:
  - Checking text length, detecting question marks
  - Determining if an item is verified/endorsed
  - Recursively parsing comments
  - Parsing each top-level object
  - Grouping users by their counts
  - Writing a CSV file (`write_csv_output`)

- **`scraper.py`**  
  The main entry point:
  - Reads the JSON file into memory
  - Loops over each top-level thread, calling `parse_post_or_announcement`
  - Prints the final user counts
  - Writes them to a CSV file

---

## Usage

1. **Clone this repo** or copy both Python files (`utils.py` and `scraper.py`) into the same folder.
2. **Obtain your Ed Discussion JSON** and name it `cpsc323_ed_fall24.json` (or modify `DATA_FILE_NAME` in `scraper.py` to the correct path).
3. **Install Requirements**  
   The code only uses standard Python libraries (`json`, `csv`, `collections`), so no extra installations needed.
4. **Run**  
   ```bash
   python3 scraper.py
