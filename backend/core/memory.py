
# -------- CHAT MEMORY --------
_chat_memory = []

def add_to_chat(role, content):
    if role and content:
        _chat_memory.append({
            "role": role,
            "content": content
        })

def get_chat_memory():
    return _chat_memory.copy()  # prevent accidental mutation

def clear_chat_memory():
    _chat_memory.clear()


# -------- RESEARCH MEMORY --------
_research_memory = {
    "company": None,
    "report": None
}

def set_research(company, report):
    _research_memory["company"] = company
    _research_memory["report"] = report

def get_research():
    return _research_memory.copy()

def clear_research():
    _research_memory["company"] = None
    _research_memory["report"] = None

def is_same_company(company):
    return _research_memory["company"] == company


# -------- DOCUMENT MEMORY --------
_document_memory = {
    "loaded": False
}

def set_document_loaded():
    _document_memory["loaded"] = True

def is_document_loaded():
    return _document_memory["loaded"]

def clear_document():
    _document_memory["loaded"] = False