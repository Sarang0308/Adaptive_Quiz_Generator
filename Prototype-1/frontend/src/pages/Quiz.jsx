import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";

export default function Quiz() {
  const { quizId, studentId } = useParams();
  const [q, setQ] = useState(null);
  const [answer, setAnswer] = useState("");
  const [score, setScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(60);
  const [ended, setEnded] = useState(false);
  const navigate = useNavigate();
    const fetchQ = async () => {
    const res = await fetch(`http://localhost:8000/api/quiz/${quizId}/q?student_id=${studentId}`);
    const data = await res.json();

        if (data.end) {
            alert(`✅ Quiz completed!\n\nScore: ${data.score}/${data.total}`);
            navigate("/");
            // or redirect to results page
            return;
        }

        setQ(data);
        setAnswer("");
        setTimeLeft(60);
    };


  useEffect(() => {
    fetchQ();
  }, []);

  useEffect(() => {
    if (!q || ended) return;
    if (timeLeft <= 0) submitAnswer("TIMEUP");
    const timer = setInterval(() => setTimeLeft((t) => t - 1), 1000);
    return () => clearInterval(timer);
  }, [timeLeft, q]);

  const submitAnswer = async (ans) => {
    const form = new FormData();
    form.append("student_id", studentId);
    form.append("answer", ans);

    const res = await fetch(`http://localhost:8000/api/quiz/${quizId}/ans`, {
      method: "POST",
      body: form,
    });
    const data = await res.json();
    setScore(data.score);
    if (data.end) {
      setEnded(true);
      return;
    }
    setQ(null);
    fetchQ();
  };

  if (ended) {
    return (
      <div className="min-h-screen flex items-center justify-center text-center">
        <div>
          <h1 className="text-3xl font-bold">Quiz Finished!</h1>
          <p className="text-xl mt-2">Your Score: {score}</p>
        </div>
      </div>
    );
  }

  if (!q) return <p className="text-center py-6">Loading question...</p>;

  return (
    <div className="max-w-lg mx-auto mt-10 space-y-4 px-4">
      <div className="flex justify-between text-sm text-gray-600">
        <span>⏱️ Time Left: {timeLeft}s</span>
        <span>✅ Score: {score}</span>
      </div>

      <div className="p-4 bg-white rounded shadow">
        <p className="font-medium mb-2">{q.question}</p>
        {q.type === "TF"
          ? ["True", "False"].map((opt) => (
              <button
                key={opt}
                onClick={() => submitAnswer(opt)}
                className="block w-full text-left px-4 py-2 mt-2 bg-gray-100 hover:bg-blue-100 rounded"
              >
                {opt}
              </button>
            ))
          : q.options.map((opt, idx) => (
              <button
                key={idx}
                onClick={() => submitAnswer(opt)}
                className="block w-full text-left px-4 py-2 mt-2 bg-gray-100 hover:bg-blue-100 rounded"
              >
                {opt}
              </button>
            ))}
      </div>
    </div>
  );
}
