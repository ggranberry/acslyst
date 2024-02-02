import os
from collections import Counter


class Outputter:
    def __init__(self, name, suite, timestamp):
        self.name = name
        self.directory = f"output/evaluate_pathcrawler/{timestamp}/{self.name}"
        os.makedirs(self.directory, exist_ok=True)
        self.suite = suite
        self.results = []

    def output_file(self, program, file_name):
        with open(f"{self.directory}/{file_name}", "w") as file:
            file.write(program)

    def add_pathcrawler_result(self, res_dict):
       self.results.append(res_dict) 

    def output_results(self, labels={}):
        if all(res == {"test_cases": -1, "interrupts": -1, "invalid_mem": -1} for res in self.results):
            with open(f"{self.directory}/bad_generations.txt", "w") as file:
                file.write(str("Generations didn't parse"))
            return
        else:
            max_dict = max(self.results, key=lambda x: (x['test_cases'], -(x['interrupts'] + x['invalid_mem'])))
            results = {"best": max_dict, "all": self.results} | labels
            with open(f"{self.directory}/results.txt", "w") as file:
                file.write(str(results))


    def output_exception(self, exception):
        with open(f"{self.directory}/error.txt", "w") as file:
            file.write(
                f"\n\nException:\n{exception.message}\n\n{exception.original_exception}"
            )

