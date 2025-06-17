import random

def add_emotion(response):
    expressions = [
        "Hmm...", "Interesting.", "Haha!", "Alright.", "Let me think.", "Ah!", "Very well.", "Umm..."
    ]
    expression = random.choice(expressions)
    return f"{expression} {response}"
