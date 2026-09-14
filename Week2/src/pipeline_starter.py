# Program created by: Krishna Prasad
# Created on: 13 September 2026
# Pipeline steps:
# 1. Read questions from a CSV file (Week2/data/questions.csv)
# 2. Send the questions to the LLM in chunks of 5 questions at a time  
# 3. Send the questions in each chunk to the LLM in parallel using asyncio.create_task()
# 4. Each chunk of questions is processed sequentially.

import os, sys
import asyncio
import csv
from pathlib import Path
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from pydantic_classes import Question, Answer
load_dotenv()

client = AsyncAnthropic()
model = "claude-haiku-4-5-20251001"

def read_questions_from_csv(csv_file_path: Path) -> list[Question]:
    question_list = []
    with open(csv_file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the 'text' header line
        question_list = [Question(text=row[0].strip()) for row in reader if row]
    return question_list


async def ask_llm(question: Question) -> Answer:
     response = await client.messages.create(
        model = model,
        max_tokens = 1000,
        system = "You are a helpful expert in Applied AI. Answer all questions in 2 sentences.",
        messages = [{"role": "user", "content": question.text}],
    )

     for block in response.content:
        if block.type == "text":
            return Answer(question = question.text, text = block.text)
            

async def main():
    csv_path = Path("Week2/data/questions.csv")
#   answer_list = []

# Read questions from the CSV file and create a list of Question objects
    question_list = read_questions_from_csv(csv_path)

# Process question_list in chunks of 5
    for i in range(0, len(question_list), 5):
        chunk_list = question_list[i: i + 5]
        
        print(f"\nstart of processing: questions {i + 1} to {i + len(chunk_list)}")

        tasks = [asyncio.create_task(ask_llm(q)) for q in chunk_list] 
        chunk_ans_list = await asyncio.gather(*tasks)

        for answer in chunk_ans_list:
            print(f"Q: {answer.question}\nA: {answer.text}\n")

        print(f"\nend of processing: questions {i + 1} to {i + len(chunk_list)}")

# Add the answers from the current chunk to the overall answer list, if required
#       answer_list.extend(chunk_ans_list)

if __name__ == "__main__":
    asyncio.run(main())