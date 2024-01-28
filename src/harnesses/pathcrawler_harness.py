from .harness import Harness
from .task import Task
import datetime
import glob
import os


class PathCrawlerHarness(Harness):
    def __init__(self, annotated_programs_output_dir=None):
        self.annotated_programs_output_dir = annotated_programs_output_dir

    def _generate_tasks(self):
        base_directory = "programs/pathcrawler_tests/"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return map(
            lambda directory: self.__generate_task(directory, timestamp),
            glob.glob(os.path.join(base_directory, "*/")),
        )

    def __generate_task(self, directory_path, timestamp):
        program_file = os.path.join(directory_path, "f.c")
        program_name = os.path.basename(os.path.normpath(directory_path))
        oracle_file = os.path.join(directory_path, "OtherCfiles/oracle_testme.c")
        parameters_file = os.path.join(directory_path, "params.pl")
        headers_path = directory_path

        if not os.path.exists(oracle_file):
            oracle_file = None
        if not os.path.exists(parameters_file):
            parameters_file = None

        return Task(
            program_suite="pathcrawler_tests",
            headers_path=headers_path,
            program_file=program_file,
            program_name=program_name,
            main_function="testme",
            oracle_file=oracle_file,
            oracle_main="oracle_testme",
            parameters_file=parameters_file,
            timestamp=timestamp,
            annotated_programs_output_dir=self.annotated_programs_output_dir,
        )
