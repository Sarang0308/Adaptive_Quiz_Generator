

# import torch
# print("CUDA Available:", torch.cuda.is_available())
# print("GPU Device Name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU Found")
import pdfplumber # type: ignore


def extract_text_from_pdf(pdf_path):
    text_content = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_content += page.extract_text(x_tolerance=2, y_tolerance=2) or ""
    return text_content


import spacy

nlp = spacy.load("en_core_web_sm")

def extract_key_points(text):
    doc = nlp(text)
    key_points = []
    
    # Extract headings (lines with uppercase or bold text)
    for sent in doc.sents:
        if len(sent.text.split()) <= 10 and (sent.text.isupper() or sent.text.istitle()):
            key_points.append(sent.text.strip())

    
    # Extract key points (bullets or short factual lines)
    key_points += [sent.text.strip() for sent in doc.sents 
                if sent.text.strip().startswith(("-", "•", "*", "→", "1.", "2."))]

    return key_points

from keybert import KeyBERT

kw_model = KeyBERT()

def extract_concepts(text):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=10)
    return [kw[0] for kw in keywords]

import re
from sympy import sympify, SympifyError

import pytesseract
from PIL import Image

def extract_text_ocr(pdf_path):
    text_content = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if page.to_image:
                text_content += pytesseract.image_to_string(page.to_image().original)
            else:
                text_content += page.extract_text() or ""
    return text_content

def extract_numericals(text):
    pattern = r'(\d+\s*[+\-*/=]\s*\d+(?:\s*[+\-*/=]\s*\d+)*)'
    matches = re.findall(pattern, text)
    
    numericals = []
    for match in matches:
        try:
            numericals.append(sympify(match))  # Validates solvable expressions
        except SympifyError:
            continue
    return numericals

def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    key_points = extract_key_points(text)
    concepts = extract_concepts(text)
    numericals = extract_numericals(text)
    
    print("🔹 Key Points Identified:\n", key_points)
    print("\n🔹 Key Concepts Identified:\n", concepts)
    print("\n🔹 Detected Numerical Expressions:\n", numericals)

if __name__ == "__main__":
    process_pdf("conceptCrafter.pdf")
