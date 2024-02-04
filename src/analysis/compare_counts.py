import os
import sys
import json
from collections import Counter

def find_results_files(directories):
    """Finds 'results.txt' files for each program across multiple directories."""
    program_files = {}
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == 'results.txt':
                    program_name = os.path.basename(root)  # Assuming program's folder name is unique
                    if program_name not in program_files:
                        program_files[program_name] = []
                    program_files[program_name].append(os.path.join(root, file))
    return program_files

def parse_file(file_path):
    """Parses a 'results.txt' file and returns its counts dictionary."""
    try:
        with open(file_path, 'r') as file:
            data_dict = eval(file.read(), {"__builtins__": {}}, {"Counter": Counter})
            return data_dict.get('counts', {})
    except SyntaxError as e:
        print(f"Error parsing file {file_path}: {e}")
        return {}

def compare_program_counts(program_files):
    """Compares count maps for each program across provided directories."""
    comparison_results = {}
    for program_name, files in program_files.items():
        comparison_results[program_name] = {os.path.dirname(f): parse_file(f) for f in files}
    return comparison_results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <directory1> <directory2> ...")
        sys.exit(1)

    directories = sys.argv[1:]
    program_files = find_results_files(directories)
    comparison_results = compare_program_counts(program_files)

    for program_name, dir_counts in comparison_results.items():
        print(f"\n{program_name}:")
        for dir_path, counts in dir_counts.items():
            relative_dir_path = os.path.relpath(dir_path, start=os.path.commonpath(directories))
            print(f"  {relative_dir_path}: {counts}")

