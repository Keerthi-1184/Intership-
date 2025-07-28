from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pubmed import fetch_pubmed_papers

def rag_retrieve(query, max_results=5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    papers = fetch_pubmed_papers(query, max_results)
    if not papers:
        return []
    
    abstracts = [paper["abstract"] if paper["abstract"] else "" for paper in papers]
    titles = [paper["title"] for paper in papers]
    
    query_embedding = model.encode([query])
    doc_embeddings = model.encode(abstracts)
    
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
    top_indices = np.argsort(similarities)[-max_results:][::-1]
    
    return [
        {
            "title": titles[i],
            "content": abstracts[i],
            "score": similarities[i]
        }
        for i in top_indices if abstracts[i]
    ]