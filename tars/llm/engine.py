from llama_cpp import Llama
import os

conversation_history = []
user_profile = {"name": "Dhruv"}  # Can be expanded later

# Path to your model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.gguf")

# Load the model
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=512,  # You can increase this depending on model support
    verbose=False  # Set to True if you want debug logs
)

# Get response from the local model
def get_response(prompt: str) -> str:
    conversation_history.append(f"User: {prompt}")
    
    system_prompt = (
        f"You are T.A.R.S., a helpful, arrogant,proud and clever AI assistant created by {user_profile['name']}. "
        "You never ramble and always provide very sarcastic answers. "
        "You remember what the user tells you during the conversation.\n"
    )
    
    history = "\n".join(conversation_history[-5:])  # limit context to last 5 turns

    full_prompt = f"{system_prompt}\n{history}\nT.A.R.S.:"
    response = llm(full_prompt, max_tokens=150, temperature=0.7, stop=["User:", "T.A.R.S.:"])
    
    reply = response["choices"][0]["text"].strip()
    conversation_history.append(f"T.A.R.S.: {reply}")
    
    return reply

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        print("T.A.R.S.:", get_response(user_input))
