// Import necessary React hooks and components
import { useEffect, useMemo, useState } from "react";
import ChatWindow from "./components/ChatWindow.jsx";
import { sendMessage, health } from "./api.js";

export default function App() {
    // State for managing chat messages
    const [messages, setMessages] = useState([
        { role: "assistant", content: "Hi! I'm your IT Helpdesk assistant. How can I help you today?" }
    ]);
    const [input, setInput] = useState("");
    const [serverHealth, setServerHealth] = useState(null);
    const [loading, setLoading] = useState(false);

    // Generate or retrieve session ID from localStorage
    const sessionId = useMemo(() => {
        const k = "it-helpdesk-session";
        let s = localStorage.getItem(k);
        if (!s) {
            s = crypto.randomUUID();
            localStorage.setItem(k, s);
        }
        return s;
    }, []);

    // Check server health on component mount
    useEffect(() => {
        (async () => {
            try {
                const h = await health();
                setServerHealth(h);
            } catch {
                setServerHealth({ status: "offline" });
            }
        })();
    }, []);

    // Handle sending a message
    const onSend = async () => {
        const text = input.trim();
        if (!text) return;
        setMessages((prev) => [...prev, { role: "user", content: text }]);
        setInput("");
        setLoading(true);
        try {
            const res = await sendMessage(sessionId, text);
            // Server returns full history (user + assistant). We only add the new assistant message:
            setMessages((prev) => [...prev, { role: "assistant", content: res.reply }]);
        } catch (e) {
            setMessages((prev) => [
                ...prev,
                { role: "assistant", content: "Sorry, the server is unavailable right now." }
            ]);
        } finally {
            setLoading(false);
        }
    };

    const onKey = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            onSend();
        }
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center p-4">
            <div className="w-full max-w-3xl flex flex-col gap-3">
                <header className="flex items-center justify-between">
                    <h1 className="text-xl font-semibold">IT Helpdesk Bot</h1>
                    <div className={`text-xs px-2 py-1 rounded ${serverHealth?.status === "ok" ? "bg-green-700" : "bg-red-700"}`}>
                        {serverHealth?.status === "ok" ? "API Online" : "API Offline"}
                    </div>
                </header>

                <ChatWindow messages={messages} />

                <div className="flex gap-2">
                    <textarea
                        className="flex-1 rounded-xl bg-gray-800 border border-gray-700 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
                        rows={2}
                        placeholder="Ask about VPN, Outlook, password reset... You can ask multiple questions at once."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={onKey}
                    />
                    <button
                        className="rounded-xl px-4 text-sm font-medium bg-blue-600 hover:bg-blue-500 disabled:opacity-60"
                        onClick={onSend}
                        disabled={loading}
                    >
                        {loading ? "Sending..." : "Send"}
                    </button>
                </div>

                <footer className="text-xs text-gray-400">
                    Tips: Try asking “How to reset my password? Also, how to install Outlook?”
                </footer>
            </div>
        </div>
    );
}
