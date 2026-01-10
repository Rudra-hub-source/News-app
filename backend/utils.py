from datetime import datetime

def format_iso(dt: datetime) -> str:
    if dt is None:
        return ''
    return dt.isoformat()
