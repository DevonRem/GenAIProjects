# Databricks notebook source
# MAGIC %run /Workspace/Users/devon.reminick@smoothstack.com/genAI-B1/includes

# COMMAND ----------

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# COMMAND ----------

llm=OpenAIEmbeddings(model="text-embedding-3-large")
document=TextLoader("/Workspace/Users/devon.reminick@smoothstack.com/genAI-B1/day4/job_listings.txt").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
chunks=text_splitter.split_documents(documents=document)
db=Chroma.from_documents(chunks,llm)

# COMMAND ----------

text=input("enter the query: ")
embedding_vector=llm.embed_query(text)

docs=db.similarity_search_by_vector(embedding_vector)
for docs in docs:
   print(docs.page_content)
