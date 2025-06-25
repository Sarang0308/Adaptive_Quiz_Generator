import torch
import google.generativeai as genai
import json
import re
from pdf_extractor import process_pdf
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


# Configure Gemini API
device = "cuda" if torch.cuda.is_available() else "gpu"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

print(f"✅ Model loaded on: {device}")

# Retrieve stored concepts from FAISS
def retrieve_concepts(faiss_store, num_results=5):
    """Fetch top related concepts from FAISS."""
    retrieved_docs = faiss_store.similarity_search("concept", k=num_results)
    return [doc.page_content for doc in retrieved_docs]

# Function to generate MCQs
def generate_question(faiss_store, numericals, difficulty):
    """Generates questions based on retrieved concepts and difficulty level."""
    retrieved_concepts = retrieve_concepts(faiss_store, num_results=5)

    if difficulty == "Easy":
        selected_concepts = retrieved_concepts[:1]  # 1 simple concept
    elif difficulty == "Medium":
        selected_concepts = retrieved_concepts[:2]  # 2 concepts/simple numericals
    else:  # Hard
        selected_concepts = retrieved_concepts[:3]  # 3+ concepts or hard numericals

    numerical_prompt = (
        f"\nA relevant numerical concept is: {numericals}. If applicable, generate a question involving numerical calculations."
        if numericals
        else ""
    )

    prompt = f"""
    You are a subject matter expert generating high-quality, contextually accurate multiple-choice questions (MCQs) for an exam. 
    Generate a **{difficulty}**-level question based strictly on the given concepts and context. Ensure the question is well-formed, unambiguous, and academically relevant.

    **Concepts and Context:**  
    {selected_concepts}  

    {numerical_prompt}  

    **Formatting Requirements:**  
    - The question must directly relate to the provided concepts.  
    - If numericals are present, they should be logically integrated into the question.  
    - Avoid generating additional numerical data if none exist in the given concepts.  
    - Ensure all answer choices are plausible and that there is a single correct answer.  

    **Return the response in strict JSON format:**  
    {{
      "question": "<Your Question Here>",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_option": "Correct Option (e.g., A)"
    }}
    """

    response = model.generate_content(prompt)

    # Extract JSON response safely using regex
    match = re.search(r'{.*}', response.text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            print(f"❗ Error decoding {difficulty} question JSON.")
            return None
    else:
        print(f"❗ No JSON block found for {difficulty} question.")
        return None

# Load concepts from FAISS
faiss_store, numericals = process_pdf("conceptCrafter.pdf")

# Display the generated questions
def display_question(question_data, difficulty):
    if question_data:
        print(f"\n🔹 {difficulty} Level Question: {question_data['question']}")
        for idx, option in enumerate(question_data['options']):
            print(f"  {chr(65 + idx)}) {option}")
        print(f"✅ Correct Answer: {question_data['correct_option']}")
    else:
        print(f"❗ No {difficulty} question generated.")

# Generate and display one question per difficulty
for level in ["Easy", "Medium", "Hard"]:
    question_data = generate_question(faiss_store, numericals, level)
    display_question(question_data, level)
