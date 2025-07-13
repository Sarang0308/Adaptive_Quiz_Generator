import { useState } from "react";

export default function AdminUpload() {
  const [file, setFile] = useState(null);
  const [totalQuestions, setTotalQuestions] = useState(10);
  const [uploadStatus, setUploadStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return alert("Please select a PDF file");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("total_questions", totalQuestions);

    try {
      const res = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (data.quiz_id) {
        setUploadStatus(`✅ Quiz Created! Code: ${data.quiz_id}`);
      } else {
        setUploadStatus("❌ Upload failed");
      }
    } catch (err) {
      console.error(err);
      setUploadStatus("❌ Server error");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="bg-white shadow-md rounded-md p-8 w-full max-w-md space-y-4">
        <h2 className="text-2xl font-semibold text-center text-gray-700">
          Admin: Upload PDF & Set Questions
        </h2>

        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="w-full border px-3 py-2 rounded-md text-sm"
        />

        <input
          type="number"
          min={10}
          max={15}
          value={totalQuestions}
          onChange={(e) => setTotalQuestions(e.target.value)}
          className="w-full border px-3 py-2 rounded-md text-sm"
        />

        <button
          onClick={handleUpload}
          className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
        >
          Upload & Generate Quiz
        </button>

        {uploadStatus && (
          <div className="text-center mt-4 text-green-600 font-medium">
            {uploadStatus}
          </div>
        )}
      </div>
    </div>
  );
}
