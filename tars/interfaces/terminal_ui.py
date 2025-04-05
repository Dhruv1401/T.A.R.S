from tars.interfaces.voice_input import listen_and_identify
from tars.interfaces.voice_output import speak
from tars.ai_engine.engine import get_response

def run_terminal_ui():
    print("T.A.R.S. Terminal Mode. Say 'exit' to quit.")
    while True:
        user, text = listen_and_identify()
        if text.lower() in ["exit", "quit"]:
            speak("Shutting down. Goodbye!")
            break
        reply = get_response(text, user)
        print(f"T.A.R.S.: {reply}")
        speak(reply)
