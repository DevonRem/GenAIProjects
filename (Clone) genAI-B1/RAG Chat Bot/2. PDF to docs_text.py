# Databricks notebook source
# MAGIC %run /Workspace/Users/devon.reminick@smoothstack.com/genAI-B1/includes

# COMMAND ----------

# MAGIC %pip install Pdfplumber langchain

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

import os
from pyspark.sql.functions import substring_index

# Directory path
directory_path = "/Volumes/rag/devonrem_schema/raw_pdf"

# List files in directory
file_paths = [file.path for file in dbutils.fs.ls(directory_path)]

# Extract file names from paths
df = spark.createDataFrame(file_paths, "string").select(substring_index("value", "/", -1).alias("file_name"))

# Show dataframe
df.show()

# COMMAND ----------

import os
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter

pdf_volume_path =   # Specify the path to the PDF volume directory

# Get the list of already processed PDF files from the Delta table
processed_files = spark.sql(f"SELECT DISTINCT file_name FROM rag.naval_schema.docs_track").collect()
processed_files = set(row["file_name"] for row in processed_files)

# Process only new PDF files
new_files = [file for file in os.listdir(pdf_volume_path) if file not in processed_files]

all_text = ''  # Initialize all_text to store text from new PDF files

for file_name in new_files:
    # Extract text from the PDF file
    pdf_path = os.path.join(pdf_volume_path, file_name)

    with pdfplumber.open(pdf_path) as pdf:
        for pdf_page in pdf.pages:
            single_page_text = pdf_page.extract_text()
            # Separate each page's text with newline
            all_text = all_text + '\n' + single_page_text

# Split the combined text into chunks using the RecursiveCharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

length_function = len

splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=1000,
    chunk_overlap=200,
    length_function=length_function,
)
chunks = splitter.split_text(all_text)

# COMMAND ----------

from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import ArrayType, StringType
import pandas as pd

@pandas_udf("array<string>")
def get_chunks(dummy):
    return pd.Series([chunks])

# Register the UDF
spark.udf.register("get_chunks_udf", get_chunks)

# COMMAND ----------

# MAGIC %sql
# MAGIC insert into rag.devonrem_schema.docs_text (text)
# MAGIC select explode(get_chunks_udf('dummy')) as text;
