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
from langchain.prompts import PromptTemplate
llm=ChatOpenAI(model="gpt-4o")

prompt_template=PromptTemplate(
  input_variable=["country","no_paras","language"],
  template="""You are an expert in traditional cuisines.
    You provide information about a specific dish from a specific country.
    Answer the question: What is the traditional cuisine of {country}
    Answer in {no_paras} short paras in {language}
  """
)

response=llm.invoke(prompt_template.format(country="US",no_paras="1",language="English"))
print(response.content)

# COMMAND ----------

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
llm=ChatOpenAI(model="gpt-4o")

prompt_template=PromptTemplate(
  input_variable=["country","num"],
  template="""You are an expert in traditional cuisines.
    You provide information about a specific dish from a specific country.
    Answer the question: What is the traditional cuisine of {country}
    Answer in a list containing{num} results.
  """
)

response=llm.invoke(prompt_template.format(country="US",num="4"))
print(response.content)

# COMMAND ----------

# DBTITLE 1,Travel guide app
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
llm=ChatOpenAI(model="gpt-4o")

prompt_template=PromptTemplate(
  input_variable=["country","no_paras","language"],
  template="""You are an expert in traditional cuisines.
    You provide information about a specific dish from a specific country.
    Answer the question: What is the traditional cuisine of {country}
    Answer in {no_paras} short paras in {language}
  """
)

response=llm.invoke(prompt_template.format(country="US",no_paras="1",language="English"))
print(response.content)

# COMMAND ----------

!pip install streamlit
dbutils.library.restartPython() 

# COMMAND ----------

from langchain_openai import ChatOpenAI
import streamlit as st
from langchain.prompts import PromptTemplate

llm=ChatOpenAI(model="gpt-4o")
prompt_template = PromptTemplate(
    input_variables=["country","no_of_paras","language"],
    template="""You are an expert in traditional cuisines.
    You provide information about a specific dish from a specific country.
    Avoid giving information about fictional places. If the country is fictional
    or non-existent answer: I don't know.
    Answer the question: What is the traditional cuisine of {country}?
    Answer in {no_of_paras} short paras in {language}
    """
)

st.title("Cuisine Info")

country = st.text_input("Enter the country:")
no_of_paras = st.number_input("Enter the number of paras",min_value=1,max_value=5)
language = st.text_input("Enter the language:")

if country:
    response = llm.invoke(prompt_template.format(country=country,
                                                 no_of_paras=no_of_paras,
                                                 language=language
                                                 ))
    st.write(response.content)

# COMMAND ----------

!streamlit run /databricks/python_shell/scripts/db_ipykernel_launcher.py

# COMMAND ----------

# DBTITLE 1,Travel Guide App
from langchain_openai import ChatOpenAI
import streamlit as st
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

st.title("Travel guide")

city = st.text_input("Enter the city:")
month = st.text_input("Enter the month")
language = st.text_input("Enter the language:")
budget = st.number_input("Enter the budget:")

if city:
    response = llm.invoke(prompt_template.format(city=city,
                                                 month=month,
                                                 language=language,
                                                 budget=budget
                                                 ))
    st.write(response.content)


# COMMAND ----------

!streamlit run /databricks/python_shell/scripts/db_ipykernel_launcher.py

# COMMAND ----------

# DBTITLE 1,travel guide without streamlit
from langchain_openai import ChatOpenAI
import streamlit as st
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


response=llm.invoke(prompt_template.format(city="New York",month="March",language="English",budget="1000"))
print(response.content)
