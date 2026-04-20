from documents.file_loader import load_pdf, load_docx, load_txt
from documents.chunker import chunk_text
from documents.vector_store import store_chunks, search_chunks
from core.llm import ask_llm
from core.memory import set_document_loaded, is_document_loaded, clear_document


# -------- LOAD DOCUMENT --------
def load_document(path):

    if not path:
        return "❌ Please provide a file path."

    try:
        if path.endswith(".pdf"):
            text = load_pdf(path)

        elif path.endswith(".docx"):
            text = load_docx(path)

        elif path.endswith(".txt"):
            text = load_txt(path)

        else:
            return "❌ Unsupported file format."

        if not text:
            return "❌ Failed to extract text from document."

        chunks = chunk_text(text)

        if not chunks:
            return "❌ Failed to create document chunks."

        store_chunks(chunks)

        set_document_loaded()

        return "✅ Document loaded and indexed successfully."

    except Exception as e:
        return f"❌ Error loading document: {str(e)}"


# -------- ASK DOCUMENT --------
def ask_document(question):

    if not question:
        return "❌ Please enter a question."

    if not is_document_loaded():
        return "❌ No document loaded. Please upload a document first."

    try:
        relevant_chunks = search_chunks(question)

        if not relevant_chunks:
            return "❌ No relevant information found in the document."

        context = "\n".join(relevant_chunks[:5])  # limit context

        prompt = f"""
You are a document analysis assistant.

Answer ONLY based on the provided context.
If the answer is not in the context, say: "Not found in document."

Context:
{context}

Question:
{question}

Answer clearly and concisely.
"""

        answer = ask_llm(prompt)

        return answer

    except Exception as e:
        return f"❌ Error during document query: {str(e)}"


# -------- CLI TEST --------
if __name__ == "__main__":

    path = input("Enter document path: ")
    print(load_document(path))

    while True:

        question = input("\nAsk a question about the document: ")

        if question.lower() == "exit":
            break

        answer = ask_document(question)

        print("\nAnswer:\n")
        print(answer)