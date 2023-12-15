import difflib
import os
from .wp import exec_wp, extract_proofs_and_goals


class Outputter:
    def __init__(self, name, suite, oracle_file):
        self.name = name
        self.directory = f"output/{self.name}"
        os.makedirs(self.directory, exist_ok=True)
        self.repair_counter = 0

        if oracle_file is not None:
            self.oracle = True
        else:
            self.oracle = False
        self.unit = False
        self.suite = suite

    def output_candidate(self, candidate: dict, idx: int, is_choice=False):
        program = candidate.get("program")
        score = candidate.get("rank")
        classification_counts = candidate.get("classifications")
        content = f"""Score: {score}
    
Program:
```c
{program}
```
    
Classification Counts:
{classification_counts}"""
        output_file = f"{self.directory}/candidate_{idx}.txt"

        if is_choice:
            output_file = f"{self.directory}/choice.txt"
            self.choice_classifications = classification_counts
        with open(output_file, "w") as file:
            file.write(content)
        self.current_program = program

    def output_repair(self, repaired_program: str):
        if self.current_program is None:
            raise Exception("program not set")
        diff = list(
            difflib.ndiff(
                self.current_program.splitlines(), repaired_program.splitlines()
            )
        )
        diff_str = "\n".join(diff)
        with open(f"{self.directory}/repair.txt", "a") as file:
            file.write(f"\n\nRepair{self.repair_counter}:\n{diff_str}")
        self.current_program = repaired_program
        self.repair_counter = self.repair_counter + 1

    def output_exception(self, exception):
        with open(f"output/{self.name}/error.txt", "w") as file:
            file.write(
                f"\n\nException:\n{exception.message}\n\n{exception.original_exception}"
            )

    def output_final(self, final_program: str):
        with open(f"output/{self.name}/final.c", "w") as file:
            file.write(final_program)
        self.output_results()

    def output_pathcrawler_csv(self, csv: str):
        with open(f"{self.directory}/pathcrawler.csv", "w") as file:
            file.write(csv)

    def output_pathcrawler_program(self, program: str, classification_counts: dict):
        self.pathcrawler_classification = classification_counts
        with open(f"{self.directory}/pathcrawler.txt", "w") as file:
            file.write(program)

    def get_classification_difference(self, dict_a , dict_b):
        result = {}

        # Get all unique keys from both dictionaries
        all_keys = set(dict_a.keys()) | set(dict_b.keys())

        for key in all_keys:
            # Get the value from each dictionary, defaulting to 0 if the key is not present
            a_val = dict_a.get(key, 0)
            b_val = dict_b.get(key, 0)

            # Calculate the difference and store it in the result dictionary
            result[key] = b_val - a_val
        return result

    def set_initial_wp_results(self, program: str, headers_path):
        wp_output = exec_wp(annotated_program=program, headers_path=headers_path)
        if wp_output.returncode != 0:
            raise Exception("Failed to set initial WP results")
        proved, goals = extract_proofs_and_goals(wp_output.stdout)
        self.choice_proved = proved
        self.choice_goals = goals

    def set_pathcrawler_wp_results(self, program: str, headers_path):
        wp_output = exec_wp(annotated_program=program, headers_path=headers_path)
        if wp_output.returncode != 0:
            raise Exception("Failed to set pathcrawler WP results")
        proved, goals = extract_proofs_and_goals(wp_output.stdout)
        self.pathcrawler_proved = proved
        self.pathcrawler_goals = goals



    def output_results(self):
        pathcrawler_additions = self.get_classification_difference(
            self.choice_classifications, self.pathcrawler_classification
        )
        results = {
            "choice": self.choice_classifications,
            "pathcrawler": pathcrawler_additions,
            "oracle": self.oracle,
            "unit": self.unit,
            "suite": self.suite,
            "initial_proved": self.choice_proved,
            "initial_goals": self.choice_goals,
            "pathcrawler_proved": self.pathcrawler_proved,
            "pathcrawler_goals": self.pathcrawler_goals,
        }

        with open(f"{self.directory}/results.txt", "w") as file:
            file.write(str(results))
