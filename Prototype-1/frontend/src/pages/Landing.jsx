import { useNavigate } from "react-router-dom";

export default function Landing() {
  const nav = useNavigate();
  return (
    <div className="max-w-md mx-auto text-center space-y-4">
      <h1 className="text-3xl font-bold">Adaptive Quiz Platform</h1>
      <button onClick={() => nav("/admin")} className="btn">Admin</button>
      <button onClick={() => nav("/join")} className="btn">Student</button>
    </div>
  );
}
