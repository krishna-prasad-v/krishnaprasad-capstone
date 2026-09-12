"""
+------------------------------------------------------------------------------+
| Created by: Krishna Prasad                                                   |
| Created on: 2026-09-06                                                       |
| Program Summary: Sends a question to Claude. Prints the generated answer in  |
|                  as a stream. Streaming is simulated with 2 second delay.    |
| Execution modes:                                                             |
| - Direct execution: Run the program, type the question when prompted.        |
+------------------------------------------------------------------------------+
"""

import os, sys
import time
from dotenv import load_dotenv
from anthropic import Anthropic
load_dotenv()

model = "claude-haiku-4-5-20251001"
client = Anthropic()
lv_width = 100

try:
    width = os.get_terminal_size().columns if sys.stdout.isatty() else lv_width
except:
    width = lv_width

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

messages = []

q = input("Enter your question: ")

add_user_message(messages, q)

print("-" * width)
print(f"Question to LLM: {q}")
print("-" * width)
print("Start of streaming response")
print("-" * width)

with client.messages.stream(
    model=model,
    max_tokens=2000,
    messages=messages
) as stream:
    for text in stream.text_stream:  # text_stream automatically filters and yields only text chunks
        print(text, end="", flush=True)
        time.sleep(2)  # Simulate streaming delay           

print()
print("-" * width)
print("End of streaming response")
print("-" * width)

# You also get .finalMessage after the loop completes for the full message object
final_message = stream.get_final_message()
print("Final message object:")
print("-" * width)
print(final_message)
print("-" * width)

# Output tokens only (Claude's response)
output_tokens = final_message.usage.output_tokens

# Input tokens only (your messages/prompt)
input_tokens = final_message.usage.input_tokens

# Total tokens used
total_tokens = input_tokens + output_tokens

print(f"Input tokens: {input_tokens}")
print(f"Output tokens: {output_tokens}")
print(f"Total tokens: {total_tokens}")
print("-" * width)