import os, pickle, numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path

ENCODER = VoiceEncoder()
VOICE_DIR = Path(__file__).parents[2] / "memory" / "voices"
VOICE_DIR.mkdir(parents=True, exist_ok=True)

def load_voice_embedding(user: str):
    path = VOICE_DIR / f"{user}.pkl"
    return pickle.load(open(path, "rb")) if path.exists() else None

def save_voice_embedding(user: str, emb: np.ndarray):
    pickle.dump(emb, open(VOICE_DIR / f"{user}.pkl", "wb"))

def identify_speaker(audio_path: str) -> str | None:
    wav = preprocess_wav(audio_path)
    emb = ENCODER.embed_utterance(wav)
    best, best_score = None, 0.0
    for file in VOICE_DIR.glob("*.pkl"):
        user = file.stem
        known = pickle.load(open(file, "rb"))
        score = float(np.dot(emb, known) / (np.linalg.norm(emb)*np.linalg.norm(known)))
        if score > best_score:
            best, best_score = user, score
    return best if best_score > 0.75 else None
