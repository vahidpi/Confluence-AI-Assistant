# 🤖 Confluence AI Assistant

An internal AI-powered assistant that indexes your Confluence documentation and answers natural language questions with citations and links.

## 🚀 Features

-  Ingests content from Confluence spaces
-  Splits content into chunks with metadata
-  Generates vector embeddings using Hugging Face or OpenAI
-  Stores embeddings in FAISS (can be swapped with Qdrant/Pinecone)
-  Answers user questions using GPT-4 or other LLMs
-  Displays results in a Streamlit web interface

## 📦 Tech Stack

| Layer              | Tools / Services                     |
|-------------------|--------------------------------------|
| Ingestion          | `atlassian-python-api`              |
| Chunking           | `BeautifulSoup`, custom logic       |
| Embeddings         | `sentence-transformers`, `openai`   |
| Vector DB          | `faiss`                             |
| LLM                | `OpenAI GPT-4`                      |
| Interface          | `Streamlit`                         |
| Config             | `.env`, `dotenv`                    |

## 🔧 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/confluence-ai-assistant.git
cd confluence-ai-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a .env file in the root directory with your API keys and settings (see env template).


### 4. Run the Indexer
```bash
python main.py
```

### 5. Launch the Web UI
```bash
streamlit run app/interface/streamlit_ui.py
```

✅ MVP Goals
- Crawl a selected Confluence space
- Index and embed document content
- Answer questions using relevant chunks
- Provide citations and document links

📈 Future Enhancements
- Multi-turn memory (LangChain Agent)
- Live sync with Confluence updates
- Summarization and query rewriting
- Slack or Teams bot interface

🔐 Security Notes
- Integrate SSO/OAuth2 for future access control
- Never expose restricted content via QA results



## Embedding Storage: Prototype vs Real-World
The current implementation of store_embeddings() uses an in-memory FAISS index and a Python list to store vector embeddings and their metadata. This approach is ideal for prototyping but does not persist data — meaning all embeddings and metadata are lost when the app restarts.

## Real-World Solution Options
### Option 1: FAISS + Disk Storage
To persist embeddings using FAISS, save the index and metadata separately:

```bash
import faiss
import pickle

# Save FAISS index
faiss.write_index(index, "confluence_index.faiss")

# Save metadata (e.g., chunk text, URL)
with open("metadata.pkl", "wb") as f:
    pickle.dump(stored_chunks, f)
```
To load later:
```bash
index = faiss.read_index("confluence_index.faiss")
with open("metadata.pkl", "rb") as f:
    stored_chunks = pickle.load(f)
```
Best for simple local or self-hosted deployments.

### Option 2: Use a Vector Database (e.g., Qdrant)
For scalable and production-ready storage, use a vector DB like Qdrant:
```bash
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

client = QdrantClient(host="localhost", port=6333)

# Create a collection
client.recreate_collection(
    collection_name="confluence_chunks",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Upload vectors with metadata
client.upload_points(
    collection_name="confluence_chunks",
    points=[
        PointStruct(
            id=i,
            vector=chunk["embedding"],
            payload=chunk["metadata"]
        ) for i, chunk in enumerate(vectors)
    ]
)
```
Qdrant also supports cloud hosting, filters, full-text metadata search, and fast semantic queries.