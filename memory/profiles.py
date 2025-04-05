import os, json

PATH = os.path.join(os.path.dirname(__file__), "profiles.json")
if not os.path.exists(PATH):
    json.dump({}, open(PATH,"w"))

def load_profiles() -> dict:
    return json.load(open(PATH))

def save_profiles(p: dict):
    json.dump(p, open(PATH,"w"), indent=4)

def set_user_profile(voice_id: str, name: str):
    p = load_profiles()
    p[voice_id] = name
    save_profiles(p)

def get_user_by_voice(voice_id: str) -> str | None:
    return load_profiles().get(voice_id)
