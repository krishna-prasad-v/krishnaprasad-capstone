import voyageai
import numpy as np

_vo = None

#********************************************************************************************
# Lazy load for Voyage AI Enbedding model client. 
#******************************************************************************************** 
def get_voyage_client():
    global _vo
    if _vo is None:
        _vo = voyageai.Client()
    return _vo

#********************************************************************************************
# Chunk the input text - with optional overlap.
#******************************************************************************************** 
def chunk_by_size(text, chunk_size: int, overlap: int = 0) -> list[str]:
    """   Splits the input text into chunks of specified size with optional overlap.    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")
    if overlap < 0:
        raise ValueError("overlap must be a non-negative integer.")
    if overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size.")

    chunks = []
    start_index = 0
    full_text_length = len(text)

    while start_index < full_text_length:
        end_index = min(start_index + chunk_size, full_text_length)
        
        chunk_text = text[start_index:end_index]
        chunks.append(chunk_text)

        start_index = start_index + chunk_size - overlap

    return chunks

#********************************************************************************************
# Generate enbeddings - using Vogage AI Embedding model.
#******************************************************************************************** 
def generate_embeddings( chunks: str | list[str], model = "voyage-4-lite", input_type = "query") -> list[float] | list[list[float]]:
    """   Generates embeddings for a query OR a list of text chunks using the specified model.    """
    if not chunks:
        raise ValueError("text or chunk_list must not be empty.")

    is_list = isinstance(chunks, list)
    input = chunks if is_list else [chunks]

    vo = get_voyage_client()
    
    result = vo.embed(texts = input, 
                      model = model, 
                      input_type = input_type,
                      output_dimension = 1024)

    return result.embeddings if is_list else result.embeddings[0]  

#********************************************************************************************
# calculate the cosing similarity 
#******************************************************************************************** 
def cosine_sim(a: list[float], b: list[float]) -> float:
    # Voyage AI embeddings are unit-normalized, so dot product equals cosine similarity
    return float(np.dot(a, b))

#********************************************************************************************
# Retrieve top k chunks based on cosine similarity to the query vector.
#******************************************************************************************** 
def retrieve_top_k(query_vector: list[float], index: list[dict], k: int = 3) -> list[dict]:
    scored_chunks = []
    for item in index:
        score = cosine_sim(query_vector, item["vector"])
        scored_chunks.append((score, item))

    # Sort descending by score
    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    # Collect top-k
    results = []
    count = 0
    for score, item in scored_chunks:
        if count >= k:
            break
        
        result_item = dict(item)   # creates a new dict - to avoid modifying the original dict in index
        result_item["score"] = score
        results.append(result_item)
        count += 1

    return results

#********************************************************************************************
# Sort the retrieved chunks by their original order in the document (chunk_id).
#******************************************************************************************** 
def reorder_chunks_by_document(top_matches: list[dict]) -> list[dict]:
    """
    Takes the top-K retrieved chunks and sorts them by their original 
    position (chunk_id) in the source document.
    """
    # Create a shallow copy so we don't mutate the original list order
    ordered_matches = list(top_matches)
    
    # Sort ascending by chunk_id (e.g., 6 -> 7 -> 8)
    ordered_matches.sort(key=lambda chunk: chunk["chunk_id"])
    
    return ordered_matches

#********************************************************************************************
# system prompt - strict
#******************************************************************************************** 
system_prompt_strict = (
    "You are a helpful assistant. Answer the user's question using ONLY the "
    "provided context. If the context does not contain the answer, say so "
    "plainly. Cite the chunk id in square brackets after any fact you use." )