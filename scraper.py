import json
from collections import defaultdict

# Importing all the helper functions
from utils import (
    parse_post_or_announcement,
    group_by_count,
    write_csv_output,
)

################################################## CONSTANTS ##################################################

DATA_FILE_NAME = "cpsc323_ed_fall24.json"  # Change as needed!
CSV_FILE_NAME = "cpsc323_ed_fall24_verified_endorsed_counts.csv"

################################################## CONSTANTS ##################################################


def main():
    # Reading in Ed data for class
    with open(DATA_FILE_NAME, "r", encoding="utf-8") as json_file:
        ed_data = json.load(json_file)

    # Dictionary to track user -> number_of_verified_endorsed_items
    user_counts = defaultdict(int)

    # Each element of ed_data is a top-level thread (post, question, announcement).
    for thread in ed_data:
        parse_post_or_announcement(thread, user_counts)

    # Printing user --> count sorted in descending order.
    print("Verified/Endorsed Counts per Contributor:")
    for user, count in sorted(user_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {user:35s}  -> {count}")

    # Optionally, we can also group by contribution count:
    # grouped = group_by_count(user_counts)
    # print("\nGrouping by Count:")
    # for count_val, users in sorted(grouped.items(), key=lambda x: x[0], reverse=True):
    #     print(f"Count = {count_val}:")
    #     for u in users:
    #         print(f"   {u}")

    # Write CSV output
    write_csv_output(user_counts, csv_filename=CSV_FILE_NAME)
    print(f"\nWrote CSV to {CSV_FILE_NAME}")


if __name__ == "__main__":
    main()
