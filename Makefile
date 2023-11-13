# Simple makefile with a 'clean' target

# Define the output directory
OUTPUT_DIR = output

# Default target
all:
	python src/analyzer/analyze.py

# Clean target
clean:
	rm -rf $(OUTPUT_DIR)/*

