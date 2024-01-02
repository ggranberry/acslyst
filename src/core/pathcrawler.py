import glob
import xml.etree.ElementTree as ET
import subprocess
import os
import tempfile
import shutil


def run_pathcrawler(
    program_str, main_function, headers_dir, oracle_file=None, params_file=None
):
    base_temp_dir = os.path.join(os.getcwd(), "temp_files")
    temp_dir = tempfile.mkdtemp(dir=base_temp_dir)
    try:
        res = exec_pathcrawler(
            program_str=program_str,
            temp_dir=temp_dir,
            main_function=main_function,
            headers_dir=headers_dir,
            oracle_file=oracle_file,
            params_file=params_file,
        )
        res.check_returncode()
        csv = get_test_cases_csv(f"{temp_dir}/testcases_temp_file/{main_function}/xml")
        return csv
    finally:
        shutil.rmtree(temp_dir)


def exec_pathcrawler_analyzer(
    program_str: str,
    temp_dir: str,
    main_function: str,
    headers_dir: str,
):
    temp_file_path = os.path.join(temp_dir, "temp_file.c")
    with open(temp_file_path, "w") as tmp:
        tmp.write(program_str)

    # Copy all the files from the headers_dir into the tmp dir
    for file in glob.glob(headers_dir):
        shutil.copy(file, temp_dir)

    # TODO IMPLEMENT THIS


def exec_pathcrawler(
    program_str: str,
    temp_dir: str,
    main_function: str,
    headers_dir: str,
    oracle_file=None,
    params_file=None,
):
    # Write the program to a temporary file
    temp_file_path = os.path.join(temp_dir, "temp_file.c")
    with open(temp_file_path, "w") as tmp:
        tmp.write(program_str)

    headers_dir_files = os.path.join(headers_dir, "*")

    # Copy all the files from the headers_dir into the tmp dir
    for file in glob.glob(headers_dir_files):
        if(os.path.isfile(file)):
            shutil.copy(file, temp_dir)

    # Prepare the Docker command
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

    cmd.append(temp_file_path)


    result = subprocess.run(cmd, check=False)
    print(result)
    return result


def exec_pathcrawler_docker(
    program_str: str,
    temp_dir: str,
    main_function: str,
    oracle_file: str,
    headers_dir: str,
):
    temp_file_path = os.path.join(temp_dir, "temp_file.c")

    # Write the program to a temporary file
    with open(temp_file_path, "w") as tmp:
        tmp.write(program_str)

    tmp_headers = os.path.join(temp_dir, "headers")
    shutil.copytree(headers_dir, tmp_headers)
    if oracle_file is not None:
        shutil.copy(oracle_file, temp_dir)
        oracle_command = f"-pc-oracle /work/tmp/oracle_{main_function}.c"
    else:
        oracle_command = ""

    # Prepare the Docker command
    docker_command = (
        f'frama-c -pc -no-frama-c-stdlib -variadic-no-translation -main {main_function} -cpp-command "gcc -E -I /work/tmp/headers" -no-cpp-frama-c-compliant '
        f"-machdep gcc_x86_64 -pc-xml {oracle_command} -pc-all-branches /work/tmp/temp_file.c"
    )
    cmd = [
        "docker",
        "run",
        "-w",
        "/work/output",
        "--entrypoint",
        "/bin/sh",
        "--rm",
        "--platform",
        "linux/amd64",
        "-v",
        f"{temp_dir}:/work/tmp",
        "ocaml-debug",
        "-c",
        docker_command,
    ]

    # Run the Docker command
    result = subprocess.run(cmd, check=True)
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
