import os
from collections import Counter


class Outputter:
    def __init__(self, name, suite, timestamp):
        self.name = name
        self.directory = f"output/count_annotations_pathcrawler/{timestamp}/{self.name}"
        os.makedirs(self.directory, exist_ok=True)

        self.suite = suite

    def output_results(self, generations):
        for i, generation in enumerate(generations):
            program_str = generation[0]
            with open(f"{self.directory}/initial_generation_{i}.c", "w") as file:
                file.write(program_str)

        classification_counts = [elem[1] for elem in generations]
        print("classification_counts: ", classification_counts)
        combined_dict = sum((Counter(d) for d in classification_counts), Counter())

        results = {"suite": self.suite, "program": self.name, "counts": combined_dict}

        with open(f"{self.directory}/results.txt", "w") as file:
            file.write(str(results))

    def output_pathcrawler_csv(self, csv: str):
        with open(f"{self.directory}/pathcrawler.csv", "w") as file:
            file.write(csv)

    def output_exception(self, exception):
        with open(f"{self.directory}/error.txt", "w") as file:
            file.write(
                f"\n\nException:\n{exception.message}\n\n{exception.original_exception}"
            )

