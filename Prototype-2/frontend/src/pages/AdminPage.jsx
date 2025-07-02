// --- File: src/pages/AdminPage.jsx ---
import React, { useState } from 'react';
import axios from 'axios';

function AdminPage() {
  const [pdf, setPdf] = useState(null);
  const [testId, setTestId] = useState('');
  const [numQuestions, setNumQuestions] = useState(5);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('pdf', pdf);
    formData.append('testId', testId);
    formData.append('numQuestions', numQuestions);

    try {
      const res = await axios.post('http://localhost:5000/api/generate-test', formData);
      alert('Test generated successfully!');
    } catch (err) {
      alert('Error generating test');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Admin Panel</h2>
      <input type="file" accept="application/pdf" onChange={e => setPdf(e.target.files[0])} required />
      <input type="text" placeholder="Test ID" value={testId} onChange={e => setTestId(e.target.value)} required />
      <input type="number" placeholder="Number of Questions" value={numQuestions} onChange={e => setNumQuestions(e.target.value)} required />
      <button type="submit">Generate Test</button>
    </form>
  );
}

export default AdminPage;
