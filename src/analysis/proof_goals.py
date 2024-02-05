import os
import json
import re

def fix_json_number_format(json_string):
    # Pattern to find numbers that end with a dot and are not followed by any digits
    pattern = re.compile(r'(\d+)\.(?!\d)')
    # Replace such numbers with the number itself (removing the dot)
    return pattern.sub(r'\1', json_string)

def count_proof_goals(directory):
    total_goals = 0
    proven_goals = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    report_str = f.read()
                    fixed_report_str = fix_json_number_format(report_str)
                    report = json.loads(fixed_report_str)
                    # # report = [goal for goal in report if "_rte_" not in goal.get("goal", "")]
                    # # report = [goal for goal in report if "_rte_" not in goal.get("goal", "") and "testme_requires" not in goal.get("goal", "") and "assigns" not in goal.get("goal", "")]
                    report = [goal for goal in report if  "assigns" not in goal.get("goal", "")]
                    # report = [goal for goal in report if "assert" in goal.get("goal", "")]

                    total_goals += len(report)
                    proven_goals += sum(1 for goal in report if goal.get("proved") == 1)
    return total_goals, proven_goals

def main():
    base_dir = 'output/evaluate_wp'
    pc_analysis_dir = os.path.join(base_dir, 'pc_analysis')
    plain_analysis_dir = os.path.join(base_dir, 'plain_analysis')
    
    pc_goals, pc_proven = count_proof_goals(pc_analysis_dir)
    plain_goals, plain_proven = count_proof_goals(plain_analysis_dir)
    
    print(f"PC Analysis: {pc_proven}/{pc_goals}")
    print(f"Plain Analysis: {plain_proven}/{plain_goals}")

if __name__ == "__main__":
    main()

