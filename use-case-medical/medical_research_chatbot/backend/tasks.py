# # backend/tasks.py
# from crewai import Task
# from backend.tools import pubmed_search, pubmed_fetch_details

# def create_search_task(agent, query):
#     # Since the agent has no tools, we handle the search directly
#     ids = pubmed_search(query, max_results=5)
#     if not ids:
#         return []
#     papers = pubmed_fetch_details(ids)
#     return papers

# def create_summarize_task(agent, paper):
#     return Task(
#         description=f"Summarize the abstract of the paper: {paper['title']}\nAbstract: {paper['abstract']}",
#         agent=agent,
#         expected_output="A concise summary of the paper's abstract."
#     )

# def create_insights_task(agent, summary):
#     return Task(
#         description=f"Extract insights from the summary: {summary}",
#         agent=agent,
#         expected_output="Key insights and actionable points from the summary."
#     )

# backend/tasks.py
from crewai import Task
from backend.tools import pubmed_search, pubmed_fetch_details

def create_search_task(agent, query):
    # Handle the search directly
    ids = pubmed_search(query, max_results=5)
    if not ids:
        return []
    papers = pubmed_fetch_details(ids)
    return papers
    return agent.run(query)

def create_summarize_task(agent, paper):
    return Task(
        description=f"Summarize the abstract of the paper: {paper['title']}\nAbstract: {paper['abstract']}",
        agent=agent,
        expected_output="A concise summary of the paper's abstract."
    )

def create_insights_task(agent, summary):
    return Task(
        description=f"Extract insights from the summary: {summary}",
        agent=agent,
        expected_output="Key insights and actionable points from the summary."
    )