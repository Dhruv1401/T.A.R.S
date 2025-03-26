import os
import io
import json
import datetime
import openai
import speech_recognition as sr
import pyttsx3

# Set your API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY_TARS")

# Define the conversation log file (JSON format)
LOG_FILE = "conversation_log.json"

def load_conversation_history():
    """Load conversation history from a JSON log file."""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading conversation log: {e}")
            return []
    else:
        return []

def save_conversation_history(history):
    """Save conversation history to a JSON log file."""
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)   # Adjust speech rate as needed
engine.setProperty("volume", 1.0)   # Maximum volume

def speak(text):
    """Speak out the given text using pyttsx3."""
    engine.say(text)
    engine.runAndWait()

def record_audio():
    """
    Record audio from the microphone and return an in-memory file-like object
    (no audio logs are saved to disk).
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    # Get audio data as WAV bytes and wrap it in a BytesIO object
    audio_bytes = audio.get_wav_data()
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.wav"  # Set a filename attribute (required by some APIs)
    return audio_file

def transcribe_audio(audio_file):
    """Transcribe the in-memory audio file using OpenAI's Whisper API."""
    try:
        transcription = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file
        )
        return transcription
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

def chat_with_gpt(prompt, conversation_history):
    """
    Send the prompt along with past conversation history as context to ChatGPT.
    The conversation_history is a list of {prompt, response} entries.
    """
    try:
        messages = []
        # Add past conversation entries for context
        for entry in conversation_history:
            messages.append({"role": "user", "content": entry["prompt"]})
            messages.append({"role": "assistant", "content": entry["response"]})
        # Add the current prompt
        messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response["choices"][0]["message"]["content"].strip()
        return reply
    except Exception as e:
        print(f"Error during chat completion: {e}")
        return None

def log_conversation(prompt, response):
    """Append the current prompt and response (with timestamp) to the conversation log."""
    history = load_conversation_history()
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "prompt": prompt,
        "response": response
    }
    history.append(entry)
    save_conversation_history(history)

def listen_and_process():
    """Record audio, transcribe it, and return the transcription text."""
    audio_file = record_audio()
    transcription_text = transcribe_audio(audio_file)
    if transcription_text:
        print("Transcription:", transcription_text)
    else:
        print("No transcription available.")
    return transcription_text

def main():
    conversation_history = load_conversation_history()
    speak("Hello, I am your TARS replica. How can I assist you today?")
    
    while True:
        print("Waiting for your command (say 'exit' to quit)...")
        prompt_text = listen_and_process()
        if not prompt_text:
            continue
        if "exit" in prompt_text.lower():
            speak("Goodbye!")
            break
        
        # Get GPT response with conversation history for context ("memory")
        gpt_response = chat_with_gpt(prompt_text, conversation_history)
        if gpt_response:
            print("ChatGPT Response:", gpt_response)
            speak(gpt_response)
            # Log the conversation (prompt and response)
            log_conversation(prompt_text, gpt_response)
            # Reload conversation history to include the latest conversation
            conversation_history = load_conversation_history()
        else:
            print("No response from ChatGPT.")

if __name__ == "__main__":
    main()
