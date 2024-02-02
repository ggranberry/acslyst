import glob
import xml.etree.ElementTree as ET
import subprocess
import shutil
import os
from .temp import setup_pathcrawler_tmp


def run_pathcrawler(
    program_str,
    main_function,
    headers_dir,
    oracle_file=None,
    params_file=None,
    preconds_str=None,
    precond_file_name=None,
):
    tmp_file_path, temp_dir = setup_pathcrawler_tmp(
        headers_dir=headers_dir,
        program_str=program_str,
        tmp_file_name="temp_file.c",
        precond_str=preconds_str,
        precond_file_name=precond_file_name,
    )
    # TODO this is a bit of a hack in that we don't want to run analysis on the annotated program. So we'll just run it on the original
    tmp_file_path = os.path.join(temp_dir, "f.c")

    if precond_file_name is not None:
        params_file = os.path.join(temp_dir, precond_file_name)

    try:
        res = exec_pathcrawler(
            main_function=main_function,
            tmp_file_path=tmp_file_path,
            oracle_file=oracle_file,
            params_file=params_file,
        )
        res.check_returncode()
        # TODO remember we might need to switch this back to not f
        csv = get_test_cases_csv(f"{temp_dir}/testcases_f/{main_function}/xml")
        return csv
    finally:
        shutil.rmtree(temp_dir)


# Runs the analyzer portion of pathcrawler in a temp directory and returns the parameter file as a string
def run_pathcrawler_analyzer(
    base_name: str,
    headers_dir: str,
    program_str: str,
    main_function: str,
):
    temp_file_path, temp_dir = setup_pathcrawler_tmp(
        headers_dir=headers_dir, program_str=program_str, tmp_file_name=f"{base_name}.c"
    )
    # TODO this is a bit of a hack in that we don't want to run analysis on the annotated program. So we'll just run it on the original
    temp_file_path = os.path.join(temp_dir, "f.c")
    try:
        cmd = [
            "frama-c",
            "-pc-analyzer",
            "-no-frama-c-stdlib",
            "-variadic-no-translation",
            "-main",
            main_function,
            temp_file_path,
        ]
        res = subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL)
        res.check_returncode()

        analysis_dir_name = f"pathcrawler_f"
        parameters_file_path = os.path.join(
            temp_dir, analysis_dir_name, "test_parameters.pl"
        )
        with open(parameters_file_path, "r") as file:
            content = file.read()
        return content
    finally:
        shutil.rmtree(temp_dir)


def exec_pathcrawler(
    main_function: str,
    tmp_file_path: str,
    oracle_file=None,
    params_file=None,
):
    cmd = [
        "frama-c",
        "-pc",
        "-no-frama-c-stdlib",
        "-variadic-no-translation",
        "-main",
        main_function,
        "-no-cpp-frama-c-compliant",
        "-pc-xml",
        "-pc-all-branches",
    ]

    # Append oracle_command if it's not empty
    if oracle_file is not None:
        cmd.append("-pc-oracle")
        cmd.append(oracle_file)

    # Append params_command if it's not empty
    if params_file is not None:
        cmd.append("-pc-test-params")
        cmd.append(params_file)

    cmd.append(tmp_file_path)

    result = subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, timeout=120)
    return result


def get_test_cases_csv(directory_path: str):
    """
    Returns a csv string of all test cases in the given path
    """
    xml_files = glob.glob(f"{directory_path}/TC_*.xml")
    if len(xml_files) == 0:
        return ""

    print(f"Found {len(xml_files)} test cases")
    header = get_csv_header(xml_files[0])
    rows = list(map(lambda x: get_as_csv_row(x), xml_files))
    return "\n".join([header] + rows)


def get_csv_header(xml_file: str):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    input_elements = root.findall("./Inputs/VVal/VName")
    input_columns = ",".join(list(map(lambda x: f"input_{x.text}", input_elements)))

    return f"{input_columns},output,verdict"


def get_as_csv_row(xml_file: str):
    """
    converts the test case xml into a minimal csv row
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    row = []

    input_elements = root.findall("./Inputs/VVal/Val")
    inputs = list(map(lambda x: x.text, input_elements))
    inputs = ",".join([x for x in inputs if x is not None])
    row.append(inputs)

    output_elements = root.findall("./Outputs/Output/Val")
    outputs = list(map(lambda x: x.text, output_elements))
    outputs = ",".join([x for x in outputs if x is not None])
    row.append(outputs)

    verdict = root.find("./Verdict")
    if verdict is not None:
        row.append(verdict.attrib.get("Type"))
    return ",".join(row)
