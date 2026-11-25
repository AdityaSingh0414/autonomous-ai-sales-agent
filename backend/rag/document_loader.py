from pathlib import Path


def load_documents(folder="knowledge_base"):

    documents = []

    for file in Path(folder).glob("*.txt"):

        text = file.read_text(encoding="utf-8")

        documents.append(text)

    return documents