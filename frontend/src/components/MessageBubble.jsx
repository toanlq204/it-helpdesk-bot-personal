// Component for rendering individual chat message bubbles
export default function MessageBubble({ role, content }) {
    const isUser = role === "user";

    return (
        <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
            <div className={`flex items-end gap-3 max-w-[85%] ${isUser ? "flex-row-reverse" : "flex-row"}`}>
                {/* Avatar */}
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shadow-lg flex-shrink-0 ${isUser
                        ? "bg-gradient-to-br from-blue-500 to-purple-600"
                        : "bg-gradient-to-br from-green-500 to-teal-600"
                    }`}>
                    {isUser ? (
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                    ) : (
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                    )}
                </div>

                {/* Message bubble */}
                <div className={`relative group ${isUser ? "order-first" : ""}`}>
                    <div
                        className={`rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-lg backdrop-blur-sm border transition-all duration-300 group-hover:shadow-xl ${isUser
                                ? "bg-gradient-to-br from-blue-500 to-purple-600 text-white rounded-br-sm border-blue-400/30"
                                : "bg-white/10 text-white rounded-bl-sm border-white/20"
                            }`}
                    >
                        {/* Message content */}
                        <div className="whitespace-pre-wrap break-words">
                            {content}
                        </div>

                        {/* Time indicator (optional, could be enhanced with actual timestamps) */}
                        <div className={`text-xs mt-1 opacity-70 ${isUser ? "text-blue-100" : "text-gray-300"
                            }`}>
                            {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                    </div>

                    {/* Message tail */}
                    <div className={`absolute bottom-0 w-3 h-3 ${isUser
                            ? "right-0 bg-gradient-to-br from-blue-500 to-purple-600 rounded-bl-full transform rotate-45 translate-x-1/2 translate-y-1/2"
                            : "left-0 bg-white/10 rounded-br-full transform -rotate-45 -translate-x-1/2 translate-y-1/2"
                        }`}></div>
                </div>
            </div>
        </div>
    );
}
