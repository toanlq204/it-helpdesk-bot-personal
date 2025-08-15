import React, { useState } from 'react';
import MessageBubble from './MessageBubble';
import axios from '../api';

function ChatWindow() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input };
        const updatedMessages = [...messages, userMessage];
        setMessages(updatedMessages);

        try {
            const response = await axios.post('/chat/', {
                message: input,
                conversation_history: updatedMessages,
            });
            setMessages([...updatedMessages, { role: 'bot', content: response.data.response }]);
        } catch (error) {
            console.error('Error sending message:', error);
        }

        setInput('');
    };

    return (
        <div className="w-full max-w-md bg-white shadow-lg rounded-lg p-4">
            <div className="h-96 overflow-y-auto mb-4">
                {messages.map((msg, index) => (
                    <MessageBubble key={index} role={msg.role} content={msg.content} />
                ))}
            </div>
            <div className="flex">
                <input
                    type="text"
                    className="flex-1 border rounded-l-lg p-2"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                />
                <button
                    className="bg-blue-500 text-white px-4 py-2 rounded-r-lg"
                    onClick={sendMessage}
                >
                    Send
                </button>
            </div>
        </div>
    );
}

export default ChatWindow;
