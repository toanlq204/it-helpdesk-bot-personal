import React from 'react';

function MessageBubble({ role, content }) {
    const isUser = role === 'user';
    return (
        <div className={`mb-2 flex ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div
                className={`p-2 rounded-lg max-w-xs ${isUser ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'
                    }`}
            >
                {content}
            </div>
        </div>
    );
}

export default MessageBubble;
