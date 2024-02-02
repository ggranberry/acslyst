import os
import re

def remove_comments(source_string):
    """Remove C-style comments from a string."""
    pattern = r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
    return re.sub(pattern, '', source_string)

def process_file(file_path):
    """Process a single file to remove comments."""
    with open(file_path, 'r') as file:
        content = file.read()
        content_no_comments = remove_comments(content)

    with open(file_path, 'w') as file:
        file.write(content_no_comments)

def main(directory):
    """Walk through the directory and process each 'f.c' file."""
    print("walking")
    for root, dirs, files in os.walk(directory):
        print(files, root, dirs)
        for file in files:
            print("file", file)
            if file == 'f.c':
                print("found")
                full_path = os.path.join(root, file)
                process_file(full_path)
                print(f"Processed {full_path}")

if __name__ == "__main__":
    directory = 'programs/pathcrawler_tests'  # Path to the 'programs' directory
    main(directory)
