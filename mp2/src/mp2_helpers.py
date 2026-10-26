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