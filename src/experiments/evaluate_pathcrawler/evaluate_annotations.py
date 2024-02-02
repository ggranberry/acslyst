import datetime
import glob
import os
import re

from src.core.exceptions import (
    LLMException,
    PathcrawlerException,
)
from src.core.chains import parameters_chain, parameters_chainV2

from .output import Outputter

from src.core.pathcrawler import run_pathcrawler, run_pathcrawler_analyzer


def evaluate_annotations_pathcrawler(
    program_suite: str,
    program_name: str,
    main_function: str,
    headers_path: str,
    timestamp: str,
    annotated_programs_output_dir: str,  # this is some directory where we put annotated programs
    oracle_file=None,
    parameters_file=None,
):
    always_skip = [
        "Dates",
        "Luhn",
        "Apache",
        "Tcas",
        "TcasBranch",
        "TestCondCoverage3",
        "TestCondCoverage2",
        "TestCondCoverage1",
        "Heat",
        "Heat1",
        "ApacheBranches",
    ]
    skip_programs = [
        "ADPCM1",
        "AssertAssume",
        "BsearchPrecond",
        "BugKpath",
        "DatesBranches",
        "FloatTritypeLabels",
        "Interp",
        "IntTritypeLabels",
        "LabelsTcas",
        "MergePrecond",
        "MergeWithBreaks",
        "MutualRecursion",
        "PointeurFonction1",
        # "TestCondCoverage1",
        # "TestCondCoverage3",
        # "VariableDimArray2",
        # "Luhn",
        "Struct",
        # "Alias1",
        # "Alias3",
        # "Alias5",
        # "Bsearch",
        # "BsearchPrecond1",
        # "Bsort",
        # "EchoBranches",
        # "ExSysC",
        # "Merge",
        # "MutualRecursionNoRecurLimit",
        # "PointeurFonction5",
        # "Sample",
        "Test_ptr_out",
        "Tritype",
        "VariableDimArray2"
        # "VariableDimArray1"
    ]
    skip_programs = []
    skip_programs = skip_programs + always_skip
    if program_name in skip_programs:
        return
    outputter = Outputter(program_name, program_suite, timestamp)

    # Take in a folder that has our programs with ACSL generations
    annotated_programs = os.path.join(
        annotated_programs_output_dir, program_name, "*.c"
    )
    for c_file in glob.glob(annotated_programs):
        with open(c_file) as file:
            program_str = file.read()

        # Get the base name of the generation that we are working with
        base_name = os.path.basename(c_file)
        base_name, _ = os.path.splitext(base_name)

        if parameters_file is None:
            try:
                # Run the analyzer and edit the params file that was generated
                parameters = run_pathcrawler_analyzer(
                    base_name=base_name,
                    headers_dir=headers_path,
                    program_str=program_str,
                    main_function=main_function,
                )
            except Exception as e:
                outputter.output_exception(PathcrawlerException(e))
                continue
        else:
            with open(parameters_file) as file:
                ground_truth = file.read()
                parameters = clear_preconds(ground_truth, main_function)

        try:
            params_file_str = parameters_chainV2.invoke(
                {"program": program_str, "parameters": parameters}
            )
        except Exception as e:
            outputter.output_exception(LLMException(e))
            continue

        # Output the edited params file to our folder
        outputter.output_file(
            program=params_file_str, file_name=f"{base_name}_params.pl"
        )

        try:
            csv = run_pathcrawler_generator(
                base_name=base_name,
                params_file_str=params_file_str,
                program_str=program_str,
                main_function=main_function,
                outputter=outputter,
                oracle_file=oracle_file,
                headers_dir=headers_path,
            )
        except Exception as e:
            outputter.output_exception(PathcrawlerException(e))
            continue

        csv_rating = analyze_csv(csv_string=csv, base_name=base_name)
        outputter.add_pathcrawler_result(csv_rating)

    outputter.output_results()


def clear_preconds(prolog_str, main_function):
    pattern = r"(unquantif_preconds|quantif_preconds)\(.*?\)\.\n"

    # Replace matched patterns with empty versions
    return re.sub(
        pattern,
        lambda m: f"{m.group(1)}('{main_function}',[]).\n",
        prolog_str,
        flags=re.DOTALL,
    )


def analyze_csv(csv_string, base_name):
    # Check if the CSV string is empty
    if not csv_string.strip():
        return {
            "base_name": base_name,
            "test_cases": -1,
            "interrupts": -1,
            "invalid_mem": -1,
        }

    # Split the CSV string into lines
    lines = csv_string.strip().split("\n")

    # The number of rows is the count of lines minus 1 for the header
    num_rows = len(lines) - 1

    # Count the number of rows containing the string "interrupt"
    num_interrupts = sum("interrupt" in line for line in lines[1:])  # Skip header
    num_mem = sum("invalid" in line for line in lines[1:])  # Skip header

    return {
        "base_name": base_name,
        "test_cases": num_rows,
        "interrupts": num_interrupts,
        "invalid_mem": num_mem,
    }


def run_pathcrawler_generator(
    base_name: str,
    params_file_str: str,
    program_str: str,
    main_function: str,
    oracle_file,
    headers_dir,
    outputter,
):
    precond_file_name = "params.pl"
    csv = run_pathcrawler(
        program_str=program_str,
        main_function=main_function,
        oracle_file=oracle_file,
        headers_dir=headers_dir,
        preconds_str=params_file_str,
        precond_file_name=precond_file_name,
    )

    outputter.output_file(csv, f"{base_name}.csv")
    return csv


if __name__ == "__main__":
    name = "Alias2"
    evaluate_annotations_pathcrawler(
        annotated_programs_output_dir="output/count_annotations_eva/backup_first_run",
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        program_suite="pathcrawler_tests",
        program_name=name,
        headers_path=f"programs/pathcrawler_tests/{name}/",
        main_function="testme",
        parameters_file=f"programs/pathcrawler_tests/{name}/params.pl"
        # oracle_file=f"programs/pathcrawler_tests/{name}/OtherCfiles/oracle_testme.c"
    )
