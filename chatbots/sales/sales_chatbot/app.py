from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
import os
from pathlib import Path
import logging
import base64
from io import BytesIO
from PIL import Image
import subprocess
import socket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:8502"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_ollama_models():
    """Check if required Ollama models are available"""
    required_models = [
        "deepseek-r1:1.5b",
        "mxbai-embed-large:latest",
        "llama3.2-vision:11b",
        "qwen2.5-coder:0.5b"
    ]
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        available_models = [line.split()[0] for line in result.stdout.splitlines()[1:]]
        missing_models = [model for model in required_models if model not in available_models]
        if missing_models:
            logger.error(f"Missing Ollama models: {missing_models}")
            return False
        logger.info("All required Ollama models are available")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to check Ollama models: {str(e)}")
        return False

def get_data_dir():
    """Get absolute path to sales_data directory"""
    current_dir = Path(__file__).parent
    data_dir = current_dir / "sales_data"
    data_dir.mkdir(exist_ok=True)
    return data_dir.resolve()  # Normalize path for Windows

def initialize_qa_chain():
    try:
        data_dir = get_data_dir()
        logger.info(f"Loading documents from: {data_dir}")

        # Check for text files
        text_files = list(data_dir.glob("**/*.txt"))
        if not text_files:
            logger.warning("No text files found in sales_data directory.")
            return None

        # Load documents
        loader = DirectoryLoader(
            str(data_dir),
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
            show_progress=True,
            silent_errors=False
        )
        documents = loader.load()
        
        if not documents:
            logger.warning("No documents loaded from sales_data directory")
            return None

        logger.info(f"Loaded {len(documents)} documents")

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50
        )
        texts = text_splitter.split_documents(documents)
        logger.info(f"Split into {len(texts)} text chunks")

        # Create vector store
        embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")
        db = FAISS.from_documents(texts, embeddings)
        logger.info("Vector store created successfully")

        # Initialize LLM
        try:
            llm = Ollama(model="deepseek-r1:1.5b")
            test_response = llm("Test sales pitch generation")
            logger.info(f"Text LLM test response: {test_response}")
        except Exception as e:
            logger.error(f"Failed to initialize text LLM: {str(e)}")
            return None

        # Create prompt template
        prompt_template = """
        You are a sales content expert. Generate creative, concise, and persuasive sales content (e.g., pitches, emails, social media posts) based on the user's prompt.
        Use the provided context to ground your response. If the prompt is unrelated to sales, respond: "I specialize in sales content generation only."

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

# Check Ollama models before initializing
if not check_ollama_models():
    logger.error("Required Ollama models are not available. Please pull missing models using 'ollama pull <model>'.")
    qa_chain = None
else:
    qa_chain = initialize_qa_chain()

class Query(BaseModel):
    question: str

class CodeQuery(BaseModel):
    question: str

@app.post("/query")
async def query_endpoint(query: Query):
    question = query.question.strip()
    if not question:
        return {"response": "Please provide a valid question.", "sources": []}
    if not qa_chain:
        logger.warning("QA chain not initialized. Returning fallback response.")
        return {
            "response": "I'm sorry, the sales knowledge base is not available. Please ensure the sales_data directory contains text files and Ollama is running with all required models.",
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

@app.post("/image_analysis")
async def image_analysis_endpoint(file: UploadFile = File(...)):
    try:
        # Read and process image
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        
        # Convert image to base64 for llama3.2-vision
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Initialize vision LLM
        llm = Ollama(model="llama3.2-vision:11b")
        
        # Create prompt for sales analysis
        prompt = f"""
        Analyze this image for sales purposes. Suggest how it could be used in a sales campaign (e.g., social media, ads, product promotions).
        Provide creative ideas for captions or campaign themes.
        Image data: data:image/png;base64,{img_base64}
        """
        
        response = llm(prompt)
        logger.info(f"Image analysis response: {response}")
        return {"response": response.strip()}
    except Exception as e:
        logger.error(f"Image analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/code_generation")
async def code_generation_endpoint(query: CodeQuery):
    question = query.question.strip()
    if not question:
        return {"response": "Please provide a valid code generation prompt."}
    try:
        llm = Ollama(model="qwen2.5-coder:0.5b")
        prompt = f"""
        You are a coding assistant for sales tools. Generate clean, functional code based on the user's prompt.
        Focus on sales-related tasks (e.g., HTML for landing pages, CSS for promotional banners).
        If the prompt is unrelated to sales code, respond: "I specialize in sales-related code generation only."
        
        Prompt: {question}
        """
        response = llm(prompt)
        logger.info(f"Code generation response: {response}")
        return {"response": response.strip()}
    except Exception as e:
        logger.error(f"Code generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "ready" if qa_chain else "initialization_error",
        "documents_loaded": qa_chain is not None,
        "ollama_models_available": check_ollama_models()
    }

def find_available_port(host="0.0.0.0", ports=[8000, 8001, 8002]):
    """Find an available port from the given list"""
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                logger.info(f"Port {port} is available")
                return port
            except socket.error:
                logger.warning(f"Port {port} is already in use")
                continue
    raise RuntimeError("No available ports found in the specified range")

if __name__ == "__main__":
    import uvicorn
    try:
        port = find_available_port()
        logger.info(f"Starting server on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    except RuntimeError as e:
        logger.error(str(e))
        raise