def start_terminal():
    print("Terminal Interface Online. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        print("T.A.R.S.: Processing...")
