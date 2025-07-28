# # from fastapi import FastAPI, File, UploadFile
# # from fastapi.middleware.cors import CORSMiddleware
# # from pydantic import BaseModel
# # from fastapi.responses import JSONResponse
# # import uvicorn
# # from typing import List
# # import io
# # import csv
# # import json
# # from docx import Document
# # from bs4 import BeautifulSoup
# # import PyPDF2

# # from model_handler import query_model  # Your existing model query function


# # app = FastAPI()

# # # Enable CORS for all origins (for local dev)
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )


# # class ChatRequest(BaseModel):
# #     model_name: str
# #     messages: List[dict]  # List of {"role": "...", "content": "..."}


# # @app.post("/chat/")
# # def chat_endpoint(req: ChatRequest):
# #     reply = query_model(req.model_name, req.messages)
# #     return {"response": reply}


# # # --------- Summarization Logic ---------

# # def simple_summarize(text: str, max_sentences: int = 5) -> str:
# #     sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
# #     return '. '.join(sentences[:max_sentences]) + ('.' if len(sentences) > max_sentences else '')


# # def extract_text_from_pdf(file_bytes: bytes) -> str:
# #     reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
# #     text = ""
# #     for page in reader.pages:
# #         text += page.extract_text() + "\n"
# #     return text


# # def extract_text_from_docx(file_bytes: bytes) -> str:
# #     doc = Document(io.BytesIO(file_bytes))
# #     return "\n".join([para.text for para in doc.paragraphs])


# # def extract_text_from_txt(file_bytes: bytes) -> str:
# #     return file_bytes.decode("utf-8")


# # def extract_text_from_csv(file_bytes: bytes) -> str:
# #     text = ""
# #     f = io.StringIO(file_bytes.decode("utf-8"))
# #     reader = csv.reader(f)
# #     for row in reader:
# #         text += " ".join(row) + "\n"
# #     return text


# # def extract_text_from_html(file_bytes: bytes) -> str:
# #     soup = BeautifulSoup(file_bytes, 'html.parser')
# #     return soup.get_text(separator=' ', strip=True)


# # def extract_text_from_json(file_bytes: bytes) -> str:
# #     data = json.loads(file_bytes)

# #     def json_to_text(obj):
# #         if isinstance(obj, dict):
# #             return " ".join(f"{k}: {json_to_text(v)}" for k, v in obj.items())
# #         elif isinstance(obj, list):
# #             return " ".join(json_to_text(i) for i in obj)
# #         else:
# #             return str(obj)

# #     return json_to_text(data)


# # @app.post("/summarize/")
# # async def summarize_file(file: UploadFile = File(...), model_name: str = "llama3.2-vision:11b"):
# #     contents = await file.read()
# #     filename = file.filename.lower()

# #     try:
# #         if filename.endswith(".pdf"):
# #             text = extract_text_from_pdf(file_bytes)
# #         elif filename.endswith(".docx"):
# #             text = extract_text_from_docx(file_bytes)
# #         elif filename.endswith(".txt"):
# #             text = extract_text_from_txt(file_bytes)
# #         elif filename.endswith(".csv"):
# #             text = extract_text_from_csv(file_bytes)
# #         elif filename.endswith(".html") or filename.endswith(".htm"):
# #             text = extract_text_from_html(file_bytes)
# #         elif filename.endswith(".json"):
# #             text = extract_text_from_json(file_bytes)
# #         else:
# #             return JSONResponse(status_code=400, content={"error": "Unsupported file type"})

# #         summary = simple_summarize(text)
# #         return {"summary": summary}

# #     except Exception as e:
# #         return JSONResponse(status_code=500, content={"error": str(e)})


# # if __name__ == "__main__":
# #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# from fastapi import FastAPI, File, UploadFile
# from PIL import Image
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from fastapi.responses import JSONResponse
# import uvicorn
# from typing import List
# import io
# import csv
# import json
# import time
# from docx import Document
# from bs4 import BeautifulSoup
# import PyPDF2

# from model_handler import query_model  # Ensure this supports summarization

# app = FastAPI()

# # Enable CORS for local dev
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --------- Chat Endpoint ---------

# class ChatRequest(BaseModel):
#     model_name: str
#     messages: List[dict]  # [{"role": "user", "content": "..."}]

# @app.post("/chat/")
# def chat_endpoint(req: ChatRequest):
#     start = time.time()
#     reply = query_model(req.model_name, req.messages)
#     end = time.time()
#     return {"response": reply, "time_taken_seconds": round(end - start, 2)}


# # --------- File Text Extraction Utilities ---------

# def extract_text_from_pdf(file_bytes: bytes) -> str:
#     reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
#     text = ""
#     for page in reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"
#     return text.strip()

# def extract_text_from_docx(file_bytes: bytes) -> str:
#     doc = Document(io.BytesIO(file_bytes))
#     return "\n".join([para.text for para in doc.paragraphs])

# def extract_text_from_txt(file_bytes: bytes) -> str:
#     return file_bytes.decode("utf-8")

