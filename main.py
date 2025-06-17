import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from interface import text_interface, voice_interface # type: ignore
from engine import engine as tars_engine
from engine import speech_recognition, emotion_engine


def main():
    while True:
        print("\nChoose mode:\n1. Text\n2. Voice\n3. Exit")
        choice = input("Option: ")

        if choice == '1':
            user_input = text_interface.get_text_input()
        elif choice == '2':
            user_input = speech_recognition.recognize_speech()
            if user_input is None:
                continue
        elif choice == '3':
            break
        else:
            print("Invalid option.")
            continue

        response = tars_engine.run_llm(user_input)
        response_with_emotion = emotion_engine.add_emotion(response)
        tars_engine.log_conversation(user_input, response_with_emotion)
        voice_interface.speak(response_with_emotion)

if __name__ == "__main__":
    main()
