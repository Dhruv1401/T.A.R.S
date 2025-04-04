import difflib

# Define basic intents and responses
INTENTS = {
    "name": ["what is your name", "who are you", "your name"],
    "greeting": ["hello", "hi", "hey", "greetings"],
    "status": ["how are you", "how's it going", "what's up"],
    "time": ["what time is it", "tell me the time"],
    "date": ["what's the date", "tell me the date"],
    "shutdown": ["shutdown", "turn off", "power down"],
    "exit": ["exit", "quit", "stop listening"],
}

RESPONSES = {
    "name": "I am T.A.R.S., your assistant.",
    "greeting": "Hey! How can I help you today?",
    "status": "I'm fully operational and doing great!",
    "time": "Sorry, I can't tell time yet, but my clock's ticking!",
    "date": "Can't read calendars yet, but we're working on it.",
    "shutdown": "Shutting down systems... goodbye!",
    "exit": "Okay, stopping interaction. Call me when needed.",
    "unknown": "I didn't quite get that. Could you rephrase?"
}

def match_intent(user_input):
    user_input = user_input.lower()

    for intent, patterns in INTENTS.items():
        for pattern in patterns:
            if difflib.SequenceMatcher(None, user_input, pattern).ratio() > 0.75:
                return intent
    return "unknown"

def get_response(prompt):
    intent = match_intent(prompt)
    return RESPONSES.get(intent, RESPONSES["unknown"])
