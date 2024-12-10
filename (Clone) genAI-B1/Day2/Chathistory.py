# Databricks notebook source
# MAGIC %run /Workspace/Users/devon.reminick@smoothstack.com/genAI-B1/includes

# COMMAND ----------

# MAGIC %md
# MAGIC ChatPromptTemplate

# COMMAND ----------

# DBTITLE 1,Runnable Parallel
from langchain_openai import ChatOpenAI

model=ChatOpenAI(model="gpt-4o-mini")


# COMMAND ----------

from langchain_core.prompts import ChatPromptTemplate

joke_chain=ChatPromptTemplate.from_template("Tell me a joke about {topic}") | model

joke_chain.invoke({"topic":"friends"})

# COMMAND ----------

# DBTITLE 1,runnableparallel
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel

model=ChatOpenAI(model="gpt-4o-mini")

joke_chain=ChatPromptTemplate.from_template("Tell me a joke about {topic}") | model
poem_chain=ChatPromptTemplate.from_template("Tell me a poem about {topic}") | model

both_chain=RunnableParallel(joke=joke_chain, poem=poem_chain)
both_chain.invoke({"topic":"friends"})


# COMMAND ----------

RunnablePassthrough on its own allows you to pass inputs unchanged. This typically is used in conjuction with RunnableParallel to pass data through to a new key in the map.

# COMMAND ----------

from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# COMMAND ----------

chain = RunnablePassthrough() | RunnablePassthrough()
chain.invoke("hello")

# COMMAND ----------

def input_to_upper(input: str):
  output = input.upper()
  return output

# COMMAND ----------

chain = RunnablePassthrough() | RunnableLambda(input_to_upper)
chain.invoke("hello")

# COMMAND ----------

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

model=ChatOpenAI(model="gpt-4o-mini")
prompt_template=ChatPromptTemplate.from_messages([("system","You are a Agile Coach. Answer any questions that are related to Agile"), ("human","{input}")

]
)

chain=prompt_template | model

question=input("Enter a question:")

if question:
  response=chain.invoke({"input":question})
  print(response.content)

# COMMAND ----------

# DBTITLE 1,Chat history
from langchain_openai import ChatOpenAI
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

model=ChatOpenAI(model="gpt-4o-mini")
prompt_template=ChatPromptTemplate.from_messages([("system","You are a Agile Coach. Answer any questions that are related to Agile"), MessagesPlaceholder(variable_name="chat_history"), ("human","{input}")

]
)

chain=prompt_template | model

history_for_chain=ChatMessageHistory()

chain_with_history=RunnableWithMessageHistory(
  chain,
  lambda session_id:history_for_chain,
  input_messages_key= "input",
  history_messages_key="chat_history"
)

print("Agile Guide")
while True:
  question=input("Enter a question:")
  if question:
    response=chain_with_history.invoke({"input":question}, {"configurable":{"session_id":"abc123"}})
    print(response.content)

