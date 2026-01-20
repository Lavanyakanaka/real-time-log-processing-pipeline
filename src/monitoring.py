"""
Monitoring utilities for the Real-time Log Processing Pipeline

This module provides functionality for tracking metrics and monitoring
the performance of producer and consumer services.
"""

import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional


class MetricsCollector:
    """Collects and aggregates pipeline metrics"""

    def __init__(self):
        self.start_time = datetime.now(timezone.utc)
        self.messages_processed = 0
        self.messages_filtered_out = 0
        self.errors_encountered = 0
        self.last_update_time = self.start_time

    def record_message_processed(self):
        """Record a message that was processed"""
        self.messages_processed += 1
        self.last_update_time = datetime.now(timezone.utc)

    def record_message_filtered(self):
        """Record a message that was filtered out"""
        self.messages_filtered_out += 1
        self.last_update_time = datetime.now(timezone.utc)

    def record_error(self):
        """Record an error occurrence"""
        self.errors_encountered += 1
        self.last_update_time = datetime.now(timezone.utc)

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot"""
        elapsed = (self.last_update_time - self.start_time).total_seconds()
        total_messages = self.messages_processed + self.messages_filtered_out

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": elapsed,
            "messages_processed": self.messages_processed,
            "messages_filtered_out": self.messages_filtered_out,
            "total_messages_seen": total_messages,
            "errors": self.errors_encountered,
            "throughput_msgs_per_sec": (
                total_messages / elapsed if elapsed > 0 else 0
            ),
            "filter_rate_percent": (
                (self.messages_filtered_out / total_messages * 100)
                if total_messages > 0
                else 0
            ),
        }

    def get_metrics_json(self) -> str:
        """Get metrics as JSON string"""
        return json.dumps(self.get_metrics(), indent=2)

    def reset(self):
        """Reset all metrics"""
        self.start_time = datetime.now(timezone.utc)
        self.messages_processed = 0
        self.messages_filtered_out = 0
        self.errors_encountered = 0
        self.last_update_time = self.start_time


class LogStatistics:
    """Tracks statistics about logs processed"""

    def __init__(self):
        self.level_counts: Dict[str, int] = {}
        self.service_counts: Dict[str, int] = {}

    def record_log(self, record: Dict[str, Any]):
        """Record statistics from a log record"""
        level = record.get("level", "UNKNOWN")
        self.level_counts[level] = self.level_counts.get(level, 0) + 1

        service = record.get("service_name", "UNKNOWN")
        self.service_counts[service] = self.service_counts.get(service, 0) + 1

    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        return {
            "by_level": self.level_counts,
            "by_service": self.service_counts,
            "total_unique_levels": len(self.level_counts),
            "total_unique_services": len(self.service_counts),
        }

    def get_stats_json(self) -> str:
        """Get statistics as JSON string"""
        return json.dumps(self.get_stats(), indent=2)

    def reset(self):
        """Reset all statistics"""
        self.level_counts.clear()
        self.service_counts.clear()


class HealthStatus:
    """Tracks the health status of services"""

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.is_healthy = True
        self.last_check_time = datetime.now(timezone.utc)
        self.error_message: Optional[str] = None

    def mark_healthy(self):
        """Mark service as healthy"""
        self.is_healthy = True
        self.error_message = None
        self.last_check_time = datetime.now(timezone.utc)

    def mark_unhealthy(self, error_message: str):
        """Mark service as unhealthy with error message"""
        self.is_healthy = False
        self.error_message = error_message
        self.last_check_time = datetime.now(timezone.utc)

    def get_status(self) -> Dict[str, Any]:
        """Get current health status"""
        return {
            "service": self.service_name,
            "status": "healthy" if self.is_healthy else "unhealthy",
            "last_check": self.last_check_time.isoformat(),
            "error": self.error_message,
        }

    def get_status_json(self) -> str:
        """Get status as JSON string"""
        return json.dumps(self.get_status(), indent=2)
