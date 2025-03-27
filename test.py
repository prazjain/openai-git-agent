from agents import Agent, Runner
import asyncio
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Answer questions concisely."
)

async def main():
    # First user input
    user_input = "What is the capital of France?"
    result = await Runner.run(agent, user_input)
    print(result.final_output)  # Expected output: "Paris"
    print('Input list ---' * 50)
    print(result.to_input_list())
    print('---' * 50)
    # Retrieve conversation history
    conversation_history = result.to_input_list()

    # Append new user input
    conversation_history.append({"role": "user", "content": "What about Spain?"})

    # Process the next input with conversation history
    result = await Runner.run(agent, conversation_history)
    print(result.final_output)  # Expected output: "Madrid"

    print('Input list ---' * 50)
    print(result.to_input_list())

asyncio.run(main())