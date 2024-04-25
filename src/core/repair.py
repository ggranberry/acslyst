from .chains import repair_chain, repair_eva_chain, gcc_repair_chain 
from .wp import exec_wp
from .eva import run_eva
from .gcc import compile_program


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
            final_out=wp_output,
        )
    else:
        return annotated_program, report


def repair_eva(
    annotated_program, headers_path, main_method, max_retries=2, final_out=""
):
    if max_retries <= 0:
        raise ValueError(final_out)

    res, report = run_eva(
        program_str=annotated_program,
        headers_dir=headers_path,
        main_function=main_method,
    )
    eva_output = res.stdout
    if res.returncode != 0:
        print("repairing...")
        repair_result = repair_eva_chain.invoke(
            {"eva": eva_output, "program": annotated_program}
        )
        return repair_eva(
            main_method=main_method,
            annotated_program=repair_result,
            max_retries=max_retries - 1,
            headers_path=headers_path,
            final_out=eva_output,
        )
    else:
        return annotated_program, report, eva_output


# Repair function for unannotated programs that only checks if something compiles
def repair_compile(
    headers_path, mutated_program, max_retries=2, final_out=""
):
    if max_retries <= 0:
        raise ValueError(final_out)

    result = compile_program(mutated_program, headers_path)
    compile_output = result.stdout
    if result.returncode != 0:
        print("repairing...")
        repair_result, _ = gcc_repair_chain.invoke(
            {"gcc": compile_output, "program": mutated_program}
        )
        return repair_compile(
            headers_path=headers_path,
            mutated_program= repair_result,
            max_retries=max_retries - 1,
            final_out=result,
        )
    else:
        return mutated_program 
