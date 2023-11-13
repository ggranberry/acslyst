from abc import ABC, abstractmethod
from analyzer.analyze import generate_acsl


class Harness(ABC):
    tasks: list

    @abstractmethod
    def _generate_tasks(self):
        """
        Implement this method to generate a list of tasks to run
        """

    def run(self):
        for task in self.tasks:
            generate_acsl(
                program_file=task.file_path,
                program_name=task.program_name,
                main_function=task.main_function,
                oracle_file=task.oracle_path,
                oracle_function=task.oracle_main,
            )
