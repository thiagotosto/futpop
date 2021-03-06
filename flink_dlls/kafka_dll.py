kafka_source_ddl = """
CREATE TABLE kafka_source (
 key VARCHAR,
 msg VARCHAR
) WITH (
 'connector' = 'kafka',
 'topic' = 'tweet_to_classify',
 'properties.group.id' = 'consumer-group',
 'properties.bootstrap.servers' = 'ec2-3-238-203-167.compute-1.amazonaws.com:9092',
 'properties.scan.startup.mode' = 'latest-offset',
 'format' = 'json'
)
"""
# 'connector.properties.zookeeper.connect' = 'localhost:2181',

kafka_target_ddl = """
CREATE TABLE kafka_target (
 msg VARCHAR,
 created_at VARCHAR,
 text VARCHAR
) WITH (
 'connector' = 'kafka',
 'topic' = 'test-target',
 'properties.bootstrap.servers' = 'ec2-3-238-203-167.compute-1.amazonaws.com:9092',
 'format' = 'json'
)
"""
# 'connector.properties.zookeeper.connect' = 'localhost:2181',
