
from pathlib import Path

import chromadb

from app.chunking import load_all_chunks
from app.embed import get_embedding_function, semantic_search


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "data" / "chroma"
COLLECTION_NAME = "aqi_documents"


def get_client():
    """Create a persistent ChromaDB client."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    return chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )


def get_collection():
    """Get the existing AQI collection or create it."""
    client = get_client()

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        metadata={"hnsw:space": "cosine"}
    )


def build_index():
    """Chunk, embed and store all supported documents."""
    client = get_client()

    # Rebuild the collection to avoid duplicate/stale chunks.
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print("Previous collection deleted.")
    except Exception:
        print("No previous collection found. Creating a new one.")

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        metadata={"hnsw:space": "cosine"}
    )

    chunks = load_all_chunks()

    if not chunks:
        print("No document chunks found. Nothing to index.")
        return 0

    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    # Add in batches to avoid oversized requests.
    batch_size = 100

    for start in range(0, len(chunks), batch_size):
        end = start + batch_size

        collection.add(
            ids=ids[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end]
        )

        print(f"Indexed {min(end, len(chunks))}/{len(chunks)} chunks")

    print("\nChromaDB indexing completed.")
    print("Collection:", COLLECTION_NAME)
    print("Total indexed chunks:", collection.count())

    return collection.count()


def search_chunks(question, top_k=5):
    """Search indexed documents semantically."""
    collection = get_collection()

    return semantic_search(
        collection=collection,
        question=question,
        top_k=top_k
    )


if __name__ == "__main__":
    build_index()
