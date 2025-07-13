from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from requesthandler import (
    upload_pdf_and_create_quiz,
    get_quiz_info,
    get_next_question,
    submit_answer,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload")
async def upload(file: UploadFile, total_questions: int = Form(...)):  # 👈 updated
    return upload_pdf_and_create_quiz(file, total_questions) 

@app.get("/api/quiz/{quiz_id}")
def quiz_exists(quiz_id: str):
    return get_quiz_info(quiz_id)

@app.get("/api/quiz/{quiz_id}/q")
def next_question(quiz_id: str, student_id: str):
    return get_next_question(quiz_id, student_id)

@app.post("/api/quiz/{quiz_id}/ans")
async def answer(
    quiz_id: str,
    student_id: str = Form(...),
    answer: str = Form(...)
):
    return submit_answer(quiz_id, student_id, answer)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
