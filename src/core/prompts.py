from langchain.prompts import PromptTemplate

initial_prompt = PromptTemplate.from_template(
    """
You are a LLM that takes in a C program and returns an annotated C program. Find any non-redundant properties for the program and generate ACSL annotations (from the Frama-C framework). Annotate the program with the ACSL annotations that you find and return the annotated program. Returning a program with no annotation is not a valid solution. An annotation followed by another annotation should always be put into a block. Do not edit the C code. Only add annotations.

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

```c
{program}
```"""
)


repair_template = """You are an LLM that only returns code. You are attempting to fix invalid ACSL annotations that were previously added to a C program. You are also provided output from Frama-C's WP tool which describes a syntax error in the previously generated annotations. Use the output from Frama-C's WP tool to guide you in repairing the syntax errors in the annotations. Returning a program with no annotations is not a valid solution. Returning a program with no changes to the annotations it not a valid solution. Do not edit the C code. Only edit the annotations.

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

pathcrawler_template = """You are an LLM that only returns annotated code. You receive an existing C program that was annotated with with ACSL. Additionally you receive a CSV string which represents the output of Frama-C's PathCrawler tool on the provided program. If the verdict column contains the value "unknown", this means that an oracle hasn't been provided to classify the output. If an oracle was provided, it will also be provided as context. Use these inputs to modify the existing ACSL annotations if it seems helpful in understanding the program. Returning a program with no annotations is not a valid solution. Returning a program with no changes is a valid solution, but I want you to prioritize modifications. Do not edit the C code. Only edit the annotations.


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
    input_variables=["program", "csv", "oracle"], template=pathcrawler_template
)

parameters_template = """You are an LLM that edits prolog files. You are given
- a c program annotated with ACSL
- a prolog file used to generate input parameters for a c program

Steps:
    1. Identify the preconditions defined in the ACSL annotations of the c program. 
        a. They are defined as "requires" clauses (e.g. /*@ requires x > 0 */)
        b. List dimensions are defined with the "valid" keyword clauses (e.g. /*@ requires \\valid(x+10 */)
        c. Quantified expressions are defined with the "forall" keyword clauses (e.g. /*@ requires \\forall int i; 0 <= i < 10 ==> x[i] > 0 */)

    2. Edit the prolog file to generate input parameters that satisfy the preconditions defined in the ACSL annotations of the c program
        a. For list variable instantiations, make sure that the dimension is big enough (e.g. create_input_val(dim('tab'),int([0..9]),Ins) will create a list of size up to 10)
        b. To create unquanfified expressions, use the "unquantif_preconds" function like below  which assures that the list called tab is at least size 3 and also larger than x and y
            unquantif_preconds('testme', [
                c(supegal, dim('tab'),3,  pre),
                c(supegal, dim('tab'), 'x', pre),
                c(supegal, dim('tab'), 'y', pre)
            ]).
        c. To create quantified expressions, use the "quantif_preconds" function like below which specifies that for all indicies greater than or equal to 1, the value at index I is greater than the value at index I - 1
            quantif_preconds('testme', 
                [Index],[c(supegal,Index,1,pre)],
                supegal,
                e('tab',I),
                e('tab',I – 1)),
                pre)
            ]).
        d. The conditional operators are as fallows: inf|infegal|sup|supegal|egal|diff 

FORMAT INSTRUCTIONS:

Return the annotated prolog code wrapped in markdown
```prolog
...
```

START OF INPUT:

C PROGRAM:
{program}

PARAMETERS FILE:
{parameters}"""

parameters_prompt = PromptTemplate(
    input_variables=["program", "parameters"], template=parameters_template
)

preconditions_template = """You are an LLM that edits C program files. You are given the following
- a c program possibly anootated with ACSL
- a prolog file used to generate input parameters for a c program

Steps:
    1. Analyze the inputs and preconditions defined in the prolog file
        a. Pay specific attention to domains and qualified/unqualified preconditions
        b. create variable statements such as "create_input_val('n',int([2..4]),Ins)" should not be treated as preconditions, but they might be instructive in understanding the program.
    2. Edit the C program to include ACSL preconditions
        a. Your main goal is to set sensible preconditions for the program
        b. The prolog file should be used as a guide to help you understand the program, but not the source of truth for preconditions

FORMAT INSTRUCTIONS:

Return the annotated c code wrapped in markdown
```c
...
```

START OF INPUT:

C PROGRAM:
```c
{program}
```

PARAMETERS FILE:
```prolog
{parameters}
```"""

preconditions_prompt = PromptTemplate(
    input_variables=["program", "parameters"], template=preconditions_template
)


generate_with_pathcrawler_prompt= PromptTemplate.from_template(
    """You are a LLM that takes the following inputs and returns a C program annotated with ACSL annotations.
1. A C program with no ACSL annotations
2. A CSV file the represents test runs performed by Frama-C pathcrawler

GOALS:
1. Analyze both the pathcrawler output as well as the program itself
2. Find any non-redundant properties for the program and annotate the program with the generated annotations
3. Returning a program with no annotation is not a valid solution
4. No not edit the C code, only add annotations

ANNOTATION EXAMPLES:

Example 1 (single annotation):
/*@ requires low >= 0 && high <= 9; */

Example 2 (multiple annotations):
/*@ 
  @ requires low >= 0 && high <= 9;
  @ requires elem >= 0 && elem <= 9;
*/

Example 3 (loops)(loop annotations must be placed before a loop and NOT above the function body):
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

Program:
```c
{program}
```

PathCrawler Output:
{csv}
```"""
)

