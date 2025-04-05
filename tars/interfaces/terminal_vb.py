from tars.interfaces.voice_input import listen_and_identify
from tars.interfaces.voice_output import speak
from tars.ai_engine.engine import get_response

def run_terminal_ui():
    """
    Voice+text terminal interface.
    - Identifies speaker by voice.
    - Falls back to text if voice fails.
    """
    print("T.A.R.S. Voice+Text Mode — say 'exit' to quit.")
    while True:
        user, text = listen_and_identify()
        if text.lower() in ("exit", "quit"):
            speak("Shutting down. Goodbye!")
            break
        reply = get_response(text, user=user)
        print(f"T.A.R.S.: {reply}")
        speak(reply)


#Voice Based Terminal UI