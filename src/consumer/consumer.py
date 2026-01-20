import os
import signal
import sys
from typing import Set

from kafka import KafkaConsumer

from src.consumer.processing import parse_message, should_keep

running = True


def handle_signal(sig, frame):
    global running
    print(f"Received signal {sig}, shutting down consumer...", flush=True)
    running = False


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


def get_env_var(name, default=None, required=False):
    value = os.getenv(name, default)
    if required and value is None:
        print(f"Missing required env var: {name}", file=sys.stderr, flush=True)
        sys.exit(1)
    return value


def parse_levels(env_value: str) -> Set[str]:
    return {lvl.strip() for lvl in env_value.split(",") if lvl.strip()}


def main():
    broker_url = get_env_var("KAFKA_BROKER_URL", required=True)
    topic = get_env_var("KAFKA_TOPIC", required=True)
    group_id = get_env_var("KAFKA_CONSUMER_GROUP", default="log-consumers")
    level_filter_str = get_env_var("LOG_LEVEL_FILTER", default="ERROR,WARN")
    output_file_path = get_env_var("OUTPUT_FILE_PATH", required=True)

    allowed_levels = parse_levels(level_filter_str)

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=broker_url,
        group_id=group_id,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    print(
        f"Consumer connected to {broker_url}, topic '{topic}', "
        f"filtering levels: {allowed_levels}, writing to {output_file_path}",
        flush=True,
    )

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    try:
        with open(output_file_path, "a", encoding="utf-8") as f:
            for msg in consumer:
                if not running:
                    break

                record = parse_message(msg.value)
                if record is None:
                    print("Skipping malformed message", file=sys.stderr, flush=True)
                    continue

                if not should_keep(record, allowed_levels):
                    continue

                f.write(msg.value.decode("utf-8") + "\n")
                f.flush()
                print(f"Consumed & stored: {record}", flush=True)

    except Exception as e:
        print(f"Consumer error: {e}", file=sys.stderr, flush=True)
    finally:
        print("Closing consumer...", flush=True)
        consumer.close()
        print("Consumer shut down.", flush=True)


if __name__ == "__main__":
    main()
