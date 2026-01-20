from src.consumer.processing import parse_message, should_keep


def test_parse_message_valid():
    """Test parsing valid JSON log message"""
    raw = b'{"level": "ERROR", "message": "Something bad"}'
    record = parse_message(raw)
    assert record is not None
    assert record["level"] == "ERROR"


def test_parse_message_invalid_json():
    """Test handling of invalid JSON"""
    raw = b'{"level": "ERROR", "message": "missing brace"'
    record = parse_message(raw)
    assert record is None


def test_should_keep_error_level():
    """Test filtering ERROR level logs"""
    record = {"level": "ERROR"}
    assert should_keep(record, {"ERROR", "WARN"}) is True


def test_should_keep_info_level_filtered_out():
    """Test filtering out INFO level logs"""
    record = {"level": "INFO"}
    assert should_keep(record, {"ERROR", "WARN"}) is False


def test_should_keep_missing_level():
    """Test handling logs with missing level"""
    record = {"message": "no level"}
    assert should_keep(record, {"ERROR", "WARN"}) is False


def test_parse_message_with_trace_id():
    """Test parsing message with trace ID"""
    raw = b'{"level": "WARN", "message": "DB slow", "trace_id": "abc123"}'
    record = parse_message(raw)
    assert record is not None
    assert record["trace_id"] == "abc123"


def test_should_keep_case_insensitive():
    """Test case-insensitive level filtering"""
    record = {"level": "error"}
    assert should_keep(record, {"ERROR", "WARN"}) is True


def test_parse_message_with_timestamp():
    """Test parsing message with timestamp"""
    raw = b'{"level": "ERROR", "timestamp": "2026-01-20T10:30:45.123456Z", "service": "auth"}'
    record = parse_message(raw)
    assert record is not None
    assert record["timestamp"] == "2026-01-20T10:30:45.123456Z"


def test_should_keep_multiple_levels():
    """Test filtering with multiple allowed levels"""
    record_error = {"level": "ERROR"}
    record_warn = {"level": "WARN"}
    record_info = {"level": "INFO"}

    allowed = {"ERROR", "WARN"}
    assert should_keep(record_error, allowed) is True
    assert should_keep(record_warn, allowed) is True
    assert should_keep(record_info, allowed) is False


def test_parse_message_unicode():
    """Test parsing message with unicode characters"""
    raw = '{"level": "ERROR", "message": "Errör occurred"}'.encode('utf-8')
    record = parse_message(raw)
    assert record is not None
    assert record["message"] == "Errör occurred"


def test_should_keep_non_string_level():
    """Test handling non-string level values"""
    record = {"level": 123}
    assert should_keep(record, {"ERROR", "WARN"}) is False


def test_parse_message_nested_json():
    """Test parsing message with nested JSON structure"""
    raw = b'{"level": "ERROR", "metadata": {"service": "api", "version": "1.0"}}'
    record = parse_message(raw)
    assert record is not None
    assert record["metadata"]["service"] == "api"


def test_parse_message_empty_bytes():
    """Test parsing empty bytes"""
    raw = b''
    record = parse_message(raw)
    assert record is None


def test_should_keep_empty_level():
    """Test handling empty level string"""
    record = {"level": ""}
    assert should_keep(record, {"ERROR", "WARN"}) is False

