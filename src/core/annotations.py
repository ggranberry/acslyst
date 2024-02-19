import re
import sys
from collections import Counter
import clang.cindex

clang.cindex.Config.set_library_file("/usr/lib/llvm-16/lib/libclang-16.so")
import pkg_resources


# Known annotations - behaviors are handled differently
annotation_types = [
    "loop invariant",
    "loop assigns",
    "loop variant",
    "complete behaviors",
    "disjoint behaviors",
    "requires",
    "ensures",
    "assigns",
    "assumes",
    "axiom",
    "lemma",
    "predicate",
    "logic",
    "assert",
    "ghost",
    "typedef",
    "variant",
    "invariant",
]


def extract_comments_from_function(file_path, function_name):
    # Initialize Clang index
    index = clang.cindex.Index.create()

    # Parse the source file
    tu = index.parse(file_path)

    # Find the desired function definition in the AST
    for node in tu.cursor.walk_preorder():
        if (
            node.kind == clang.cindex.CursorKind.FUNCTION_DECL
            and node.spelling == function_name
        ):
            # Found the function, now extract comments from its body
            comments = []
            tokens = node.get_tokens()  # Get all tokens in the function body
            for token in tokens:
                if token.kind == clang.cindex.TokenKind.COMMENT:
                    comments.append(token.spelling)
            return comments

    return None


def count_acsl_annotations(c_program):
    counts = Counter()

    annotation_block_pattern = r"/\*\@(.*?)\*/"
    single_line_annotation_pattern = r"//@\s*(.*?)\s*(?:\n|$)"

    # find all single line annotations
    single_line_annotations = re.findall(single_line_annotation_pattern, c_program)
    for stm in single_line_annotations:
        match = re.search(
            r"\b(" + "|".join(re.escape(at) for at in annotation_types) + r")\b",
            stm,
        )
        if match:
            counts[match.group(1)] += 1

    # Find all annotation blocks
    annotation_blocks = re.findall(annotation_block_pattern, c_program, re.DOTALL)
    for block in annotation_blocks:
        # Extract and count behavior lines
        behavior_lines = re.findall(r"behavior\s+\w+\s*: *\n", block)
        for _ in behavior_lines:
            counts["behavior"] += 1  # Increment count for "behavior"

        # Split the block into statements based on ';'
        statements = re.split(r";(?:\s*//.*)? *\n", block)
        for statement in statements:
            # Extract the first keyword from each statement
            match = re.search(
                r"\b(" + "|".join(re.escape(at) for at in annotation_types) + r")\b",
                statement,
            )
            if match:
                counts[match.group(1)] += 1

    return {k: v for k, v in counts.items() if v > 0}


def main(filename):
    comments = extract_comments_from_function(filename, "testme")
    print(comments)
    return
    try:
        with open(filename, "r") as file:
            c_program = file.read()
            counts = count_acsl_annotations(c_program)
            print(f"ACSL Annotation Counts for {filename}:")
            for annotation, count in counts.items():
                print(f"  {annotation}: {count}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    main(filename)
