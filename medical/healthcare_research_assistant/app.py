# import streamlit as st
# from pubmed import search_pubmed
# from summarizer import summarize_text
# from ner import extract_entities
# from utils import extract_text_from_pdf

# st.title("Healthcare Research Assistant")

# option = st.radio("Choose input type:", ["PubMed Search", "Upload PDF"])

# if option == "PubMed Search":
#     query = st.text_input("Enter PubMed search query:")
#     if st.button("Search"):
#         if query.strip():
#             with st.spinner("Searching PubMed..."):
#                 results = search_pubmed(query, max_results=5)
#             if results:
#                 for i, article in enumerate(results, 1):
#                     st.subheader(f"{i}. {article['title']}")
#                     st.write(article['abstract'])
#                     summary = summarize_text(article['abstract'])
#                     st.markdown("**Summary:**")
#                     st.write(summary)
#                     ents = extract_entities(article['abstract'])
#                     if ents:
#                         st.markdown("**Entities:**")
#                         st.write(ents)
#             else:
#                 st.write("No results found.")
#         else:
#             st.error("Please enter a query.")

# elif option == "Upload PDF":
#     uploaded_file = st.file_uploader("Upload medical research PDF", type=["pdf"])
#     if uploaded_file is not None:
#         with st.spinner("Extracting text..."):
#             text = extract_text_from_pdf(uploaded_file)
#         st.write(text[:1000] + "...")
#         if st.button("Summarize"):
#             summary = summarize_text(text)
#             st.markdown("**Summary:**")
#             st.write(summary)
#             ents = extract_entities(text)
#             if ents:
#                 st.markdown("**Entities:**")
#                 st.write(ents)


import streamlit as st
import pandas as pd
from pubmed import fetch_pubmed_papers
from summarizer import summarize_text
from utils import extract_pdf_text
from hypothesis_generator import generate_hypotheses
from rag_retriever import rag_retrieve
from paper_structurer import structure_paper
from clinical_trials import fetch_clinical_trials
import traceback

st.set_page_config(page_title="Medical Research Assistant", layout="wide")
st.title("🧠 Medical Research Assistant")

# Sidebar for navigation
option = st.sidebar.selectbox("Select Functionality", [
    "Summarize Literature",
    "Generate Hypotheses",
    "Literature Review",
    "Structure Paper",
    "Find Clinical Trials"
])

# Initialize session state for storing papers
if "papers" not in st.session_state:
    st.session_state["papers"] = []

# Summarize Literature
if option == "Summarize Literature":
    st.header("Summarize Medical Literature")
    query = st.text_input("Enter search query (e.g., diabetes and AI)")
    uploaded_file = st.file_uploader("Upload a PDF (optional)", type="pdf")
    max_results = st.slider("Number of papers to retrieve", 1, 10, 5)
    
    if st.button("Search and Summarize"):
        try:
            if uploaded_file:
                text = extract_pdf_text(uploaded_file)
                summary = summarize_text(text)
                st.write("### PDF Summary")
                st.markdown(summary)
            elif query:
                st.write("### Retrieved Papers")
                papers = fetch_pubmed_papers(query, max_results)
                if papers:
                    st.session_state["papers"] = papers
                    paper_data = []
                    for i, paper in enumerate(papers, 1):
                        summary = summarize_text(paper["abstract"])
                        paper_data.append({
                            "Paper #": i,
                            "Title": paper["title"],
                            "Authors": ", ".join(paper["authors"]),
                            "DOI": paper["doi"],
                            "Journal": f"{paper['journal']} ({paper['year']})",
                            "Summary": summary
                        })
                    
                    df = pd.DataFrame(paper_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    selected_paper = st.selectbox("Select a paper to view full abstract", 
                                                options=[f"Paper {i}: {paper['title']}" for i, paper in enumerate(papers, 1)])
                    if selected_paper:
                        paper_idx = int(selected_paper.split(":")[0].split()[-1]) - 1
                        st.write("### Full Abstract")
                        st.markdown(papers[paper_idx]["abstract"])
                else:
                    st.error("No papers found for the query. Try a broader search term (e.g., 'diabetes').")
            else:
                st.warning("Please enter a query or upload a PDF.")
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")
            print(traceback.format_exc())

# Generate Hypotheses
elif option == "Generate Hypotheses":
    st.header("Generate Research Hypotheses")
    topic = st.text_input("Enter research topic (e.g., metformin and cancer)")
    if st.button("Generate"):
        try:
            hypotheses = generate_hypotheses(topic)
            st.write("### Hypotheses")
            for i, hyp in enumerate(hypotheses, 1):
                st.markdown(f"{i}. {hyp}")
        except Exception as e:
            st.error(f"Error generating hypotheses: {str(e)}")
            print(traceback.format_exc())

# Literature Review
elif option == "Literature Review":
    st.header("Literature Review with RAG")
    query = st.text_input("Enter review query")
    if st.button("Retrieve"):
        try:
            results = rag_retrieve(query)
            if results:
                st.write("### Relevant Documents")
                for i, doc in enumerate(results, 1):
                    st.markdown(f"**{i}. {doc['title']}** (Score: {doc['score']:.2f})\n\n{doc['content'][:200]}...")
            else:
                st.error("No relevant documents found.")
        except Exception as e:
            st.error(f"Error retrieving documents: {str(e)}")
            print(traceback.format_exc())

# Structure Paper
elif option == "Structure Paper":
    st.header("Structure Research Paper")
    query = st.text_input("Enter research topic for paper generation")
    use_retrieved_papers = st.checkbox("Use retrieved papers from Summarize Literature")
    if st.button("Structure"):
        try:
            if use_retrieved_papers and st.session_state["papers"]:
                structured = structure_paper(query, st.session_state["papers"])
            else:
                structured = structure_paper(query)
            st.write("### Structured Paper")
            for section, text in structured.items():
                st.write(f"## {section}")
                st.markdown(text)
        except Exception as e:
            st.error(f"Error structuring paper: {str(e)}")
            print(traceback.format_exc())

# Find Clinical Trials
elif option == "Find Clinical Trials":
    st.header("Find Relevant Clinical Trials")
    condition = st.text_input("Enter condition (e.g., breast cancer)")
    if st.button("Search"):
        try:
            trials = fetch_clinical_trials(condition)
            if trials:
                st.write("### Clinical Trials")
                for i, trial in enumerate(trials, 1):
                    st.markdown(f"{i}. **{trial['title']}** (Phase: {trial['phase']})")
            else:
                st.error("No trials found for the condition.")
        except Exception as e:
            st.error(f"Error fetching trials: {str(e)}")
            print(traceback.format_exc())