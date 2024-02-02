import datetime
import glob
import os

from src.core.exceptions import (
    WPException,
)

from .output import Outputter

from src.core.repair import repair


def evaluate_annotations_wp(
    program_suite: str,
    program_name: str,
    main_function: str,
    headers_path: str,
    timestamp: str,
    annotated_programs_output_dir: str,  # this is some directory where we put annotated programs
):
    # skip_programs = ["ADPCM1","AssertAssume","BsearchPrecond", "BsearchPrecond1", "DatesBranches", "FloatTritypeLabels", "LabelsTcas", "Luhn", "MergePrecond",  "MutualRecursion", "PointeurFonction1", "PointeurFonction5", "Test_ptr_out", "TestCondCoverage3" "MergeWithBreaks", "Struct", "BugKpath", "FloatTritypeLabels", "Tritype", "TestCondConverage1", "VariableDimArray2", "ADPCM", "MergeWithBreaks"]
    skip_programs = []
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

        try:
            _, report = repair(
                annotated_program=program_str,
                headers_path=headers_path,
                main_method=main_function,
            )
        except Exception as e:
            outputter.output_exception(WPException(e), base_name)
            continue
        outputter.output_wp_result(base_name,report)

if __name__ == "__main__":
    name = "EchoBranches"
    evaluate_annotations_wp(
        annotated_programs_output_dir="output/count_annotations_pathcrawler/third_run_headers/",
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        program_suite="pathcrawler_tests",
        program_name=name,
        headers_path=f"programs/pathcrawler_tests/{name}/",
        main_function="testme",
    )
