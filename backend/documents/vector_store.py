from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------- GLOBAL STORAGE --------
documents = []
vectorizer = TfidfVectorizer()
doc_vectors = None


# -------- STORE CHUNKS --------
def store_chunks(chunks):
    global documents, vectorizer, doc_vectors

    if not chunks:
        return

    documents = chunks
    doc_vectors = vectorizer.fit_transform(documents)


# -------- SEARCH --------
def search_chunks(query, top_k=3):
    global documents, vectorizer, doc_vectors

    if not documents or doc_vectors is None:
        return []

    query_vec = vectorizer.transform([query])

    similarities = cosine_similarity(query_vec, doc_vectors)[0]

    top_indices = similarities.argsort()[-top_k:][::-1]

    return [documents[i] for i in top_indices]