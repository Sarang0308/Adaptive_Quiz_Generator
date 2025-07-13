import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import AdminUpload from "./pages/AdminUpload";
import Quiz from "./pages/Quiz";

function App() {
  return (
  
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin/upload" element={<AdminUpload />} />
        <Route path="/quiz/:quizId/:studentId" element={<Quiz />} />
      </Routes>
  );
}

export default App;
