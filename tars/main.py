from core.speech_recognition import listen_and_respond
from interfaces.terminal import start_terminal
from llm.engine import get_response

def main():
    print("T.A.R.S. booting up...")
    while True:
        user_input = listen_and_respond()
        if user_input.lower() in ["exit", "quit"]:
            print("T.A.R.S. shutting down. Goodbye!")
            break
        response = get_response(user_input)
        print("T.A.R.S.:", response)

if __name__ == "__main__":
    main()
