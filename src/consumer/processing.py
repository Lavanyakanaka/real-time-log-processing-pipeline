import json
from typing import Any, Dict, Optional, Set


def parse_message(raw_value: bytes) -> Optional[Dict[str, Any]]:
    try:
        text = raw_value.decode("utf-8")
        return json.loads(text)
    except Exception:
        return None


def should_keep(record: Dict[str, Any], allowed_levels: Set[str]) -> bool:
    level = record.get("level")
    if not isinstance(level, str):
        return False
    return level.upper() in {lvl.upper() for lvl in allowed_levels}
