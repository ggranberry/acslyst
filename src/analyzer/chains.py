from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
import prompts
from langchain.schema.output_parser import StrOutputParser
from sanitize import llm_output_parser


model = ChatOpenAI(model="gpt-4-1106-preview", max_tokens=1000)

acsl_generation_chain = (
    prompts.initial_prompt | model | StrOutputParser() | llm_output_parser
)

repair_chain = LLMChain(
    prompt=prompts.repair_prompt,
    llm=model,
    output_parser=StrOutputParser(),
)

pathcrawler_chain = prompt=prompts.pathcrawler_prompt | model | StrOutputParser() | llm_output_parser
