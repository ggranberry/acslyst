from .annotations import count_acsl_annotations

def extract_c_program(text):
    _, after = text.split("```c",1)
    return after.split("```")[0]

def llm_output_parser(llm_output):
    program = extract_c_program(llm_output)
    classification_counts = count_acsl_annotations(program)
    return program, classification_counts

