import datetime

from src.core.exceptions import (
    LLMException,
)
from src.core.chains import (
    pathcrawler_chain,
)

from src.core.pathcrawler import run_pathcrawler

from .output import Outputter


def count_annotations(
    program_suite: str,
    program_name: str,
    program_file: str,
    main_function: str,
    headers_path: str,
    timestamp: str,
    oracle_file=None,
    parameters_file=None,
):
    outputter = Outputter(program_name, program_suite, timestamp)
    with open(program_file) as file:
        content = file.read()

    csv = run_pathcrawler(
        program_str=content,
        main_function=main_function,
        oracle_file=oracle_file,
        params_file=parameters_file,
        headers_dir=headers_path,
    )

    try:
        initial_generations = generations_with_pathcrawler_csv(content,csv)
    except Exception as e:
        outputter.output_exception(LLMException(e))
        return

    outputter.output_results(initial_generations)


def generations_with_pathcrawler_csv(program_str, csv):
    # First we generate 5 initial attempts to try and find a good starting point
    initial_generations = [
        pathcrawler_chain.invoke({"program": program_str, "csv": csv}) for _ in range(3)
    ]
    return [x for x in initial_generations if x is not None]


if __name__ == "__main__":
    name = "Alias3"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    count_annotations(
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        program_suite="pathcrawler_tests",
        program_name=name,
        program_file=f"programs/pathcrawler_tests/{name}/f.c",
        headers_path=f"programs/pathcrawler_tests/{name}/",
        main_function="testme",
    )
