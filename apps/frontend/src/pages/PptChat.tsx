import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export default function PptChat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!question.trim()) return;

    // Adiciona a pergunta ao histórico
    const newUserMessage: ChatMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, newUserMessage]);
    setQuestion("");

    try {
      const res = await axios.post("http://127.0.0.1:8000/ppt-search", {
        query: question,
      });
      const newAssistantMessage: ChatMessage = {
        role: "assistant",
        content: res.data.response,
      };

      // Adiciona a resposta ao histórico
      setMessages((prev) => [...prev, newAssistantMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Erro ao obter resposta.",
        },
      ]);
      console.error(error);
    }
  };

  const fixMarkdown = (md: string) => {
    return md
      .replace(/(#+ .+)(\n)([^#\n-])/g, "$1\n\n$3")
      .replace(/\n(-{1} .*\n)(-{1} )/g, "\n$1  $2");
  };

  return (
    <div
      className="page-container"
      style={{ padding: "2rem", width: "100%", height: "80%" }}
    >
      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: "8px",
          padding: "1rem",
          height: "100%",
          width: "100%",
          overflowY: "auto",
          marginBottom: "1rem",
          backgroundColor: "#fafafa",
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              display: "flex",
              justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
              marginBottom: "1rem",
              alignItems: "flex-start",
            }}
          >
            {msg.role === "assistant" && (
              <img
                src="/robot.svg"
                alt="Assistant Avatar"
                style={{
                  width: "40px",
                  height: "40px",
                  borderRadius: "50%",
                  marginRight: "0.5rem",
                }}
              />
            )}
            <div
              style={{
                display: "inline-block",
                padding: "0.5rem 1rem",
                borderRadius: "10px",
                backgroundColor: msg.role === "user" ? "#d1e7dd" : "#d7e0f8",
                color: "#000",
              }}
            >
              <div style={{ padding: "1rem" }}>
                <strong>{msg.role === "user" ? "Você" : "Assistente"}:</strong>{" "}
                {msg.role === "assistant" ? (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {fixMarkdown(msg.content)}
                  </ReactMarkdown>
                ) : (
                  msg.content
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      <form
        onSubmit={handleSubmit}
        style={{ display: "flex", gap: "1rem", width: "100%" }}
      >
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Write your question here..."
          style={{
            flex: 1,
            padding: "0.5rem",
          }}
        />
        <button
          type="submit"
          disabled={!question}
          style={{ backgroundColor: "#378fc6" }}
        >
          Send
        </button>
      </form>
    </div>
  );
}
