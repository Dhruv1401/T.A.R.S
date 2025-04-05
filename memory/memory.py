import os, json

DIR = os.path.join(os.path.dirname(__file__))
os.makedirs(DIR, exist_ok=True)

def load_memory(user: str) -> dict:
    path = os.path.join(DIR, f"{user}.json")
    return json.load(open(path)) if os.path.exists(path) else {}

def save_memory(user: str, data: dict):
    json.dump(data, open(os.path.join(DIR, f"{user}.json")), indent=4)
