import os
import subprocess
from .temp import setup_pathcrawler_tmp


def run_eva(program_str: str, main_function: str, headers_dir: str):
    tmp_file_name,temp_dir = setup_pathcrawler_tmp(headers_dir, program_str, tmp_file_name="eva_temp.c")
    report_path = os.path.join(temp_dir, "temp_report.csv")

    command = [
        "frama-c",
        "-eva",
        "-lib-entry",
        "-eva-precision",
        "7",
        "-main",
        main_function,
        tmp_file_name,
        "-then",
        "-report-csv",
        report_path
    ]
    try:
        res = subprocess.run(command, capture_output=True, text=True)
        if os.path.exists(report_path):
            with open(report_path, 'r') as file:
                report = file.read()
        else:
            report = ""
        return res, report
    finally:
        os.remove(tmp_file_name)
