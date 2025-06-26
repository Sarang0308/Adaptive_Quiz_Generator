# main.py

import random
import json
from question_generator import generate_question
from pdf_extractor import process_pdf

def display_question(question_data, idx):
    print(f"\n🔹 Q{idx + 1}: {question_data['question']}")
    if question_data["type"] in ["MCQ", "FIB"]:
        for i, option in enumerate(question_data["options"]):
            print(f"   {chr(65 + i)}) {option}")
    print(f"✅ Correct Answer: {question_data['correct_option']}")

def choose_difficulty(streak, counts):
    if streak >= 2 and counts["Hard"] < counts["limits"]["Hard"]:
        return "Hard"
    elif streak == 1 and counts["Medium"] < counts["limits"]["Medium"]:
        return "Medium"
    elif counts["Easy"] < counts["limits"]["Easy"]:
        return "Easy"
    elif counts["Medium"] < counts["limits"]["Medium"]:
        return "Medium"
    return "Hard"

def main():
    total_q = int(input("How many questions do you want? (15-20): "))
    total_q = max(15, min(total_q, 20))

    fib_q = max(1, total_q // 10)
    tf_q = max(1, total_q // 10)
    mcq_q = total_q - (fib_q + tf_q)

    counts = {
        "Easy": 0,
        "Medium": 0,
        "Hard": 0,
        "limits": {
            "Easy": int(0.8 * mcq_q),
            "Medium": int(0.15 * mcq_q),
            "Hard": mcq_q - int(0.8 * mcq_q) - int(0.15 * mcq_q)
        }
    }

    streak = 0
    questions = []

    faiss_store, numericals = process_pdf("conceptCrafter.pdf")

    # Generate True/False Questions
    for _ in range(tf_q):
        q = generate_question(faiss_store, numericals, "Easy", "TF")
        if q:
            questions.append(q)

    # Generate Fill in the Blanks Questions
    for _ in range(fib_q):
        q = generate_question(faiss_store, numericals, "Medium", "FIB")
        if q:
            questions.append(q)

    # Generate MCQs with Adaptive Difficulty
    for _ in range(mcq_q):
        difficulty = choose_difficulty(streak, counts)
        q = generate_question(faiss_store, numericals, difficulty, "MCQ")
        if not q:
            continue
        questions.append(q)
        counts[difficulty] += 1

        # Simulated correctness: randomly true/false; replace with real logic if needed
        answered_correct = random.choice([True, False])
        streak = streak + 1 if answered_correct else 0

    # Shuffle questions
    random.shuffle(questions)

    # Display all questions
    for idx, q in enumerate(questions):
        display_question(q, idx)

    # Save to JSON file
    with open("generated_questions.json", "w") as f:
        json.dump(questions, f, indent=2)

    print(f"\n✅ All questions saved to 'generated_questions.json'")

if __name__ == "__main__":
    main()
