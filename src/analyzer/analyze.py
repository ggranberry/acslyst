from .exceptions import (
    LLMException,
    HeuristicException,
    RepairException,
    PathcrawlerException,
)
from .chains import acsl_generation_chain, pathcrawler_chain, precondition_chain, paramters_chain
from .repair import repair
from .pathcrawler import run_pathcrawler
from .annotation_evaluator import AnnotationEvaluator
from .output import Outputter


def generate_acsl(
    program_suite: str,
    program_name: str,
    program_file: str,
    main_function=None,
    oracle_file=None,
    unit_test_file=None,
    oracle_function=None,
    headers_path=None,
    params_file=None,
):
    outputter = Outputter(program_name, program_suite, oracle_file, unit_test_file)
    with open(program_file) as file:
        content = file.read()

    try:
        initial_generations = generate_initial(content)
    except Exception as e:
        outputter.output_exception(LLMException(e))
        return

    try:
        choice_program = rank(initial_generations, headers_path, outputter)
    except Exception as e:
        outputter.output_exception(HeuristicException(e))
        return

    try:
        repaired_choice_program = initial_repair(
            choice_program, headers_path, outputter
        )
    except Exception as e:
        outputter.output_exception(RepairException(e))
        return

    try:
        csv = generate_pathcrawler_csv(
            repaired_choice_program, main_function, oracle_file, headers_path
        )
    except Exception as e:
        outputter.output_exception(PathcrawlerException(e))
        return

    try:
        pathcrawler_program = generate_with_pathcrawler_csv(
            oracle_file, repaired_choice_program, csv, outputter, program_file
        )
    except Exception as e:
        outputter.output_exception(PathcrawlerException(e))
        return

    try:
        repaired_pathcrawler_program = pathcrawler_repair(
            pathcrawler_program, headers_path, outputter
        )
    except Exception as e:
        outputter.output_exception(RepairException(e))
        return

    outputter.output_final(repaired_pathcrawler_program)


def generate_preconditions_from_params(program, params_file):
    candidates = [
        precondition_chain.invoke({"program": program, "params": params_file})
    ]
    return [x for x in candidates if x is not None]


def generate_initial(content):
    # First we generate 5 initial attempts to try and find a good starting point
    initial_generations = [
        acsl_generation_chain.invoke({"program": content}) for _ in range(5)
    ]
    return [x for x in initial_generations if x is not None]


def rank(initial_generations, headers_path, outputter):
    # Then we evaluate the initial attempts and pick the best one
    evalulator = AnnotationEvaluator()

    ranked_results = list(
        map(
            lambda x: evalulator.evaluate_strings(
                prediction=x[0],
                classification_counts=x[1],
                headers_path=headers_path,
            ),
            initial_generations,
        )
    )
    # Output the initial attempts to files
    for idx, candidate in enumerate(ranked_results):
        outputter.output_candidate(candidate=candidate, idx=idx)

    # Pick the best one
    choice = max(ranked_results, key=lambda x: x["rank"])
    outputter.output_candidate(candidate=choice, idx=-1, is_choice=True)
    return choice["program"]


def initial_repair(choice_program, headers_path, outputter):
    # First round of repairs
    repaired_choice_program = repair(
        annotated_program=choice_program,
        outputter=outputter,
        headers_path=headers_path,
        repair_step="initial acsl",
    )

    # see how much we proved with our repaired program
    outputter.set_initial_wp_results(repaired_choice_program, headers_path=headers_path)

    return repaired_choice_program


def generate_pathcrawler_csv(
    repaired_choice_program, main_function, oracle_file, headers_path
):
    # Generate pathcrawler csv to use as context
    csv = run_pathcrawler(
        program_str=repaired_choice_program,
        main_function=main_function,
        oracle_file=oracle_file,
        headers_dir=headers_path,
    )
    return csv


def generate_with_pathcrawler_csv(
    oracle_file, repaired_choice_program, csv, outputter, program_file
):
    oracle_text = "Not provided"
    if oracle_file is not None:
        with open(program_file) as oracle_content:
            oracle_text = oracle_content.read()

    pathcrawler_program, pathcrawler_classifications = pathcrawler_chain.invoke(
        {"csv": csv, "program": repaired_choice_program, "oracle": oracle_text}
    )
    outputter.output_pathcrawler_program(
        pathcrawler_program, pathcrawler_classifications
    )
    return pathcrawler_program


def pathcrawler_repair(pathcrawler_program, headers_path, outputter):
    repaired_pathcrawler_program = repair(
        annotated_program=pathcrawler_program,
        outputter=outputter,
        headers_path=headers_path,
        repair_step="with pathcrawler context",
    )
    outputter.set_pathcrawler_wp_results(
        program=repaired_pathcrawler_program,
        headers_path=headers_path,
    )
    return repaired_pathcrawler_program


if __name__ == "__main__":
    name = "Alias3"
    generate_acsl(
        program_suite="pathcrawler_tests",
        program_name=name,
        program_file=f"programs/pathcrawler_tests/{name}/f.c",
        main_function="testme",
        # oracle_file=f"programs/pathcrawler_tests/{name}/OtherCfiles/oracle_testme.c",
        headers_path=f"programs/pathcrawler_tests/{name}/",
    )
