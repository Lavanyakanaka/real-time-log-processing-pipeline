.PHONY: help up down logs test clean build

help:
	@echo "Real-time Log Processing Pipeline - Available Commands"
	@echo "======================================================"
	@echo ""
	@echo "Development:"
	@echo "  make up              - Start all services"
	@echo "  make down            - Stop all services"
	@echo "  make logs            - View logs from all services"
	@echo "  make logs-producer   - View logs from producer"
	@echo "  make logs-consumer   - View logs from consumer"
	@echo "  make logs-broker     - View logs from broker"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test            - Run all tests"
	@echo "  make test-consumer   - Run consumer tests"
	@echo "  make test-coverage   - Run tests with coverage"
	@echo "  make lint            - Run linting checks"
	@echo ""
	@echo "Maintenance:"
	@echo "  make build           - Build Docker images"
	@echo "  make clean           - Remove containers and volumes"
	@echo "  make ps              - Show running containers"
	@echo "  make shell-consumer  - Open shell in consumer container"
	@echo "  make shell-producer  - Open shell in producer container"
	@echo ""
	@echo "Monitoring:"
	@echo "  make tail-logs       - Tail processed logs"
	@echo "  make count-logs      - Count processed logs"
	@echo "  make health          - Check service health"
	@echo "  make stats           - Show container statistics"
	@echo ""

up:
	docker-compose up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-producer:
	docker-compose logs -f producer

logs-consumer:
	docker-compose logs -f consumer

logs-broker:
	docker-compose logs -f broker

test:
	docker-compose run --rm consumer pytest -v

test-consumer:
	docker-compose run --rm consumer pytest tests/test_consumer_processing.py -v

test-coverage:
	docker-compose run --rm consumer pytest --cov=src/consumer tests/

lint:
	docker-compose run --rm consumer flake8 src/consumer tests/

build:
	docker-compose build

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov

ps:
	docker-compose ps

shell-consumer:
	docker-compose exec consumer /bin/bash

shell-producer:
	docker-compose exec producer /bin/bash

tail-logs:
	docker-compose exec consumer tail -f /data/processed_errors_warnings.jsonl

count-logs:
	docker-compose exec consumer wc -l /data/processed_errors_warnings.jsonl

health:
	docker-compose exec broker kafka-broker-api-versions --bootstrap-server localhost:9092

stats:
	docker-compose stats

restart:
	docker-compose restart

restart-producer:
	docker-compose restart producer

restart-consumer:
	docker-compose restart consumer

reset:
	docker-compose down -v
	docker-compose up --build
