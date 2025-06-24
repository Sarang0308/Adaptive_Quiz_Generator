from extractor import extract_text_from_pdf, extract_concepts, enhance_context, extract_numericals
from faiss_store import create_faiss
from question_generator import generate_question
from utils import save_questions_json, save_questions_csv

pdf_path = "sample2.pdf"
text = extract_text_from_pdf(pdf_path)
concepts = extract_concepts(text)
context_map = enhance_context(text, concepts)
numericals = extract_numericals(text)

faiss_store = create_faiss(context_map)

question_types = ["MCQ", "TrueFalse", "FillBlank"]
difficulties = ["Easy", "Medium", "Hard"]
all_questions = []

for diff in difficulties:
    for qtype in question_types:
        q = generate_question(faiss_store, numericals, diff, qtype)
        if q:
            all_questions.append(q)

save_questions_json(all_questions)
save_questions_csv(all_questions)
print(f"✅ Generated {len(all_questions)} questions.")
