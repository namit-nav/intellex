from documents.chunker import chunk_text
from documents.vector_store import store_chunks, search_chunks
from core.llm import ask_llm
from core.memory import set_document, is_document_loaded, clear_document


# -------- LOAD DOCUMENT FROM TEXT --------
def load_document_text(content):

    if not content:
        return "Please provide document content."

    try:
        chunks = chunk_text(content)

        if not chunks:
            return "Failed to process document."

        store_chunks(chunks)

        set_document(content)

        return "Document loaded successfully."

    except Exception as e:
        return f"Error loading document: {str(e)}"


# -------- ASK DOCUMENT --------
def ask_document(question, content=None):

    if not question:
        return "Please enter a question."

    # If content is sent from frontend → load it first
    if content:
        load_document_text(content)

    if not is_document_loaded():
        return "No document loaded."

    try:
        relevant_chunks = search_chunks(question)

        if not relevant_chunks:
            return "No relevant information found."

        context = "\n".join(relevant_chunks[:5])

        prompt = f"""
You are a strict document analysis assistant.

Rules:
- Answer ONLY from the provided context
- If answer is not present, say: Not found in document
- Do NOT assume or guess
- Keep answer concise

Context:
{context}

Question:
{question}
"""

        answer = ask_llm(prompt)

        return answer

    except Exception as e:
        return f"Error during query: {str(e)}"