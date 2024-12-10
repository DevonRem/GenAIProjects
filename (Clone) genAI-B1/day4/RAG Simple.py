# Databricks notebook source
# MAGIC %run /Workspace/Users/devon.reminick@smoothstack.com/genAI-B1/includes

# COMMAND ----------

# DBTITLE 1,RAG example
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# COMMAND ----------

embedding=OpenAIEmbeddings(model="text-embedding-3-large")
llm=ChatOpenAI(model="gpt-4o", temperature=0.5)

# COMMAND ----------


document=TextLoader("/Workspace/Users/devon.reminick@smoothstack.com/genAI-B1/day4/product-data.txt").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
chunks=text_splitter.split_documents(documents=document)
vectore_store=Chroma.from_documents(chunks,embedding)

retriever = vectore_store.as_retriever()

prompt_template=ChatPromptTemplate.from_messages([
  ("system",""" You are an assistance for anserwing questions. 
   Use the provided context to respond. If the answer isn't clear, acknowledge that you don't know. Limit your response to three concise sentences.{context} 
   """),
  ("human","{input}")
])

# COMMAND ----------

qa_chain=create_stuff_documents_chain(llm,prompt_template)

rag_chain=create_retrieval_chain(retriever,qa_chain)

# COMMAND ----------

print("Chat with your DATA")
question=input("What is your question: ")

if question:
   response=rag_chain.invoke({"input":question})
   print(response['answer'])



# COMMAND ----------


