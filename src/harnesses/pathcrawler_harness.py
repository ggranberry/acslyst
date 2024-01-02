from .harness import Harness
from .task import Task
import datetime
import glob
import os


class PathCrawlerHarness(Harness):
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
        oracle_path = os.path.join(directory_path, "OtherCfiles/oracle_testme.c")
        headers_path = directory_path
        if not os.path.exists(oracle_path):
            oracle_path = None
        return Task(
            program_suite="pathcrawler_tests",
            headers_path=headers_path,
            program_file=program_file,
            program_name=program_name,
            main_function="testme",
            oracle_path=oracle_path,
            oracle_main="oracle_testme",
            timestamp=timestamp,
        )
