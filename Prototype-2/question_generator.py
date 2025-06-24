import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv
from faiss_store import retrieve_concepts

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_question(faiss_store, numericals, difficulty="Easy", q_type="MCQ"):
    base_context = retrieve_concepts(faiss_store)
    numerical_info = f"\nUse this numerical: {numericals[0]}" if numericals else ""
    prompt = build_prompt(base_context, numerical_info, difficulty, q_type)

    response = model.generate_content(prompt)
    return extract_json(response.text)

def build_prompt(concepts, numerical, difficulty, q_type):
    format_part = {
        "MCQ": '''{
  "type": "MCQ",
  "question": "...",
  "options": ["A", "B", "C", "D"],
  "correct_option": "A"
}''',
        "TrueFalse": '''{
  "type": "TrueFalse",
  "question": "...",
  "answer": "True"
}''',
        "FillBlank": '''{
  "type": "FillBlank",
  "question": "___ is the ..."
}'''
    }

    return f"""
You are an expert question generator. Generate a **{difficulty}** {q_type} based on:

**Concepts and Context:**
{concepts}
{numerical}

Respond ONLY in JSON format like:
{format_part[q_type]}
"""

def extract_json(text):
    match = re.search(r'{.*}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None
