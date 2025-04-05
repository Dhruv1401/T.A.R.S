import pyttsx3

engine = pyttsx3.init()

def speak(text: str):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()
