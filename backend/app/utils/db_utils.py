from models.database import TextChunk
import json

def store_chunks_to_db(db, doc_title, chunks, ids, embeddings):
    for i, (chunk, uid, emb) in enumerate(zip(chunks, ids, embeddings)):
        record = TextChunk(
            id=uid,
            file_name=doc_title,
            content=chunk,
            position=i,
            embedding=json.dumps(emb.tolist())
        )
        db.add(record)
    db.commit()