import speech_recognition as sr

def listen():
    """Capture and return transcribed speech (empty string if unrecognized)."""
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        r.adjust_for_ambient_noise(mic)
        audio = r.listen(mic)
    try:
        return r.recognize_google(audio)
    except (sr.UnknownValueError, sr.RequestError):
        return ""
