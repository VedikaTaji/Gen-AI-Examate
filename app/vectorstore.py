from pathlib import Path

import chromadb
from chromadb.errors import NotFoundError

from app.chunking import load_all_chunks
from app.embed import get_embedding_function, semantic_search

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "data" / "chroma"
COLLECTION_NAME = "aqi_documents"


def get_client():
    """Create a persistent ChromaDB client."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection(collection_name=COLLECTION_NAME):
    """Get an existing collection or create it."""
    client = get_client()

    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=get_embedding_function(),
        metadata={"hnsw:space": "cosine"},
    )


def build_index(chunk_size=900, overlap=150, collection_name=COLLECTION_NAME):
    """Chunk, embed and store documents in a named collection."""
    client = get_client()

    # Delete only the collection being rebuilt.
    try:
        client.delete_collection(name=collection_name)
        print(f"Previous collection deleted: {collection_name}")
    except NotFoundError:
        print(f"No previous collection found: {collection_name}")

    collection = client.create_collection(
        name=collection_name,
        embedding_function=get_embedding_function(),
        metadata={"hnsw:space": "cosine"},
    )

    # Generate chunks using the selected configuration.
    chunks = load_all_chunks(chunk_size=chunk_size, overlap=overlap)

    if not chunks:
        print("No document chunks found. Nothing to index.")
        return 0

    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    # Add chunks in batches.
    batch_size = 100

    for start in range(0, len(chunks), batch_size):
        end = start + batch_size

        collection.add(
            ids=ids[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end],
        )

        print(f"Indexed {min(end, len(chunks))}/{len(chunks)} chunks")

    print("\nChromaDB indexing completed.")
    print("Collection:", collection_name)
    print("Chunk size:", chunk_size)
    print("Overlap:", overlap)
    print("Total indexed chunks:", collection.count())

    return collection.count()


def search_chunks(question, top_k=5, collection_name=COLLECTION_NAME):
    """Search a selected collection semantically."""
    collection = get_collection(collection_name)

    return semantic_search(collection=collection, question=question, top_k=top_k)


if __name__ == "__main__":
    build_index()
