// Import necessary React hooks and components
import { useEffect, useMemo, useState } from "react";
import ChatWindow from "./components/ChatWindow.jsx";
import { sendMessage, health } from "./api.js";

export default function App() {
    // State for managing chat messages
    const [messages, setMessages] = useState([
        { role: "assistant", content: "Hello there! 👋 Welcome to your **Enhanced IT Helpdesk Assistant**! \n\n🚀 **New Advanced Features:**\n\n🔍 **Smart Knowledge Base Search** - Get detailed troubleshooting guides\n🛠️ **Interactive Troubleshooting** - Step-by-step guidance for Wi-Fi, printers, and email\n🎫 **Enhanced Ticket Management** - Auto-categorized tickets with priority levels\n🧠 **Context Memory** - I remember our conversation and handle follow-ups\n📦 **Batch Processing** - Ask multiple questions at once!\n\n� **Try asking:**\n• \"How to fix slow Wi-Fi? Also, how do I reset my password?\"\n• \"Start troubleshooting my printer issues\"\n• \"Search knowledge base for VPN problems\"\n• \"Create a ticket for my broken laptop screen\"\n• \"Show me all my tickets\"\n\nHow can I help you today?" }
    ]);
    const [input, setInput] = useState("");
    const [serverHealth, setServerHealth] = useState(null);
    const [loading, setLoading] = useState(false);
    const [ticketStats, setTicketStats] = useState(null);

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
                setTicketStats(h.tickets_total || 0);
            } catch {
                setServerHealth({ status: "offline" });
            }
        })();
    }, []);

    // Handle sending a message
    const onSend = async () => {
        const text = input.trim();
        if (!text || loading) return;
        setMessages((prev) => [...prev, { role: "user", content: text }]);
        setInput("");
        setLoading(true);
        try {
            const res = await sendMessage(sessionId, text);
            // Server returns full history (user + assistant). We only add the new assistant message:
            setMessages((prev) => [...prev, { role: "assistant", content: res.reply }]);

            // Update ticket stats if provided in response
            if (res.stats) {
                setTicketStats(res.stats.total || 0);
            }
        } catch (e) {
            setMessages((prev) => [
                ...prev,
                { role: "assistant", content: "Sorry, the server is unavailable right now. Please try again later. 😔" }
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
        <div className="min-h-screen w-full flex items-center justify-center p-4 relative overflow-hidden">
            {/* Background decorative elements */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse-custom"></div>
                <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse-custom" style={{ animationDelay: '1s' }}></div>
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-60 h-60 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse-custom" style={{ animationDelay: '2s' }}></div>
            </div>

            <div className="w-full max-w-4xl flex flex-col gap-6 relative z-10 animate-fadeInUp">
                {/* Header with improved design */}
                <header className="glass rounded-2xl p-6 shadow-2xl">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                                </svg>
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-white">Enhanced IT Helpdesk Assistant</h1>
                                <p className="text-blue-200 text-sm">Advanced AI support with context memory & smart troubleshooting</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-4">
                            {/* Ticket Stats Display */}
                            {ticketStats !== null && (
                                <div className="bg-blue-500/20 text-blue-300 border border-blue-500/30 px-3 py-1 rounded-lg text-sm">
                                    🎫 {ticketStats} tickets
                                </div>
                            )}
                            <div className={`flex items-center gap-2 px-4 py-2 rounded-xl shadow-lg transition-all duration-300 ${serverHealth?.status === "ok"
                                ? "bg-green-500/20 text-green-300 border border-green-500/30"
                                : "bg-red-500/20 text-red-300 border border-red-500/30"
                                }`}>
                                <div className={`w-2 h-2 rounded-full ${serverHealth?.status === "ok" ? "bg-green-400 animate-pulse-custom" : "bg-red-400"
                                    }`}></div>
                                <span className="text-sm font-medium">
                                    {serverHealth?.status === "ok" ? "Enhanced Mode" : "Offline"}
                                </span>
                            </div>
                        </div>
                    </div>
                </header>

                {/* Chat Window with enhanced styling */}
                <div className="glass-dark rounded-2xl p-2 shadow-2xl" style={{ height: '500px' }}>
                    <ChatWindow messages={messages} loading={loading} />
                </div>

                {/* Input area with improved design */}
                <div className="glass rounded-2xl p-4 shadow-2xl">
                    <div className="flex gap-4">
                        <div className="flex-1 relative">
                            <textarea
                                className="w-full rounded-xl bg-white/10 backdrop-blur-sm border border-white/20 p-4 text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all duration-300 resize-none"
                                rows={2}
                                placeholder="💬 Try: 'How to reset password? Also, start Wi-Fi troubleshooting' or 'Create ticket for broken printer'"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={onKey}
                                disabled={loading}
                            />
                            {input.length > 0 && (
                                <div className="absolute bottom-2 right-2 text-xs text-blue-300">
                                    Press Enter to send
                                </div>
                            )}
                        </div>
                        <button
                            className={`btn-primary rounded-xl px-8 py-4 text-white font-semibold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed min-w-[100px] flex items-center justify-center gap-2 ${loading ? 'animate-pulse' : ''
                                }`}
                            onClick={onSend}
                            disabled={loading || !input.trim()}
                        >
                            {loading ? (
                                <>
                                    <div className="typing-indicator">
                                        <div className="typing-dot"></div>
                                        <div className="typing-dot"></div>
                                        <div className="typing-dot"></div>
                                    </div>
                                    <span>Sending</span>
                                </>
                            ) : (
                                <>
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                                    </svg>
                                    Send
                                </>
                            )}
                        </button>
                    </div>
                </div>

                {/* Enhanced footer with tips */}
                <footer className="glass rounded-xl p-4 shadow-lg">
                    <div className="flex items-center gap-3 text-blue-200">
                        <div className="w-6 h-6 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center">
                            <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                            </svg>
                        </div>
                        <div>
                            <p className="text-sm font-medium">� Enhanced Features Active:</p>
                            <p className="text-xs opacity-75">Smart troubleshooting • Context memory • Batch questions • Auto-categorized tickets • Knowledge base search</p>
                        </div>
                    </div>
                </footer>
            </div>
        </div>
    );
}
