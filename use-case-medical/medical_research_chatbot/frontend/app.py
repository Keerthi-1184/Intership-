# import streamlit as st
# from backend.tasks import search_task, summary_task, insights_task
# from backend.agents import literature_finder, paper_summarizer, insights_extractor
# from backend.tools import DuckDuckGoSearchTool, PaperSummaryTool, InsightExtractionTool

# st.set_page_config(page_title="Medical Research Assistant", layout="centered")
# st.title("🧠 Medical Research Assistant")

# query = st.text_input("Enter your medical research topic:", "Diabetes and AI")

# if st.button("Start Research"):
#     # 1. Search Task: Use literature_finder agent with DuckDuckGoSearchTool
#     search_tool = DuckDuckGoSearchTool()
#     search_result = search_tool._run(query)  # Directly call tool's _run method
    
#     st.write("### Search Results")
#     st.write(search_result)
    
#     # For simplicity, let's assume the search_result includes paths to downloaded papers
#     # You need to extract those paths if needed; here we'll just fake paper paths list
#     paper_paths = [
#         # You should extract actual downloaded filenames from search_result
#         # For example purposes, using dummy file names:
#         "medical_papers/sample_paper_1.pdf",
#         "medical_papers/sample_paper_2.pdf"
#     ]
    
#     # 2. Summary Task: Summarize each paper with paper_summarizer agent and PaperSummaryTool
#     summary_tool = PaperSummaryTool()
#     summaries = []
#     for path in paper_paths:
#         summary = summary_tool._run(path)
#         summaries.append(summary)
    
#     st.write("### Summaries")
#     for s in summaries:
#         st.write(s)
    
#     # 3. Insights Task: Extract insights from summaries with insights_extractor and InsightExtractionTool
#     insights_tool = InsightExtractionTool()
#     all_insights = []
#     for summary in summaries:
#         insights = insights_tool._run(summary)
#         all_insights.append(insights)
    
#     st.write("### Insights")
#     for ins in all_insights:
#         st.write(ins)
    
#     st.success("Research process completed.")


# # frontend/app.py
# import streamlit as st
# from crewai import Crew
# from backend.agents import create_literature_finder, create_paper_summarizer, create_insight_extractor
# from backend.tasks import create_search_task, create_summarize_task, create_insights_task

# st.title("🧠 Medical Research Assistant")

# # User inputs
# query = st.text_input("Enter your medical research topic:", "Diabetes and AI")

# if st.button("Start Research"):
#     with st.spinner("Researching..."):
#         # Create agents
#         literature_finder = create_literature_finder()
#         paper_summarizer = create_paper_summarizer()
#         insight_extractor = create_insight_extractor()

#         # Step 1: Search for papers directly
#         papers = create_search_task(literature_finder, query)  # Call directly, no Crew needed

#         # Display search results
#         if not papers:
#             st.warning("No papers found for your query.")
#         else:
#             st.write("### Search Results")
#             for i, paper in enumerate(papers, 1):
#                 st.write(f"**Paper {i}:** {paper['title']}")
#                 st.write(f"Authors: {', '.join(paper['authors']) if paper['authors'] else 'N/A'}")
#                 st.write(f"Journal: {paper['journal']} ({paper['year']})")
#                 st.write(f"Abstract: {paper['abstract']}\n")

#             # Step 2: Summarize each paper
#             st.write("### Summaries")
#             summaries = []
#             for paper in papers:
#                 summarize_task = create_summarize_task(paper_summarizer, paper)
#                 crew = Crew(
#                     agents=[paper_summarizer],
#                     tasks=[summarize_task],
#                     verbose=True
#                 )
#                 summary = crew.kickoff()
#                 summaries.append(summary)
#                 st.write(summary)

#             # Step 3: Extract insights from each summary
#             st.write("### Insights")
#             for summary in summaries:
#                 insights_task = create_insights_task(insight_extractor, summary)
#                 crew = Crew(
#                     agents=[insight_extractor],
#                     tasks=[insights_task],
#                     verbose=True
#                 )
#                 insights = crew.kickoff()
#                 st.write(insights)

