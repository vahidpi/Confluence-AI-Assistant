from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(chunks):
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    return [
        {
            "embedding": emb,
            "text": chunk["text"],
            "metadata": chunk["metadata"]
        } for emb, chunk in zip(embeddings, chunks)
    ]
