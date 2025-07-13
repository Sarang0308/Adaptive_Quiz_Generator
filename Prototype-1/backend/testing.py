# question_generator.py

import torch
import google.generativeai as genai
import json
import re
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
device = "cuda" if torch.cuda.is_available() else "gpu"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

print(f"✅ Model loaded on: {device}")

# Retrieve top concepts from FAISS
def retrieve_concepts(faiss_store, num_results=6):
    """Fetch top related concepts from FAISS."""
    retrieved_docs = faiss_store.similarity_search("concept", k=num_results)
    return [doc.page_content for doc in retrieved_docs]

# Single-prompt question generation
def generate_question_bank(faiss_store, numericals, total_questions):
    """
    Generates a set of questions (MCQ, TF, FIB) in a single Gemini API call.
    Uses concept context from FAISS and numerical expressions (if any).
    """
    retrieved_concepts = retrieve_concepts(faiss_store, num_results=6)

    # Calculate distribution
    num_mcq = int(0.8 * total_questions)
    num_tf = int(0.1 * total_questions)
    num_fib = total_questions - num_mcq - num_tf

    base_context = "\n".join(retrieved_concepts)
    numerical_part = f"\nRelevant numerical expressions: {numericals}." if numericals else ""

    # Gemini prompt
    prompt = f"""
You are a subject matter expert. Based strictly on the given academic context, generate exam questions.
base questions={total_questions}
🔹 Question Distribution:
- 80% MCQs, 10% True/False, 10% Fill-in-the-Blanks (FIB)
**BUT GENERATE WORST CASE NUMBER OF QUESTIONS ACCORDING TO DIFFICULT AS IT IS ADAPTIVE 
 EXAMPLE- WHEN A PERSON GETS TWO CORRECT ANSWERS THEN DIFFICULTY LEVEL RISES(I.E. STREAK WHICH IS 2) AND IF PERSON HE GETS WRONG THEN STREAK GOES 0
  AND DIFFICULTY LEVEL DROPS I.E. HARD-> MEDIUM ELSE MEDIUM -> EASY 
 CONSIDERING THIS POSSIBILTY GENERATE QUESTION AT WORST CASE POSSIBLE
  example generate number of easy question as total number of question and use the analogy to find the number of hard and medium questions  **
- Mix of Easy, Medium, Hard difficulties 
- Use numerical concepts if available
- Each question must be based on the provided context

📚 Concepts:
{base_context}
{numerical_part}

🔸 Return strict JSON:
{{
  "questions": [
    {{
      "type": "MCQ",
      "difficulty": "Easy",
      "question": "Which of the following ...?",
      "options": ["A", "B", "C", "D"],
      "correct_option": "B"
    }},
    {{
      "type": "TF",
      "difficulty": "Medium",
      "question": "X is always true.",
      "correct_option": "False"
    }},
    {{
      "type": "FIB",
      "difficulty": "Hard",
      "question": "The ____ controls ...",
      "options": ["A", "B", "C", "D"],
      "correct_option": "C"
    }}
  ]
}}
Ensure the list is in valid JSON.
"""

    # Call Gemini
    response = model.generate_content(prompt)
    match = re.search(r'{.*}', response.text, re.DOTALL)

    if match:
        try:
            data = json.loads(match.group(0))
            return data["questions"]
        except json.JSONDecodeError:
            print("❗ JSON Decode Error in Gemini response.")
            return []
    else:
        print("❗ No valid JSON found in Gemini response.")
        return []
