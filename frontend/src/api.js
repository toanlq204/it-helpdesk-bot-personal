// API configuration and functions for communicating with backend
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

// Send a chat message to the backend
export async function sendMessage(sessionId, message) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });
  if (!res.ok) {
    throw new Error(`Server error: ${res.status}`);
  }
  return res.json();
}

// Check server health status
export async function health() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}
