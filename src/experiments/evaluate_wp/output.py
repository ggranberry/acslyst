import os
import json
from collections import Counter


class Outputter:
    def __init__(self, name, suite, timestamp):
        self.name = name
        self.directory = f"output/evaluate_wp/{timestamp}/{self.name}"
        os.makedirs(self.directory, exist_ok=True)
        self.suite = suite
        self.results = []

    def output_wp_result(self, base_name, report):
        result_path = os.path.join(self.directory, f"{base_name}.json")
        with open(result_path, 'w') as file:
            json.dump(report, file, indent=4)


    def output_exception(self, exception, base_name):
        with open(f"{self.directory}/{base_name}.txt", "w") as file:
            file.write(
                f"\n\nException:\n{exception.message}\n\n{exception.original_exception}"
            )

