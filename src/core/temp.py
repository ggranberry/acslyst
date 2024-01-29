import os, glob, shutil
import tempfile

def setup_wp_tmp(headers_dir, program_str):
    temp_dir = __create_tmp_dir()
    temp_file_path = os.path.join(temp_dir, "temp.c")

    with open(temp_file_path, "w") as tmp:
        tmp.write(program_str)
    __copy_headers(headers_dir, temp_dir)
    return temp_file_path, temp_dir

def setup_pathcrawler_tmp(
    headers_dir,
    program_str,
    tmp_file_name,
    precond_str=None,
    precond_file_name=None,
):
    temp_dir = __create_tmp_dir()
    temp_file_path = os.path.join(temp_dir, tmp_file_name)

    with open(temp_file_path, "w") as tmp:
        tmp.write(program_str)

    __copy_headers(headers_dir, temp_dir)
    

    if precond_str is not None and precond_file_name is not None:
        c_precond_file_path = os.path.join(temp_dir, precond_file_name)
        with open(c_precond_file_path, "w") as c_pre:
            c_pre.write(precond_str)

    return temp_file_path, temp_dir

def __create_tmp_dir():
    base_temp_dir = os.path.join(os.getcwd(), "temp_files")
    os.makedirs(base_temp_dir, exist_ok=True)
    temp_dir = tempfile.mkdtemp(dir=base_temp_dir)
    return temp_dir

def __copy_headers(headers_dir: str, temp_dir: str):
    headers_dir_files = os.path.join(headers_dir, "*")

    # Copy all the files from the headers_dir into the tmp dir
    for file in glob.glob(headers_dir_files):
        if os.path.isfile(file):
            shutil.copy(file, temp_dir)

