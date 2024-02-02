import os
import sys
import re
from collections import Counter

def find_results_files(directory):
    pattern = r'^initial_generation_\d+\.json$'
    for root, dirs, files in os.walk(directory):
        for file in files:
            with open(file, 'r') as f:
                name = f.name
                if re.match(pattern, name):
                    yield os.path.join(root, file)

def parse_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Use eval in a safer way
            data_dict = eval(file.read(), {"__builtins__": {}}, {"Counter": Counter})
            return data_dict.get('counts', {})
    except SyntaxError as e:
        print(f"Error parsing file {file_path}: {e}")
        return {}

def merge_counts(directories):
    total_counts = Counter()
    for directory in directories:
        for file_path in find_results_files(directory):
            counts = parse_file(file_path)
            total_counts.update(counts)
    return total_counts

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <directory1> <directory2> ...")
        sys.exit(1)

    directories = sys.argv[1:]
    merged_counts = merge_counts(directories)
    print("Merged Counts:", merged_counts)

