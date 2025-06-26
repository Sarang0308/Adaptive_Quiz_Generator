# question_generator.py

import torch
import google.generativeai as genai
import json
import re
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
device = "cuda" if torch.cuda.is_available() else "gpu"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

print(f"✅ Model loaded on: {device}")

def retrieve_concepts(faiss_store, num_results=5):
    retrieved_docs = faiss_store.similarity_search("concept", k=num_results)
    return [doc.page_content for doc in retrieved_docs]

def build_prompt(concepts, numericals, difficulty, q_type):
    base_context = "\n".join(concepts)
    numerical_part = f"\nA numerical concept is: {numericals}." if numericals else ""

    type_instruction = {
        "MCQ": """
Generate a multiple-choice question (MCQ) strictly based on the given concepts.
""",
        "TF": """
Generate a True or False question based strictly on the given concepts.
Ensure the statement is unambiguous and clearly either true or false.
""",
        "FIB": """
Generate a fill-in-the-blank question with four options based on the concepts.
Mark the correct answer.
"""
    }

    formatting = {
        "MCQ": '''
Return in JSON:
{
  "type": "MCQ",
  "question": "Your question",
  "options": ["A", "B", "C", "D"],
  "correct_option": "A"
}''',
        "TF": '''
Return in JSON:
{
  "type": "TF",
  "question": "Your true or false question",
  "correct_option": "True" or "False"
}''',
        "FIB": '''
Return in JSON:
{
  "type": "FIB",
  "question": "Your FIB with ____",
  "options": ["A", "B", "C", "D"],
  "correct_option": "A"
}'''
    }

    return f"""
You are a subject matter expert generating high-quality exam questions. Use the given context and concepts.

Concepts:
{base_context}

{numerical_part}

{type_instruction[q_type]}

Ensure academic relevance and clarity.

{formatting[q_type]}
"""

def generate_question(faiss_store, numericals, difficulty, q_type="MCQ"):
    retrieved_concepts = retrieve_concepts(faiss_store, num_results=5)
    if difficulty == "Easy":
        selected_concepts = retrieved_concepts[:1]
    elif difficulty == "Medium":
        selected_concepts = retrieved_concepts[:2]
    else:
        selected_concepts = retrieved_concepts[:3]

    prompt = build_prompt(selected_concepts, numericals, difficulty, q_type)
    response = model.generate_content(prompt)
    match = re.search(r'{.*}', response.text, re.DOTALL)
    # Add at the end of generate_question() function in question_generator.py
    if match:
        try:
            data = json.loads(match.group(0))
            data["difficulty"] = difficulty  # Add difficulty level to output
            data["numericals"] = numericals if numericals else []
            return data
        except json.JSONDecodeError:
            print(f"❗ Error decoding JSON for {difficulty}-{q_type}")
            return None

