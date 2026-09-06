import csv
import os
import re
import difflib
from collections import Counter

# File paths
folder = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(folder, "mn.csv")
header_file = os.path.join(folder, "mn_headers.csv")
output_file = os.path.join(folder, "mn_cleaned.csv")

# Read the data
with open(data_file, "r") as f:
    data = list(csv.reader(f))

with open(header_file, "r") as f:
    headers = list(csv.reader(f))

# Replace short headers with readable headers
header_names = {}

for row in headers:
    if len(row) >= 2:
        header_names[row[0]] = row[1]

new_headers = []

for header in data[0]:
    if header in header_names:
        new_headers.append(header_names[header])
    else:
        new_headers.append(header)

# Clean the values
def clean_value(value):
    value = value.strip()

    if value == "" or value.lower() in ["na", "n/a", "null"]:
        return "NA"

    return re.sub(r"\s+", " ", value)

cleaned_data = []

for row in data[1:]:
    cleaned_row = []

    for value in row:
        cleaned_row.append(clean_value(value))

    cleaned_data.append(cleaned_row)

# Find missing values
na_count = Counter()

for row in cleaned_data:
    for i, value in enumerate(row):
        if value == "NA":
            na_count[new_headers[i]] += 1

print("Rows:", len(cleaned_data))
print("Columns:", len(new_headers))
print("Missing values:", sum(na_count.values()))

# Check data types
print("\nData types:")

for i, header in enumerate(new_headers):
    values = [row[i] for row in cleaned_data if row[i] != "NA"]

    numbers = 0

    for value in values:
        try:
            float(value)
            numbers += 1
        except:
            pass

    if values and numbers == len(values):
        print(header, ": numeric")
    else:
        print(header, ": text")

# Find duplicate rows
duplicates = Counter(tuple(row) for row in cleaned_data)

duplicate_count = 0

for row, count in duplicates.items():
    if count > 1:
        duplicate_count += count - 1

print("\nDuplicate rows:", duplicate_count)

# Simple fuzzy matching
print("\nPossible similar values:")

for i, header in enumerate(new_headers):
    values = list(set(
        row[i] for row in cleaned_data
        if row[i] != "NA"
    ))

    if len(values) <= 100:
        for x in range(len(values)):
            for y in range(x + 1, len(values)):
                score = difflib.SequenceMatcher(
                    None, values[x].lower(), values[y].lower()
                ).ratio()

                if score >= 0.9 and values[x] != values[y]:
                    print(header, ":", values[x], "<->", values[y])

# Simple regex example
print("\nRegex check:")

for row in cleaned_data:
    for value in row:
        if re.search(r"\d+", value):
            pass

print("Regex check completed.")

# Basic numerical statistics
print("\nNumerical statistics:")

for i, header in enumerate(new_headers):
    numbers = []

    for row in cleaned_data:
        try:
            numbers.append(float(row[i]))
        except:
            pass

    if numbers:
        print(header)
        print("Minimum:", min(numbers))
        print("Maximum:", max(numbers))
        print("Average:", round(sum(numbers) / len(numbers), 2))

# Save cleaned data
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(new_headers)
    writer.writerows(cleaned_data)

print("\nCleaned data saved:", output_file)