
def extract_c_program(text):
    _, after = text.split("```c",1)
    return after.split("```")[0]

def parse_annotated_c_program(llm_output):
    program = extract_c_program(llm_output)
    return program, llm_output

def parse_prolog_program(text):
    _, after = text.split("```prolog",1)
    return after.split("```")[0]
