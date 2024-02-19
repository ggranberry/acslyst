import csv
import os
from io import StringIO


# Function to recursively find CSV files
def find_csv_files(root_dir, pattern):
    matches = []
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if pattern in filename:
                matches.append(os.path.join(root, filename))
    return matches

# Function to count the properties' statuses in a CSV file
def count_properties_in_file(filepath):
    counts = {'Unknown': 0, 'Valid': 0, 'Dead': 0, 'Invalid': 0}
    with open(filepath, newline='') as csvfile:
        csv_str = csvfile.read()
        sanitized = csv_str.replace('\t', ',')
        io_sanitized = StringIO(sanitized)
        reader = csv.DictReader(io_sanitized)
        for row in reader:
            if 'status' in row:
                status = row['status']
                # Consider "Considered valid" as "Valid"
                if status == 'Considered valid':
                    status = 'Valid'
                if status in counts:
                    counts[status] += 1
    return counts

# Main function to aggregate counts from all files
def aggregate_counts(root_dir):
    csv_files = find_csv_files(root_dir, 'initial_generation_')
    total_counts = {'Unknown': 0, 'Valid': 0, 'Dead': 0, 'Invalid': 0}
    for filepath in csv_files:
        counts = count_properties_in_file(filepath)
        for key in total_counts:
            total_counts[key] += counts.get(key, 0)
    return total_counts

# Example usage
plain_path = 'output/evaluate_eva/plain_analysis_2'
plain_counts = aggregate_counts(plain_path)
print(f"plain: {plain_counts}")

pc_path = 'output/evaluate_eva/pc_analysis_2'
pc_counts = aggregate_counts(pc_path)
print(f"pc: {pc_counts}")

eva_path = 'output/evaluate_eva/eva_analysis_2'
eva_counts = aggregate_counts(eva_path)
print(f"eva: {eva_counts}")

