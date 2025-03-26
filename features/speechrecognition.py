import openai
import speech_recognition as sr
import pyttsx3 as pyt
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY_TARS")

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyt.init()

def recognize_speech():
    with sr.Microphone() as source:
        print("Please say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            # Use OpenAI's Whisper model for transcription
            with open("audio.wav", "wb") as f:
                f.write(audio.get_wav_data())

            # Transcribe using OpenAI's Whisper model
            with open("audio.wav", "rb") as audio_file:
                transcription = openai.Audio.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                print(f"You said: {transcription['text']}")
                return transcription['text']
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results from Speech Recognition service.")
            return None

def generate_response(prompt):
    try:
        print("Generating response...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a friendly AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        message = response['choices'][0]['message']['content']
        print(f"AI: {message}")
        return message
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

def speak_text(text):
    if text:
        engine.say(text)
        engine.runAndWait()

if __name__ == "__main__":
    while True:
        speech_text = recognize_speech()
        if speech_text:
            ai_response = generate_response(speech_text)
            speak_text(ai_response)
