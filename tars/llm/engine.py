from llama_cpp import Llama
import os

# Path to your model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "claude2-alpaca-7b.Q4_K_M.gguf")

# Load the model
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=512,  # You can increase this depending on model support
    verbose=False  # Set to True if you want debug logs
)

# Get response from the local model
def get_response(prompt: str) -> str:
    response = llm(prompt, max_tokens=150, temperature=0.7, stop=["</s>"])
    return response["choices"][0]["text"].strip()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        print("T.A.R.S.:", get_response(user_input))
