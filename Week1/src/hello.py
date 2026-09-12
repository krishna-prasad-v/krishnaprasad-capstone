"""
+------------------------------------------------------------------------------+
| Created by: Krishna Prasad                                                   |
| Created on: 2026-09-06                                                       |
| Program Summary: Sends a question to Claude. Prints the generated answer or  |
|                  saves the results in a text file based on execution mode    |
| Execution modes:                                                             |
| - Direct execution: Run the program and type the question when prompted.     |
| - Argument execution: Pass the question in quotes after the script name.     |
|    - Example argument: python Week1/src/hello.py "In what scenario is a ThreadPool preferable over asyncio in a Python AI workflow program? - answer in 3 sentences, start each sentence in new line." > Week1/runs/run_04.txt    |
+------------------------------------------------------------------------------+
"""

import os, sys
from dotenv import load_dotenv
from anthropic import Anthropic
load_dotenv()

model = "claude-haiku-4-5-20251001"
lv_width = 100
try:
    width = os.get_terminal_size().columns if sys.stdout.isatty() else lv_width
except:
    width = lv_width


client = Anthropic()

def ask(question):
    response = client.messages.create(
        model = model,
        max_tokens = 4000,
        messages=[
            {"role": "user",   "content": question},
        ],
    )
    return response.content

if __name__ == "__main__":
    print("-" * width)
    print("Hello, what is your question")
    print("-" * width)

    q = sys.argv[1] if len(sys.argv) > 1 else input()

    if len(sys.argv) > 1:
        print(q)
    
    answer = ask(q)

    print("-" * width)

    for block in answer:
        if block.type == "text":
            print(f'{block.text}')
            print("-" * width)