from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time

input_file = open('bus2.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']

def generate_uuid():
    return uuid.uuid4()

client = KafkaClient(hosts = '127.0.0.1:9092')
topic =  client.topics['geodata_final']
producer = topic.get_sync_producer()

data = {}
data['busline'] = '00002'

def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(1)
        
        if(i == len(coordinates) - 1):
            i = 0
        else:
            i += 1
            
generate_checkpoint(coordinates)


