from abc import ABC, abstractmethod
from src.analyzer.analyze import generate_acsl
import os


class Harness(ABC):

    @abstractmethod
    def _generate_tasks(self) -> list:
        """
        Implement this method to generate a list of tasks to run
        """

    def run(self):
        tasks = self._generate_tasks()
        for task in tasks:
            print(f"Generating ACSL for {task.program_name}...")
            if task.oracle_path is None or not os.path.exists(task.oracle_path):
                task.oracle_path = None

            generate_acsl(
                program_suite=task.program_suite,
                program_file=task.file_path,
                program_name=task.program_name,
                main_function=task.main_function,
                oracle_file=task.oracle_path,
                oracle_function=task.oracle_main,
                headers_path=task.headers_path,
            )
