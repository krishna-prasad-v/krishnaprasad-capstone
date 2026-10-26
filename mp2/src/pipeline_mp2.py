from __future__ import annotations
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from openai import OpenAI
from mp2_helpers import chunk_by_size
import uuid
load_dotenv()
assert os.environ.get('OPENAI_API_KEY'), 'Set OPENAI_API_KEY first'
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, PointStruct, VectorParams

# ─── Configuration ──────────────────────────────────────────────────────

CORPUS_DIR        = Path(__file__).resolve().parent.parent / "corpus"
DATA_DIR          = Path(__file__).resolve().parent.parent / "data"
COLLECTION_NAME   = "mp2_sherlock"
EMBEDDING_MODEL   = "text-embedding-3-small"
EMBEDDING_DIM     = 1536
CHAT_MODEL        = "gpt-4o-mini"
TARGET_CHUNK_SIZE = 500   # characters
CHUNK_OVERLAP     = 100    # characters

openai = OpenAI()
qdrant = QdrantClient(
    url=os.environ["QDRANT_URL"],
    api_key=os.environ.get("QDRANT_API_KEY"), )

print(qdrant.get_collections())

# ─── Step 1: Load the corpus ────────────────────────────────────────────

def load_corpus(corpus_dir: Path) -> list[dict[str, Any]]:
    """Load all .txt files in the corpus directory into a list of dictionaries"""

    if not corpus_dir.is_dir():
        raise FileNotFoundError(f"Corpus directory not found: {corpus_dir}")
  
    docs_dict = []
  
    for file in sorted(corpus_dir.glob("*.txt")):
        text = file.read_text(encoding="utf-8")
        non_empty_lines_generator = (line.strip() for line in text.splitlines() if line.strip())
        title = next(non_empty_lines_generator, None)
        docs_dict.append({
            "source": file.name, 
            "title": title, 
            "text": text})

    return docs_dict  

# ─── Step 2: Chunk each document ────────────────────────────────────────

def chunk_document(doc: dict[str, Any]) -> list[dict[str, Any]]:
    """Splits a document into chunks of text with metadata"""

    doc_text_chunks = chunk_by_size(doc["text"], chunk_size=TARGET_CHUNK_SIZE, overlap=CHUNK_OVERLAP)

    chunks = []
    
    for text in doc_text_chunks:
        single_chunk = {
            "source": doc["source"],
            "title": doc["title"],
            "section": "N/A",
            "text": text,    }
        chunks.append(single_chunk)

    return chunks   

# ─── Step 3: Embed text ─────────────────────────────────────────────────

def embed_texts(texts: list[str]) -> list[list[float]]:
    """Batch-embed a list of texts using OpenAI's embedding model.
    Returns a list of 1536-dim float vectors (same order as inputs)."""

    if not texts:
        return []

    response = openai.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,  )
    # Sort by index to guarantee the same order as inputs
    embeddings_list = [item.embedding for item in sorted(response.data, key=lambda d: d.index)]
    if not embeddings_list :
        raise ValueError("Embedding API returned no embeddings.")
    if len(embeddings_list) != len(texts):      
        raise ValueError("Embedding API returned unexpected number of embeddings.")
    return embeddings_list  # list of vectors


# ─── Step 4: Set up the Qdrant collection ───────────────────────────────

def setup_collection() -> None:
    """Create (or recreate) the Qdrant collection. """

    if qdrant.collection_exists(COLLECTION_NAME):
        qdrant.delete_collection(collection_name=COLLECTION_NAME)

    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    )

    qdrant.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="source",
    field_schema=models.PayloadSchemaType.KEYWORD, )

# ─── Step 5: Ingest chunks into Qdrant ──────────────────────────────────

def ingest_chunks(chunks: list[dict[str, Any]]) -> None:
    """Embed every chunk and upsert into Qdrant"""
    if not chunks:
        return
    
    text_list = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(text_list)

    points = []
    for chunk, embedding in zip(chunks, embeddings):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload=chunk,     )
        points.append(point)

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)    

# ─── Step 6: Retrieve ───────────────────────────────────────────────────

def retrieve(query: str, k: int = 3) -> list[dict[str, Any]]:
    """Retrieve top-k chunks for a query"""

    embeddings = embed_texts([query])
    query_vector = embeddings[0] 

    response = qdrant.query_points(
       collection_name=COLLECTION_NAME,
       query=query_vector,
       limit=k,
       with_payload=True,    )

    top_k_chunks = []

    for point in response.points:
        chunk = dict(point.payload)   # dictionary copy of the "payload"
        chunk["score"] = point.score  # add "score" key to the chunk dictionary
        top_k_chunks.append(chunk)    # append - list of dictionaries with payload data and score

    return top_k_chunks               # list of dictionaries


