import re


def clean_text(text):

    # Remove multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)

    # Remove long numbers (IDs, tracking codes)
    text = re.sub(r'\b\d{8,}\b', '', text)

    # Remove unwanted symbols
    text = re.sub(r'[^\w\s.,%()-]', '', text)

    # Remove repeated punctuation
    text = re.sub(r'\.{2,}', '.', text)

    # Trim spaces
    text = text.strip()

    return text