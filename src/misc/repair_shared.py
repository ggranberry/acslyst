import os

def check_repaired_version_exists(file_path):
    # Check if the file path has a "_repaired" version
    dir_path, filename = os.path.split(file_path)
    base, ext = os.path.splitext(filename)
    repaired_filename = f"{base}_repaired{ext}"
    repaired_file_path = os.path.join(dir_path, repaired_filename)
    exists = os.path.exists(repaired_file_path)
    return exists, repaired_file_path
