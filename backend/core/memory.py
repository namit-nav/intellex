# -------- CHAT MEMORY --------
_chat_memory = []
MAX_CHAT_HISTORY = 20


def add_to_chat(role, content):
    if not role or not content:
        return

    _chat_memory.append({
        "role": role,
        "content": content
    })

    # Limit memory size
    if len(_chat_memory) > MAX_CHAT_HISTORY:
        _chat_memory.pop(0)


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
    if not company or not report:
        return

    _research_memory["company"] = company.strip().lower()
    _research_memory["report"] = report


def get_research():
    return _research_memory.copy()


def clear_research():
    _research_memory["company"] = None
    _research_memory["report"] = None


def is_same_company(company):
    if not company:
        return False

    return _research_memory["company"] == company.strip().lower()


# -------- DOCUMENT MEMORY --------
_document_memory = {
    "loaded": False,
    "content": None
}


def set_document(content):
    if not content:
        return

    _document_memory["loaded"] = True
    _document_memory["content"] = content


def get_document():
    return _document_memory["content"]


def is_document_loaded():
    return _document_memory["loaded"]


def clear_document():
    _document_memory["loaded"] = False
    _document_memory["content"] = None