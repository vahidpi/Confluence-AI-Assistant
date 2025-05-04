from app.ingestion.confluence_fetcher import fetch_confluence_docs
from app.processing.chunker import chunk_documents
from app.embedding.embedder import generate_embeddings
from app.vector_store.vector_db import store_embeddings
from app.qa.qa_pipeline import answer_question

def main():
    docs = fetch_confluence_docs()
    chunks = chunk_documents(docs)
    vectors = generate_embeddings(chunks)
    store_embeddings(vectors)

    # Example query
    query = "How to Deploy a Dockerized App to AWS ECS?"
    response = answer_question(query)
    print(response)

if __name__ == "__main__":
    main()
