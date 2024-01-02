from .chains import repair_chain
from .sanitize import extract_c_program
from .wp import exec_wp


def repair(annotated_program, outputter, repair_step, headers_path, max_retries=5):
    if max_retries <= 0:
        raise ValueError("Maximum repair attempts reached.")

    if "```c" in annotated_program:
        annotated_program = extract_c_program(annotated_program)

    wp_result = exec_wp(annotated_program=annotated_program, headers_path=headers_path)
    if wp_result.returncode != 0:
        wp_output = wp_result.stdout
        repair_result = repair_chain.invoke(
            {"wp": wp_output, "program": annotated_program}
        )
        repaired_program = repair_result.get("text")
        outputter.output_repair(repaired_program)
        repair(
            annotated_program == repaired_program,
            outputter=outputter,
            repair_step=repair_step,
            max_retries=max_retries - 1,
            headers_path=headers_path,
        )
    return annotated_program
