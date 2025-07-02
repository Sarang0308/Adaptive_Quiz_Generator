# --- File: server.py ---
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid

from extractor import extract_text_from_pdf, extract_concepts, enhance_concepts_with_context, extract_numericals
from question_generator import generate_question
from faiss_store import create_faiss

app = Flask(__name__)
CORS(app)

# In-memory database (replace with MongoDB/PostgreSQL in prod)
tests = {}
student_scores = {}

@app.route('/api/generate-test', methods=['POST'])
def generate_test():
    file = request.files['pdf']
    test_id = request.form['testId']
    num_questions = int(request.form['numQuestions'])
    file_path = f"uploads/{uuid.uuid4()}.pdf"
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)

    text = extract_text_from_pdf(file_path)
    concepts = extract_concepts(text)
    context = enhance_concepts_with_context(text, concepts)
    numericals = extract_numericals(text)
    faiss_store = create_faiss(context)

    questions = []
    levels = ["Easy", "Medium", "Hard"]
    for i in range(num_questions):
        q = generate_question(faiss_store, numericals, difficulty=levels[i % 3])
        if q: questions.append(q)

    tests[test_id] = {"questions": questions, "faiss": faiss_store}
    return jsonify({"message": "Test created", "testId": test_id})

@app.route('/api/start-test', methods=['POST'])
def start_test():
    data = request.json
    test_id = data['testId']
    roll_no = data['rollNo']
    if test_id not in tests:
        return jsonify({"error": "Test not found"}), 404
    student_scores[(test_id, roll_no)] = {"score": 0, "index": 0}
    return jsonify({"question": tests[test_id]['questions'][0]})

@app.route('/api/next-question', methods=['POST'])
def next_question():
    data = request.json
    test_id = data['testId']
    roll_no = data['rollNo']
    answer = data['answer']
    q_index = data['qIndex']
    current_q = tests[test_id]['questions'][q_index]
    correct = answer.strip() == current_q['options'][ord(current_q['correct_option']) - 65].strip()

    student_scores[(test_id, roll_no)]['score'] += int(correct)
    student_scores[(test_id, roll_no)]['index'] += 1

    if student_scores[(test_id, roll_no)]['index'] >= len(tests[test_id]['questions']):
        return jsonify({"done": True, "score": student_scores[(test_id, roll_no)]['score']})
    next_q = tests[test_id]['questions'][student_scores[(test_id, roll_no)]['index']]
    return jsonify({"done": False, "question": next_q})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
