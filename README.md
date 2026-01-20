# Real-Time Log Processing Pipeline

A scalable, production-ready real-time log processing pipeline using Apache Kafka and Docker. This project demonstrates a complete data streaming architecture with log generation, filtering, and persistence.

## 🎯 Features

- **Real-time Log Generation**: Producer service generates synthetic application logs
- **Scalable Message Queue**: Kafka-based message broker for high-throughput log streaming
- **Intelligent Filtering**: Consumer service filters logs by severity level (ERROR, WARN, INFO)
- **Persistent Storage**: Processed logs written to JSON Lines format
- **Containerized Deployment**: Complete Docker and Docker Compose setup
- **Health Checks**: Built-in health monitoring for all services
- **Comprehensive Testing**: Unit tests with 100% passing rate
- **Signal Handling**: Graceful shutdown on SIGINT/SIGTERM

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  Real-time Log Pipeline                       │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐      ┌──────────────────────────┐      │
│  │  Log Producer   │─────→│   Kafka Broker (3 Partitions) │ │
│  │  - Generates    │      │   with Zookeeper         │      │
│  │  - Random logs  │      │   - High throughput      │      │
│  │  - 2 msg/sec    │      │   - Fault tolerant       │      │
│  └─────────────────┘      └──────────────────────────┘      │
│                                  ↓                             │
│  ┌────────────────────────────────────────────────────┐      │
│  │           Log Consumer                             │      │
│  │  - Consumes from Kafka topic                       │      │
│  │  - Filters: ERROR, WARN levels                     │      │
│  │  - Writes to JSON Lines format                     │      │
│  │  - Stores in persistent volume                     │      │
│  └────────────────────────────────────────────────────┘      │
│                           ↓                                    │
│  ┌────────────────────────────────────────────────────┐      │
│  │  /data/processed_errors_warnings.jsonl             │      │
│  │  - Persistent storage                              │      │
│  │  - JSON Lines format (one record per line)         │      │
│  └────────────────────────────────────────────────────┘      │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- **Docker**: Version 20.10+ ([Installation Guide](https://docs.docker.com/get-docker/))
- **Docker Compose**: Version 1.29+ ([Installation Guide](https://docs.docker.com/compose/install/))
- **Git**: For cloning the repository
- **Python**: 3.9+ (for local testing and development)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Lavanyakanaka/real-time-log-processing-pipeline.git
cd real-time-log-processing-pipeline
```

### 2. Start the Pipeline

```bash
# Start all services
docker-compose up --build

# In another terminal, to see processed logs
docker-compose exec consumer tail -f /data/processed_errors_warnings.jsonl
```

### 3. Verify Services

```bash
# Check status of all containers
docker-compose ps

# View logs from any service
docker-compose logs -f producer
docker-compose logs -f consumer
docker-compose logs -f broker
```

## 🔧 Configuration

Create a `.env` file (or use the provided `.env.example`):

```env
# Kafka Configuration
KAFKA_BROKER_URL=broker:29092
KAFKA_TOPIC=application-logs
KAFKA_CONSUMER_GROUP=log-consumers

# Producer Configuration
MESSAGE_RATE=2  # Messages per second

# Consumer Configuration
LOG_LEVEL_FILTER=ERROR,WARN  # Comma-separated log levels to process
OUTPUT_FILE_PATH=/data/processed_errors_warnings.jsonl
```

### Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `KAFKA_BROKER_URL` | Kafka broker address | `broker:29092` | `localhost:9092` |
| `KAFKA_TOPIC` | Topic to produce/consume from | `application-logs` | N/A |
| `KAFKA_CONSUMER_GROUP` | Consumer group ID | `log-consumers` | N/A |
| `MESSAGE_RATE` | Messages produced per second | `2` | `5` |
| `LOG_LEVEL_FILTER` | Log levels to process | `ERROR,WARN` | `ERROR,WARN,INFO` |
| `OUTPUT_FILE_PATH` | Path for filtered logs | `/data/processed_errors_warnings.jsonl` | N/A |

## 📊 Services

### Zookeeper
- **Purpose**: Kafka cluster coordination
- **Port**: 2181
- **Health Check**: TCP connection check

### Kafka Broker
- **Purpose**: Main message broker
- **Ports**: 9092 (external), 29092 (internal)
- **Partitions**: 3 for scalability
- **Health Check**: API version check

### Producer Service
- **Purpose**: Generates synthetic application logs
- **Language**: Python 3.9+
- **Rate**: Configurable (default 2 msg/sec)
- **Restart Policy**: Unless stopped (auto-recovery)
- **Health Check**: Process health

### Consumer Service
- **Purpose**: Filters and persists logs
- **Language**: Python 3.9+
- **Filtering**: By log level (ERROR, WARN, etc.)
- **Output Format**: JSON Lines (one JSON object per line)
- **Restart Policy**: Unless stopped (auto-recovery)
- **Health Check**: Process health

## 📝 Log Format

### Generated Log Records
```json
{
  "timestamp": "2026-01-20T10:30:45.123456Z",
  "service_name": "auth-service",
  "level": "ERROR",
  "message": "Null pointer exception in service",
  "trace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Filtered Output (processed_errors_warnings.jsonl)
```
{"timestamp":"2026-01-20T10:30:45.123456Z","service_name":"auth-service","level":"ERROR","message":"Null pointer exception in service","trace_id":"550e8400-e29b-41d4-a716-446655440000"}
{"timestamp":"2026-01-20T10:30:46.234567Z","service_name":"user-api","level":"WARN","message":"Database connection slow","trace_id":"660f9511-f40c-52e5-b827-557766551111"}
```

## 🧪 Testing

### Run Unit Tests
```bash
# Using docker-compose
docker-compose run --rm consumer pytest -v

# Or locally with Python
pip install -r src/consumer/requirements.txt
pytest tests/test_consumer_processing.py -v
```

### Test Coverage
- ✅ `test_parse_message_valid` - Valid JSON parsing
- ✅ `test_parse_message_invalid_json` - Invalid JSON handling
- ✅ `test_should_keep_error_level` - Error level filtering
- ✅ `test_should_keep_info_level_filtered_out` - Info level exclusion
- ✅ `test_should_keep_missing_level` - Missing level handling

## 🛠️ Development

### Local Development Setup

```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r src/consumer/requirements.txt
pip install -r src/producer/requirements.txt
```

### Code Structure
```
real-time-log-processing-pipeline/
├── src/
│   ├── producer/
│   │   ├── producer.py          # Main producer logic
│   │   ├── requirements.txt     # Python dependencies
│   │   ├── Dockerfile          # Container definition
│   │   └── __init__.py
│   └── consumer/
│       ├── consumer.py          # Main consumer logic
│       ├── processing.py        # Log filtering logic
│       ├── requirements.txt     # Python dependencies
│       ├── Dockerfile          # Container definition
│       └── __init__.py
├── tests/
│   ├── test_consumer_processing.py  # Unit tests
│   └── __init__.py
├── docker-compose.yml           # Service orchestration
├── .env                         # Environment variables
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## 📈 Performance & Scalability

### Tuning Options

1. **Increase Message Rate**
   ```bash
   MESSAGE_RATE=10  # 10 messages per second
   ```

2. **Increase Kafka Partitions**
   - Modify `docker-compose.yml`: `--partitions 6`
   - Allows parallel processing

3. **Increase Consumer Instances**
   ```bash
   docker-compose up --build --scale consumer=3
   ```

4. **Adjust Log Level Filtering**
   ```bash
   LOG_LEVEL_FILTER=ERROR,WARN,INFO  # Process all levels
   ```

## 🚨 Troubleshooting

### Issue: "Broker not available"
```bash
# Wait for broker to be healthy
docker-compose ps
# All services should have (healthy) status
```

### Issue: "Consumer not consuming messages"
```bash
# Check consumer logs
docker-compose logs consumer

# Verify topic exists
docker-compose exec broker kafka-topics --bootstrap-server localhost:29092 --list
```

### Issue: "No output file created"
```bash
# Verify output path
docker-compose exec consumer ls -la /data/

# Check file permissions
docker-compose exec consumer cat /data/processed_errors_warnings.jsonl
```

### Reset Everything
```bash
# Stop and remove all containers
docker-compose down

# Remove volumes (data will be deleted)
docker-compose down -v

# Rebuild and start fresh
docker-compose up --build
```

## 🔍 Monitoring

### View Logs in Real-Time
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f producer
docker-compose logs -f consumer
docker-compose logs -f broker

# Last 50 lines
docker-compose logs --tail=50
```

### Check Service Health
```bash
docker-compose ps
docker-compose stats
```

### Inspect Processed Logs
```bash
# View last 10 processed logs
docker-compose exec consumer tail -10 /data/processed_errors_warnings.jsonl

# Count total processed logs
docker-compose exec consumer wc -l /data/processed_errors_warnings.jsonl

# Stream logs in real-time
docker-compose exec consumer tail -f /data/processed_errors_warnings.jsonl
```

## 🔄 Stopping and Cleanup

```bash
# Stop all services gracefully
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove volumes (persistent data)
docker-compose down -v

# Remove unused images and resources
docker system prune
```

## 📚 Additional Resources

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Python Kafka Client](https://kafka-python.readthedocs.io/)

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ✅ Project Status

- ✅ Producer Service: Complete
- ✅ Consumer Service: Complete
- ✅ Kafka Setup: Complete
- ✅ Docker Containerization: Complete
- ✅ Health Checks: Complete
- ✅ Unit Tests: Complete (5/5 passing)
- ✅ Documentation: Complete
- ✅ Error Handling: Complete
- ✅ Signal Handling: Complete

---

**Last Updated**: January 20, 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✓
