import argparse
from src.harnesses.pathcrawler_harness import PathCrawlerHarness
from src.experiments.count_annotations.count_annotations import count_annotations
from src.experiments.count_annotations_pathcrawler.count_annotations import count_annotations_pathcrawler

def main(args):
    # Your main function logic goes here

    harness = PathCrawlerHarness()
    experiment = count_annotations
    model = "openai"

    for suite in args.suite:
        if suite == "pathcrawler_tests":
            harness = PathCrawlerHarness()
            if args.suite in ["formati", "svcomp", "industrial"]:
                raise Exception(f"Unsupported suite: {args.suite}")

    if args.experiment == "count":
        experiment = count_annotations
    elif args.experiment == "count_pathcrawler":
        experiment = count_annotations_pathcrawler
    else:
        raise Exception(f"Invalid experiment name: {args.experiment}")

    if args.model == "openai" or args.model == "gemini":
        model = args.model
    else:
        raise Exception(f"Invalid model name: {args.model}")

    harness.run(experiment)

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Generate ACSL annotations for a suite of C programs")

    # Add flags with restrictions
    parser.add_argument('-s', '--suite', nargs='+', required=True, help='Specify the test suites: pathcrawler_tests, formai, svcomp, industrial', choices=["pathcrawler_tests", "formai", "svcomp", "industrial"])
    parser.add_argument('-e', '--experiment', required=True, help='Specify the experiment: count, count_pathcrawler', choices=["count", "count_pathcrawler"])
    parser.add_argument('-m', '--model', required=True, help='Specify the model: openai, gemini', choices=["openai", "gemini"])

    # Parse arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args)

