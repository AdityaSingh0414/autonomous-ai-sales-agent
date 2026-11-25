from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
    import faiss
except ImportError:
    SentenceTransformer = None
    faiss = None

from backend.rag.document_loader import load_documents


model = None
documents = []
index = None


def _initialize_retriever():
    global model, documents, index

    if index is not None:
        return
    if SentenceTransformer is None or faiss is None:
        documents = load_documents(str(Path.cwd() / "knowledge_base"))
        return

    model = SentenceTransformer("all-MiniLM-L6-v2")
    documents = load_documents(str(Path.cwd() / "knowledge_base"))
    if not documents:
        return

    embeddings = model.encode(documents, convert_to_numpy=True)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype("float32"))


def retrieve_context(question):
    _initialize_retriever()

    if model is None or index is None or not documents:
        return "\n".join(documents)

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True
    )

    _, indices = index.search(
        query_embedding.astype("float32"),
        k=min(2, len(documents))
    )

    results = []
    for idx in indices[0]:
        if idx >= 0:
            results.append(documents[idx])

    return "\n".join(results)
