import sys

import os

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from flink_dlls.kafka_dll import *
#from kafka_dll import *
from pyflink.table.descriptors import Kafka, Json, FileSystem, Schema
import glob
from pyflink.table.udf import udf
from pyflink.table import DataTypes
import datetime as dt
import json

# Table Environment
env = StreamExecutionEnvironment.get_execution_environment()
#env = RemoteStreamEnvironment('localhost', 18082).get_execution_environment()
t_env = StreamTableEnvironment.create(
   env,
   environment_settings=EnvironmentSettings.new_instance().use_blink_planner().build())

t_env.get_config().get_configuration().set_string("pipeline.jars", "file:////home/ubuntu/futpop/docs/flink-json-1.10.2.jar;"
                                                                   "file:////home/ubuntu/futpop/docs/flink-sql-connector-kafka_2.11-1.11.2.jar;"
                                                                   "file:////home/ubuntu/futpop/docs/kafka-clients-2.6.0.jar"
                                                                  )
t_env.get_config().get_configuration().set_string("taskmanager.memory.task.off-heap.size", '80m')

@udf(input_types=[DataTypes.STRING()], result_type=DataTypes.STRING())
def extract_column(json_text, column):
    #dt.datetime.strptime('','')
    return json.loads(json_text)[column]

# Kafka source
t_env.sql_update(kafka_source_ddl)
# Kafka target
t_env.sql_update(kafka_target_ddl)

# 添加依赖的Python文件
t_env.add_Python_file(
     os.path.dirname(os.path.abspath(__file__)) + "/udf/sentiment.py")
# t_env.add_Python_file(os.path.dirname(
#     os.path.abspath(__file__)) + "/enjoyment/cdn/cdn_connector_ddl.py")

# UDF
t_env.register_function("extract_column", extract_column)
t_env.register_function("sentiment_predict", sentiment_predict)

# Insert data
t_env.from_path("kafka_source")\
   .select("msg,"
           "extract_column(msg, 'created_at') as created_at,"
           "extract_column(msg, 'text') as text"
           )\
   .insert_into("kafka_target")

# Executing
t_env.execute("test_flink")
