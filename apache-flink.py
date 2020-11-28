import sys

#sys.append('../')
import os

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
#from flink_dlls.kafka_dll import *
from kafka_dll import *
from pyflink.table.descriptors import Kafka, Json, FileSystem, Schema
import glob
#import sys

# directories=['/Users/thiagotosto/Documents/Pessoal/futpop/docs/']
# for directory in directories:
#     for jar in glob.glob(os.path.join(directory,'*.jar')):
#                 sys.path.append(jar)

#from org.apache.flink.streaming.connectors.kafka import


INPUT_TOPIC = 'json-topic'

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

# Kafka source
t_env.sql_update(kafka_source_ddl)
# Kafka target
t_env.sql_update(kafka_target_ddl)


# UDF
#t_env.register_function("ip_to_province", ip_to_province)

# 添加依赖的Python文件
# t_env.add_Python_file(
#     os.path.dirname(os.path.abspath(__file__)) + "/enjoyment/cdn/cdn_udf.py")
# t_env.add_Python_file(os.path.dirname(
#     os.path.abspath(__file__)) + "/enjoyment/cdn/cdn_connector_ddl.py")

# Insert data
t_env.from_path("kafka_source")\
   .select("msg")\
   .insert_into("kafka_target")

# Executing
t_env.execute("test_flink")
