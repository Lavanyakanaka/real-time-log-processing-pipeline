# Real-Time Log Processing Pipeline

This project implements a real-time log processing pipeline using Kafka, with:
- A producer service generating synthetic application logs.
- A Kafka cluster running in Docker.
- A consumer service filtering logs by level (ERROR/WARN) and writing them to a JSON Lines file.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Lavanyakanaka/real-time-log-processing-pipeline.git
   cd real-time-log-processing-pipeline
