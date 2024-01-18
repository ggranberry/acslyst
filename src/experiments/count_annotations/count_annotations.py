import datetime

from src.core.exceptions import (
    LLMException,
)
from src.core.chains import (
    acsl_generation_chain,
)
from .output import Outputter


def count_annotations(
    program_suite: str,
    program_name: str,
    program_file: str,
    timestamp: str,
):
    outputter = Outputter(program_name, program_suite, timestamp)
    with open(program_file) as file:
        content = file.read()

    try:
        initial_generations = generate_initial(content)
    except Exception as e:
        outputter.output_exception(LLMException(e))
        return

    outputter.output_results(initial_generations)


def generate_initial(content):
    # First we generate 5 initial attempts to try and find a good starting point
    initial_generations = [
        acsl_generation_chain.invoke({"program": content}) for _ in range(5)
    ]
    return [x for x in initial_generations if x is not None]


if __name__ == "__main__":
    name = "TestCondCoverage3"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    count_annotations(
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        program_suite="pathcrawler_tests",
        program_name=name,
        program_file=f"programs/pathcrawler_tests/{name}/f.c",
    )
