import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import speech_recognition as sr
import pyttsx3

# Configure logging to save conversation history to a file.
logging.basicConfig(
    filename='chat_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def log_message(message: str):
    """Log a message to the chat log file."""
    logging.info(message)

def load_conversational_model(model_name="microsoft/DialoGPT-small"):
    """Load the pre-trained conversational model and tokenizer."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

def speak_text(engine, text):
    """Speak the given text using the pyttsx3 engine."""
    engine.say(text)
    engine.runAndWait()

def get_audio_input(recognizer, microphone):
    """Capture audio input from the microphone and return recognized text."""
    with microphone as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("User: " + text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return None

def main():
    # Initialize speech recognizer, microphone, and TTS engine.
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    engine = pyttsx3.init()
    
    # Load the conversational model and tokenizer.
    tokenizer, model = load_conversational_model()
    chat_history_ids = None
    
    # Initial greeting.
    greeting = "Hello, I'm TARS, your friendly AI robot. How can I help you today?"
    print("TARS: " + greeting)
    speak_text(engine, greeting)
    
    while True:
        print("\nPlease say something (or say 'exit' to quit):")
        user_input = get_audio_input(recognizer, microphone)
        if user_input is None:
            continue  # Try again if audio wasn't clear.
        if user_input.lower() in ["exit", "quit"]:
            farewell = "Goodbye!"
            print("TARS: " + farewell)
            speak_text(engine, farewell)
            break
        
        log_message("User: " + user_input)
        
        # Prepare input for the model.
        new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids
        
        # Generate a response.
        chat_history_ids = model.generate(
            bot_input_ids, 
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            top_k=50,
            top_p=0.95
        )
        
        # Decode the AI's response.
        ai_output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print("TARS: " + ai_output)
        speak_text(engine, ai_output)
        log_message("TARS: " + ai_output)

if __name__ == "__main__":
    main()
