from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serializing_producer import SerializingProducer
import time
import random

subject = 'CTSCAN-ROOM-value'

# 1. Define the Avro Schema

avro_schema_str = """
{
  "type": "record",
  "name": "CTScanData",
  "namespace": "hospital.radiology",
  "doc": "CT Scan patient data from radiology operation room",
  "fields": [
    {
      "name": "ScanDate",
      "type": {"type": "long", "logicalType": "timestamp-millis"}
    },
    {"name": "Room_Number", "type": ["null", "int"], "default": null},
    {"name": "ScanID", "type": "string"},
    {
      "name": "CTSCAN_Type",
      "type": {
        "type": "enum",
        "name": "CTScanType",
        "symbols": ["HEAD", "CHEST", "ABDOMEN", "PELVIS", "SPINE", "CARDIAC", "WHOLE_BODY"]
      }
    },
    {"name": "Radiologist", "type": "string"},
    {"name": "HN", "type": "string"},
    {"name": "Name", "type": "string"},
    {"name": "Surname", "type": "string"},
    {"name": "Telephone", "type": "string"},
    {"name": "Age", "type": "int"},
    {
      "name": "Gender",
      "type": {
        "type": "enum",
        "name": "GenderType",
        "symbols": ["M", "F", "OTH"]
      }
    },
    {"name": "RadiationDose", "type": "int", "default":10},
    {"name": "Diagnosis", "type": "string"}
  ]
}
"""

# 2. Setup Registry Client and Serializer
sr_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(sr_conf)


v1_meta = schema_registry_client.get_version(subject, version=1)
v1_schema_str = v1_meta.schema.schema_str
avro_serializer = AvroSerializer(schema_registry_client, v1_schema_str)

# 3. Setup Producer
producer_conf = {
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099',
    'key.serializer': StringSerializer(),
    'value.serializer': avro_serializer
    
}

avro_serializer = AvroSerializer(schema_registry_client, v1_schema_str)
p = SerializingProducer(producer_conf)
        
data = {
    "ScanDate": int(time.time() * 1000),
    "Room_Number": 1,
    "ScanID": "S-001",
    "CTSCAN_Type": "HEAD",
    "Radiologist" : "Kritsada",
    "HN": "HN-"+str(random.randint(10000, 99999)),
    "Name": "Sahaphum",
    "Surname": "Ketkaew",
    "Telephone": "083-6163669",
    "Age": 32,
    "Gender": "M",
    "RadiationDose": 10,
    "Diagnosis": "Tumor"
}
# Produce - SerializingProducer handles encoding automatically
p.produce(topic='CTSCAN-ROOM', key="c001", value=data)
p.flush()
print("Avro message produced.")