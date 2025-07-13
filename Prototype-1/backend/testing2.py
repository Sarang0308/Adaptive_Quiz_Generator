from testing import generate_question_bank
from pdf_extractor import process_pdf

faiss_store, numericals = process_pdf("sample.pdf")
questions = generate_question_bank(faiss_store, numericals, total_questions=7)

# Save to JSON
import json
with open("question_bank.json", "w") as f:
    json.dump(questions, f, indent=2)
