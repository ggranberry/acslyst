from .chains import repair_chain
from .wp import exec_wp, extract_proofs_and_goals


def repair(annotated_program, outputter, repair_step, headers_path, max_retries=5):
    if max_retries <= 0:
        raise ValueError("Maximum repair attempts reached.")

    wp_result = exec_wp(annotated_program=annotated_program, headers_path=headers_path)
    wp_output = wp_result.stdout
    if wp_result.returncode != 0:
        repair_result = repair_chain.invoke(
            {"wp": wp_output, "program": annotated_program}
        )
        outputter.output_repair(repair_result)
        return repair(
            annotated_program == repair_result,
            outputter=outputter,
            repair_step=repair_step,
            max_retries=max_retries - 1,
            headers_path=headers_path,
        )
    else:
        proofs, goals = extract_proofs_and_goals(wp_output=wp_output)
        return annotated_program, proofs, goals
