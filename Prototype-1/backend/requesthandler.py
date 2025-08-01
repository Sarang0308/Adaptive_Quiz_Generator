# requesthandler.py

import uuid
from fastapi import UploadFile
from pdf_extractor import process_pdf
from question_generator import generate_question

# In-memory store (replace with DB in production)
QUIZZES = {}
STUDENT_PROGRESS = {}

# POST /api/upload → Admin uploads PDF, returns quiz_id
def upload_pdf_and_create_quiz(file: UploadFile, total_questions: int):
    contents = file.file.read()
    pdf_path = f"temp_{uuid.uuid4()}.pdf"
    with open(pdf_path, "wb") as f:
        f.write(contents)

    faiss_store, numericals = process_pdf(pdf_path)
    quiz_id = str(uuid.uuid4())

    QUIZZES[quiz_id] = {
        "faiss_store": faiss_store,
        "numericals": numericals,
        "questions": [],
        "total_questions": total_questions 
    }
    return {"quiz_id": quiz_id}

# GET /api/quiz/:id → validate quiz code
def get_quiz_info(quiz_id: str):
    if quiz_id in QUIZZES:
        return {"status": "valid", "quiz_id": quiz_id}
    return {"status": "invalid"}

# GET /api/quiz/:id/q → get next question for student
def get_next_question(quiz_id: str, student_id: str):
    key = f"{quiz_id}:{student_id}"
    if key not in STUDENT_PROGRESS:
        STUDENT_PROGRESS[key] = {
            "streak": 0, "questions": [], "score": 0, 
            "current_q": None, "used_q": [],
        }
    quiz_data = QUIZZES.get(quiz_id)
    if not quiz_data:
        return {"error": "Invalid quiz ID"}
    
    MAX_QUESTIONS = quiz_data["total_questions"]
    progress = STUDENT_PROGRESS[key]

    # ❌ If question count reached limit, stop
    if len(progress["questions"]) >= MAX_QUESTIONS:
        return {"end": True, "score": progress["score"], "total": MAX_QUESTIONS}

    # ✅ Return current question if exists
    if progress["current_q"] is not None:
        return progress["current_q"]

    # 🎯 Adjust difficulty based on streak
    streak = progress["streak"]
    difficulty = "Easy" if streak <= 0 else "Medium" if streak == 1 else "Hard"

    from random import choices
    q_type = choices(["MCQ", "TF", "FIB"], weights=[0.8, 0.1, 0.1])[0]

    quiz_data = QUIZZES[quiz_id]
    attempts = 0
    MAX_ATTEMPTS = 5
    q = None

    while attempts < MAX_ATTEMPTS:
        candidate = generate_question(quiz_data["faiss_store"], quiz_data["numericals"], difficulty, q_type)
        if candidate and candidate["question"] not in progress["used_q"]:
            q = candidate
            break
        attempts += 1

    if not q:
        return {"error": "No new question could be generated."}

    progress["current_q"] = q
    progress["used_q"].append(q["question"])  # ✅ Mark as used
    return q


# POST /api/quiz/:id/ans → student submits answer
def submit_answer(quiz_id: str, student_id: str, answer: str):
    key = f"{quiz_id}:{student_id}"
    progress = STUDENT_PROGRESS.get(key)
    if not progress or not progress.get("current_q"):
        return {"error": "No current question"}

    q = progress["current_q"]
    correct = False

    if q["type"] == "TF":
        correct = answer.strip().lower() == q["correct_option"].strip().lower()
    else:
        idx = ord(q["correct_option"].upper()) - 65
        correct = answer.strip() == q["options"][idx].strip()

    if correct:
        progress["score"] += 1
        progress["streak"] += 1
    else:
        progress["streak"] = 0

    progress["questions"].append({
        "question": q["question"],
        "type": q["type"],
        "difficulty": q["difficulty"],
        "answer": answer,
        "correct": q["correct_option"],
        "is_correct": correct
    })

    progress["current_q"] = None  # Reset for next

    # ✅ Check if max questions reached
    total_limit = QUIZZES[quiz_id].get("total_questions", 10)  # Default to 10 if not set
    if len(progress["questions"]) >= total_limit:
        return {
            "message": "Quiz complete",
            "score": progress["score"],
            "done": True,
            "responses": progress["questions"]
        }

    return {"correct": correct, "score": progress["score"], "done": False}
