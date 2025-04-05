import os, datetime, random, logging, wave, tempfile
from llama_cpp import Llama
from tars.core.sentiment import analyze_sentiment
from tars.core.memory import load_memory, save_memory
from tars.core.profiles import get_user_by_voice, set_user_profile
from tars.core.speaker_recognition import identify_speaker, save_voice_embedding, preprocess_wav, ENCODER
from tars.intent import detect_intent
from tars.parameters import load_params

# Load parameters
params = load_params()

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "claude2-alpaca-7b.Q4_K_M.gguf")
llm = Llama(model_path=MODEL_PATH, n_ctx=512, n_threads=4)

# Setup chatlogs
LOG_BASE = os.path.join(os.path.dirname(__file__), "..", "..", "chatlogs")
os.makedirs(LOG_BASE, exist_ok=True)
today = datetime.datetime.now().strftime("%Y-%m-%d")
LOG_FILE = os.path.join(LOG_BASE, today, "log.txt")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# Thinking fillers
fillers = ["Uhh...", "Hmm...", "Let me think...", "Calculating...", "Ahh..."]

def record_and_identify(recognizer, mic):
    audio = recognizer.listen(mic)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = tmp.name
        with wave.open(wav_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio.sample_width)
            wf.setframerate(audio.sample_rate)
            wf.writeframes(audio.get_wav_data())
    speaker = identify_speaker(wav_path)
    if not speaker:
        print("T.A.R.S.: I don't recognize your voice. What is your name?")
        name = input("You: ").strip()
        emb = ENCODER.embed_utterance(preprocess_wav(wav_path))
        save_voice_embedding(name, emb)
        set_user_profile(wav_path, name)
        speaker = name
    return speaker, recognizer.recognize_google(audio)

def get_response(user_input: str, user: str) -> str:
    # Log and sentiment
    sentiment = analyze_sentiment(user_input)
    logging.info(f"{user} [{sentiment}]: {user_input}")

    # Intent
    intent = detect_intent(user_input)
    if intent == "exit":
        return "Shutting down. Bye!"
    if intent == "greeting":
        return random.choice(["Hey there!", "Hello!", "What's up?"])
    if intent == "ask_name":
        return "I'm T.A.R.S., your tactical assistant."
    if intent == "ask_time":
        return datetime.datetime.now().strftime("It's %H:%M now.")
    if intent == "ask_date":
        return datetime.datetime.now().strftime("Today is %Y-%m-%d.")

    # Thinking filler
    print(random.choice(fillers))

    # Build prompt
    prompt = f"{SYSTEM_PROMPT}\\nUser: {user_input}\\nT.A.R.S.:"
    resp = llm(prompt, max_tokens=150, temperature=params["humor"], top_p=params["honesty"], stop=["User:", "T.A.R.S:"])
    reply = resp["choices"][0]["text"].strip()

    # Log reply
    logging.info(f"T.A.R.S.: {reply}")
    # Save memory
    mem = load_memory(user)
    mem[datetime.datetime.now().isoformat()] = user_input
    save_memory(user, mem)

    return reply
