import argparse
from src.experiments.count_annotations_eva.count_annotations import (
    count_annotations_eva,
)
from src.harnesses.pathcrawler_harness import PathCrawlerHarness
from src.experiments.count_annotations.count_annotations import count_annotations
from src.experiments.count_annotations_pathcrawler.count_annotations import (
    count_annotations_pathcrawler,
)
from src.experiments.evaluate_pathcrawler.evaluate_annotations import (
    evaluate_annotations_pathcrawler,
)
import os


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
    elif args.experiment == "count_eva":
        experiment = count_annotations_eva
    elif args.experiment == "evaluate_pathcrawler":
        if (
            not hasattr(args, "annotations_output_dir")
            or not args.annotations_output_dir
        ):
            raise Exception(
                "The 'annotations_output_dir' argument is required for the 'evaluate_pathcrawler' experiment."
            )
        if not os.path.isdir(args.annotations_output_dir):
            raise Exception(
                f"The specified directory does not exist: {args.annotations_output_dir}"
            )
        harness = PathCrawlerHarness(args.annotations_output_dir)
        experiment = evaluate_annotations_pathcrawler
    else:
        raise Exception(f"Invalid experiment name: {args.experiment}")

    if args.model == "openai" or args.model == "gemini":
        model = args.model
    else:
        raise Exception(f"Invalid model name: {args.model}")

    harness.run(experiment)


if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Generate ACSL annotations for a suite of C programs"
    )

    # Add flags with restrictions
    parser.add_argument(
        "-s",
        "--suite",
        nargs="+",
        required=True,
        help="Specify the test suites: pathcrawler_tests, formai, svcomp",
        choices=["pathcrawler_tests", "formai", "svcomp"],
    )
    parser.add_argument(
        "-e",
        "--experiment",
        required=True,
        help="Specify the experiment: count, count_pathcrawler, count_eva, evaluate_pathcrawler, evaluate_wp",
        choices=[
            "count",
            "count_pathcrawler",
            "count_eva",
            "evaluate_pathcrawler",
            "evaluate_wp",
        ],
    )
    parser.add_argument(
        "-m",
        "--model",
        required=True,
        help="Specify the model: openai, gemini",
        choices=["openai", "gemini"],
    )

    # Optionally add the annotations_output_dir argument
    # It will be checked for existence later if necessary
    parser.add_argument(
        "-o",
        "--annotations_output_dir",
        help="Specify the output directory for annotations (required for evaluate_pathcrawler)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args)
