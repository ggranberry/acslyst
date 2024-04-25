import os
import shutil
import glob

class Outputter:
    def __init__(self, name, suite, timestamp):
        self.name = name
        self.directory = f"output/mutate_programs/{suite}/{timestamp}/{name}"
        os.makedirs(self.directory, exist_ok=True)

        self.suite = suite

    def copy_dir(self, headers_dir):
        headers_dir_files = os.path.join(headers_dir, "*")
        for file in glob.glob(headers_dir_files):
            if os.path.isfile(file):
                shutil.copy(file, self.directory)

    def output_results(self, mutated_program, full_txt):
        with open(f"{self.directory}/f.c", "w") as file:
            file.write(mutated_program)
        with open(f"{self.directory}/full_output.txt", "w") as file:
            file.write(full_txt)

    def output_exception(self, exception):
        with open(f"{self.directory}/error.txt", "w") as file:
            file.write(
                f"\n\nException:\n{exception.message}\n\n{exception.original_exception}"
            )
