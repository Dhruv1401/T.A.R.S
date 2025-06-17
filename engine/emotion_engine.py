import random
import json

# Load parameters from JSON
with open("engine/parameters.json", "r") as f:
    parameters = json.load(f)

def add_emotion(response):
    expressions = [
        "Hmm...", "Interesting.", "Haha!", "Alright.", "Let me think.", "Ah!", "Very well.", "Umm..."
    ]

    # Humor factor adjustment
    if parameters["humor"] > 70:
        expressions.extend(["That cracked me up!", "😂 LOL!", "Hehe."])

    expression = random.choice(expressions)
    return f"{expression} {response}"
