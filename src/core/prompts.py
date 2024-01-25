from langchain.prompts import PromptTemplate

initial_prompt = PromptTemplate.from_template(
    """You are a LLM that takes the following inputs and returns a C program annotated with ACSL annotations.
1. A C program with no ACSL annotations

GOALS:
1. Describe any abstract properties that could be represented as ACSL annotations
2. Generate ACSL annotations based on your analysis of the program
3. Returning a program with no annotation is not a valid solution
4. Do not edit the C code, only add annotations

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

parameters_prompt = PromptTemplate.from_template(
    """You are an LLM that edits prolog files. You are given
- a C program annotated with ACSL
- a prolog file used to generate input parameters for a C program

Steps:
1. Identify the preconditions defined in the ACSL annotations of the c program. 
    a. They are defined as "requires" clauses (e.g. /*@ requires x > 0 */)
    b. List dimensions are defined with the "valid" keyword clauses (e.g. /*@ requires \\valid(x+10 */)
    c. Quantified expressions are defined with the "forall" keyword clauses (e.g. /*@ requires \\forall int i; 0 <= i < 10 ==> x[i] > 0 */)

2. Edit the prolog file to generate input parameters that satisfy the preconditions defined in the ACSL annotations of the c program
    a. For list variable instantiations, make sure that the dimension is big enough (e.g. create_input_val(dim('tab'),int([0..9]),Ins) will create a list of size up to 10)
    b. Don't use integer values that are too large or too small. For example use the dimensions [0..99] rather than [-2147483648..2147483647]
    c. Don't try to perform arithmetic or comparisons in the variable instantitiations. Instead create a quantified/unquantified condition if you need to
    d. To create unquanfified expressions, use the "unquantif_preconds" function like below  which assures that the list called tab is at least size 3 and also larger than x and y
        unquantif_preconds('testme', [
            c(supegal, dim('tab'),3,  pre),
            c(supegal, dim('tab'), 'x', pre),
            c(supegal, dim('tab'), 'y', pre)
        ]).
    e. To create quantified expressions, use the "quantif_preconds" function like below which specifies that for all indicies greater than or equal to 1, the value at index I is greater than the value at index I - 1
        quantif_preconds('testme', 
            [Index],[c(supegal,Index,1,pre)],
            supegal,
            e('tab',I),
            e('tab',I – 1)),
            pre)
        ]).
    f. Addition and subtraction operation are handled using the <operator>(i(math)<val1>,<val2>) syntax in quantified/unquantified preconditions. For example the following qunatified precond states that for all UQV1 where UQV1 is greater than or equal to 1, the element at A[UQV1] >= A[UQV1 - 1].
        quantif_preconds('testme',[uq_cond([UQV1],
                                   [c(supegal,UQV1,1,pre)],
                                   supegal,
                                   e('A',UQV1),
                                   e('A',-(i(math),UQV1,1)),
                                   pre)]).

    g. The conditional operators are as fallows: inf|infegal|sup|supegal|egal|diff 
    h. Accessing an element of an Array in quantified/unquantified preconditions is done using the e('<variable>', <idx>) syntax
    i. Do not use macros like INT_MAX or INT_MIN for ranges

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
)


example_c_precond_fn = """int Merge_precond(int t1[], int t2[], int t3[], int l1, int l2) '{
    if ( l1 > pathcrawler_dimension(t1)
    || l2 > pathcrawler_dimension(t2)
    || l1+l2 > pathcrawler_dimension(t3)) {
        return 0;
    }
    int i;
    for (i=1; i < l1; i++) {
        if (t1[i-1] > t1[i]) {
            return 0;
        }
    }
    for (i=1; i < l2; i++) {
        if (t2[i-1] > t2[i]) {
            return 0;
        }
    }
    return 1;
}"""


parameters_c_prompt = PromptTemplate.from_template(
    """You are an LLM prodcuces a C function. You are given
- A C program edited with ACSL annotations

GOALS
1. Identify the preconditions defined in the ACSL annotations of the c program. 
    a. They are defined as "requires" clauses (e.g. /*@ requires x > 0 */)
    b. List dimensions are defined with the "valid" keyword clauses (e.g. /*@ requires \\valid(x+10 */)
    c. Quantified expressions are defined with the "forall" keyword clauses (e.g. /*@ requires \\forall int i; 0 <= i < 10 ==> x[i] > 0 */)
2. Describe all of the preconditions you identified in the ACSL
3. Produce a C function called {main}_precond that uses C logic to check if given input parameters satisfy the preconditions describes above
    a. it returns a nonzero value if the input respects the preconditions, and zero otherwise
    b. {main}_precond should have the same function parameters (both name and type) as the {main} function in the provided program.
    c. The patchcrawler_dimension(<some array>) function which gives the number of elements in input arrays

EXAMPLE:
```c
{c_preconds}
```

FORMAT INSTRUCTIONS
Return the C function wrapped in markdown
```c
...
```

START OF INPUT:
C PROGRAM:
```c
{program}
```
                                                   """,
    partial_variables={"c_preconds": example_c_precond_fn},
)

# preconditions_template = """You are a LLM that takes the following inputs and returns a Prolog file
# - a c program annotated wtih ACSL
# - a prolog file used to generate input parameters for a c program
#
# Goals:
# 1. Analyze the inputs and preconditions defined in the prolog file
#     a. Pay specific attention to domains and qualified/unqualified preconditions
#     b. create variable statements such as "create_input_val('n',int([2..4]),Ins)" should not be treated as preconditions, but they might be instructive in understanding the program.
# 2. Edit the C program to include ACSL preconditions
#     a. Your main goal is to set sensible preconditions for the program
#     b. The prolog file should be used as a guide to help you understand the program, but not the source of truth for preconditions
#
# FORMAT INSTRUCTIONS:
#
# Return the annotated c code wrapped in markdown
# ```c
# ...
# ```
#
# START OF INPUT:
#
# C PROGRAM:
# ```c
# {program}
# ```
#
# PARAMETERS FILE:
# ```prolog
# {parameters}
# ```"""
#
# preconditions_prompt = PromptTemplate(
#     input_variables=["program", "parameters"], template=preconditions_template
# )


generate_with_pathcrawler_prompt = PromptTemplate.from_template(
    """You are a LLM that takes the following inputs and returns a C program annotated with ACSL annotations.
1. A C program with no ACSL annotations
2. A possibly empty CSV file that represents test runs performed by Frama-C pathcrawler

GOALS:
1. Analyze the pathcrawler CSV and describe any patterns that you see that could help you understand the behaviors of the program based on given input/output pairs
2. Describe how these behaviors could be used into creating ACSL annotations
3. Generate ACSL annotations based on your analysis of the program and take special account of the properties described when analyzing the Pathcrawler CSV file
4. Returning a program with no annotation is not a valid solution
5. Do not edit the C code, only add annotations

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

START OF INPUT:

Program:
```c
{program}
```

PathCrawler Output:
{csv}
```"""
)

generate_with_eva_prompt = PromptTemplate.from_template(
    """You are a LLM that takes the following inputs and returns a C program annotated with ACSL annotations.
1. A C program with optional ACSL annotations
2. A report from the Eva static analysis tool from Frama-C

GOALS:
1. Analyze the Eva report and describe how the results could be used in generating ACSL annotations
2. Generate ACSL annotations based on your analysis of the program and take special account of the properties described when analyzing the Eva report
3. Returning a program with no annotation is not a valid solution
4. Do not edit the C code, only annotations

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

START OF INPUT:

Program:
```c
{program}
```

Eva Report:
{eva}
```"""
)
