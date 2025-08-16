// Import necessary React hooks and components
import { useEffect, useRef, useState } from "react";
import MessageBubble from "./MessageBubble.jsx";

export default function ChatWindow({ messages, loading, audioData, onAudioPlay }) {
    const listRef = useRef(null);
    const audioRef = useRef(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [audioError, setAudioError] = useState(null);

    // Auto-scroll to bottom when new messages are added
    useEffect(() => {
        listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
    }, [messages]);

    // Handle audio playback when audioData is provided
    useEffect(() => {
        if (audioData && audioData.audio_data) {
            playAudio(audioData);
        }
    }, [audioData]);

    const playAudio = async (audioResponse) => {
        try {
            setAudioError(null);
            setIsPlaying(true);

            // Convert base64 to blob
            const binaryString = atob(audioResponse.audio_data);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }

            const audioBlob = new Blob([bytes], { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);

            if (audioRef.current) {
                audioRef.current.src = audioUrl;
                await audioRef.current.play();

                // Notify parent component that audio is playing
                if (onAudioPlay) {
                    onAudioPlay(true);
                }
            }
        } catch (error) {
            console.error('Error playing audio:', error);
            setAudioError('Failed to play audio response');
            setIsPlaying(false);
        }
    };

    const handleAudioEnded = () => {
        setIsPlaying(false);
        if (onAudioPlay) {
            onAudioPlay(false);
        }
    };

    const handleAudioError = () => {
        setIsPlaying(false);
        setAudioError('Audio playback failed');
        if (onAudioPlay) {
            onAudioPlay(false);
        }
    };

    return (
        <div className="h-full flex flex-col">
            {/* Hidden audio element for TTS playback */}
            <audio
                ref={audioRef}
                onEnded={handleAudioEnded}
                onError={handleAudioError}
                style={{ display: 'none' }}
            />

            <div
                ref={listRef}
                className="flex-1 overflow-y-auto p-6 space-y-4"
            >
                {/* Render all messages */}
                {messages.map((m, idx) => (
                    <div key={idx} className="message-enter">
                        <MessageBubble
                            role={m.role}
                            content={m.content}
                            isPlaying={idx === messages.length - 1 && m.role === 'assistant' && isPlaying}
                            audioError={idx === messages.length - 1 && m.role === 'assistant' ? audioError : null}
                        />
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

                {/* Audio status indicator */}
                {isPlaying && (
                    <div className="flex justify-center">
                        <div className="bg-blue-500/20 border border-blue-400/30 rounded-lg px-3 py-2 flex items-center space-x-2">
                            <div className="flex space-x-1">
                                <div className="w-1 h-4 bg-blue-400 rounded-full animate-pulse"></div>
                                <div className="w-1 h-4 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: '0.1s' }}></div>
                                <div className="w-1 h-4 bg-blue-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                            </div>
                            <span className="text-blue-300 text-sm">Playing voice response...</span>
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
