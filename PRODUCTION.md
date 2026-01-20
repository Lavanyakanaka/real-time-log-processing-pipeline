# Production-grade Docker configuration guide

## Producer Service - Production Considerations

1. **Resource Limits**: Add CPU and memory constraints
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '0.5'
         memory: 512M
       reservations:
         cpus: '0.25'
         memory: 256M
   ```

2. **Logging Configuration**: Implement centralized logging
   ```yaml
   logging:
     driver: json-file
     options:
       max-size: "10m"
       max-file: "3"
   ```

3. **Environment Variables**: Use secure secrets management
   - Docker Secrets for swarm mode
   - AWS Secrets Manager for ECS
   - HashiCorp Vault for Kubernetes

## Consumer Service - Production Considerations

1. **Scaling**: Run multiple replicas
   ```bash
   docker-compose up --scale consumer=3
   ```

2. **Storage**: Use external volumes or cloud storage
   - AWS EBS for EC2
   - Azure Managed Disks for AKS
   - GCS for GKE

3. **Backup Strategy**: Regular snapshots of processed logs

## Kafka Broker - Production Considerations

1. **Replication Factor**: Increase from 1 to 3
   ```yaml
   KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
   ```

2. **Retention Policy**: Implement log retention
   ```yaml
   environment:
     LOG_RETENTION_MS: 604800000  # 7 days
   ```

3. **Monitoring**: Enable JMX metrics
   ```yaml
   environment:
     KAFKA_JMX_PORT: 9999
   ```

## Security Considerations

1. **Network Security**
   - Use private networks
   - Enable SSL/TLS for Kafka
   - Implement VPN or service mesh

2. **Authentication**
   - SASL/SCRAM for Kafka clients
   - OAuth 2.0 for services

3. **Data Protection**
   - Encrypt data at rest
   - Encrypt data in transit
   - Implement access controls

## Deployment on Kubernetes

```yaml
apiVersion: v1
kind: Deployment
metadata:
  name: log-producer
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: producer
        image: your-registry/log-producer:latest
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: KAFKA_BROKER_URL
          value: kafka-broker:29092
        livenessProbe:
          exec:
            command: ["python", "-c", "import sys; sys.exit(0)"]
          initialDelaySeconds: 10
          periodSeconds: 30
```

## Performance Optimization

1. **Batch Processing**: Process logs in batches
2. **Compression**: Enable Snappy or LZ4 compression
3. **Partitioning**: Increase partitions for parallelism
4. **Connection Pooling**: Reuse Kafka connections

## Monitoring and Observability

1. **Prometheus Metrics**: Export metrics for scraping
2. **ELK Stack**: Elasticsearch, Logstash, Kibana
3. **Jaeger**: Distributed tracing
4. **Grafana**: Visualization and alerting

## CI/CD Integration

See `.github/workflows/` for GitHub Actions examples
