import { useState } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState(null);
  const [loading, setLoading] = useState(false);

  const sendData = async () => {
    if (!input) return;

    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/ai-agent", {
        text: input,
      });

      setOutput(res.data.result);
    } catch (err) {
      alert("Backend connection error");
    }
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>💊 AI CRM Assistant</h1>

      {/* Input Card */}
      <div style={styles.card}>
        <h3>Enter Doctor Interaction</h3>
        <textarea
          style={styles.textarea}
          placeholder="e.g. Met Dr. Reddy. Discussed insulin. He is interested..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />

        <button style={styles.button} onClick={sendData}>
          {loading ? "Processing..." : "Analyze"}
        </button>
      </div>

      {/* Output Card */}
      {output && (
        <div style={styles.card}>
          <h3>Structured Output</h3>

          <p><strong>👨‍⚕️ Doctor:</strong> {output.hcp_name}</p>
          <p><strong>💊 Product:</strong> {output.product_discussed}</p>
          <p><strong>📝 Notes:</strong> {output.interaction_notes}</p>
          <p><strong>📊 Summary:</strong> {output.interaction_summary}</p>
          <p><strong>➡️ Next Action:</strong> {output.next_action}</p>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    fontFamily: "Arial",
    padding: "30px",
    backgroundColor: "#f4f6f8",
    minHeight: "100vh",
  },
  title: {
    textAlign: "center",
    marginBottom: "30px",
  },
  card: {
    background: "#fff",
    padding: "20px",
    borderRadius: "12px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
    marginBottom: "20px",
  },
  textarea: {
    width: "100%",
    height: "100px",
    padding: "10px",
    borderRadius: "8px",
    border: "1px solid #ccc",
    marginTop: "10px",
  },
  button: {
    marginTop: "15px",
    padding: "10px 20px",
    border: "none",
    backgroundColor: "#007bff",
    color: "#fff",
    borderRadius: "8px",
    cursor: "pointer",
  },
};

export default App;