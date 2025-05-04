import faiss
import numpy as np

index = faiss.IndexFlatL2(384)  # 384 for MiniLM
stored_chunks = []

def store_embeddings(vectors):
    global stored_chunks
    embeddings_np = np.array([v["embedding"] for v in vectors])
    index.add(embeddings_np)
    stored_chunks.extend(vectors)

def search_similar(query_emb, top_k=5):
    _, indices = index.search(np.array([query_emb]), top_k)
    return [stored_chunks[i] for i in indices[0] if i < len(stored_chunks)]
