from langchain.prompts import PromptTemplate

from .prompts_examples import valid_assigns, invalid_assigns


initial_prompt = PromptTemplate.from_template(
    """You are a LLM that takes the following inputs and returns a C program annotated with ACSL annotations.

Inputs:
1. A C program with no ACSL annotations

GOALS:
1. Describe any abstract properties that could be represented as ACSL annotations
2. Generate ACSL annotations based on your analysis of the program
3. Returning a program with no annotation is not a valid solution
4. Do not edit the C code, only add annotations
5. Make sure to describe your thought process behind the annotations
6. Do not skip any code in the returned solution to make it shorter.
7. If you break any of these rules then my family will disown me.

ANNOTATION EXAMPLES:

Examples 1 (single annotation):
/*@ requires low >= 0 && high <= 9; */

Example 2 (block annotation style):
//Only use this style for function headers. Do not use blocks for multiple annoations in the function body
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

Example 5 (assigns must be in scope):
//This is VALID because x is a parameter that the function contract can see
{valid_assigns}

// this is NOT VALID because x is in the function body and can not be seen by the contract
{invalid_assigns}


FORMAT INSTRUCTIONS:

First describe your reasoning behind the added annotations

Return the annotated c code wrapped in markdown
```c
...
```
 
START OF INPUT:

```c
{program}
```""",
    partial_variables={
        "valid_assigns": valid_assigns,
        "invalid_assigns": invalid_assigns,
    },
)


repair_template = """You are an LLM that edits C files annotated with ACSL. You are given
- A C program with ACSL annotations
- The most recent output from Frama-C's WP tool which describes a syntax error in the previously generated annotations

STEPS:
    1. Describe the syntax error explained by WP
    2. Edit the ACSL annotations to fix the syntax error described by WP
    3. Do not edit the C code. Only edit the annotations
    4. Returning a program with no annotations or no changes to the annotations is not a valid solution

FORMAT INSTRUCTIONS:

Return the annotated c code wrapped in markdown
```c
...
```

START OF INPUT:

MOST RECENT WP OUTPUT:
{wp}

MOST RECENT PROGRAM:
```c
{program}
```
"""

repair_prompt = PromptTemplate(
    input_variables=["program", "wp"], template=repair_template
)

repair_eva_prompt = PromptTemplate.from_template(
    """
You are an LLM that edits C files annotated with ACSL. You are given
- A C program with ACSL annotations
- The most recent output from Frama-C's Eva tool which describes a syntax error in the previously generated annotations

STEPS:
    1. Describe the syntax error explained by Eva
    2. Edit the ACSL annotations to fix the syntax error described by Eva
    3. Do not edit the C code. Only edit the annotations
    4. Returning a program with no annotations or no changes to the annotations is not a valid solution

FORMAT INSTRUCTIONS:

Return the annotated c code wrapped in markdown
```c
...
```

START OF INPUT:

MOST RECENT EVA OUTPUT:
{eva}

MOST RECENT PROGRAM:
```c
{program}
```"""
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



generate_with_pathcrawler_prompt = PromptTemplate.from_template(
    """You are a LLM that takes the following inputs and returns a C program annotated with ACSL annotations.
1. A C program with no ACSL annotations
2. A possibly empty CSV file that represents test runs performed by Frama-C pathcrawler

GOALS:
1. Describe any abstract properties of the input program that could be represented as ACSL annotations
2. Analyze the pathcrawler CSV and describe any patterns that you see that could help you understand the behaviors of the program based on given input/output pairs
3. Describe how these behaviors could be used into creating ACSL annotations
4. Generate ACSL annotations based on your analysis of the program and take special account of the properties described when analyzing the Pathcrawler CSV file
5. Returning a program with no annotation is not a valid solution
6. Do not edit the C code, only add annotations
7. Make sure to describe your thought process behind the annotations
8. Do not skip any code in the returned solution to make it shorter.
9. If you break any of these rules then my family will disown me.

ANNOTATION EXAMPLES:

Example 1 (single annotation):
/*@ requires low >= 0 && high <= 9; */

Example 2 (block annotation style):
//Only use this style for function headers. Do not use blocks for multiple annoations in the function body
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

Example 5 (assigns must be in scope):
//This is VALID because x is a parameter that the function contract can see
{valid_assigns}

// this is NOT VALID because x is in the function body and can not be seen by the contract
{invalid_assigns}


FORMAT INSTRUCTIONS:

First describe your reasoning behind the added annotations


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
```""",
    partial_variables={
        "invalid_assigns": invalid_assigns,
        "valid_assigns": valid_assigns,
    },
)

generate_with_eva_prompt = PromptTemplate.from_template(
    """You are a LLM that takes the following inputs and returns a C program annotated with ACSL annotations.
1. A C program with optional ACSL annotations
2. A report from the Eva static analysis tool from Frama-C

GOALS:
1. Describe any abstract properties of the input program that could be represented as ACSL annotations
2. Analyze the Eva report and describe how the results could be used in generating ACSL annotations
3. Generate ACSL annotations based on your analysis of the program and take special account of the properties described when analyzing the Eva report
4. Returning a program with no annotation is not a valid solution
5. Do not edit the C code, only annotations
6. Make sure to describe your thought process behind the annotations
7. Do not skip any code in the returned solution to make it shorter.
8. If you break any of these rules then my family will disown me.

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

Example 5 (assigns must be in scope):
//This is VALID because x is a parameter that the function contract can see
{valid_assigns}

// this is NOT VALID because x is in the function body and can not be seen by the contract
{invalid_assigns}


FORMAT INSTRUCTIONS:

First describe your reasoning behind the added annotations

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
```""",
    partial_variables={
        "invalid_assigns": invalid_assigns,
        "valid_assigns": valid_assigns,
    },
)

mutate_program = PromptTemplate.from_template(
    """You are an LLM edits C programs. Given the following inputs:
1. An original C program

GOALS:
1. Make 1 or 2 small changes to the semantics of the program. Here are some Examples
  - Change any string literals or primitive values
  - Change arithmetic operations such as '+' and '-'
  - Change conditional operators
  - The code should still compile
  - If the code does not compile then my apartment complex will explode with everyone inside

FORMAT INSTRUCTIONS:

Return the altered c code wrapped in markdown
```c
...
```

START OF INPUT:
{program}
                             """
)


gcc_repair_prompt = PromptTemplate.from_template(
    """You are an LLM that edits C files. You are given
- A C program
- The most recent output from GCC when attempting to compile

STEPS:
    1. Describe the syntax error explained by GCC
    2. Edit the program to fix the syntax error described by GCC

FORMAT INSTRUCTIONS:

First describe your changes

Return the annotated c code wrapped in markdown
```c
...
```

START OF INPUT:

MOST RECENT GCC OUTPUT:
{gcc}

MOST RECENT PROGRAM:
```c
{program}
```
"""
)
