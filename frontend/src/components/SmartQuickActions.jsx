import { useState } from 'react';

const SmartQuickActions = ({ onActionClick, loading }) => {
    const [hoveredAction, setHoveredAction] = useState(null);

    const actionCategories = [
        {
            title: "🔍 Knowledge Search",
            color: "from-purple-500 to-blue-500",
            actions: [
                {
                    id: 'search_vpn',
                    icon: '�',
                    title: 'VPN Setup',
                    query: 'Search knowledge base for VPN configuration and setup guides',
                    description: 'Find VPN setup instructions and troubleshooting'
                },
                {
                    id: 'search_network',
                    icon: '🌐',
                    title: 'Network Issues',
                    query: 'Search for network connectivity and troubleshooting guides',
                    description: 'Get network problem solving resources'
                }
            ]
        },
        {
            title: "🎫 Support Tickets",
            color: "from-orange-500 to-red-500",
            actions: [
                {
                    id: 'create_ticket',
                    icon: '📝',
                    title: 'Create Ticket',
                    query: 'Create a support ticket for my computer issue that needs urgent attention',
                    description: 'Submit a new support request'
                },
                {
                    id: 'check_status',
                    icon: '📋',
                    title: 'Check Status',
                    query: 'Show me the status of all my current support tickets',
                    description: 'View your ticket status and updates'
                }
            ]
        },
        {
            title: "� Troubleshooting",
            color: "from-green-500 to-teal-500",
            actions: [
                {
                    id: 'wifi_help',
                    icon: '📶',
                    title: 'Wi-Fi Problems',
                    query: 'I cannot connect to the office Wi-Fi, please help me troubleshoot step by step',
                    description: 'Get guided Wi-Fi troubleshooting'
                },
                {
                    id: 'printer_help',
                    icon: '🖨️',
                    title: 'Printer Issues',
                    query: 'My printer is not working, help me diagnose and fix the problem',
                    description: 'Resolve printer connectivity issues'
                }
            ]
        },
        {
            title: "🤖 AI-Powered Help",
            color: "from-pink-500 to-purple-500",
            actions: [
                {
                    id: 'smart_help',
                    icon: '�',
                    title: 'Smart Assistant',
                    query: 'I need help with password reset and also setting up email on my phone',
                    description: 'Multi-task AI assistance'
                },
                {
                    id: 'comprehensive',
                    icon: '⚡',
                    title: 'Auto-Resolve',
                    query: 'Search for printer driver issues and automatically create a ticket if needed',
                    description: 'AI-powered problem resolution'
                }
            ]
        }
    ];

    return (
        <div className="glass rounded-2xl p-4 shadow-2xl">
            <div className="flex items-center gap-2 mb-4">
                <div className="w-6 h-6 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg flex items-center justify-center">
                    <span className="text-white text-sm">⚡</span>
                </div>
                <div>
                    <h3 className="text-white font-bold text-sm">Quick Help</h3>
                    <p className="text-blue-200 text-xs">Try these common IT requests</p>
                </div>
            </div>

            <div className="space-y-4">
                {actionCategories.map((category, categoryIdx) => (
                    <div key={categoryIdx} className="space-y-2">
                        <div className={`bg-gradient-to-r ${category.color} rounded-lg p-2`}>
                            <h4 className="text-white font-semibold text-xs">{category.title}</h4>
                        </div>

                        <div className="grid grid-cols-1 gap-2">
                            {category.actions.map((action) => (
                                <div
                                    key={action.id}
                                    className="relative group"
                                    onMouseEnter={() => setHoveredAction(action.id)}
                                    onMouseLeave={() => setHoveredAction(null)}
                                >
                                    <button
                                        onClick={() => onActionClick(action.query)}
                                        disabled={loading}
                                        className="w-full bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 rounded-lg p-3 text-left transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed group-hover:transform group-hover:scale-105"
                                    >
                                        <div className="flex items-center gap-3">
                                            <div className="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center flex-shrink-0">
                                                <span className="text-lg">{action.icon}</span>
                                            </div>
                                            <div className="flex-1 min-w-0">
                                                <h5 className="text-white font-medium text-sm mb-1">{action.title}</h5>
                                                <p className="text-blue-200 text-xs leading-relaxed">
                                                    {action.description}
                                                </p>
                                            </div>
                                        </div>

                                        {loading && (
                                            <div className="absolute inset-0 bg-black/20 backdrop-blur-sm rounded-lg flex items-center justify-center">
                                                <div className="typing-indicator">
                                                    <div className="typing-dot bg-white"></div>
                                                    <div className="typing-dot bg-white"></div>
                                                    <div className="typing-dot bg-white"></div>
                                                </div>
                                            </div>
                                        )}
                                    </button>

                                    {/* Tooltip with full query */}
                                    {hoveredAction === action.id && (
                                        <div className="absolute z-50 bottom-full left-0 right-0 mb-2 p-2 bg-black/90 backdrop-blur-sm rounded-lg border border-white/20 shadow-2xl">
                                            <p className="text-white text-xs font-medium mb-1">Example Query:</p>
                                            <p className="text-blue-200 text-xs italic">"{action.query}"</p>
                                            <div className="absolute top-full left-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-black/90"></div>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            {/* Pro Tips */}
            <div className="mt-4 pt-3 border-t border-white/10">
                <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-lg p-3 border border-blue-400/30">
                    <div className="flex items-start gap-2">
                        <div className="w-5 h-5 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg flex items-center justify-center flex-shrink-0">
                            <span className="text-white text-xs">💡</span>
                        </div>
                        <div>
                            <h5 className="text-white font-medium text-xs mb-1">AI Tips:</h5>
                            <ul className="space-y-1 text-blue-200 text-xs">
                                <li>• Ask multiple questions: "Reset password AND help with VPN"</li>
                                <li>• Be specific: "Office printer on 3rd floor won't print"</li>
                                <li>• I remember our conversation context</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SmartQuickActions;
