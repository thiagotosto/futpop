kafka_source_ddl = """
CREATE TABLE kafka_source (
 key VARCHAR,
 msg VARCHAR
) WITH (
 'connector' = 'kafka',
 'topic' = 'tweet_to_classify',
 'properties.group.id' = 'consumer-group',
 'properties.bootstrap.servers' = 'ip-172-31-83-128.ec2.internal:9092',
 'properties.scan.startup.mode' = 'latest-offset',
 'format' = 'json'
)
"""
# 'connector.properties.zookeeper.connect' = 'localhost:2181',

kafka_target_ddl = """
CREATE TABLE kafka_target (
 msg VARCHAR
) WITH (
 'connector' = 'kafka',
 'topic' = 'test-target',
 'properties.bootstrap.servers' = 'ip-172-31-83-128.ec2.internal:9092',
 'format' = 'json'
)
"""
# 'connector.properties.zookeeper.connect' = 'localhost:2181',
