import subprocess
import datetime

def run_llm(prompt):
    try:
        result = subprocess.run(
            ['./llama.cpp/main',
             '-m', 'models/claude2-alpaca-7b.Q4_K_M.gguf',
             '-p', prompt,
             '-n', '500'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error running model: {e}"

def log_conversation(user_input, response):
    date_str = datetime.datetime.now().strftime("%d%m%Y")
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    with open(f'logs/{date_str}.txt', 'a') as log_file:
        log_file.write(f"[{time_str}] User: {user_input}\n")
        log_file.write(f"[{time_str}] TARS: {response}\n\n")
