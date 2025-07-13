import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const [quizId, setQuizId] = useState("");
  const [studentId, setStudentId] = useState("");
  const [role, setRole] = useState("student");
  const navigate = useNavigate();

  const proceed = () => {
    if (role === "admin") {
      navigate("/admin/upload");
    } else {
      if (!quizId || !studentId) return alert("Enter both fields.");
      navigate(`/quiz/${quizId}/${studentId}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center items-center px-4">
      <div className="bg-white shadow p-6 rounded-md space-y-4 w-full max-w-sm">
        <h2 className="text-xl font-semibold text-center">Join Quiz Platform</h2>

        <div>
          <label className="block text-sm font-medium text-gray-600">Role</label>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="w-full border px-3 py-2 rounded-md text-sm"
          >
            <option value="student">Student</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        {role === "student" && (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-600">Quiz Code</label>
              <input
                type="text"
                value={quizId}
                onChange={(e) => setQuizId(e.target.value)}
                className="w-full border px-3 py-2 rounded-md text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-600">Your ID</label>
              <input
                type="text"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                className="w-full border px-3 py-2 rounded-md text-sm"
              />
            </div>
          </>
        )}

        <button
          onClick={proceed}
          className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
        >
          Proceed
        </button>
      </div>
    </div>
  );
}
