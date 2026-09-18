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
import logging
from pathlib import Path
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from pydantic_classes import Question, Answer
from logging_setup import configure_logging
load_dotenv()
logger = logging.getLogger(__name__)

client = AsyncAnthropic()
model = "claude-haiku-4-5-20251001"

#********************************************************************************************
# Read questions from CSV file
#********************************************************************************************
def read_questions_from_csv(csv_file_path: Path) -> list[Question]:
    question_list = []
    with open(csv_file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the 'text' header line
        question_list = [Question(text=row[0].strip()) for row in reader if row]
        logger.info(f"Successfully loaded {len(question_list)} questions from {csv_file_path}")
    return question_list

#********************************************************************************************
# Call the LLM with the question and return the answer
#********************************************************************************************
async def ask_llm(question: Question) -> Answer:
    logger.debug(f"Sending prompt to model '{model}' for question: {question.text}")
    response = await client.messages.create(
        model = model,
        max_tokens = 1000,
        system = "You are a helpful expert in Applied AI. Answer all questions in 2 sentences.",
        messages = [{"role": "user", "content": question.text}],
    )
    logger.debug(f"Received response from model '{model}' for question: {question.text}")

# Normally, with no tool use involved, Claude returns a single text block.
# However, the API can return multiple text blocks if thinking is involved.
# In newer Claude models, thinking is done by default/whenever required.
# So it is better to handle multiple text blocks.
    text_parts = [block.text for block in response.content if block.type == "text"]
    if not text_parts:
        raise ValueError("No text block found in the response.")

    logger.debug(f"Extracted ({len(text_parts)} text parts) from response for question: {question.text}")
    return Answer(question=question.text, text="".join(text_parts))

#********************************************************************************************
# wrap the rety logic around the ask_llm function
#********************************************************************************************
async def ask_llm_with_retry(question: Question, max_retries: int = 3) -> Answer:
    max_retries = max_retries + 1  # Adjust for initial attempt
    for attempt in range(max_retries):
        if attempt == 0:
            logger.info(f"Initial attempt for question: {question.text}")

        try:
            ans = await ask_llm(question)
            ans.retries = attempt  # 0 represents no retries (first attempt successful)
            return ans
        except ValueError as ve:
            logger.exception(f"ValueError from LLM API call: {question.text}.")
            raise  
        except Exception as e:
            if attempt == max_retries:
                logger.exception(f"Max retries reached for question: {question.text}.")
                raise  # Re-raise the exception if max retries reached
            else:
                logger.warning(f"Retry attempt: {attempt} for question: {question.text}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff 

#********************************************************************************************
# main()
#********************************************************************************************            
async def main():
    configure_logging(logging.INFO)
    csv_path = Path("Week2/data/questions.csv")
    logger.info("Pipeline started.")

# currently not used, but can be used to store all answers if needed
#   answer_list = []  

# Read questions from the CSV file and create a list of Question objects
    question_list = read_questions_from_csv(csv_path)

# Process question_list in chunks of 5
    for i in range(0, len(question_list), 5):
        chunk_list = question_list[i: i + 5]
        logger.info(f"Pipeline: Processing questions {i + 1} to {i + len(chunk_list)}")
        print(f"\nstart of processing: questions {i + 1} to {i + len(chunk_list)}")

        tasks = [asyncio.create_task(ask_llm_with_retry(q)) for q in chunk_list] 
        chunk_ans_list = await asyncio.gather(*tasks, return_exceptions=True)

        for answer in chunk_ans_list:
            if isinstance(answer, Exception):
                print(f"Failed to process the question")
            else:    
                print(f"Q: {answer.question}\nA: {answer.text}\n")

        logger.info(f"Pipeline: Finished processing questions {i + 1} to {i + len(chunk_list)}\n")
        print(f"\nend of processing: questions {i + 1} to {i + len(chunk_list)}")

# Add the answers from the current chunk to the overall answer list, if required
#       answer_list.extend(chunk_ans_list)

    logger.info("Pipeline Ended.")

if __name__ == "__main__":
    asyncio.run(main())