from .harness import Harness
from .task import Task
import glob
import os


class PathCrawlerHarness(Harness):
    def _generate_tasks(self):
        base_directory = "programs/pathcrawler_tests/"
        return map(self.__generate_task, glob.glob(os.path.join(base_directory, "*/")))

    def __generate_task(self, directory_path):
        file_path = os.path.join(directory_path, "f.c")
        program_name = os.path.basename(os.path.normpath(directory_path))
        oracle_path = os.path.join(directory_path, "OtherCfiles/oracle_testme.c")
        headers_path = directory_path
        if not os.path.exists(oracle_path):
            oracle_path = None
        return Task(
            program_suite = "pathcrawler_tests",
            headers_path = headers_path,
            file_path=file_path,
            program_name=program_name,
            main_function="testme",
            oracle_path=oracle_path,
            oracle_main="oracle_testme",
        )
