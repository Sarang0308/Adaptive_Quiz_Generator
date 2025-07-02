// --- File: src/pages/StudentPage.jsx ---
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function StudentPage() {
  const [rollNo, setRollNo] = useState('');
  const [testId, setTestId] = useState('');
  const [question, setQuestion] = useState(null);
  const [selected, setSelected] = useState('');
  const [score, setScore] = useState(0);
  const [qIndex, setQIndex] = useState(0);
  const [totalQs, setTotalQs] = useState(5);
  const navigate = useNavigate();

  const fetchNextQuestion = async (answer) => {
  try {
    const res = await axios.post('http://localhost:5000/api/next-question', {
      rollNo, testId, answer, qIndex
    });
    if (res.data.done) {
      navigate('/result', { state: { score: res.data.score, total: totalQs } });
    } else {
      setQuestion(res.data.question);
      setSelected(""); // 🔥 Add this to reset radio
      setQIndex(prev => prev + 1);
    }
  } catch (err) {
    console.error(err);
  }
};


  const startTest = async () => {
    try {
      const res = await axios.post('http://localhost:5000/api/start-test', { rollNo, testId });
      setQuestion(res.data.question);
    } catch (err) {
      alert('Test not found or error');
    }
  };

  return (
    <div>
      {!question ? (
        <div>
          <input type="text" placeholder="Roll No" value={rollNo} onChange={e => setRollNo(e.target.value)} />
          <input type="text" placeholder="Test ID" value={testId} onChange={e => setTestId(e.target.value)} />
          <button onClick={startTest}>Start Test</button>
        </div>
      ) : (
        <div>
          <h3>Q{qIndex + 1}: {question.question}</h3>
          {question.options.map((opt, idx) => (
            <div key={idx}>
              <input type="radio" name="opt" value={opt} onChange={() => setSelected(opt)} /> {opt}
            </div>
          ))}
          <button onClick={() => fetchNextQuestion(selected)}>Submit Answer</button>
        </div>
      )}
    </div>
  );
}

export default StudentPage;