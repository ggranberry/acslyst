from langchain.prompts import PromptTemplate

initial_prompt = PromptTemplate.from_template(
    """
You are a LLM that takes in a C program and returns an annotated C program. Find any non-redundant properties for the program and generate ACSL annotations (from the Frama-C framework). Annotate the program with the ACSL annotations that you find and return the annotated program. Returning a program with no annotation is not a valid solution. An annotation followed by another annotation should always be put into a block.

ANNOTATION EXAMPLES:

Examples 1 (single annotation):
/*@ requires low >= 0 && high <= 9; */

Example 2 (multiple annotations):
/*@ 
  @ requires low >= 0 && high <= 9;
  @ requires elem >= 0 && elem <= 9;
*/

Example 3 (loops):
/*@
  @ loop invariant low <= high;
  @ loop variant high - low;
*/
while(low <= high) 

Example 4 (loop assigns) (loop assigns must be placed before loop variant):
/*@
  @ loop invariant i >= 0 && i <= 3;
  @ loop assigns fa;
  @ loop variant 3 - i;
*/
while(low <= high) 

FORMAT INSTRUCTIONS:

Return the annotated c code wrapped in markdown
```c
...
```

Additionally count each annoataion type and provide a list which shows how often each type occurred and return the list in the format wrapped in "###Classification". Follow these examples:

###Classification
requires: 5
loop invariant: 2
ensures: 1
###
 
START OF INPUT:

```
{program}
```"""
)


repair_template = """You are an LLM that only returns code. You are attempting to fix invalid ACSL annotations that were previously added to a C program. You are also provided output from Frama-C's WP tool which describes a syntax error in the previously generated annotations. Use the output from Frama-C's WP tool to guide you in repairing the syntax errors in the annotations. Returning a program with no annotations is not a valid solution. Returning a program with no changes to the annotations it not a valid solution.

FORMAT INSTRUCTIONS:

Return the annotated c code wrapped in markdown
```c
...
```

START OF INPUT:

MOST RECENT WP OUTPUT:
{wp}

MOST RECENT PROGRAM:
{program}"""

repair_prompt = PromptTemplate(
    input_variables=["program", "wp"], template=repair_template
)

pathcrawler_template = """You are an LLM that only returns annotated code. You receive an existing C program that was annotated with with ACSL. Additionally you receive a CSV string which represents the output of Frama-C's PathCrawler tool on the provided program. If the verdict column contains the value "unknown", this means that an oracle hasn't been provided to classify the output. If an oracle was provided, it will also be provided as context. Use these inputs to modify the existing ACSL annotations if it seems helpful in understanding the program. Returning a program with no annotations is not a valid solution. Returning a program with no changes is a valid solution, but I want you to prioritize modifications.

FORMAT INSTRUCTIONS:

Return the annotated c code wrapped in markdown
```c
...
```

Additionally count each annoataion type and provide a list which shows how often each type occurred and return the list in the format wrapped in "###Classification". Follow these examples:

###Classification
requires: 5
loop invariant: 2
ensures: 1
###

START OF INPUT:
MOST RECENT PROGRAM:
```c
{program}
```

PathCrawler Output:
{csv}

Oracle (if provided):
{oracle}
"""

pathcrawler_prompt = PromptTemplate(
    input_variables=["program", "csv"], template=pathcrawler_template
)
