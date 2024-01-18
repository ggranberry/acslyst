import re
import sys
from collections import Counter

def count_acsl_annotations(c_program):
    # Known annotations
    annotation_types = [
        'loop invariant', 'loop assigns', 'loop variant',
        'complete behaviors', 'disjoint behaviors',
        'requires', 'ensures', 'assigns',
        'behavior', 'assumes',
        'axiom', 'lemma', 'predicate', 'logic',
        'assert', 'ghost', 'typedef', 'variant', 'invariant'
    ]

    # Build the regular expression pattern for all known annotations
    known_annotation_pattern = r'@\s*(' + '|'.join(re.escape(at) for at in annotation_types) + r')\b'

    # Pattern to find annotation blocks
    annotation_pattern = r'/\*\@(.*?)\@*/'
    behavior_pattern = r'behavior\s+\w+\s*:(.*?)@'

    # Find all annotation blocks
    annotations = re.findall(annotation_pattern, c_program, re.DOTALL)

    counts = Counter()
    for annotation in annotations:
        # Count known annotations in the general block
        found_annotations = re.findall(known_annotation_pattern, annotation)
        counts.update(found_annotations)

        # Find and count annotations within behavior blocks
        behavior_blocks = re.findall(behavior_pattern, annotation, re.DOTALL)
        for block in behavior_blocks:
            found_annotations = re.findall(known_annotation_pattern, block)
            counts.update(found_annotations)

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
