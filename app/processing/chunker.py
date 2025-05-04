from bs4 import BeautifulSoup

def chunk_documents(documents):
    chunks = []
    for doc in documents:
        soup = BeautifulSoup(doc["html"], "html.parser")
        paragraphs = soup.get_text().split("\n")
        for p in paragraphs:
            if len(p.strip()) > 50:
                chunks.append({
                    "text": p.strip(),
                    "metadata": {
                        "title": doc["title"],
                        "url": doc["url"]
                    }
                })
    return chunks
