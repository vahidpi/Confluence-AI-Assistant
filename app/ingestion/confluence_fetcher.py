from atlassian import Confluence
import os

def fetch_confluence_docs():
    confluence = Confluence(
        url=os.getenv("CONFLUENCE_URL"),
        username=os.getenv("CONFLUENCE_USER"),
        password=os.getenv("CONFLUENCE_API_TOKEN")
    )

    space_key = os.getenv("CONFLUENCE_SPACE_KEY")
    pages = confluence.get_all_pages_from_space(space=space_key, limit=50, status="current")
    docs = []

    for page in pages:
        content = confluence.get_page_by_id(page['id'], expand='body.storage')
        docs.append({
            "id": page['id'],
            "title": page['title'],
            "url": f"{os.getenv('CONFLUENCE_URL')}/pages/viewpage.action?pageId={page['id']}",
            "html": content['body']['storage']['value']
        })

    return docs

