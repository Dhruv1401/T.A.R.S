import os, datetime, random, logging
from llama_cpp import Llama
from tars.ai_engine.sentiment import analyze_sentiment
from tars.core.memory import load_memory, save_memory
from tars.memory.profiles import get_user_by_voice, set_user_profile
from tars.ai_engine.speaker_recognition import identify_speaker
from tars.parameters import load_params
from tars.intent import detect_intent  # remove if you truly don't want intent.py

# Load parameters
params = load_params()

# Load GGUF model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "claude2-alpaca-7b.Q4_K_M.gguf")
llm = Llama(model_path=MODEL_PATH, n_ctx=512, n_threads=4)

# Setup daily chat log
BASE_LOG = os.path.join(os.path.dirname(__file__), "..", "..", "chatlogs")
today = datetime.datetime.now().strftime("%Y-%m-%d")
LOG_PATH = os.path.join(BASE_LOG, today, "log.txt")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format="%(asctime)s - %(message)s")

# Thinking fillers
fillers = params.get("thinking_fillers", ["Uhh...", "Hmm...", "Let me think..."])

def get_response(text: str, user: str) -> str:
    # Speaker identification if needed
    if user == "default":
        speaker = identify_speaker(text)
        if speaker:
            user = speaker
        else:
            print("T.A.R.S.: I don't know you. What's your name?")
            name = input("You: ").strip()
            set_user_profile(text, name)
            user = name

    # Sentiment log
    sentiment = analyze_sentiment(text)
    logging.info(f"{user} [{sentiment}]: {text}")

    # Intent (optional)
    intent = detect_intent(text) if 'detect_intent' in globals() else None
    if intent == "exit":
        return "Shutting down. Bye!"
    if intent == "greeting":
        return random.choice(["Hey!", "Hello!", "Yo!"])
    if intent == "ask_name":
        return "I'm T.A.R.S., your tactical assistant."

    # Thinking
    print(random.choice(fillers))

    # LLM call
    prompt = f"{text}\nT.A.R.S.:"
    out = llm(prompt, max_tokens=150,
              temperature=params["humor"],
              top_p=params["honesty"],
              stop=["User:", "T.A.R.S:"])
    reply = out["choices"][0]["text"].strip()

    # Log and memory
    logging.info(f"T.A.R.S.: {reply}")
    mem = load_memory(user)
    mem[datetime.datetime.now().isoformat()] = text
    save_memory(user, mem)

    return reply
