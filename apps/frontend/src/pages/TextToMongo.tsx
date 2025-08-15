import { useState } from "react";
import axios from "axios";

export default function TextToMongo() {
  const [questionMongo, setQuestionMongo] = useState("");
  const [answerMongo, setAnswerMongo] = useState("");

  const handleSubmitMongo = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:8000/text-to-mongo", {
        query: questionMongo,
      });
      setAnswerMongo(res.data.response.trim());
    } catch (error) {
      setAnswerMongo("Erro ao obter resposta.");
      console.error(error);
    }
  };

  return (
    <div className="page-container">
      <form
        onSubmit={handleSubmitMongo}
        style={{
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
          width: "100%",
          height: "90%",
          marginBottom: "1rem",
          gap: "1rem",
        }}
      >
        <input
          value={questionMongo}
          onChange={(e) => setQuestionMongo(e.target.value)}
          placeholder="Write your sentence here..."
          style={{ flex: 1 }}
        />
        <button disabled={!questionMongo} type="submit">
          Send
        </button>
      </form>

      <textarea
        value={answerMongo}
        readOnly
        style={{
          width: "100%",
          height: "500px",
          fontFamily: "monospace",
          fontSize: "14px",
          whiteSpace: "pre-wrap",
          padding: "1rem",
          border: "1px solid #ccc",
          borderRadius: "4px",
          backgroundColor: "#f5f5f5",
          color: "#333",
          resize: "none",
        }}
      />
    </div>
  );
}
