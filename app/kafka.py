from aiokafka import AIOKafkaProducer
import json
import os

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")
TOPIC = "applications"

producer: AIOKafkaProducer = None


async def init_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)
        await producer.start()


async def send_message(application_data):
    await init_producer()
    try:
        message = json.dumps(application_data).encode("utf-8")
        await producer.send_and_wait(TOPIC, message)
    except Exception as e:
        print(f"Error sending message: {e}")
    finally:
        pass
