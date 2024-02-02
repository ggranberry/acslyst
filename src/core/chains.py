from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import src.core.prompts as prompts
from langchain.schema.output_parser import StrOutputParser
from .sanitize import extract_c_program, parse_annotated_c_program, parse_prolog_program


model = ChatOpenAI(model="gpt-4", max_tokens=4096)
# model = ChatGoogleGenerativeAI(model="gemini-pro")

# Generate ACSL annotations for the provided program
acsl_generation_chain = (
    prompts.initial_prompt | model | StrOutputParser() | parse_annotated_c_program
)


# Use the provided WP output to repair the annotations
repair_chain = (
    prompts.repair_prompt | model | StrOutputParser() | extract_c_program
)

# Use the provided prolog file as context to generate precondition annotations
# precondition_chain = prompt = (
#     prompts.preconditions_prompt | model | StrOutputParser() | llm_output_parser
# )

# Use the provided annotated program to edit the prolog file's input parameters
parameters_chain = prompt = (
    prompts.parameters_prompt | model | StrOutputParser() | parse_prolog_program
)

parameters_chainV2= prompt = (
    prompts.parameters_prompt2 | model | StrOutputParser() | parse_prolog_program
)

parameters_c_chain = prompt = (
    prompts.parameters_c_prompt | model | StrOutputParser() | parse_annotated_c_program
)

# Generate ACSL annotations with a pathcrawler CSV as context
acsl_generation_pathcrawler_chain = prompt = (
    prompts.generate_with_pathcrawler_prompt
    | model
    | StrOutputParser()
    | parse_annotated_c_program
)

# Generate ACSL annotations with Eva report as context
acsl_generation_eva_chain = prompt = (
    prompts.generate_with_eva_prompt
    | model
    | StrOutputParser()
    | parse_annotated_c_program
)
