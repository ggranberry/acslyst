import glob
import xml.etree.ElementTree as ET
import subprocess
import os
import tempfile
import shutil

base_temp_dir = os.path.join(os.getcwd(), "temp_files")

def run_pathcrawler(program_str):
    base_temp_dir = os.path.join(os.getcwd(), "temp_files")
    temp_dir = tempfile.mkdtemp(dir=base_temp_dir)
    shutil.copy("./examples/Bsearch/OtherCfiles/oracle_testme.c", temp_dir)
    try:
        res = exec_pathcrawler(program_str, temp_dir)
        res.check_returncode()
        csv = get_test_cases_csv(f"{temp_dir}/testcases_temp_file/main/xml")
        return csv
    finally:
        shutil.rmtree(temp_dir)


def exec_pathcrawler(program_str: str, temp_dir: str):
    example_dir = "examples"
    temp_file_path = os.path.join(temp_dir, "temp_file.c")

    # Write the program to a temporary file
    with open(temp_file_path, "w") as tmp:
        tmp.write(program_str)

    # Prepare the Docker command
    docker_command = (
    f"frama-c -pc -no-frama-c-stdlib -variadic-no-translation "
    f"-machdep gcc_x86_64 -lib-entry -pc-xml -pc-oracle /work/tmp/oracle_testme.c -pc-all-branches /work/tmp/temp_file.c && ls -la /work/tmp"
)
    cmd = [
        "docker",
        "run",
        "-w",
        "/work/output",
        "--entrypoint", "/bin/sh",
        "--rm",
        "--platform",
        "linux/amd64",
        "-v",
        f"{temp_dir}:/work/tmp",
        "ocaml-debug",
        "-c", docker_command
    ]

    # Run the Docker command
    result = subprocess.run(cmd, check=True)
    return result 


def get_test_cases_csv(directory_path: str):
    """
    Returns a csv string of all test cases in the given path
    """
    xml_files = glob.glob(f"{directory_path}/TC_*.xml")

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
