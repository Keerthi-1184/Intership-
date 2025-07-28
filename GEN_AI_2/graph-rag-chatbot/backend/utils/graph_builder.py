import networkx as nx
import pickle
from backend.utils.text_splitter import split_text
from backend.models.embedder import Embedder
import PyPDF2

def build_graph(pdf_path: str, output_path: str):
    """Build and serialize a document graph from a PDF."""
    # Extract text from PDF
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = "".join(page.extract_text() for page in reader.pages)
    
    # Split text into chunks
    chunks = split_text(text)
    
    # Embed chunks
    embedder = Embedder(model_name="nomic-embed-text")
    embeddings = [embedder.embed(chunk) for chunk in chunks]
    
    # Create graph
    G = nx.Graph()
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        G.add_node(i, text=chunk, embedding=embedding)
    
    # Add edges based on similarity (placeholder logic)
    for i in range(len(chunks)):
        for j in range(i + 1, len(chunks)):
            # Placeholder: Add edge if cosine similarity > threshold
            similarity = 0.8  # Replace with actual cosine similarity
            if similarity > 0.7:
                G.add_edge(i, j, weight=similarity)
    
    # Serialize graph
    with open(output_path, "wb") as f:
        pickle.dump(G, f)

def load_graph(graph_path: str) -> nx.Graph:
    """Load serialized graph."""
    with open(graph_path, "rb") as f:
        return pickle.load(f)