# def extract_text_from_csv(file_bytes: bytes) -> str:
#     text = ""
#     f = io.StringIO(file_bytes.decode("utf-8"))
#     reader = csv.reader(f)
#     for row in reader:
#         text += " ".join(row) + "\n"
#     return text.strip()

# def extract_text_from_html(file_bytes: bytes) -> str:
#     soup = BeautifulSoup(file_bytes, 'html.parser')
#     return soup.get_text(separator=' ', strip=True)

# def extract_text_from_json(file_bytes: bytes) -> str:
#     decoded = file_bytes.decode("utf-8")
#     try:
#         data = json.loads(decoded)
#     except json.JSONDecodeError:
#         # Handle cases with multiple JSON objects (e.g., JSONL files)
#         lines = decoded.strip().splitlines()
#         data = [json.loads(line) for line in lines if line.strip()]
    
#     def json_to_text(obj):
#         if isinstance(obj, dict):
#             return " ".join(f"{k}: {json_to_text(v)}" for k, v in obj.items())
#         elif isinstance(obj, list):
#             return " ".join(json_to_text(i) for i in obj)
#         else:
#             return str(obj)

#     return json_to_text(data)



# # --------- Chunking + Summarization ---------

# def chunk_text(text, max_chunk_size: int=3000) -> List[str]:
#     chunks, start = [], 0
#     while start < len(text):
#         end = start + max_chunk_size
#         chunks.append(text[start:end])
#         start = end
#     return chunks

# def full_summarize_with_model(text: str, model_name: str) -> str:
#     chunks = chunk_text(text)
#     chunk_summaries = []
#     print(f"Total chunks to summarize: {len(chunks)}")

#     for i, chunk in enumerate(chunks):
#         print(f"Summarizing chunk {i+1}/{len(chunks)} (length: {len(chunk)})")
#         prompt = f"Summarize this: {chunk}"
#         messages = [{"role": "user", "content": prompt}]
#         summary = query_model(model_name, messages)
#         chunk_summaries.append(summary.strip())

#     combined = " ".join(chunk_summaries)
#     print("Summarizing all chunk summaries into one final summary.")
#     final_prompt = f"Summarize the following combined summaries into one concise summary:\n\n{combined}"
#     final_summary = query_model(model_name, [{"role": "user", "content": final_prompt}])
#     return final_summary.strip()


# # --------- Summarization Endpoint ---------

# @app.post("/summarize/")
# async def summarize_file(file: UploadFile = File(...), model_name: str = "llama3.2-vision:11b"):
#     start_time = time.time()

#     contents = await file.read()

#     try:
#         contents = await file.read()
#         filename = file.filename.lower()
#         if filename.endswith(".pdf"):
#             text = extract_text_from_pdf(contents)
#         elif filename.endswith(".docx"):
#             text = extract_text_from_docx(contents)
#         elif filename.endswith(".txt"):
#             text = extract_text_from_txt(contents)
#         elif filename.endswith(".csv"):
#             text = extract_text_from_csv(contents)
#         elif filename.endswith(".html") or filename.endswith(".htm"):
#             text = extract_text_from_html(contents)
#         elif filename.endswith(".json"):
#             text = extract_text_from_json(contents)
#         else:
#             return JSONResponse(status_code=400, content={"error": "Unsupported file type"})

#         if not text.strip():
#             return JSONResponse(status_code=400, content={"error": "File contains no extractable text."})

#         summary = full_summarize_with_model(text, model_name)
#         return {"summary": summary, "processing_time": time.time() - start_time}

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return JSONResponse(status_code=500, content={"error": str(e)})


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import time

from utils.pdf_utils import summarize_pdf
from utils.docx_utils import summarize_docx
from utils.txt_utils import summarize_txt
from utils.csv_utils import summarize_csv
from utils.html_utils import summarize_html
from utils.json_utils import summarize_json
from utils.model_loader import get_model_client  # make sure this exists

app = FastAPI()

# CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as per frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize/")
async def summarize_file(file: UploadFile = File(...), model_name: str = "llama3.2-vision:11b"):
    start_time = time.time()
    contents = await file.read()

    try:
        client = get_model_client(model_name)

        summary = ""
        file_type = file.content_type

        if file_type.startswith("image/"):
            image = Image.open(io.BytesIO(contents)).convert("RGB")
            prompt = "Describe the contents of this image in detail."
            result = client.generate(prompt=prompt, image=image)
            summary = result["text"] if isinstance(result, dict) else str(result)

        elif file.filename.endswith(".pdf"):
            summary = await summarize_pdf(contents, client)

        elif file.filename.endswith(".docx"):
            summary = await summarize_docx(contents, client)

        elif file.filename.endswith(".txt"):
            summary = await summarize_txt(contents, client)

        elif file.filename.endswith(".csv"):
            summary = await summarize_csv(contents, client)

        elif file.filename.endswith(".html") or file_type == "text/html":
            summary = await summarize_html(contents, client)

        elif file.filename.endswith(".json"):
            summary = await summarize_json(contents, client)

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        processing_time = time.time() - start_time

        return JSONResponse(content={
            "message": "Successfully uploaded",
            "summary": summary,
            "processing_time": processing_time
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
