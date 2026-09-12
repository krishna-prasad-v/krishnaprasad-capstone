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

stream = client.messages.create(
    model=model,
    max_tokens=2000,
    messages=messages,
    stream=True    # returns a generator - Stream[MessageStreamEvent]
)
print("-" * width)
print(f"Question to LLM: {q}")
print("-" * width)
print("Start of streaming response")
print("-" * width)

# Loop through the stream and print the content blocks as they arrive
for event in stream:
    if  event.type == 'content_block_delta':
        if event.delta.type == "text_delta":
            print(event.delta.text, end="", flush=True) 
            time.sleep(2)  # Simulate streaming delay

print()
print("-" * width)
print("End of streaming response")
print("-" * width)

# How the streaming works: a sample output of the raw stream response is as below:
# Content blocks have an index - in this case, index = 0.
# In the Anthropic streaming protocol, content blocks are strictly sequential and never interleaved or parallel.
# Content block (index = 1) will never start until content block(index = 0) has completely finished with a RawContentBlockStopEvent.
# Content blocks can be of different types. In this example, we have only text content blocks.
# Text content blocks can have multiple delta events, each containing a portion of the text. 
# The "text" field in the delta event contains the actual text content. 
# This "text" should be printed for every content block delta sequentially as they arrive.
# The "type" field indicates that this is a text delta.
# Depending on what Claude is generating, event.content_block will be an instance of one of these classes:
#  -  TextBlock, ToolUseBlock, ThinkingBlock
# Similarly, event.delta will be an instance of one of these classes:
#  -  TextDelta, InputJSONDelta, ThinkingDelta
#*********************************************************************************************************************************************************************************************************************************************************************************************************************************
# RawMessageStartEvent(
#          message=Message(
#                          id='msg_011CeqJVwt6W1rJfU1g8hZLp', 
#                          container=None, 
#                          content=[], 
#                          model='claude-haiku-4-5-20251001', 
#                          role='assistant', 
#                          stop_details=None, 
#                          stop_reason=None, 
#                          stop_sequence=None, 
#                          type='message', 
#                          usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo='not_available', input_tokens=22, output_tokens=1, output_tokens_details=None, server_tool_use=None, service_tier='standard')
#                         ), 
#         type='message_start'
#                     )
# RawContentBlockStartEvent(
#                           content_block=TextBlock(
#                                                   citations=None, 
#                                                   text='', 
#                                                   type='text'), 
#                           index=0, 
#                           type='content_block_start'
#                          )

# RawContentBlockDeltaEvent(
#                           delta=TextDelta(
#  -->> print this                          text='#',             
#                                           type='text_delta'),     --> before printing text, ensure type is "text_delta"
#                           index=0, 
#                           type='content_block_delta')

# RawContentBlockDeltaEvent(
#                           delta=TextDelta(
#  -->> print this                          text=' ThreadPoolExecutor in Python\n\nThreadPoolExecutor is a class from the `concurrent.futures` module that manages a pool of worker threads to execute tasks concurr', 
#                                           type='text_delta'), 
#                           index=0, 
#                           type='content_block_delta')

# RawContentBlockDeltaEvent(delta=TextDelta(
# -->> print this                           text='ently, allowing you to submit multiple functions to run in parallel and retrieve their results.', 
#                                           type='text_delta'), 
#                            index=0, 
#                            type='content_block_delta')

# RawContentBlockStopEvent(index=0, type='content_block_stop')

# RawMessageDeltaEvent(
#                       delta=Delta(
#                                   container=None, 
#                                   stop_details=None, 
# -->> note this stop_reason        stop_reason='end_turn', 
#                                   stop_sequence=None
#                                   ), 
#                        type='message_delta', 
#                        usage=MessageDeltaUsage(cache_creation_input_tokens=0, cache_read_input_tokens=0, input_tokens=22, output_tokens=55, output_tokens_details=None, server_tool_use=None)
#                     )
#
# RawMessageStopEvent(type='message_stop')
#**********************************************************************************************************************************************************************************************************************************************************************************************************************************