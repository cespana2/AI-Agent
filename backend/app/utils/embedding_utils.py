import numpy as np

def embed_chunks(model, chunks):
    embeddings = model.encode(chunks)
    normalized = embeddings / np.linalg.norm(embeddings, axis=1)[:, np.newaxis]
    return normalized