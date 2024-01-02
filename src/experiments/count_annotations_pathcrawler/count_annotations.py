import datetime

from src.core.exceptions import (
    LLMException,
    PathcrawlerException,
)
from src.core.chains import (
    acsl_generation_pathcrawler_chain
)

from src.core.pathcrawler import run_pathcrawler

from .output import Outputter


def count_annotations_pathcrawler(
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

    try:
        csv = run_pathcrawler(
            program_str=content,
            main_function=main_function,
            oracle_file=oracle_file,
            params_file=parameters_file,
            headers_dir=headers_path,
        )

        outputter.output_pathcrawler_csv(csv)
    except Exception as e:
        outputter.output_exception(PathcrawlerException(e))
        return

    try:
        initial_generations = generations_with_pathcrawler_csv(content,csv, oracle_file)
    except Exception as e:
        outputter.output_exception(LLMException(e))
        return

    outputter.output_results(initial_generations)


def generations_with_pathcrawler_csv(program_str, csv, oracle_file):
    if oracle_file is not None:
        with open(oracle_file) as file:
            oracle = file.read()
    else:
        oracle = ""

    # First we generate 5 initial attempts to try and find a good starting point
    initial_generations = [
            acsl_generation_pathcrawler_chain.invoke({"program": program_str, "csv": csv, "oracle": oracle}) for _ in range(3)
    ]
    return [x for x in initial_generations if x is not None]


if __name__ == "__main__":
    name = "ADPCM"
    count_annotations_pathcrawler(
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        program_suite="pathcrawler_tests",
        program_name=name,
        program_file=f"programs/pathcrawler_tests/{name}/f.c",
        headers_path=f"programs/pathcrawler_tests/{name}/",
        main_function="testme",
        parameters_file=f"programs/pathcrawler_tests/{name}/params.pl",
        # oracle_file=f"programs/pathcrawler_tests/{name}/OtherCfiles/oracle_testme.c"
    )
