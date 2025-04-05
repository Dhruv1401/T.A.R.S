import os
import datetime
import random
import logging
from pathlib import Path
from llama_cpp import Llama

# === Init Model ===
MODEL_PATH = "tars/llm/claude2-alpaca-7b.Q4_K_M.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=512)

# === Random Thinking Prompts ===
thinking_prompts = ["Hmm...", "Uhh...", "Let me think...", "Interesting...", "Ahh...", "Wait a sec...", "Calculating sarcasm..."]

SYSTEM_PROMPT = """You are T.A.R.S., a sarcastic AI assistant built by Dhruv. 
You are witty, humorous, brutally honest, and sometimes even disrespectful — 
but in a way that entertains your creator, Dhruv. Speak like a human with 
sharp wit, short retorts, and a touch of arrogance, but still help in your own way."""


# === Setup Logging ===
def setup_logger():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    folder_path = Path("chatlogs") / today
    folder_path.mkdir(parents=True, exist_ok=True)
    log_file = folder_path / "chatlog.txt"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        filemode='a'
    )

setup_logger()

# === Chat Loop ===
def chat():
    print("T.A.R.S. is online. Ask me anything...\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("T.A.R.S.: Shutting down. Try not to miss me.")
            break

        # Log user input
        logging.info(f"User: {user_input}")

        # Thinking prompt
        print("T.A.R.S.:", random.choice(thinking_prompts))

        # Get response
        output = llm(f"User: {user_input}\nT.A.R.S.:", max_tokens=200, stop=["User:", "T.A.R.S:"])
        response = output["choices"][0]["text"].strip()

        # Print & log response
        print(f"T.A.R.S.: {response}")
        logging.info(f"T.A.R.S.: {response}")

if __name__ == "__main__":
    chat()
