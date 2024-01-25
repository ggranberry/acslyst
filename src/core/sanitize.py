from .annotations import count_acsl_annotations

def extract_c_program(text):
    _, after = text.split("```c",1)
    return after.split("```")[0]

def parse_annotated_c_program(llm_output):
    program = extract_c_program(llm_output)
    classification_counts = count_acsl_annotations(program)
    return program, classification_counts

def parse_prolog_program(text):
    _, after = text.split("```prolog",1)
    return after.split("```")[0]
