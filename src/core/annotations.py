import re
from collections import Counter

def count_acsl_annotations(c_program):
    # list of known ACSL annotations
    annotation_types = [
        'requires', 'ensures', 'assigns', 
        'loop invariant', 'loop assigns', 'loop variant', 
        'behavior', 'assumes', 'complete behaviors', 'disjoint behaviors',
        'axiom', 'lemma', 'predicate', 'logic',
        'assert', 'ghost', 'typedef', 'variant', 'invariant'
    ]

    # Regular expression patterns
    annotation_pattern = r'/\*\@(.*?)\@*/'
    generic_annotation_pattern = r'@\s*([\w\s]+?):'

    # Find all annotations in the C program
    annotations = re.findall(annotation_pattern, c_program, re.DOTALL)

    # Count each type of annotation
    counts = Counter()
    for annotation in annotations:
        found = False
        for annotation_type in annotation_types:
            if annotation_type in annotation:
                counts[annotation_type] += 1
                found = True

        # If no known type is found, check for unknown types
        if not found:
            other_annotations = re.findall(generic_annotation_pattern, annotation)
            for other in other_annotations:
                counts["other (" + other.strip() + ")"] += 1

    # Remove zero counts
    return {k: v for k, v in counts.items() if v > 0}
