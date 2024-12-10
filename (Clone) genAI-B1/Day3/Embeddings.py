# Databricks notebook source
# MAGIC %run /Workspace/Users/devon.reminick@smoothstack.com/genAI-B1/includes

# COMMAND ----------

from langchain_openai import OpenAIEmbeddings

llm=OpenAIEmbeddings(model="text-embedding-3-large")
text=input("Enter a text")
response=llm.embed_query(text)
print(response)

# COMMAND ----------

import numpy as np

# COMMAND ----------

from langchain_openai import OpenAIEmbeddings

llm=OpenAIEmbeddings(model="text-embedding-3-large")
text1=input("Enter a text")
text2=input("Enter a text")
response1=llm.embed_query(text1)
response2=llm.embed_query(text2)
similarity=np.dot(response1,response2)
print(similarity*100, '%')

# COMMAND ----------

from langchain_databricks import DatabricksEmbeddings

embeddings=DatabricksEmbeddings(endpoint="databricks-gte-large-en")

text=input("Enter the text")
response=embeddings.embed_query(text)
print(response)

# COMMAND ----------

# DBTITLE 1,embedding similarity with 2 different llms is worse
from langchain_databricks import DatabricksEmbeddings

embeddings1=DatabricksEmbeddings(endpoint="databricks-gte-large-en")
embeddings2=DatabricksEmbeddings(endpoint="databricks-bge-large-en")

text1=input("Enter a text")
text2=input("Enter a text")

response1=embeddings1.embed_query(text1)
response2=embeddings2.embed_query(text2)
similarity=np.dot(response1,response2)
print(similarity*100, '%')

# COMMAND ----------


