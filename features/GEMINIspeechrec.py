from google import genai

client = genai.Client(api_key='GEMINI_API_KEY')

chat = client.aio.chats.create(
    model='gemini-2.5-pro-exp-03-25',  # or gemini-2.0-flash-thinking-exp
)
async def main():
    response = await chat.send_message('What is your name?')
    print(response.text)
    response = await chat.send_message('What did you just say before this?')
    print(response.text)

import asyncio
asyncio.run(main())