# ─── Step 7: Generate the answer ────────────────────────────────────────

SYSTEM_PROMPT = """You are a helpful assistant answering questions about a small
collection of Sherlock Holmes stories. You will be given the user's question and
several relevant excerpts. Use ONLY the provided excerpts to answer. If the
excerpts don't contain the answer, say so plainly. Cite the source (story title
+ section) in your answer."""


def answer(question: str, k: int = 3) -> dict[str, Any]:
    """End-to-end: retrieve, format context, call LLM, return result"""
    
    start = time.perf_counter()

    chunks = retrieve(question, k=k)  #retrieve top-k cunks
#*************************************************************
    # for chunk in chunks:
    #     print("\n")
    #     print(json.dumps(chunk, indent=2))
#*************************************************************

    context_parts = []
    for chunk in chunks:
        context_parts.append(f"[Source: {chunk['title']} — {chunk['section']}]\n{chunk['text']}")
    
    context = "\n\n".join(context_parts)
    user_message = f"Context:\n{context}\n\nQuestion: {question}"

    response = openai.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}, ],
        temperature=0,    )

    answer_text = response.choices[0].message.content

    #*************************************************************
    # print("\n")
    # print(f"Answer: {answer_text}")
    #*************************************************************

    latency_ms = round((time.perf_counter() - start) * 1000)

    citations = []
    for chunk in chunks:
        citations.append(
            {
                "source": chunk["source"],
                "title": chunk["title"],
                "section": chunk["section"],
                "score": chunk["score"],      }    )

    return {
       "question": question,
       "answer": answer_text,
       "citations": citations,
       "latency_ms": latency_ms,    }

# ─── Validation harness (provided — do not modify) ──────────────────────

def validate_against(jsonl_path: Path) -> None:
    questions = [json.loads(line) for line in jsonl_path.read_text().splitlines() if line.strip()]
    print(f"\n  Validating {len(questions)} questions from {jsonl_path.name}…\n")
    if not questions:
        print("  No questions found. Skipping validation.")
        return
    hits = 0
    for q in questions:
        result = answer(q["question"], k=3)
        cited_sources = {cit["source"] for cit in result["citations"]}
        source_hit = q["expected_source"] in cited_sources

        ans_lower = result["answer"].lower()
        facts_hit = sum(1 for fact in q.get("expected_facts", []) if fact.lower() in ans_lower)
        facts_total = len(q.get("expected_facts", []))

        verdict = "✓" if source_hit else "✗"
        print(f"  {verdict} {q['id']}")
        print(f"      Q: {q['question']}")
        print(f"      Cited: {', '.join(cited_sources)}")
        print(f"      Expected: {q['expected_source']}")
        print(f"      Facts matched: {facts_hit}/{facts_total}")
        print(f"      Latency: {result.get('latency_ms', '?')}ms")
        print()
        if source_hit:
            hits += 1

    print(f"  Source-match: {hits}/{len(questions)}")

# ─── CLI (provided — do not modify) ─────────────────────────────────────

def cmd_ingest() -> None:
    print("→ Loading corpus…")
    docs_dict = load_corpus(CORPUS_DIR)
    print(f"  {len(docs_dict)} documents loaded")

    print("→ Chunking…")
    all_chunks: list[dict[str, Any]] = []
    for doc in docs_dict:
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)
        print(f"  {doc['source']}: {len(chunks)} chunks")

    print(f"→ Total chunks: {len(all_chunks)}")

    print("\nchunk 1 :\n")
    print(json.dumps(all_chunks[0], indent=2))

    print("→ Setting up Qdrant collection…")
    setup_collection()

    print("→ Ingesting…")
    ingest_chunks(all_chunks)
    print("\n✓ Done. Try: python mp2_rag.py ask")


def cmd_ask() -> None:
    print("Mini-RAG over the Sherlock Holmes corpus.")
    print("Type your question. Empty line or Ctrl-C to exit.\n")
    while True:
        try:
            q = input("? ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not q:
            return
        result = answer(q, k=3)
        print(f"\n{result['answer']}\n")
        print("  Sources:")
        for c in result["citations"]:
            print(f"    - {c['title']} — {c['section']}")
        print(f"  Latency: {result.get('latency_ms', '?')}ms\n")


def cmd_validate() -> None:
    validate_against(DATA_DIR / "predefined_questions.jsonl")

    learner_path = DATA_DIR / "learner_questions.jsonl"
    if learner_path.exists():
        first = json.loads(learner_path.read_text().splitlines()[0])
        if not first["question"].startswith("Replace this"):
            validate_against(learner_path)


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "ingest":   cmd_ingest()
    elif cmd == "ask":    cmd_ask()
    elif cmd == "validate": cmd_validate()
    else:
        print(f"Unknown command: {cmd}\n")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()