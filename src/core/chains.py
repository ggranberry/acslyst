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
repair_eva_chain = (
    prompts.repair_eva_prompt | model | StrOutputParser() | extract_c_program
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

mutate_chain = (
        prompts.mutate_program
        | model
        | StrOutputParser()
        | parse_annotated_c_program
        )

gcc_repair_chain = (
        prompts.gcc_repair_prompt
        | model
        | StrOutputParser()
        | parse_annotated_c_program
        )
