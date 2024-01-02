from abc import ABC, abstractmethod
from src.core.analyze import generate_acsl
import os
import inspect


class Harness(ABC):

    @abstractmethod
    def _generate_tasks(self) -> list:
        """
        Implement this method to generate a list of tasks to run
        """

    def run(self, experiment):
        # Get the function's signature
        signature = inspect.signature(experiment)

        # Extract the parameter names
        parameter_names = signature.parameters.keys()

        # Each task represents a details needed to analyze a program 
        tasks = self._generate_tasks()

        for task in tasks:
            print(f"Generating ACSL for {task.program_name}...")

            # Extract the corresponding values from the task object
            function_arguments = {}
            for parameter_name in parameter_names:
                function_arguments[parameter_name] = getattr(task, parameter_name)

            experiment(**function_arguments)

