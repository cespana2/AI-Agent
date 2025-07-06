import json
import numpy as np
from typing import List, Dict, Optional, Union
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
from models.database import TextChunk

def search(
    query: str, 
    db: Session, 
    model: SentenceTransformer, 
    k: int = 5,
    similarity_threshold: float = 0.0
) -> Dict[str, List[Dict[str, Union[str, float]]]]:
    """
    Search for the most similar document chunks using database records.

    Args:
        query (str): The search query
        db (Session): SQLAlchemy database session
        model (SentenceTransformer): The encoder model
        k (int, optional): Number of results to return. Defaults to 5.
        similarity_threshold (float, optional): Minimum similarity score. Defaults to 0.0.

    Returns:
        Dict[str, List[Dict[str, Union[str, float]]]]: Search results with chunks and scores
    """
    try:
        # Generate and normalize query embedding
        query_embedding = model.encode([query], normalize_embeddings=True)[0]
        
        # Get all chunks from database
        chunks = db.query(TextChunk).all()
        if not chunks:
            return {"results": [], "message": "No documents found in database"}
        
        # Create embedding matrix from stored embeddings
        embedding_matrix = np.array([
            json.loads(chunk.embedding) for chunk in chunks
        ], dtype=np.float32)
        
        # Calculate cosine similarities (embeddings are already normalized)
        similarities = np.dot(query_embedding, embedding_matrix.T)
        
        # Get top k indices
        top_indices = np.argsort(similarities)[-k:][::-1]
        
        # Build results
        results = [
            {
                "chunk": chunks[idx].content,
                "similarity": float(similarities[idx]),
                "id": chunks[idx].id,
                "position": chunks[idx].position
            }
            for idx in top_indices
            if similarities[idx] > similarity_threshold
        ]
        print(f"Found {len(results)} relevant chunks out of {len(chunks)} total chunks.")
        
        return {
            "results": results,
            "total_chunks": len(chunks),
            "filtered_chunks": len(results)
        }
        
    except Exception as e:
        return {
            "results": [],
            "error": str(e),
            "message": "Error occurred during search"
        }