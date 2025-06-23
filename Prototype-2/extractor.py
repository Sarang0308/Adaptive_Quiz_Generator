import pdfplumber
import spacy
from keybert import KeyBERT
import re
from sympy import sympify, SympifyError
from sentence_transformers import SentenceTransformer

nlp = spacy.load("en_core_web_sm")
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
kw_model = KeyBERT(sentence_model)

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_concepts(text, top_n=10):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=top_n)
    return [kw[0] for kw in keywords]

def enhance_context(text, concepts):
    doc = nlp(text)
    context = {}
    for concept in concepts:
        for sent in doc.sents:
            if concept in sent.text:
                context[concept] = sent.text.strip()
                break
    return context

def extract_numericals(text):
    pattern = r'\b\d+\.?\d*\s*[+\-*/=]\s*\d+\.?\d*\b'
    matches = re.findall(pattern, text)
    return [str(sympify(m)) for m in matches if is_valid_expr(m)]

def is_valid_expr(expr):
    try:
        sympify(expr)
        return True
    except SympifyError:
        return False
