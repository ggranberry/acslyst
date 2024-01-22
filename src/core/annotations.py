import re
import sys
from collections import Counter

def count_acsl_annotations(c_program):
    # Known annotations - behaviors are handled differently
    annotation_types = [
        'loop invariant', 'loop assigns', 'loop variant',
        'complete behaviors', 'disjoint behaviors',
        'requires', 'ensures', 'assigns', 'assumes',
        'axiom', 'lemma', 'predicate', 'logic',
        'assert', 'ghost', 'typedef', 'variant', 'invariant'
    ]

    annotation_block_pattern = r'/\*\@(.*?)\*/'

    # Find all annotation blocks
    annotation_blocks = re.findall(annotation_block_pattern, c_program, re.DOTALL)

    counts = Counter()
    for block in annotation_blocks:
        # Extract and count behavior lines
        behavior_lines = re.findall(r'behavior\s+\w+\s*: *\n', block)
        for _ in behavior_lines:
            counts['behavior'] += 1  # Increment count for "behavior"

        # Split the block into statements based on ';'
        # statements = re.split('; *\n', block)
        statements = re.split(r';(?:\s*//.*)? *\n', block)
        for statement in statements:
            # Extract the first keyword from each statement
            match = re.search(r'\b(' + '|'.join(re.escape(at) for at in annotation_types) + r')\b', statement)
            if match:
                counts[match.group(1)] += 1

    return {k: v for k, v in counts.items() if v > 0}

def main(filename):
    try:
        with open(filename, 'r') as file:
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
