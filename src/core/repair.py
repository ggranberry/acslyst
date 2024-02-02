from .chains import repair_chain
from .wp import exec_wp


def repair(annotated_program, headers_path, main_method, max_retries=2, final_out=""):
    if max_retries <= 0:
        raise ValueError(final_out)

    wp_result, report = exec_wp(
        annotated_program=annotated_program,
        headers_path=headers_path,
        main_method=main_method,
    )
    wp_output = wp_result.stdout
    if wp_result.returncode != 0:
        print("repairing...")
        repair_result = repair_chain.invoke(
            {"wp": wp_output, "program": annotated_program}
        )
        return repair(
            main_method=main_method,
            annotated_program=repair_result,
            max_retries=max_retries - 1,
            headers_path=headers_path,
            final_out=wp_output
        )
    else:
        return annotated_program, report
