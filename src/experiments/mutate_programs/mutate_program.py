import datetime

from src.core.exceptions import (
    LLMException,
)
from src.core.chains import (
    mutate_chain,
)
from src.core.repair import repair_compile
from .output import Outputter


def mutate_program(
    program_suite: str,
    program_name: str,
    program_file: str,
    headers_path: str,
    timestamp: str,
):
    outputter = Outputter(program_name, program_suite, timestamp)
    outputter.copy_dir(headers_path)
    with open(program_file) as file:
        content = file.read()


    try:
        mutated, full_txt = mutate_chain.invoke({"program": content})
    except Exception as e:
        outputter.output_exception(LLMException(e))
        return

    repaired = repair_compile(headers_path=headers_path,mutated_program=mutated)

    outputter.output_results(repaired, full_txt)


if __name__ == "__main__":
    name = "TestCondCoverage3"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    mutate_program(
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        program_suite="pathcrawler_tests",
        program_name=name,
        headers_path="programs/pathcrawler_tests/{name}",
        program_file=f"programs/pathcrawler_tests/{name}/f.c",
    )
