import json
import csv

def save_questions_json(questions, filename="questions.json"):
    with open(filename, "w") as f:
        json.dump(questions, f, indent=2)

def save_questions_csv(questions, filename="questions.csv"):
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "Question", "Options", "Correct"])
        for q in questions:
            writer.writerow([
                q.get("type", ""),
                q.get("question", ""),
                ", ".join(q.get("options", [])),
                q.get("correct_option", q.get("answer", ""))
            ])
