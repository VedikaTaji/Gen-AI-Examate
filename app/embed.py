
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


def get_embedding_function():
    """Return Chroma's default text embedding function."""
    return DefaultEmbeddingFunction()


def semantic_search(collection, question, top_k=5):
    """Find the most semantically relevant document chunks."""
    question = question.strip()

    if not question:
        raise ValueError("Search question cannot be empty.")

    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[question],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    hits = []

    for index, document in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][index]
        distance = results["distances"][0][index]

        hits.append({
            "text": document,
            "source": metadata.get("source", ""),
            "title": metadata.get("title", ""),
            "page": metadata.get("page", ""),
            "chunk_index": metadata.get("chunk_index", 0),
            "distance": round(float(distance), 4),
            "similarity": round(1 - float(distance), 4)
        })

    return hits
