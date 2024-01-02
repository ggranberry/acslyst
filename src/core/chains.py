from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import src.core.prompts as prompts
from langchain.schema.output_parser import StrOutputParser
from .sanitize import llm_output_parser


model = ChatOpenAI(model="gpt-4", max_tokens=4096)
# model = ChatGoogleGenerativeAI(model="gemini-pro")

# Generate ACSL annotations for the provided program
acsl_generation_chain = (
    prompts.initial_prompt | model | StrOutputParser() | llm_output_parser
)


# Use the provided WP output to repair the annotations
repair_chain = LLMChain(
    prompt=prompts.repair_prompt,
    llm=model,
    output_parser=StrOutputParser(),
)

# Use the provided pathcrawler results csv to generate new annotations
pathcrawler_chain = prompt = (
    prompts.pathcrawler_prompt | model | StrOutputParser() | llm_output_parser
)

# Use the provided prolog file as context to generate precondition annotations
precondition_chain = prompt = (
    prompts.preconditions_prompt | model | StrOutputParser() | llm_output_parser
)

# Use the provided annotated program to edit the prolog file's input parameters
paramters_chain = prompt = (
    prompts.parameters_prompt | model | StrOutputParser() | llm_output_parser
)
