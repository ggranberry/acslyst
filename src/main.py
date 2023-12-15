import argparse
from src.harnesses.pathcrawler_harness import PathCrawlerHarness

def main(args):
    # Your main function logic goes here
    if args.pathcrawler:
        harness = PathCrawlerHarness()
        harness.run()

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Generate ACSL annotations for a suite of C programs")

    # Add flags
    parser.add_argument('-p', '--pathcrawler', action='store_true', help='Generate for pathcrawler test suite')

    # Parse arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args)

