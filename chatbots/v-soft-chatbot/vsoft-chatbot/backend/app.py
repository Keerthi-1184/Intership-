from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import DirectoryLoader, UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:8502"],  # Support multiple Streamlit ports
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_data_dir():
    """Get absolute path to vsoft_data directory"""
    current_dir = Path(__file__).parent
    data_dir = current_dir / "vsoft_data"
    data_dir.mkdir(exist_ok=True)
    return data_dir

def initialize_qa_chain():
    try:
        data_dir = get_data_dir()
        logger.info(f"Loading documents from: {data_dir}")

        # Check for HTML files
        html_files = list(data_dir.glob("**/*.html"))
        if not html_files:
            logger.warning("No HTML files found in vsoft_data directory. Using fallback response.")
            return None

        # Load documents
        loader = DirectoryLoader(
            str(data_dir),
            glob="**/*.html",
            loader_cls=UnstructuredHTMLLoader,
            show_progress=True,
            silent_errors=True
        )
        documents = loader.load()
        
        if not documents:
            logger.warning("No documents loaded from vsoft_data directory")
            return None

        logger.info(f"Loaded {len(documents)} documents")

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,  # Reduced for lower memory usage
            chunk_overlap=50
        )
        texts = text_splitter.split_documents(documents)
        logger.info(f"Split into {len(texts)} text chunks")

        # Create vector store
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.from_documents(texts, embeddings)
        logger.info("Vector store created successfully")

        # Initialize LLM
        try:
            llm = Ollama(model="deepseek-r1:1.5b")
            test_response = llm("Test query to verify LLM")
            logger.info(f"LLM test response: {test_response}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            return None

        # Create prompt template
        prompt_template = """
        You are a helpful assistant for VSoft Consulting. Only answer questions related to VSoft.
        If the question is not about VSoft, respond: "I specialize in VSoft Consulting information only."

        Context: {context}
        Question: {question}
        Answer:
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        logger.info("QA chain initialized successfully")
        return qa_chain

    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}")
        return None

# Initialize QA chain
qa_chain = initialize_qa_chain()

class Query(BaseModel):
    question: str

@app.post("/query")
async def query_endpoint(query: Query):
    question = query.question.strip()
    if not question:
        return {"response": "Please provide a valid question.", "sources": []}
    if not qa_chain:
        logger.warning("QA chain not initialized. Returning fallback response.")
        return {
            "response": "I'm sorry, the VSoft Consulting knowledge base is not available. Please ensure the vsoft_data directory contains HTML files and Ollama is running.",
            "sources": []
        }
    try:
        result = qa_chain({"query": question})
        logger.info(f"\nQuery: {question}")
        logger.info(f"Result: {result['result']}")
        logger.info(f"Sources: {[doc.metadata['source'] for doc in result['source_documents']]}")
        sources = list(set([doc.metadata["source"] for doc in result["source_documents"]]))
        
        return {
            "response": result["result"].strip(),
            "sources": sources
        }
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "ready" if qa_chain else "initialization_error",
        "documents_loaded": qa_chain is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)