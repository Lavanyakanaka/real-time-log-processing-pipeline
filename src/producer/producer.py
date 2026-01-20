import json
import os
import random
import signal
import sys
import time
import uuid
from datetime import datetime, timezone

from kafka import KafkaProducer

running = True


def handle_signal(sig, frame):
    global running
    print(f"Received signal {sig}, shutting down producer...", flush=True)
    running = False


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


def get_env_var(name, default=None, required=False):
    value = os.getenv(name, default)
    if required and value is None:
        print(f"Missing required env var: {name}", file=sys.stderr, flush=True)
        sys.exit(1)
    return value


def create_producer(bootstrap_servers: str) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def generate_log_record() -> dict:
    services = ["auth-service", "user-api", "payment-service"]
    levels = ["INFO", "WARN", "ERROR"]
    messages = [
        "User logged in successfully",
        "Payment processed",
        "Database connection slow",
        "Timeout while calling external API",
        "Null pointer exception in service",
    ]

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "service_name": random.choice(services),
        "level": random.choice(levels),
        "message": random.choice(messages),
        "trace_id": str(uuid.uuid4()),
    }
    return record


def main():
    broker_url = get_env_var("KAFKA_BROKER_URL", required=True)
    topic = get_env_var("KAFKA_TOPIC", required=True)
    message_rate = float(get_env_var("MESSAGE_RATE", default="2"))

    interval = 1.0 / message_rate if message_rate > 0 else 1.0

    producer = create_producer(broker_url)
    print(f"Producer connected to {broker_url}, sending to topic '{topic}'", flush=True)

    try:
        while running:
            record = generate_log_record()
            producer.send(topic, value=record)
            print(f"Produced: {record}", flush=True)
            time.sleep(interval)
    except Exception as e:
        print(f"Producer error: {e}", file=sys.stderr, flush=True)
    finally:
        print("Flushing and closing producer...", flush=True)
        producer.flush()
        producer.close()
        print("Producer shut down.", flush=True)


if __name__ == "__main__":
    main()
