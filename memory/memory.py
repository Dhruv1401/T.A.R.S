import json, os

MEMORY_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'memory')
os.makedirs(MEMORY_DIR, exist_ok=True)

def load_memory(user: str) -> dict:
    path = os.path.join(MEMORY_DIR, f"{user}.json")
    if os.path.exists(path):
        return json.load(open(path))
    return {}

def save_memory(user: str, data: dict):
    path = os.path.join(MEMORY_DIR, f"{user}.json")
    json.dump(data, open(path, 'w'), indent=4)
