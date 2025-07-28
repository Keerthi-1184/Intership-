from backend.models.embedder import Embedder
from backend.models.generator import Generator
from backend.utils.retriever import Retriever
from backend.utils.graph_builder import load_graph

class GraphRAG:
    def __init__(self):
        self.embedder = Embedder(model_name="nomic-embed-text")
        self.generator = Generator(model_name="llama3")
        self.retriever = Retriever(graph=load_graph("backend/data/graph.pkl"))

    def query(self, query: str) -> str:
        # Embed query
        query_embedding = self.embedder.embed(query)
        # Retrieve relevant nodes and neighbors
        context = self.retriever.retrieve(query_embedding)
        # Generate response
        prompt = f"Context: {context}\nQuery: {query}\nAnswer:"
        response = self.generator.generate(prompt)
        return response