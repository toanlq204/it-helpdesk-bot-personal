// Import necessary React hooks and components
import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble.jsx";

export default function ChatWindow({ messages, loading }) {
    const listRef = useRef(null);

    // Auto-scroll to bottom when new messages are added
    useEffect(() => {
        listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
    }, [messages]);

    return (
        <div className="h-full flex flex-col">
            <div
                ref={listRef}
                className="flex-1 overflow-y-auto p-6 space-y-4"
            >
                {/* Render all messages */}
                {messages.map((m, idx) => (
                    <div key={idx} className="message-enter">
                        <MessageBubble role={m.role} content={m.content} />
                    </div>
                ))}

                {/* Loading indicator */}
                {loading && (
                    <div className="flex justify-start my-2">
                        <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl rounded-bl-sm px-4 py-3 shadow-lg">
                            <div className="typing-indicator">
                                <div className="typing-dot bg-blue-300"></div>
                                <div className="typing-dot bg-blue-300"></div>
                                <div className="typing-dot bg-blue-300"></div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Chat background pattern */}
            <div className="absolute inset-0 opacity-5 pointer-events-none">
                <div className="absolute inset-0" style={{
                    backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
                    backgroundSize: '60px 60px'
                }}></div>
            </div>
        </div>
    );
}
