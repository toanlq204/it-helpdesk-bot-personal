// Component for rendering individual chat message bubbles
export default function MessageBubble({ role, content }) {
    const isUser = role === "user";
    return (
        <div className={`flex ${isUser ? "justify-end" : "justify-start"} my-2`}>
            <div
                className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm leading-relaxed shadow
          ${isUser ? "bg-blue-600 text-white rounded-br-sm" : "bg-gray-800 text-gray-100 rounded-bl-sm"}
        `}
            >
                {content}
            </div>
        </div>
    );
}
