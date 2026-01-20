from src.consumer.processing import parse_message, should_keep


def test_parse_message_valid():
    raw = b'{"level": "ERROR", "message": "Something bad"}'
    record = parse_message(raw)
    assert record is not None
    assert record["level"] == "ERROR"


def test_parse_message_invalid_json():
    raw = b'{"level": "ERROR", "message": "missing brace"'
    record = parse_message(raw)
    assert record is None


def test_should_keep_error_level():
    record = {"level": "ERROR"}
    assert should_keep(record, {"ERROR", "WARN"}) is True


def test_should_keep_info_level_filtered_out():
    record = {"level": "INFO"}
    assert should_keep(record, {"ERROR", "WARN"}) is False


def test_should_keep_missing_level():
    record = {"message": "no level"}
    assert should_keep(record, {"ERROR", "WARN"}) is False
