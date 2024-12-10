# Databricks notebook source
# MAGIC %pip install --upgrade --quiet  langchain langchain-community langchainhub langchain-openai langchain-databricks langchain-chroma bs4
# MAGIC  
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run /Workspace/Users/naval.yemul@smoothstack.com/GenAI-B1/Day1/secret

# COMMAND ----------

import os
os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY

# COMMAND ----------

# DBTITLE 1,Prompt Template with user input
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm=ChatOpenAI(model="gpt-4o")
prompt_template = PromptTemplate(
    input_variables=["city","month","language","budget"],
    template="""
    Welcome to the {city} travel guide!.
    If you're visiting in {month}, here's what you can do:
    1.Must Visit attractions.
    2.Local Cuisine
    3.Useful phrases in {language}.
    4.Tips for travelling on a {budget} budget
    """
)

chain = prompt_template | llm

print("Travel Guide App")

city=input("Enter the city: ")
month=input("Enter the month: ")
language=input("Enter the language: ")
budget=input("Enter the budget: ")

if city and month and language and budget:
  response=chain.invoke({"city":city,"month":month,"language":language,"budget":budget})
print(response.content)

# COMMAND ----------

# MAGIC %md
# MAGIC Chains:
# MAGIC Lang chain provides a declarative way to sequentially execute the prompts and the llms
# MAGIC pipe symbol (|)

# COMMAND ----------



# COMMAND ----------

# DBTITLE 1,chain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm=ChatOpenAI(model="gpt-4o")
title_template = PromptTemplate(
    input_variables=["topic"],
    template="""
    You are an experienced speech writer.
    You need to craft an impactful title for a speech 
    on the following topic: {topic}
    Answer exactly with one title.	
    """
)

speech_prompt = PromptTemplate(
input_variables=["title"],
template="""
    You need to write a powerful speech of 250 words
     for the following title: {title}
"""
)



first_chain = title_template | llm | StrOutputParser() | (lambda title: (print(title), title[1]))
second_chain = speech_prompt | llm
final_chain = first_chain | second_chain

print("Speech Generator")

topic=input("Enter the topic: ")


if topic:
  response=final_chain.invoke({"topic":topic})
print(response.content)


# COMMAND ----------

# DBTITLE 1,chain with 2 different llms
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatDatabricks

llm=ChatOpenAI(model="gpt-4o")
llm2=ChatDatabricks(endpoint="databricks-meta-llama-3-1-70b-instruct")

title_template = PromptTemplate(
    input_variables=["topic"],
    template="""
  You are a professional blogger.
    Create an outline for a blog post on the following topic: {topic}
    The outline should include:
    - Introduction
    - 3 main points with subpoints
    - Conclusion
    """
)

speech_prompt = PromptTemplate(
input_variables=["outline"],
template="""
  You are a professional blogger.
    Write an engaging introduction paragraph based on the following
    outline:{outline}
    The introduction should hook the reader and provide a brief
    overview of the topic
"""
)

first_chain = title_template | llm | StrOutputParser() | (lambda title: (print(title), title[1]))
second_chain = speech_prompt | llm2
final_chain = first_chain | second_chain

print("Speech Generator")

topic=input("Enter the topic: ")


if topic:
  response=final_chain.invoke({"topic":topic})
print(response.content)


# COMMAND ----------

# DBTITLE 1,chain with a second input
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

llm=ChatOpenAI(model="gpt-4o")
title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""You are an experienced speech writer.
    You need to craft an impactful title for a speech 
    on the following topic: {topic}
    Answer exactly with one title.	
    """
)

speech_prompt = PromptTemplate(
    input_variables=["title","emotion"],
    template="""You need to write a powerful {emotion} speech of 250 words
     for the following title: {title}
    """
)

first_chain = title_prompt | llm | StrOutputParser() | (lambda title: (print(title),title)[1])
second_chain = speech_prompt | llm | JsonOutputParser()
final_chain = first_chain |(lambda title:{"title":title,"emotion":emotion}) |second_chain

print("Speech Generator")

topic = input("Enter the topic:")
emotion=input("Enter the emotion:")

if topic and emotion:
    response = final_chain.invoke({"topic":topic})
    print(response.content)

# COMMAND ----------

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini")
model.invoke("what color is the sky?")

# COMMAND ----------

# DBTITLE 1,streaming chunks
chunks=[]
for chunk in model.stream("what color is the sky?"):
  chunks.append(chunk)
  print(chunk.content, end="|")
