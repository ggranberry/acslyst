import os
import re

def count_alarms_in_file_filtered(filepath):
    """Count the number of alarm lines in a given file, excluding certain alarms based on the next line's content."""
    alarm_count = 0
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    i = 0
    while i < len(lines) - 1:
        current_line = lines[i]
        next_line = lines[i + 1]
        # Check if current line is an alarm and if next line does not contain the excluded pattern
        if current_line.startswith('[eva:alarm]'):
            exclude_pattern = re.compile(r'function testme: precondition .+ got status unknown')
            if not exclude_pattern.search(next_line):
                alarm_count += 1
        i += 1

    return alarm_count
def count_alarms_in_file(filepath):
    """Count the number of alarm lines in a given file."""
    alarm_count = 0
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('[eva:alarm]'):
                alarm_count += 1
    return alarm_count

def find_and_count_alarms(directory):
    """Recursively find files and count alarms."""
    pattern = re.compile(r'initial_generation_\d+_stdout\.txt$')
    total_alarms = 0

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if pattern.search(filename):
                filepath = os.path.join(root, filename)
                total_alarms += count_alarms_in_file_filtered(filepath)


    return total_alarms

# Replace 'path_to_directory' with the path to your target directory
plain_path = 'output/evaluate_eva/plain_analysis_2'
plain_alarms = find_and_count_alarms(plain_path)
print(f"plain: {plain_alarms}")

pc_path = 'output/evaluate_eva/pc_analysis_2'
pc_alarms = find_and_count_alarms(pc_path)
print(f"pc: {pc_alarms}")

eva_path = 'output/evaluate_eva/eva_analysis_2'
eva_alarms = find_and_count_alarms(eva_path)
print(f"eva: {eva_alarms}")

