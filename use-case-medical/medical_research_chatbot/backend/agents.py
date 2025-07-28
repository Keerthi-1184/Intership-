# # backend/agents.py
# from crewai import Agent
# from backend.tools import pubmed_search, pubmed_fetch_details

# # Define the CrewAI agents
# def create_literature_finder():
#     return Agent(
#         role="Literature Finder",
#         goal="Search for relevant medical research papers on PubMed based on a given query.",
#         backstory="I am a specialized research assistant with expertise in navigating PubMed to find the most relevant and recent medical papers for a given topic.",
#         tools=[],  # No tools, we'll handle the search directly in the task
#         verbose=True
#     )

# def create_paper_summarizer():
#     return Agent(
#         role="Paper Summarizer",
#         goal="Summarize the abstract of a medical research paper to provide a concise overview.",
#         backstory="I am an expert in medical literature summarization, capable of distilling complex abstracts into clear and concise summaries.",
#         llm=get_summarization_llm(),  # Using qwen2.5-coder:0.5b
#         verbose=True
#     )

# def create_insight_extractor():
#     return Agent(
#         role="Insight Extractor",
#         goal="Extract key insights and actionable points from a summarized medical paper.",
#         backstory="I am a skilled analyst with a background in medical research, adept at identifying key insights and implications from summaries of scientific papers.",
#         llm=get_insight_llm(),  # Using deepseek-r1:1.5b
#         verbose=True
#     )

# # Import LLMs (to avoid circular imports)
# from backend.llms import get_summarization_llm, get_insight_llm



# # backend/agents.py
# from crewai import Agent
# from langchain.tools import BaseTool
# from typing import Optional, Type
# from pydantic import BaseModel, Field
# from backend.tools import pubmed_search, pubmed_fetch_details

# # Define the input schema for the tool
# class PubMedSearchToolInput(BaseModel):
#     query: str = Field(..., description="The search query for PubMed")
#     max_results: int = Field(default=5, description="Maximum number of results to return")

# # Define a proper LangChain tool for PubMed search
# class PubMedSearchTool(BaseTool):
#     name: str = "PubMed Search Tool"
#     description: str = "A tool to search for medical research papers on PubMed and fetch their details."
#     args_schema: Type[BaseModel] = PubMedSearchToolInput

#     def _run(self, query: str, max_results: int = 5) -> list:
#         """Synchronous method to search PubMed and fetch paper details."""
#         ids = pubmed_search(query, max_results=max_results)
#         if not ids:
#             return []
#         papers = pubmed_fetch_details(ids)
#         return papers

#     async def _arun(self, query: str, max_results: int = 5) -> list:
#         """Asynchronous method (not implemented for now)."""
#         raise NotImplementedError("Asynchronous PubMed search not supported.")

# # Define the CrewAI agents
# def create_literature_finder():
#     return Agent(
#         role="Literature Finder",
#         goal="Search for relevant medical research papers on PubMed based on a given query.",
#         backstory="I am a specialized research assistant with expertise in navigating PubMed to find the most relevant and recent medical papers for a given topic.",
#         tools=[PubMedSearchTool()],
#         verbose=True
#     )

# def create_paper_summarizer():
#     return Agent(
#         role="Paper Summarizer",
#         goal="Summarize the abstract of a medical research paper to provide a concise overview.",
#         backstory="I am an expert in medical literature summarization, capable of distilling complex abstracts into clear and concise summaries.",
#         llm=get_summarization_llm(),  # Now returns "ollama/qwen2.5-coder:0.5b"
#         verbose=True
#     )

# def create_insight_extractor():
#     return Agent(
#         role="Insight Extractor",
#         goal="Extract key insights and actionable points from a summarized medical paper.",
#         backstory="I am a skilled analyst with a background in medical research, adept at identifying key insights and implications from summaries of scientific papers.",
#         llm=get_insight_llm(),  # Now returns "ollama/deepseek-r1:1.5b"
#         verbose=True
#     )

# # Import LLMs (to avoid circular imports)
# from backend.llms import get_summarization_llm, get_insight_llm



# backend/agents.py
from crewai import Agent
from backend.tools import pubmed_search, pubmed_fetch_details

# Define the CrewAI agents
def create_literature_finder():
    return Agent(
        role="Literature Finder",
        goal="Search for relevant medical research papers on PubMed based on a given query.",
        backstory="I am a specialized research assistant with expertise in navigating PubMed to find the most relevant and recent medical papers for a given topic.",
        tools=[],  # No tools, we'll handle the search directly in the task
        verbose=True
    )

def create_paper_summarizer():
    return Agent(
        role="Paper Summarizer",
        goal="Summarize the abstract of a medical research paper to provide a concise overview.",
        backstory="I am an expert in medical literature summarization, capable of distilling complex abstracts into clear and concise summaries.",
        llm=get_summarization_llm(),  # Using qwen2.5-coder:0.5b
        verbose=True
    )

def create_insight_extractor():
    return Agent(
        role="Insight Extractor",
        goal="Extract key insights and actionable points from a summarized medical paper.",
        backstory="I am a skilled analyst with a background in medical research, adept at identifying key insights and implications from summaries of scientific papers.",
        llm=get_insight_llm(),  # Using deepseek-r1:1.5b
        verbose=True
    )

# Import LLMs (to avoid circular imports)
from backend.llms import get_summarization_llm, get_insight_llm