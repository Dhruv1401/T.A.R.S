import speech_recognition as sr
from tars.llm.engine import record_and_identify

def listen_and_identify():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        speaker, text = record_and_identify(recognizer, source)
    return speaker, text
