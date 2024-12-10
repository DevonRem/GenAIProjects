# Databricks notebook source
# DBTITLE 1,Imports
# MAGIC %pip install --upgrade --quiet  langchain langchain-community langchainhub langchain-openai langchain-databricks langchain-chroma bs4
# MAGIC  
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Secret
# MAGIC %run /Workspace/Users/naval.yemul@smoothstack.com/GenAI-B1/Day1/secret

# COMMAND ----------

import os
os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY

# COMMAND ----------

# DBTITLE 1,ChatOpenAI class
from langchain_openai import ChatOpenAI
llm=ChatOpenAI(model="gpt-4o")

# COMMAND ----------

question=input("Enter a question")
response=llm.invoke(question)
print(response.content)

# COMMAND ----------

!pip install -U langchain-databricks
dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,ChatDataBricks llama
from langchain_community.chat_models import ChatDatabricks
chat_model=ChatDatabricks(endpoint="databricks-meta-llama-3-1-70b-instruct")

# COMMAND ----------

question=input("enter a question: ")
response=chat_model.invoke(question)
print(response.content)

# COMMAND ----------

from langchain_community.chat_models import ChatDatabricks
chat_model=ChatDatabricks(endpoint="databricks-meta-llama-3-1-70b-instruct")
question=input("enter a question: ")
response=chat_model.invoke(question)
print(response.content)
