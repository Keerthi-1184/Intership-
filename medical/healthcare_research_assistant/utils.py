# import pdfplumber

# def extract_text_from_pdf(uploaded_file):
#     text = ""
#     with pdfplumber.open(uploaded_file) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() + "\n"
#     return text


import PyPDF2

def extract_pdf_text(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip() if text else "No content extracted."
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return "Error extracting PDF text."

def clean_text(text):
    return text.strip() if text else "No content available."
