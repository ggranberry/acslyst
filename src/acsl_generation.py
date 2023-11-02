from chains import acsl_generation_chain, pathcrawler_chain
from repair import repair
from pathcrawler import run_pathcrawler
from annotation_evaluator import AnnotationEvaluator


def exec_on_program(
    program_file: str, main_function=None, oracle_file=None, oracle_function=None
):
    with open(program_file) as file:
        content = file.read()

    print("generating ACSL annotations...")
    # First we generate 5 initial attempts to try and find a good starting point
    initial_generations = [
        acsl_generation_chain.invoke({"program": content}).get("text") for _ in range(5)
    ]
    evalulator = AnnotationEvaluator()
    ranked_results = list(
        map(lambda x: evalulator.evaluate_strings(prediction=x), initial_generations)
    )
    choice = max(ranked_results, key=lambda x: x["rank"])
    most_recent_program = choice["program"]

    print("validating...")
    most_recent_program = repair(most_recent_program, "initial acsl")
    print(most_recent_program)

    print("generating pathcrawler output...")
    csv = run_pathcrawler(most_recent_program)

    print("gaining new insight from pathcrawler output...")
    res = pathcrawler_chain.invoke({"csv": csv, "program": most_recent_program})
    print(res.get("text"))

if __name__ == "__main__":
    print("This script is being run directly.")
    exec_on_program("examples/Bsearch/f.c")
