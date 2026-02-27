import os
from langchain_community.document_loaders import PyPDFLoader


def read_pdf(path: str) -> str:
    """Read full PDF text once."""

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found at {path}")

    loader = PyPDFLoader(path)
    docs = loader.load()

    full_text = ""
    for page in docs:
        content = page.page_content.replace("\n\n", "\n")
        full_text += content + "\n"

    return full_text