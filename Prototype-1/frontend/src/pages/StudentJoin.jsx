import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function StudentJoin() {
  const nav = useNavigate();
  const [quizId, setQuizId] = useState("");
  const [name, setName] = useState("");

  const start = async () => {
    const res = await fetch(`http://localhost:8000/api/quiz/${quizId}`);
    const data = await res.json();
    if (data.status === "valid") {
      nav(`/quiz/${quizId}/${name}`);
    } else {
      alert("Invalid Quiz ID");
    }
  };

  return (
    <div className="max-w-md mx-auto space-y-4">
      <h2 className="text-2xl">Join Quiz</h2>
      <input placeholder="Quiz ID" value={quizId} onChange={(e) => setQuizId(e.target.value)} className="w-full input" />
      <input placeholder="Your Name" value={name} onChange={(e) => setName(e.target.value)} className="w-full input" />
      <button onClick={start} className="btn" disabled={!quizId || !name}>Start Quiz</button>
    </div>
  );
}
