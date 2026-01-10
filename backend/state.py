"""Simple in-memory state storage for demonstration/testing."""
_state = {}

def get(key, default=None):
    return _state.get(key, default)

def set(key, value):
    _state[key] = value

def all_state():
    return dict(_state)
