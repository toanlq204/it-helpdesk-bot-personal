// Component for rendering individual chat message bubbles
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

export default function MessageBubble({ role, content, isPlaying, audioError }) {
    const isUser = role === "user";
    const [isExpanded, setIsExpanded] = useState(false);

    // Character limit for responses
    const CHARACTER_LIMIT = 800;
    const shouldTruncate = !isUser && content.length > CHARACTER_LIMIT;
    const displayContent = shouldTruncate && !isExpanded
        ? content.substring(0, CHARACTER_LIMIT) + "..."
        : content;

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
                        className={`rounded-2xl px-5 py-4 text-sm leading-relaxed shadow-lg backdrop-blur-sm border transition-all duration-300 group-hover:shadow-xl ${isUser
                            ? "bg-gradient-to-br from-blue-500 to-purple-600 text-white rounded-br-sm border-blue-400/30"
                            : "bg-gradient-to-br from-gray-800/90 to-gray-900/90 text-white rounded-bl-sm border-white/20 min-w-[300px]"
                            }`}
                    >
                        {/* Message content */}
                        <div className="whitespace-pre-wrap break-words">
                            {isUser ? (
                                // For user messages, display as plain text
                                displayContent
                            ) : (
                                // For assistant messages, render as markdown
                                <div className="prose-chat">
                                    <ReactMarkdown
                                        components={{
                                            // Enhanced styling for headers with proper hierarchy
                                            h1: ({ children }) => (
                                                <h1 className="text-xl font-bold text-white mb-4 pb-2 border-b border-white/20">
                                                    {children}
                                                </h1>
                                            ),
                                            h2: ({ children }) => (
                                                <h2 className="text-lg font-bold text-white mb-3 mt-4 flex items-center">
                                                    <span className="w-1 h-6 bg-blue-400 mr-3 rounded"></span>
                                                    {children}
                                                </h2>
                                            ),
                                            h3: ({ children }) => (
                                                <h3 className="text-base font-semibold text-blue-200 mb-2 mt-3 flex items-center">
                                                    <span className="w-2 h-2 bg-blue-400 mr-2 rounded-full"></span>
                                                    {children}
                                                </h3>
                                            ),
                                            h4: ({ children }) => (
                                                <h4 className="text-sm font-medium text-blue-300 mb-2 mt-2">
                                                    {children}
                                                </h4>
                                            ),

                                            // Enhanced paragraph styling
                                            p: ({ children }) => (
                                                <p className="text-white mb-3 last:mb-0 leading-relaxed">
                                                    {children}
                                                </p>
                                            ),

                                            // Better list styling with spacing
                                            ul: ({ children }) => (
                                                <ul className="list-none text-white mb-3 space-y-2 pl-0">
                                                    {children}
                                                </ul>
                                            ),
                                            ol: ({ children }) => (
                                                <ol className="list-none text-white mb-3 space-y-2 pl-0 counter-reset-list">
                                                    {children}
                                                </ol>
                                            ),
                                            li: ({ children, ordered }) => (
                                                <li className={`text-white flex items-start ${ordered ? 'counter-increment-list' : ''}`}>
                                                    {ordered ? (
                                                        <span className="bg-blue-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center mr-3 mt-0.5 flex-shrink-0 font-medium counter-content">
                                                        </span>
                                                    ) : (
                                                        <span className="w-2 h-2 bg-blue-400 rounded-full mr-3 mt-2 flex-shrink-0"></span>
                                                    )}
                                                    <span className="flex-1">{children}</span>
                                                </li>
                                            ),

                                            // Enhanced text formatting
                                            strong: ({ children }) => (
                                                <strong className="font-bold text-yellow-300 bg-yellow-500/10 px-1 rounded">
                                                    {children}
                                                </strong>
                                            ),
                                            em: ({ children }) => (
                                                <em className="italic text-blue-200 font-medium">
                                                    {children}
                                                </em>
                                            ),

                                            // Better code styling
                                            code: ({ children }) => (
                                                <code className="bg-gray-900/60 text-green-300 px-2 py-1 rounded-md text-sm font-mono border border-gray-700/50">
                                                    {children}
                                                </code>
                                            ),
                                            pre: ({ children }) => (
                                                <pre className="bg-gray-900/80 text-green-300 p-4 rounded-lg text-sm font-mono overflow-x-auto mb-3 border border-gray-700/50 shadow-inner">
                                                    {children}
                                                </pre>
                                            ),

                                            // Enhanced blockquote
                                            blockquote: ({ children }) => (
                                                <blockquote className="border-l-4 border-blue-400 pl-4 py-2 bg-blue-500/10 rounded-r-lg italic text-blue-100 mb-3 shadow-inner">
                                                    {children}
                                                </blockquote>
                                            ),

                                            // Better link styling
                                            a: ({ href, children }) => (
                                                <a
                                                    href={href}
                                                    className="text-blue-300 hover:text-blue-200 underline decoration-blue-400 underline-offset-2 transition-colors duration-200 font-medium"
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                >
                                                    {children}
                                                </a>
                                            ),

                                            // Table styling
                                            table: ({ children }) => (
                                                <div className="overflow-x-auto mb-3">
                                                    <table className="min-w-full bg-white/5 rounded-lg border border-white/10">
                                                        {children}
                                                    </table>
                                                </div>
                                            ),
                                            thead: ({ children }) => (
                                                <thead className="bg-white/10">
                                                    {children}
                                                </thead>
                                            ),
                                            th: ({ children }) => (
                                                <th className="px-4 py-2 text-left text-white font-semibold border-b border-white/10">
                                                    {children}
                                                </th>
                                            ),
                                            td: ({ children }) => (
                                                <td className="px-4 py-2 text-white border-b border-white/5">
                                                    {children}
                                                </td>
                                            ),

                                            // Horizontal rule
                                            hr: () => (
                                                <hr className="border-white/20 my-4" />
                                            ),
                                        }}
                                        remarkPlugins={[]}
                                        rehypePlugins={[]}
                                    >
                                        {displayContent}
                                    </ReactMarkdown>
                                </div>
                            )}
                        </div>

                        {/* Show more/less button for long responses */}
                        {shouldTruncate && (
                            <div className="mt-2 pt-2 border-t border-white/10">
                                <button
                                    onClick={() => setIsExpanded(!isExpanded)}
                                    className="text-xs text-blue-300 hover:text-blue-200 transition-colors duration-200 flex items-center gap-1"
                                >
                                    {isExpanded ? (
                                        <>
                                            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                                            </svg>
                                            Show less
                                        </>
                                    ) : (
                                        <>
                                            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                            </svg>
                                            Show more ({content.length - CHARACTER_LIMIT} more characters)
                                        </>
                                    )}
                                </button>
                            </div>
                        )}

                        {/* Audio status indicators for assistant messages */}
                        {!isUser && (isPlaying || audioError) && (
                            <div className="flex items-center gap-2 mt-2 pt-2 border-t border-white/10">
                                {isPlaying && (
                                    <>
                                        <div className="flex items-center gap-1">
                                            <svg className="w-4 h-4 text-blue-300" fill="currentColor" viewBox="0 0 24 24">
                                                <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z" />
                                                <path d="M14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z" />
                                            </svg>
                                            <span className="text-xs text-blue-300">Playing audio...</span>
                                        </div>
                                        <div className="flex space-x-1">
                                            <div className="w-1 h-3 bg-blue-300 rounded-full animate-pulse"></div>
                                            <div className="w-1 h-3 bg-blue-300 rounded-full animate-pulse" style={{ animationDelay: '0.1s' }}></div>
                                            <div className="w-1 h-3 bg-blue-300 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                                        </div>
                                    </>
                                )}
                                {audioError && (
                                    <div className="flex items-center gap-1">
                                        <svg className="w-4 h-4 text-red-300" fill="currentColor" viewBox="0 0 24 24">
                                            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                                        </svg>
                                        <span className="text-xs text-red-300">{audioError}</span>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Time indicator */}
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
