import pdfplumber  # PDF Extraction
import spacy  # NLP for Concept-Context Mapping
from keybert import KeyBERT  # Concept Extraction
import re
from sympy import sympify, SympifyError  # Numerical Extraction

# Initialize models
nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()

# PDF Text Extraction
def extract_text_from_pdf(pdf_path):
    text_content = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_content += page.extract_text() or ""
    return text_content

# Concept Extraction with KeyBERT
def extract_concepts(text):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=10)
    return [kw[0] for kw in keywords]

# Enhanced Concept-Context Mapping
def enhance_concepts_with_context(text, concepts):
    doc = nlp(text)
    enriched_concepts = {}
    
    for concept in concepts:
        for sent in doc.sents:
            if concept in sent.text:
                enriched_concepts[concept] = sent.text.strip()
                break  # Stop after finding the first valid context
    
    return enriched_concepts

# Numerical Data Extraction
def extract_numericals(text):
    pattern = r'\b\d+\.?\d*\s*[+\-*/=]\s*\d+\.?\d*\b'
    matches = re.findall(pattern, text)
    numericals = []

    for match in matches:
        try:
            numericals.append(str(sympify(match)))  # Ensures valid expressions only
        except SympifyError:
            continue
    return numericals

# Process PDF
def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    concepts = extract_concepts(text)
    concept_context = enhance_concepts_with_context(text, concepts)
    numericals = extract_numericals(text)

    # print("🔹 Key Concepts Identified:", concepts)
    # print("\n🔹 Concept with Context Mapping:", concept_context)
    # print("\n🔹 Detected Numerical Expressions:", numericals)
    return concept_context,numericals

if __name__ == "__main__":
    process_pdf("conceptCrafter.pdf")
