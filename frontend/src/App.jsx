// Import necessary React hooks and components
import { useEffect, useMemo, useState, useRef } from "react";
import ChatWindow from "./components/ChatWindow.jsx";
import { sendMessage, health } from "./api.js";

export default function App() {
    // State for managing chat messages
    const [messages, setMessages] = useState([
        { role: "assistant", content: "Hello! 👋 Welcome to your **Enhanced IT Helpdesk Assistant**! \n\n✅ **Verified Working Features:**\n\n🔍 **Knowledge Base Search** - Comprehensive IT help articles\n🛠️ **Interactive Troubleshooting** - Step-by-step guidance\n🎫 **Smart Ticket Management** - Auto-categorized with priorities\n🧠 **Context Memory** - I remember our conversation\n📦 **Batch Processing** - Handle multiple questions at once\n📊 **System Statistics** - Real-time ticket monitoring\n🔊 **Voice Response** - Text-to-speech powered by HuggingFace\n\n💡 **Quick Actions:** Use the buttons below or ask directly!\n\nHow can I help you today?" }
    ]);
    const [input, setInput] = useState("");
    const [serverHealth, setServerHealth] = useState(null);
    const [loading, setLoading] = useState(false);
    const [ticketStats, setTicketStats] = useState(null);
    const [audioData, setAudioData] = useState(null);
    const [isAudioPlaying, setIsAudioPlaying] = useState(false);

    // Audio refs for voice playback
    const audioRef = useRef(null);

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

    // Audio playback effect
    useEffect(() => {
        if (audioData && audioData.audio_data && audioData.success) {
            try {
                // Create audio blob from base64 data
                const audioBytes = atob(audioData.audio_data);
                const audioArray = new Uint8Array(audioBytes.length);
                for (let i = 0; i < audioBytes.length; i++) {
                    audioArray[i] = audioBytes.charCodeAt(i);
                }

                const audioBlob = new Blob([audioArray], { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);

                if (audioRef.current) {
                    audioRef.current.src = audioUrl;
                    audioRef.current.play();
                }
            } catch (error) {
                console.error('Error playing audio:', error);
            }
        }
    }, [audioData]);

    // Handle sending a message
    const onSend = async () => {
        const text = input.trim();
        if (!text || loading) return;
        setMessages((prev) => [...prev, { role: "user", content: text }]);
        setInput("");
        setLoading(true);
        setAudioData(null); // Clear previous audio data

        try {
            const res = await sendMessage(sessionId, text);
            // Server returns full history (user + assistant). We only add the new assistant message:
            setMessages((prev) => [...prev, { role: "assistant", content: res.reply }]);

            // Update ticket stats if provided in response
            if (res.stats) {
                setTicketStats(res.stats.total || 0);
            }

            // Handle audio response if available
            if (res.audio && res.audio.audio_data) {
                setAudioData(res.audio);
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

    const handleAudioPlay = (playing) => {
        setIsAudioPlaying(playing);
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
                    <ChatWindow
                        messages={messages}
                        loading={loading}
                        audioData={audioData}
                        onAudioPlay={handleAudioPlay}
                    />
                </div>

                {/* Quick Action Buttons */}
                <div className="glass rounded-2xl p-4 shadow-2xl">
                    <h3 className="text-white font-medium mb-3 text-sm">🚀 Quick Actions</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                        <button
                            onClick={() => setInput("How do I reset my password?")}
                            className="quick-action-btn"
                            disabled={loading}
                        >
                            <span className="text-lg">🔑</span>
                            <span className="text-xs">Reset Password</span>
                        </button>
                        <button
                            onClick={() => setInput("Start Wi-Fi troubleshooting")}
                            className="quick-action-btn"
                            disabled={loading}
                        >
                            <span className="text-lg">📶</span>
                            <span className="text-xs">Wi-Fi Issues</span>
                        </button>
                        <button
                            onClick={() => setInput("Create a ticket for printer problems")}
                            className="quick-action-btn"
                            disabled={loading}
                        >
                            <span className="text-lg">🎫</span>
                            <span className="text-xs">Create Ticket</span>
                        </button>
                        <button
                            onClick={() => setInput("Show me my tickets")}
                            className="quick-action-btn"
                            disabled={loading}
                        >
                            <span className="text-lg">📋</span>
                            <span className="text-xs">My Tickets</span>
                        </button>
                        <button
                            onClick={() => setInput("Search knowledge base for VPN setup")}
                            className="quick-action-btn"
                            disabled={loading}
                        >
                            <span className="text-lg">🔍</span>
                            <span className="text-xs">Search KB</span>
                        </button>
                        <button
                            onClick={() => setInput("Start printer troubleshooting")}
                            className="quick-action-btn"
                            disabled={loading}
                        >
                            <span className="text-lg">🖨️</span>
                            <span className="text-xs">Printer Help</span>
                        </button>
                        <button
                            onClick={() => setInput("Show helpdesk statistics")}
                            className="quick-action-btn"
                            disabled={loading}
                        >
                            <span className="text-lg">📊</span>
                            <span className="text-xs">Statistics</span>
                        </button>
                        <button
                            onClick={() => setInput("How to reset password? Also help with VPN setup")}
                            className="quick-action-btn"
                            disabled={loading}
                        >
                            <span className="text-lg">📦</span>
                            <span className="text-xs">Multi-Query</span>
                        </button>
                    </div>
                </div>

                {/* Input area with improved design */}
                <div className="glass rounded-2xl p-4 shadow-2xl">
                    <div className="flex gap-4">
                        <div className="flex-1 relative">
                            <textarea
                                className={`w-full rounded-xl bg-white/10 backdrop-blur-sm border border-white/20 p-4 text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all duration-300 resize-none ${isAudioPlaying ? 'border-blue-400/50' : ''}`}
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

                {/* Enhanced footer with tips and audio controls */}
                <footer className="glass rounded-xl p-4 shadow-lg">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3 text-blue-200">
                            <div className="w-6 h-6 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center">
                                <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                                </svg>
                            </div>
                            <div>
                                <p className="text-sm font-medium">✅ Enhanced IT Helpdesk Features:</p>
                                <p className="text-xs opacity-75">ChromaDB Knowledge Base • OpenAI SDK • HuggingFace TTS • Context Memory • Smart Troubleshooting</p>
                            </div>
                        </div>

                        {/* Audio Controls */}
                        {audioData && (
                            <div className="flex items-center gap-2 text-blue-200">
                                {audioData.success ? (
                                    <div className="flex items-center gap-2 bg-green-500/20 rounded-lg px-3 py-1">
                                        <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 14.142M8.5 12H4a1 1 0 00-1 1v4a1 1 0 001 1h4.5l5 4V8l-5 4z" />
                                        </svg>
                                        <span className="text-xs">Voice Ready</span>
                                    </div>
                                ) : (
                                    <div className="flex items-center gap-2 bg-yellow-500/20 rounded-lg px-3 py-1">
                                        <svg className="w-4 h-4 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                                        </svg>
                                        <span className="text-xs">TTS Loading</span>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </footer>

                {/* Hidden audio element for voice playback */}
                <audio
                    ref={audioRef}
                    onPlay={() => setIsAudioPlaying(true)}
                    onEnded={() => setIsAudioPlaying(false)}
                    onError={() => setIsAudioPlaying(false)}
                />
            </div>
        </div>
    );
}
