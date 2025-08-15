// Import necessary React hooks and components
import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble.jsx";

export default function ChatWindow({ messages }) {
    const listRef = useRef(null);

    // Auto-scroll to bottom when new messages are added
    useEffect(() => {
        listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
    }, [messages]);

    return (
        <div
            ref={listRef}
            className="flex-1 overflow-y-auto p-4 bg-gray-900 rounded-xl border border-gray-800"
        >
            {/* Render all messages */}
            {messages.map((m, idx) => (
                <MessageBubble key={idx} role={m.role} content={m.content} />
            ))}
        </div>
    );
}
