// --- File: src/App.jsx ---
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AdminPage from './pages/AdminPage';
import StudentPage from './pages/StudentPage';
import ResultPage from './pages/ResultPage';
import RoleSelector from './components/RoleSelector';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<RoleSelector />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/student" element={<StudentPage />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </Router>
  );
}

export default App;