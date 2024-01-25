import datetime

from src.core.exceptions import (
    LLMException,
    EvaException,
)
from src.core.chains import (
    acsl_generation_eva_chain
)

from src.core.eva import run_eva

from .output import Outputter


def count_annotations_eva(
    program_suite: str,
    program_name: str,
    program_file: str,
    main_function: str,
    headers_path: str,
    timestamp: str,
):
    outputter = Outputter(program_name, program_suite, timestamp)
    with open(program_file) as file:
        content = file.read()

    try:
        report = run_eva(
            program_str=content,
            main_function=main_function,
            headers_dir=headers_path,
        )

        outputter.output_report(report)
    except Exception as e:
        outputter.output_exception(EvaException(e))
        return

    try:
        initial_generations = generations_with_eva(content,report)
    except Exception as e:
        outputter.output_exception(LLMException(e))
        return

    outputter.output_results(initial_generations)


def generations_with_eva(program_str, report):
    # First we generate 5 initial attempts to try and find a good starting point
    initial_generations = [
            acsl_generation_eva_chain.invoke({"program": program_str, "eva": report}) for _ in range(3)
    ]
    return [x for x in initial_generations if x is not None]


if __name__ == "__main__":
    name = "BugKpath"
    count_annotations_eva(
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        program_suite="pathcrawler_tests",
        program_name=name,
        program_file=f"programs/pathcrawler_tests/{name}/f.c",
        headers_dir=f"programs/pathcrawler_tests/{name}/",
        main_function="testme",
    )
