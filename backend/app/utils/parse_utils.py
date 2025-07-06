import tempfile
import pymupdf4llm
import os
import mammoth

def convert_file_to_markdown(file_bytes: bytes, file_type: str) -> str:
    if file_type == "application/pdf":
        return convert_pdf_to_markdown(file_bytes)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return convert_docx_to_markdown(file_bytes)
    else:
        raise ValueError("Unsupported file type. Only PDF and Docx files are allowed.")

def convert_docx_to_markdown(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    try:
        result = mammoth.convert_to_markdown(tmp_path)
        return result.value
    finally:
        os.remove(tmp_path)

def convert_pdf_to_markdown(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    try:
        return pymupdf4llm.to_markdown(tmp_path)
    finally:
        os.remove(tmp_path)