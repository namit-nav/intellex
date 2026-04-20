import chromadb
from sentence_transformers import SentenceTransformer
import uuid


# -------- INIT CHROMA (PERSISTENT) --------
client = chromadb.Client()

# ✅ FIX: no crash if exists
collection = client.get_or_create_collection("documents")

# -------- EMBEDDING MODEL --------
model = SentenceTransformer("all-MiniLM-L6-v2")


# -------- STORE CHUNKS --------
def store_chunks(chunks):

    if not chunks:
        return

    embeddings = model.encode(chunks).tolist()

    ids = [str(uuid.uuid4()) for _ in chunks]  # unique IDs

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )


# -------- SEARCH --------
def search_chunks(query, top_k=3):

    if not query:
        return []

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    if not results or not results.get("documents"):
        return []

    return results["documents"][0]