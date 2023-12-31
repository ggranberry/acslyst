def extract_c_program(text):
    _, after = text.split("```c",1)
    return after.split("```")[0]

def extract_classification_count(text):
    _, after = text.split("###Classification",1)
    classifications_string = after.split("###")[0]
    classifications_lines = classifications_string.split("\n")
    classifications = {}
    for l in classifications_lines:
        if ":" not in l:
            continue
        name , count = l.split(":")
        classifications[name.strip()] = int(count)
    return classifications

def llm_output_parser(llm_output):
    program = extract_c_program(llm_output)
    classification_counts = extract_classification_count(llm_output)
    return program, classification_counts

