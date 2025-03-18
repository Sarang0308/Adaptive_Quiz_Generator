
#
import google.generativeai as genai
import json
import re
from pdf_extractor import process_pdf
# Configure Gemini API
genai.configure(api_key="Your API Key Here")
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate MCQs based on concepts and context
def generate_question(concept_context,numericals, difficulty):
    prompt = f"""
    Generate a {difficulty} multiple-choice question (MCQ) based on the following concept and its related context.

    Concept and Context: "{concept_context}"
    Difficulty Level: {difficulty}
    For these {numericals} consider this numerical expression and generate a Hard Question based on it if present.
    **Format the response strictly in the following JSON format:**
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

# Sample Concept and Context
concept_context,numericals = process_pdf("conceptCrafter.pdf")

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
    question_data = generate_question(concept_context,numericals, level)
    display_question(question_data, level)
