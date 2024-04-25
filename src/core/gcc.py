import subprocess
import shutil
from src.core.temp import setup_wp_tmp

def compile_program(program_str,headers_path):
    temp_file_path, temp_dir = setup_wp_tmp(
        headers_dir=headers_path, program_str=program_str
    )
    try:
        return subprocess.run(["gcc", "-c", temp_file_path])
    finally:
        shutil.rmtree(temp_dir)
