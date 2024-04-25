import re
from pathlib import Path
from collections import Counter
import clang.cindex
clang.cindex.Config.set_library_file("/usr/lib/llvm-16/lib/libclang-16.so")
from src.misc.repair_shared import check_repaired_version_exists


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


def extract_function_body_comments(file_path):
    index = clang.cindex.Index.create()
    tu = index.parse(file_path)
    comments = []
    for node in tu.cursor.walk_preorder():
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            tokens = node.get_tokens()  # Get all tokens in the function body
            for token in tokens:
                if token.kind == clang.cindex.TokenKind.COMMENT:
                    comments.append(token.spelling)

    return comments


def extract_comments(c_file_path):
    index = clang.cindex.Index.create()
    ast = index.parse(c_file_path)
    comments = []
    for token in ast.cursor.get_tokens():
        if token.kind == clang.cindex.TokenKind.COMMENT:
            comments.append(token.spelling)
    return comments


def count_acsl_annotations(comments):
    counts = Counter()
    annotation_block_pattern = r"/\*\@(.*?)\*/"

    # Process single-line annotations
    for comment in comments:
        if comment.startswith("//@"):
            match = re.search(
                r"\b(" + "|".join(re.escape(at) for at in annotation_types) + r")\b",
                comment,
            )
            if match:
                counts[match.group(1)] += 1

    # Process annotation blocks
    for comment in comments:
        if comment.startswith("/*@"):
            block_matches = re.findall(annotation_block_pattern, comment, re.DOTALL)
            for block in block_matches:
                behavior_lines = re.findall(r"behavior\s+\w+\s*: *\n", block)
                for _ in behavior_lines:
                    counts["behavior"] += 1

                statements = re.split(r";(?:\s*//.*)? *\n", block)
                for statement in statements:
                    match = re.search(
                        r"\b("
                        + "|".join(re.escape(at) for at in annotation_types)
                        + r")\b",
                        statement,
                    )
                    if match:
                        counts[match.group(1)] += 1

    return {k: v for k, v in counts.items() if v > 0}

def process_directory(directory_path, function_bodies_only = False):
    # Compile the file name pattern for matching
    pattern = re.compile(r"initial_generation_\d+\.c$")
    
    # Initialize a counter to hold counts across all files
    total_counts = Counter()

    # Walk through the directory and its subdirectories
    for path in Path(directory_path).rglob('*'):
        if path.is_file() and pattern.search(path.name):
            repaired_exists, repaired_file_path = check_repaired_version_exists(path)
            if repaired_exists:
                path = repaired_file_path
            if function_bodies_only:
                comments = extract_function_body_comments(str(path))
            else:
                comments = extract_comments(str(path))
            counts = count_acsl_annotations(comments)
            total_counts += counts

    return total_counts

if __name__ == "__main__":
    plain_dir = "output/count_annotations/3_generations"
    pc_dir = "output/count_annotations_pathcrawler/third_run_headers"
    eva_dir = "output/count_annotations_eva/backup_first_run"

    plain_annotations = process_directory(plain_dir)
    print("Plain annotations:", plain_annotations)

    pc_annotations = process_directory(pc_dir)
    print("PC annotations:", pc_annotations)

    eva_annotations = process_directory(eva_dir)
    print("Eva annotations:", eva_annotations)


    plain_annotations = process_directory(plain_dir, True)
    print("Plain body annotations:", plain_annotations)

    pc_annotations = process_directory(pc_dir, True)
    print("PC body annotations:", pc_annotations)

    eva_annotations = process_directory(eva_dir, True)
    print("Eva body annotations:", eva_annotations)
