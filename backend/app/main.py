import json
import os
from typing import Dict, List, Union
from fastapi import FastAPI, HTTPException, UploadFile, File
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware
import faiss
import numpy as np
import uuid
from dotenv import load_dotenv


from pathlib import Path
from utils.chunk_utils import chunk_text, convert_tables_to_html
from utils.search_utils import search
from utils.prompt_utils import generate_answer, build_prompt
from models.database import SessionLocal, TextChunk
from utils.embedding_utils import embed_chunks
from utils.db_utils import store_chunks_to_db
from utils.parse_utils import convert_file_to_markdown

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:3000",  # React dev server
]

# Allow all origins for development purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# FAISS index setup
embedding_dim = 768
index = faiss.IndexFlatIP(embedding_dim)

# Load the pre-trained SentenceTransformer model
embedding_model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
model = SentenceTransformer(embedding_model_name)

# Add this near your other constants
PROMPT_TEMPLATE_PATH = Path(__file__).parent / "prompts" / "default_prompt.txt"

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)) -> dict:
    doc_title = file.filename
    file_type = file.content_type
    if not file_type or not file_type.startswith(("application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF and Docx files are allowed."
        )
    contents = await file.read()
    # Save the uploaded file to a temp file
    md = convert_file_to_markdown(contents, file_type)
    md = convert_tables_to_html(md)
    chunks = chunk_text(md, max_tokens=700)
    ids = [str(uuid.uuid4()) for _ in chunks]

    embeddings = embed_chunks(model, chunks)

    # Add to FAISS index
    index.add(np.array(embeddings).astype('float32'))
    
    # Store in database
    db = SessionLocal()
    try:
        store_chunks_to_db(db, doc_title, chunks, ids, embeddings)
        return {"message": "Uploaded and indexed.", "chunks": len(chunks), "ids": ids}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        db.close()

@app.get("/debug/chunks")
def get_chunks() -> Dict[str, List[Dict[str, str]]]:
    """Get all chunks from the database with their content."""
    db = SessionLocal()
    try:
        chunks = db.query(TextChunk).all()
        return {
            "chunks": [
                {
                    "id": c.id,
                    "file_name": c.file_name,
                    "content": c.content
                } 
                for c in chunks
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve chunks from database"
        )
    finally:
        db.close()

@app.get("/answer/")
async def answer(query: str) -> Dict[str, Union[str, List[Dict[str, Union[str, float]]]]]:
    """
    Generate an answer for a query using relevant document chunks.
    """
    db = SessionLocal()
    try:
        # Search for the most relevant chunks
        search_results = search(
            query=query,
            db=db,
            model=model,
            k=10,
            similarity_threshold=0.1
        )
        results = search_results.get("results", [])
        
        if not results:
            return {
                "answer": "No relevant information found.",
                "context": []
            }

        # Build the context for the prompt
        context = {
            "query": query,
            "context": [result["chunk"] for result in results]
        }

        try:
            # Load and build prompt
            with open(PROMPT_TEMPLATE_PATH, 'r') as file:
                template = file.read()
            prompt = build_prompt(template, context)
            
            # Generate answer
            answer = generate_answer(prompt)
            
            return {
                "answer": answer,
                "context": results  # Return full result objects
            }
        except FileNotFoundError:
            raise HTTPException(
                status_code=500,
                detail=f"Prompt template not found at {PROMPT_TEMPLATE_PATH}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating answer: {str(e)}"
            )
            
    finally:
        db.close()