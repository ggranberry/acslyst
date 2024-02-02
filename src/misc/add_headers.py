import glob
import os

def prepend_include_to_specific_c_files(directory):
    # Pattern to match specific C files in the directory and its subdirectories
    pattern = os.path.join(directory, '**', 'initial_generation_*.c')

    # Use glob with recursive=True to find all matching files
    for file_path in glob.glob(pattern, recursive=True):
        with open(file_path, 'r+') as f:
            content = f.read()
            # Move back to the start of the file so we overwrite
            f.seek(0, 0)
            # Prepend the #include statement only if it's not already there
            if not content.startswith('#include <limits.h>'):
                f.write('#include <limits.h>\n' + content)

# Replace 'your/directory/path' with the path to your directory
directory_path = 'output/count_annotations_pathcrawler/third_run_headers/'
prepend_include_to_specific_c_files(directory_path)
