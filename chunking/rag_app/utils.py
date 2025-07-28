# rag_app/utils.py
from sentence_transformers import SentenceTransformer

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text, max_chunk_size=500):
    # Simple chunking by sentences or fixed size chunks
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) <= max_chunk_size:
            chunk += sentence + " "
        else:
            chunks.append(chunk.strip())
            chunk = sentence + " "
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def load_embed_model():
    # Change to your preferred local or remote model
    model_name = "thenlper/gte-large"  # example open model with 1024 dim embeddings
    return SentenceTransformer(model_name)
