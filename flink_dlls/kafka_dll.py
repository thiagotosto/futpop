kafka_source_ddl = """
CREATE TABLE kafka_source (
 msg VARCHAR
) WITH (
 'connector.type' = 'kafka',
 'connector.version' = 'universal',
 'connector.topic' = 'j8g0bh8g-json-test',
 'connector.properties.bootstrap.servers' = 'tricycle-01.srvs.cloudkafka.com:9094',
 'connector.properties.scan.startup.mode' = 'earliest-offset',
 'format.type' = 'json'
)
"""
# 'connector.properties.zookeeper.connect' = 'localhost:2181',

kafka_target_ddl = """
CREATE TABLE kafka_target (
 msg VARCHAR
) WITH (
 'connector.type' = 'kafka',
 'connector.version' = 'universal',
 'connector.topic' = 'test-target',
 'connector.properties.bootstrap.servers' = 'tricycle-01.srvs.cloudkafka.com:9094',
 'format.type' = 'json'
)
"""
# 'connector.properties.zookeeper.connect' = 'localhost:2181',
