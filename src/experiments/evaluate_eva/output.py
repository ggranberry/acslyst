import os


class Outputter:
    def __init__(self, name, suite, timestamp):
        self.name = name
        self.directory = f"output/evaluate_eva/{timestamp}/{self.name}"
        os.makedirs(self.directory, exist_ok=True)
        self.suite = suite
        self.results = []

    def output_eva_csv(self, base_name, csv_string):
        result_path = os.path.join(self.directory, f"{base_name}.csv")
        with open(result_path, 'w') as file:
            file.write(csv_string)

    def output_eva_stdout(self, base_name, stdout):
        result_path = os.path.join(self.directory, f"{base_name}_stdout.txt")
        with open(result_path, 'w') as file:
            file.write(stdout)

    def output_repaired_program(self, base_name, program_str, dir_to_output):
        result_path = os.path.join(dir_to_output, f"{base_name}_repaired.c")
        with open(result_path, 'w') as file:
            file.write(program_str)


    def output_exception(self, exception, base_name):
        with open(f"{self.directory}/{base_name}.txt", "w") as file:
            file.write(
            f"\n\nException:\n{exception.message}\n\n{exception.original_exception}"
            )