#     st.success("Research process completed.")



# frontend/app.py
import streamlit as st
from crewai import Crew
from backend.agents import create_literature_finder, create_paper_summarizer, create_insight_extractor
from backend.tasks import create_search_task, create_summarize_task, create_insights_task
import os
from backend.llms import get_summarization_llm, get_insight_llm

# Ensure Ollama API base is set for litellm
os.environ["OLLAMA_API_BASE"] = "http://localhost:11434"

# Set the title of the Streamlit app
st.title("🧠 Medical Research Assistant")

# User inputs
query = st.text_input("Enter your medical research topic:", "Diabetes and AI")

# Start research when the button is clicked
if st.button("Start Research"):
    with st.spinner("Researching..."):
        # Ensure query is defined and accessible
        if not query:
            st.error("Please enter a research topic.")
        else:
            # Create agents
            literature_finder = create_literature_finder()
            paper_summarizer = create_paper_summarizer()
            insight_extractor = create_insight_extractor()

            # Step 1: Search for papers directly
            papers = create_search_task(literature_finder, query)  # Pass query to the function

            # Display search results
            if not papers:
                st.warning("No papers found for your query.")
            else:
                st.write("### Search Results")
                for i, paper in enumerate(papers, 1):
                    st.write(f"**Paper {i}:** {paper['title']}")
                    st.write(f"Authors: {', '.join(paper['authors']) if paper['authors'] else 'N/A'}")
                    st.write(f"Journal: {paper['journal']} ({paper['year']})")
                    st.write(f"Abstract: {paper['abstract']}\n")

                # # Step 2: Summarize each paper using LangChain Ollama directly
                # st.write("### Summaries")
                # summaries = []
                # summarizer_llm = get_summarization_llm()
                # prompt = "Summarize this medical paper in simple terms."
                # for paper in papers:
                #      prompt = f"Summarize the abstract of the paper: {paper['title']}\nAbstract: {paper['abstract']}\nProvide a concise summary in 2-3 sentences."
                #      summary = summarizer_llm.invoke(prompt)
                #      summaries.append(summary)
                #      st.write(f"**Summary for '{paper['title']}':** {summary}")

                # # Step 3: Extract insights from each summary using CrewAI
                # st.write("### Insights")
                # insight_llm = get_insight_llm()
                # for idx, summary in enumerate(summaries):
                #     prompt = f"Extract insights from the summary: {summary}\nProvide key insights as bullet points (each starting with -)."
                #     insights = insight_llm.invoke(prompt)
                #     st.write(f"**Insights for '{papers[idx]['title']}':**")
                #     st.write(insights)

                # frontend/app.py (summarization and insight extraction sections only)

# ... (previous code unchanged until line 66)

                # Step 2: Summarize each paper using LangChain Ollama directly
                st.write("### Summaries")
                summaries = []
                summarizer_llm = get_summarization_llm()
                for paper in papers:
                    prompt = f"Summarize the abstract of the paper: {paper['title']}\nAbstract: {paper['abstract']}\nStrictly provide a summary in exactly 2 or 3 sentences, no more, no less."
                    summary = summarizer_llm.invoke(prompt)
                    # Post-process to ensure summary is 2-3 sentences
                    sentences = [s.strip() for s in summary.split('.') if s.strip()]
                    if len(sentences) > 3:
                        summary = '. '.join(sentences[:3]) + '.'
                    elif len(sentences) < 2:
                        summary = summary + " No additional details provided."
                    summaries.append(summary)
                    st.markdown(f"**Summary for '{paper['title']}':**  \n{summary}\n")

                # Step 3: Extract insights from each summary using LangChain Ollama directly
                st.write("### Insights")
                insight_llm = get_insight_llm()
                for idx, summary in enumerate(summaries):
                    prompt = f"Extract insights from the summary: {summary}\nProvide key insights as bullet points (each starting with -)."
                    insights = insight_llm.invoke(prompt)
                    st.markdown(f"**Insights for '{papers[idx]['title']}':**  \n{insights}\n")

            st.success("Research process completed.")
           
                