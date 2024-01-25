import os
import subprocess
from .temp import setup_tmp


def run_eva(program_str: str, main_function: str, headers_dir: str):
    tmp_file_name = setup_tmp(headers_dir, program_str)

    command = [
        "frama-c",
        "-eva",
        "-lib-entry",
        "-eva-precision",
        "7",
        "-main",
        main_function,
        tmp_file_name,
    ]
    try:
        res = subprocess.run(command, capture_output=True, text=True)
        res.check_returncode()
        return res.stdout
    finally:
        os.remove(tmp_file_name)
