import speech_recognition as sr
import tempfile, wave, os
from tars.ai_engine.speaker_recognition import identify_speaker, save_voice_embedding, preprocess_wav, VoiceEncoder

ENC = VoiceEncoder()

def listen_and_identify():
    """Listen, save WAV, identify speaker, return (username, text)."""
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        r.adjust_for_ambient_noise(mic)
        audio = r.listen(mic)
    # save temp wav
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with wave.open(tmp.name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.sample_width)
        wf.setframerate(audio.sample_rate)
        wf.writeframes(audio.get_wav_data())
    # identify or enroll
    user = identify_speaker(tmp.name)
    if not user:
        print("T.A.R.S.: I don't recognize you. What is your name?")
        user = input("You: ").strip()
        emb = ENC.embed_utterance(preprocess_wav(tmp.name))
        save_voice_embedding(user, emb)
    # transcribe
    try:
        text = r.recognize_google(audio)
    except:
        text = ""
    os.unlink(tmp.name)
    return user, text
