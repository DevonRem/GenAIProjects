# Databricks notebook source
# MAGIC %run /Workspace/Users/devon.reminick@smoothstack.com/genAI-B1/includes

# COMMAND ----------

!pip install wikipedia duckduckgo-search youtube-search

# COMMAND ----------

dbutils.library.restartPython()


# COMMAND ----------

# DBTITLE 1,wikipedia retrieval
from langchain_community.retrievers import WikipediaRetriever
retriever=WikipediaRetriever()
docs=retriever.invoke(input="Generative AI")
print(docs)

# COMMAND ----------

# DBTITLE 1,youtube search tool
from langchain_community.tools import YouTubeSearchTool
tool=YouTubeSearchTool()
tool.run("The Data Master")

# COMMAND ----------

# DBTITLE 1,Agentic AI, function calls youtube/wikipedia
from langchain_community.chat_models import ChatDatabricks
from langchain.prompts import PromptTemplate
from langchain.agents import Tool, initialize_agent
from langchain.chains import LLMChain

chat_model=ChatDatabricks(endpoint='databricks-meta-llama-3-1-70b-instruct')

prompt_template=PromptTemplate.from_template("Suggest a {type} vacation destination in {country}.")

wiki_tool=Tool(name="Wikipedia", func=WikipediaRetriever().run, description="Search Wikipedia for relevant information.")

youtube_tool=Tool(name="Youtube Search", func=YouTubeSearchTool().run, description="Search Youtube for video related to the topic.")

prompt_chain=LLMChain(llm=chat_model, prompt=prompt_template)

tools=[wiki_tool, youtube_tool]
agent=initialize_agent(
    tools=tools,
    llm=chat_model,
    agent="zero-shot-react-description",
    verbose=True
)

print("Hello, I am a chatbot. Ask me anything about vacations.")

try:
    vacation_type = input("Enter the type of vacation (e.g., beach, adventure, cultural): ").strip()
    country = input("Enter the country: ").strip()

    if vacation_type and country:
        input_query = f"Suggest a {vacation_type} vacation destination in {country}."
        response = agent.run(input_query)
        print("\nResponse:\n", response)
    else:
        print("Please provide both the type of vacation and the country.")
except Exception as e:
    print("An error occurred:", e)


# COMMAND ----------


