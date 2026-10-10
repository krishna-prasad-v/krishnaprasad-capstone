# Program created by: Krishna Prasad
# Created on: 10 October 2026
# This is a demo program on naive RAG using Claude LLM.
# Source file used is: ./Week6/corpus_files/ABAP_Objects.md
# import voyageai
import os, sys
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic, AnthropicError
from helpers import *
load_dotenv()
client = Anthropic()
model = "claude-haiku-5-5"
# model = "claude-sonnet-5-5"

#********************************************************************************************
# Call the LLM with the question and return the answer
#********************************************************************************************
def ask_llm(question: str, ordered_matches: list[dict], system_prompt: str) -> str:
    """
    Constructs a prompt using the question and the ordered chunks, 
    then sends it to the LLM for an answer.
    """
    # Construct the prompt with the question and the ordered chunks
    context_text = "\n\n".join([f"Chunk {match['chunk_id']}:\n{match['text']}" for match in ordered_matches])
    prompt = f"Answer the following question.\n\nContext:\n{context_text}\n\nQuestion: {question}\n\n"

    try:
        response = client.messages.create(
            model=model,
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}],
        )
    except AnthropicError as e:
        print(f"Error calling LLM: {e}")
        sys.exit(1)

    # Extract text from response
    text_parts = [block.text for block in response.content if block.type == "text"]
    if not text_parts:
        raise ValueError("No text block found in the response.")

    return "\n".join(text_parts)

#********************************************************************************************
# main()
#******************************************************************************************** 
def main():
    file_path  = Path(__file__).resolve().parent.parent / "corpus_files" / "object_oriented_abap_knowledge_base.md"

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunk_list = chunk_by_size(text, chunk_size=600, overlap=150)

    # for index, chunk in enumerate(chunk_list):
    #     print(f"Chunk {index+1}: {chunk}\n{'-'*40}\n")

    try:
        embeddings = generate_embeddings(chunk_list, input_type="document")
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        sys.exit(1)    

    # ─── Step 1: Pair chunks and embeddings into an index ───────────
    index = []
    chunk_number = 1
    for chunk_text, vector in zip(chunk_list, embeddings):
        index.append({
            "chunk_id": chunk_number,
            "text": chunk_text,
            "vector": vector
        })
        chunk_number += 1

    user_query = "What is a Final class?"

    try:
        query_vector = generate_embeddings(user_query, input_type="query")   
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        sys.exit(1)      

    top_matches = retrieve_top_k(query_vector, index, k=3)

    # Re-order the top k matches by chunk_id - so that they are in the order they appear in the original document
    ordered_matches = reorder_chunks_by_document(top_matches)

    # for match in ordered_matches:
    #     print(f"\n--- Chunk ID: {match['chunk_id']} (Score: {match['score']:.4f}) ---")
    #     print(match["text"])

    answer = ask_llm(user_query, ordered_matches, system_prompt=system_prompt_strict)

    print(f"\n\nuser_query: {user_query}")
    print(f"\n\n--- LLM Answer ---\n{answer}\n\n")

if __name__ == "__main__":
    main()