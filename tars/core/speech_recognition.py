import speech_recognition as sr

def listen_and_respond():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "I didn't get that."
    except sr.RequestError:
        return "Speech service error."
