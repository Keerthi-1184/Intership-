from langchain_community.llms.ollama import Ollama
from summarizer import summarize_text

def structure_paper(query, papers=None):
    try:
        llm = Ollama(model="deepseek-r1:1.5b", base_url="http://localhost:11434")
        context = " ".join(paper["abstract"] for paper in papers if paper and paper["abstract"]) if papers else "No papers provided."
        summary = summarize_text(context) if context else "No summary available."
        
        sections = {
            "Introduction": llm.invoke(f"Write an introduction for a research paper on {query} in 3-4 sentences."),
            "Methods": llm.invoke(f"Describe methods for a study on {query} in 2-3 sentences."),
            "Results": f"Results: Based on the literature, {summary}",
            "Discussion": llm.invoke(f"Discuss findings on {query} in 3-4 sentences, focusing on implications.")
        }
        return sections
    except Exception as e:
        print(f"Error structuring paper: {e}")
        return {
            "Introduction": "Error generating content.",
            "Methods": "Error generating content.",
            "Results": "Error generating content.",
            "Discussion": "Error generating content."
        }