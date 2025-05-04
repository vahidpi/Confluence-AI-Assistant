from app.embedding.embedder import model
from app.vector_store.vector_db import search_similar
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment")
openai_client = OpenAI(api_key=api_key)

def answer_question(question):
    query_emb = model.encode([question])[0]
    relevant_chunks = search_similar(query_emb)

    context = "\n\n".join([f"{c['text']}\n(Source: {c['metadata']['url']})" for c in relevant_chunks])
    prompt = f"""Answer the question using the context below. Cite sources.
    Context: {context}
    Question: {question}"""

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
