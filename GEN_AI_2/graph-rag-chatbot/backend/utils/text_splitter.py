def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """Split text into chunks with specified size and overlap."""
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks