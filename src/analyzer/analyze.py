from exceptions import (
    LLMException,
    HeuristicException,
    RepairException,
    PathcrawlerException,
)
from chains import acsl_generation_chain, pathcrawler_chain 
from repair import repair
from pathcrawler import run_pathcrawler
from annotation_evaluator import AnnotationEvaluator
from output import Outputter


def generate_acsl(
    program_suite: str,
    program_name: str,
    program_file: str,
    main_function=None,
    oracle_file=None,
    oracle_function=None,
):
    outputter = Outputter(program_name, program_suite)
    with open(program_file) as file:
        content = file.read()

    try:
        print("generating ACSL annotations...")
        # First we generate 5 initial attempts to try and find a good starting point
        initial_generations = [
            acsl_generation_chain.invoke({"program": content}) for _ in range(5)
        ]
        initial_generations = [x for x in initial_generations if x is not None]
    except Exception as e:
        outputter.output_exception(LLMException(e))
        return

    try:
        # Then we evaluate the initial attempts and pick the best one
        evalulator = AnnotationEvaluator()
        
        ranked_results = list(
            map(
                lambda x: evalulator.evaluate_strings(
                    prediction=x[0], classification_counts=x[1]
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
        choice_program = choice["program"]

        # see how much we proved with our repaired program
        outputter.set_wp_results(choice_program, "initial")

    except Exception as e:
        outputter.output_exception(HeuristicException(e))
        return

    try:
        # First round of repairs
        print("validating...")
        repaired_choice_program = repair(choice_program, outputter, "initial acsl")
    except Exception as e:
        outputter.output_exception(HeuristicException(e))
        return

    try:
        # Generate pathcrawler csv to use as context
        print("generating pathcrawler output...")
        csv = run_pathcrawler(repaired_choice_program, main_function, oracle_file)
        outputter.output_pathcrawler_csv(csv)
    except Exception as e:
        outputter.output_exception(PathcrawlerException(e))
        return

    try:
        print("gaining new insight from pathcrawler output...")
        oracle_text = "Not provided"
        if oracle_file is not None:
            with open(program_file) as oracle_content:
                oracle_text = oracle_content.read()

        pathcrawler_program , pathcrawler_classifications = pathcrawler_chain.invoke(
            {"csv": csv, "program": repaired_choice_program, "oracle": oracle_text}
        )
        outputter.output_pathcrawler_program(pathcrawler_program, pathcrawler_classifications)
    except Exception as e:
        outputter.output_exception(PathcrawlerException(e))
        return

    try:
        print("validating...")
        repaired_pathcrawler_program = repair(
            pathcrawler_program, outputter, "with pathcrawler context"
        )
        outputter.set_wp_results(repaired_pathcrawler_program, "pathcrawler")
    except Exception as e:
        outputter.output_exception(RepairException(e))
        return

    outputter.output_final(repaired_pathcrawler_program)


if __name__ == "__main__":
    name = "Bsearch"
    generate_acsl(
        program_suite="pathcrawler_tests",
        program_name=name,
        program_file=f"programs/pathcrawler_tests/{name}/f.c",
        main_function="testme",
        oracle_file=f"programs/pathcrawler_tests/{name}/OtherCfiles/oracle_testme.c",
    )
