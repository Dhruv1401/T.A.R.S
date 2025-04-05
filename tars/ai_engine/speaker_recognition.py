import pickle, numpy as np, os
from resemblyzer import VoiceEncoder, preprocess_wav

VOICE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "memory", "voices")
os.makedirs(VOICE_DIR, exist_ok=True)
ENC = VoiceEncoder()

def save_voice_embedding(user: str, emb):
    pickle.dump(emb, open(os.path.join(VOICE_DIR, f"{user}.pkl"), "wb"))

def identify_speaker(wav_path: str) -> str | None:
    emb = ENC.embed_utterance(preprocess_wav(wav_path))
    best, score = None, 0
    for fn in os.listdir(VOICE_DIR):
        user = fn[:-4]
        known = pickle.load(open(os.path.join(VOICE_DIR, fn),"rb"))
        s = np.dot(emb,known)/(np.linalg.norm(emb)*np.linalg.norm(known))
        if s>score:
            best, score = user, s
    return best if score>0.75 else None
