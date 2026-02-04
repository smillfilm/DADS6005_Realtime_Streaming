from confluent_kafka import Consumer
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.deserializing_consumer import DeserializingConsumer

# 1. Setup Registry Client
subject = 'CTSCAN-ROOM-value'
sr_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(sr_conf)

#latest_meta = schema_registry_client.get_latest_version(subject)
latest_meta = schema_registry_client.get_version(subject, version=1)
v2_schema_str = latest_meta.schema.schema_str
print(f"Consumer pulled Latest Schema Version: {latest_meta.version}")
#print(f"Data :{v2_schema_str}")

# 2. Setup Avro Deserializer 
# the consumer pulls it from the Registry using the ID in the message.
avro_deserializer = AvroDeserializer(schema_registry_client)

# 3. Setup Consumer
consumer_conf = {
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099',
    'key.deserializer': StringDeserializer(),
    'value.deserializer': avro_deserializer,
    'group.id': 'avro-group-ct-scan-room-1',
    'auto.offset.reset': 'latest'
}

consumer = DeserializingConsumer(consumer_conf)
consumer.subscribe(['CTSCAN-ROOM'])

print("Waiting for Messages...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        CT_INFORM = msg.value()
        print(f"Consumed Avro CT SCAN : \n ROOM_ID : {CT_INFORM['Room_Number']} \n ScanID : {CT_INFORM['ScanID']} \n CTSCAN_Type : {CT_INFORM['CTSCAN_Type']} \n HN : {CT_INFORM['HN']} \n Name :{CT_INFORM['Name']} {CT_INFORM['Surname']} \n Age : {CT_INFORM['Age']} \n  ---------------")

except KeyboardInterrupt:
    pass

finally:
    consumer.close()