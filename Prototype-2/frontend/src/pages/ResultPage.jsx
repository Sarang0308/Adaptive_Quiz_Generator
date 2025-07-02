// --- File: src/pages/ResultPage.jsx ---
import React from 'react';
import { useLocation } from 'react-router-dom';

function ResultPage() {
  const { state } = useLocation();
  return (
    <div>
      <h2>Test Completed</h2>
      <p>Your Score: {state.score} / {state.total}</p>
    </div>
  );
}

export default ResultPage;