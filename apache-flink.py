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
INPUT_TABLE = 'raw_message'
PROD_ZOOKEEPER = '...'
PROD_KAFKA = '...'

OUTPUT_TOPIC = 'test-target'
OUTPUT_TABLE = 'target'
LOCAL_ZOOKEEPER = 'localhost:2181'
LOCAL_KAFKA = 'localhost:9092'

# Table Environment
env = StreamExecutionEnvironment.get_execution_environment()
#env = RemoteStreamEnvironment('localhost', 18082).get_execution_environment()
t_env = StreamTableEnvironment.create(
   env,
   environment_settings=EnvironmentSettings.new_instance().use_blink_planner().build())

#t_env.get_config().get_configuration().set_string("pipeline.jars","file:////home/ubuntu/futpop/docs/flink-connector-kafka-base_2.11-1.11.2.jar;"
#                                                                  "file:////home/ubuntu/futpop/docs/flink-json-1.10.2.jar;"
#                                                                  "file:////home/ubuntu/futpop/docs/flink-sql-connector-kafka_2.11-1.11.2.jar;"
#                                                                  "file:////home/ubuntu/futpop/docs/kafka-clients-2.6.0.jar"
#                                                                  )
t_env.get_config().get_configuration().set_string("pipeline.jars", "file:////home/ubuntu/futpop/docs/flink-json-1.10.2.jar;"
                                                                  "file:////home/ubuntu/futpop/docs/flink-sql-connector-kafka_2.11-1.11.2.jar;"
                                                                  "file:////home/ubuntu/futpop/docs/kafka-clients-2.6.0.jar"
                                                                  )
#t_env.get_config().get_configuration().set_string("classpath.jars","file:///Users/thiagotosto/Documents/Pessoal/futpop/docs/flink-connector-kafka_2.11-1.11.2.jar;file:///Users/thiagotosto/Documents/Pessoal/flink-1.11.2/bin/flink-table-blink_2.11-1.11.2.jar")
#t_env.get_config().get_configuration()

# Kafka source
t_env.sql_update(kafka_source_ddl)
# Kafka target
t_env.sql_update(kafka_target_ddl)
# t_env.connect(
#     Kafka()
#     .version('universal')
#     .topic(INPUT_TOPIC)
#     .property("bootstrap.servers", PROD_KAFKA)
#
#     .start_from_latest()
# ) \
# .with_format(
#     Json()
#     .json_schema(
#         "{"
#         "  type: 'object',"
#         "  msg: {"
#         "    lon: {"
#         "      type: 'string'"
#         "    }"
#         "  }"
#         "}"
#     )
# )


# 注册IP转换地区名称的UDF
#t_env.register_function("ip_to_province", ip_to_province)

# 添加依赖的Python文件
# t_env.add_Python_file(
#     os.path.dirname(os.path.abspath(__file__)) + "/enjoyment/cdn/cdn_udf.py")
# t_env.add_Python_file(os.path.dirname(
#     os.path.abspath(__file__)) + "/enjoyment/cdn/cdn_connector_ddl.py")

# 核心的统计逻辑
t_env.from_path("kafka_source")\
   .select("msg")\
   .insert_into("kafka_target")

# 执行作业
t_env.execute("test_flink")
