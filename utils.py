import fitz

def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

def chunk_text(text, chunk_size=12000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]