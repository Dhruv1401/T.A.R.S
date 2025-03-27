import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import speech_recognition as sr
import pyttsx3

# Configure logging to save conversation history.
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
    # Explicitly set the pad token ID to avoid attention mask warnings.
    model.config.pad_token_id = tokenizer.eos_token_id
    return tokenizer, model

def speak_text(engine, text):
    """Convert text to speech using pyttsx3."""
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
    
    # Load model and tokenizer.
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
            continue  # Retry if the input wasn't clear.
        if user_input.lower() in ["exit", "quit"]:
            farewell = "Goodbye!"
            print("TARS: " + farewell)
            speak_text(engine, farewell)
            break
        
        log_message("User: " + user_input)
        
        # Encode the user input.
        new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
        
        # Append new input to conversation history.
        if chat_history_ids is not None:
            bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
        else:
            bot_input_ids = new_input_ids

        # Create an attention mask explicitly.
        attention_mask = torch.ones_like(bot_input_ids)
        
        # Generate a response using tuned generation parameters.
        chat_history_ids = model.generate(
            bot_input_ids,
            attention_mask=attention_mask,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.1,       # Lower temperature for more coherent responses.
            top_k=50,
            top_p=0.95,
            repetition_penalty=1.2
        )
        
        # Extract only the newly generated tokens.
        ai_output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print("TARS: " + ai_output)
        speak_text(engine, ai_output)
        log_message("TARS: " + ai_output)
        
        # Optional: Reset conversation history periodically if output drifts.
        if chat_history_ids.shape[-1] > 1500:
            chat_history_ids = None

if __name__ == "__main__":
    main()
