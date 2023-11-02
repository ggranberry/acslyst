from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
import prompts
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema.output_parser import StrOutputParser



model = ChatOpenAI(max_tokens=1000)
# memory = ConversationBufferWindowMemory(k=1, memory_key="history")

acsl_generation_chain = LLMChain(
    prompt=prompts.initial_prompt,
    llm=model,
    output_parser=StrOutputParser(),
)

# RunnablePassthrough.map
# v2 = RunnablePassthrough.assign(
#     memory=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
# ) | prompts.initial_prompt | model | StrOutputParser()

repair_chain = LLMChain(
    prompt=prompts.repair_prompt,
    llm=model,
    output_parser=StrOutputParser(),
    verbose=True,
)

# Don't provide memory here
pathcrawler_chain = LLMChain(
    prompt=prompts.pathcrawler_prompt,
    llm=model,
    output_parser=StrOutputParser(),
    verbose=True,
)
