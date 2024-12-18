# Databricks notebook source
# MAGIC %sql
# MAGIC use catalog rag;
# MAGIC create schema if not exists rag.DevonRem_schema;
# MAGIC use schema DevonRem_schema

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS rag.DevonRem_schema.docs_text ( id BIGINT GENERATED BY DEFAULT AS IDENTITY, text STRING ) tblproperties (delta.enableChangeDataFeed = true);

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS rag.DevonRem_schema.docs_track (file_name STRING) tblproperties (delta.enableChangeDataFeed = true);
