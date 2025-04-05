from tars.ai_engine.engine import get_response

def run_terminal():
    """Simple text-only chat loop."""
    print("T.A.R.S. Text Mode — type 'exit' to quit.")
    while True:
        text = input("You: ").strip()
        if text.lower() in ("exit", "quit"):
            print("T.A.R.S.: Goodbye!")
            break
        reply = get_response(text, user="default")
        print(f"T.A.R.S.: {reply}")

#Use only for text-based I/O