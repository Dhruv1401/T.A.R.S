import json, os

PROFILES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'memory', 'profiles.json')
os.makedirs(os.path.dirname(PROFILES_PATH), exist_ok=True)
if not os.path.exists(PROFILES_PATH):
    json.dump({}, open(PROFILES_PATH, 'w'))

def load_profiles() -> dict:
    return json.load(open(PROFILES_PATH))

def save_profiles(profiles: dict):
    json.dump(profiles, open(PROFILES_PATH, 'w'), indent=4)

def get_user_by_voice(voice_id: str) -> str | None:
    return load_profiles().get(voice_id)

def set_user_profile(voice_id: str, name: str):
    profiles = load_profiles()
    profiles[voice_id] = name
    save_profiles(profiles)
