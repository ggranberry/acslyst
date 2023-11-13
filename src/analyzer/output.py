import difflib
import os
from sanitize import extract_classification_count


class Outputter:
    def __init__(self, name, suite):
        self.name = name
        self.directory = f"output/{self.name}"
        os.makedirs(self.directory, exist_ok=True)
        self.repair_counter = 0

        self.oracle = False
        self.unit = False
        self.suite = suite

    def output_candidate(self, choice: dict, idx: int, is_choice=False):
        program = choice.get("program")
        score = choice.get("rank")
        classification_counts = choice.get("classifications")
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
        with open(f"output/{self.name}/final.txt", "w") as file:
            file.write(final_program)

    def output_pathcrawler_csv(self, csv: str):
        with open(f"{self.directory}/pathcrawler.csv", "w") as file:
            file.write(csv)

    def output_pathcrawler_program(self, program: str):
        self.pathcrawler_classification = extract_classification_count(program)
        with open(f"{self.directory}/pathcrawler.txt", "w") as file:
            file.write(program)

    def get_classification_difference(self, dict_a: dict, dict_b: dict):
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
        }

        with open(f"{self.directory}/results.txt", "w") as file:
            file.write(str(results))
