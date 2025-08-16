# Intelligent Function Handler with AI Agent Tools
# IT Helpdesk Bot with Advanced Function Calling and Agent Execution

import os
import json
import logging
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime

# LangChain tools and agents (will be installed via requirements)
try:
    from langchain.tools import Tool, BaseTool
    from langchain.agents import AgentExecutor, create_openai_functions_agent
    from langchain.schema import AgentAction, AgentFinish
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_openai import AzureChatOpenAI
    from langchain.memory import ConversationBufferWindowMemory
    LANGCHAIN_TOOLS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"LangChain tools not available: {e}")
    LANGCHAIN_TOOLS_AVAILABLE = False

# Import existing functions
from ..knowledge_base import search_knowledge_base, search_enhanced_faq, get_troubleshooting_flow
from ..ticket_management import create_enhanced_ticket, get_ticket_status, list_user_tickets

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HelpdeskTool(BaseTool if LANGCHAIN_TOOLS_AVAILABLE else object):
    """Base class for IT Helpdesk intelligent tools"""

    def __init__(self, name: str, description: str, func: Callable, args_schema=None):
        if LANGCHAIN_TOOLS_AVAILABLE:
            super().__init__()
        self.name = name
        self.description = description
        self.func = func
        self.args_schema = args_schema

    def _run(self, *args, **kwargs):
        """Execute the tool function"""
        try:
            return self.func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in tool {self.name}: {e}")
            return f"Error executing {self.name}: {str(e)}"

    def _arun(self, *args, **kwargs):
        """Async execution (not implemented)"""
        raise NotImplementedError("Async execution not implemented")


class IntelligentFunctionAgent:
    """Intelligent function agent with advanced tool execution capabilities"""

    def __init__(self, vector_store_manager=None, conversation_manager=None):
        """Initialize intelligent function agent"""
        self.vector_store_manager = vector_store_manager
        self.conversation_manager = conversation_manager

        # Initialize OpenAI chat model for agents
        if LANGCHAIN_TOOLS_AVAILABLE:
            self.llm = AzureChatOpenAI(
                azure_deployment=os.getenv(
                    "AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version=os.getenv(
                    "AZURE_OPENAI_API_VERSION", "2024-07-01-preview"),
                temperature=0.1,
                max_tokens=1500
            )

        # Initialize tools and agent
        self.tools = []
        self.agent_executor = None
        self._setup_tools()
        self._setup_agent()

        # Session memories for agent conversations
        self.session_memories = {}

        logger.info("IntelligentFunctionAgent initialized")

    def _setup_tools(self):
        """Setup LangChain tools for IT helpdesk functions"""

        # 1. Vector Search Tool
        def vector_search_tool(query: str, namespace: str = "faqs") -> str:
            """Search vector database for IT knowledge"""
            if self.pinecone_handler:
                try:
                    from .pinecone_handler import query_pinecone_knowledge
                    return query_pinecone_knowledge(query, namespace)
                except Exception as e:
                    logger.error(f"Pinecone search error: {e}")

            # Fallback to ChromaDB
            try:
                from .faq_handler import query_it_knowledge
                return query_it_knowledge(query)
            except Exception as e:
                return f"Vector search unavailable: {e}"

        # 2. Knowledge Base Search Tool
        def knowledge_search_tool(query: str, max_results: int = 3) -> str:
            """Search traditional knowledge base articles"""
            try:
                results = search_knowledge_base(query, max_results)
                return json.dumps(results, indent=2)
            except Exception as e:
                return f"Knowledge base search error: {e}"

        # 3. FAQ Search Tool
        def faq_search_tool(query: str, max_results: int = 3) -> str:
            """Search FAQ database"""
            try:
                results = search_enhanced_faq(query, max_results)
                return json.dumps(results, indent=2)
            except Exception as e:
                return f"FAQ search error: {e}"

        # 4. Troubleshooting Flow Tool
        def troubleshooting_tool(issue_type: str) -> str:
            """Start interactive troubleshooting flow"""
            try:
                flow = get_troubleshooting_flow(issue_type)
                if flow:
                    return json.dumps(flow, indent=2)
                return f"No troubleshooting flow found for: {issue_type}"
            except Exception as e:
                return f"Troubleshooting flow error: {e}"

        # 5. Ticket Creation Tool
        def create_ticket_tool(title: str, description: str, category: str = "general",
                               priority: str = "medium", user_email: str = "user@company.com") -> str:
            """Create a new IT support ticket"""
            try:
                ticket = create_enhanced_ticket(
                    title=title,
                    description=description,
                    category=category,
                    priority=priority,
                    user_email=user_email
                )
                return json.dumps(ticket, indent=2)
            except Exception as e:
                return f"Ticket creation error: {e}"

        # 6. Ticket Status Tool
        def ticket_status_tool(ticket_id: str) -> str:
            """Check the status of a support ticket"""
            try:
                status = get_ticket_status(ticket_id)
                return json.dumps(status, indent=2)
            except Exception as e:
                return f"Ticket status error: {e}"

        # 7. User Tickets Tool
        def user_tickets_tool(user_email: str = "user@company.com", limit: int = 5) -> str:
            """List tickets for a user"""
            try:
                tickets = list_user_tickets(user_email, limit)
                return json.dumps(tickets, indent=2)
            except Exception as e:
                return f"User tickets error: {e}"

        # 8. System Information Tool
        def system_info_tool(info_type: str = "general") -> str:
            """Get system information and status"""
            try:
                if info_type == "helpdesk_stats":
                    from ..ticket_management import get_ticket_statistics
                    stats = get_ticket_statistics()
                    return json.dumps(stats, indent=2)
                elif info_type == "vector_stats":
                    if self.pinecone_handler:
                        stats = self.pinecone_handler.get_namespace_stats()
                        return json.dumps(stats, indent=2)
                    return "Vector database statistics not available"
                else:
                    return json.dumps({
                        "timestamp": datetime.now().isoformat(),
                        "system": "IT Helpdesk Bot",
                        "version": "Workshop 4 Enhanced",
                        "status": "operational"
                    }, indent=2)
            except Exception as e:
                return f"System info error: {e}"

        # Create LangChain tools if available
        if LANGCHAIN_TOOLS_AVAILABLE:
            self.tools = [
                Tool(
                    name="vector_search",
                    description="Search vector database for IT knowledge (FAQs, articles, policies). Use this for comprehensive knowledge search.",
                    func=vector_search_tool
                ),
                Tool(
                    name="knowledge_search",
                    description="Search traditional knowledge base articles for detailed technical information.",
                    func=knowledge_search_tool
                ),
                Tool(
                    name="faq_search",
                    description="Search FAQ database for quick answers to common questions.",
                    func=faq_search_tool
                ),
                Tool(
                    name="start_troubleshooting",
                    description="Start interactive troubleshooting flow for specific issues (wifi_issues, printer_issues, email_issues).",
                    func=troubleshooting_tool
                ),
                Tool(
                    name="create_ticket",
                    description="Create a new IT support ticket when manual assistance is needed.",
                    func=create_ticket_tool
                ),
                Tool(
                    name="check_ticket_status",
                    description="Check the status of an existing support ticket using ticket ID.",
                    func=ticket_status_tool
                ),
                Tool(
                    name="list_user_tickets",
                    description="List all tickets for a specific user email address.",
                    func=user_tickets_tool
                ),
                Tool(
                    name="get_system_info",
                    description="Get system information and statistics (general, helpdesk_stats, vector_stats).",
                    func=system_info_tool
                )
            ]
        else:
            # Store functions for manual calling
            self.functions = {
                "vector_search": vector_search_tool,
                "knowledge_search": knowledge_search_tool,
                "faq_search": faq_search_tool,
                "start_troubleshooting": troubleshooting_tool,
                "create_ticket": create_ticket_tool,
                "check_ticket_status": ticket_status_tool,
                "list_user_tickets": user_tickets_tool,
                "get_system_info": system_info_tool
            }

    def _setup_agent(self):
        """Setup OpenAI Functions Agent"""
        if not LANGCHAIN_TOOLS_AVAILABLE or not self.tools:
            logger.warning("Cannot setup agent: LangChain tools not available")
            return

        try:
            # Create agent prompt
            system_message = """You are an expert IT Helpdesk assistant with access to comprehensive tools and knowledge bases.

Your capabilities:
- Search vector databases for accurate IT knowledge
- Access traditional knowledge bases and FAQs  
- Guide users through troubleshooting workflows
- Create and manage support tickets
- Provide system information and statistics

Guidelines:
1. Always search for knowledge first before suggesting ticket creation
2. Use troubleshooting flows for common issues (WiFi, printer, email)
3. Create tickets only when hands-on assistance is truly needed
4. Be thorough but concise in your responses
5. Maintain conversation context and remember previous interactions

Tools available: {tool_names}

Approach each query systematically:
1. Understand the user's problem
2. Search relevant knowledge sources
3. Provide step-by-step solutions when possible
4. Escalate to ticket creation if needed
5. Follow up on outcomes"""

            prompt = ChatPromptTemplate.from_messages([
                ("system", system_message),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
                MessagesPlaceholder(
                    variable_name="chat_history", optional=True)
            ])

            # Create agent
            agent = create_openai_functions_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=prompt
            )

            # Create agent executor
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True,
                max_iterations=5,
                max_execution_time=60,
                return_intermediate_steps=True
            )

            logger.info("OpenAI Functions Agent setup completed")

        except Exception as e:
            logger.error(f"Error setting up agent: {e}")
            self.agent_executor = None

    def get_session_memory(self, session_id: str) -> Optional[ConversationBufferWindowMemory]:
        """Get or create session memory"""
        if not LANGCHAIN_TOOLS_AVAILABLE:
            return None

        if session_id not in self.session_memories:
            self.session_memories[session_id] = ConversationBufferWindowMemory(
                k=10,  # Keep last 10 exchanges
                memory_key="chat_history",
                input_key="input",
                output_key="output",
                return_messages=True
            )
        return self.session_memories[session_id]

    def execute_with_agent(self, query: str, session_id: str = "default") -> Dict[str, Any]:
        """Execute query using OpenAI Functions Agent"""
        if not self.agent_executor:
            return {
                "output": "Agent not available. Please ensure LangChain is properly installed.",
                "error": True
            }

        try:
            # Get session memory
            memory = self.get_session_memory(session_id)

            # Prepare input with memory
            agent_input = {"input": query}
            if memory:
                # Add chat history to input
                chat_history = memory.chat_memory.messages
                agent_input["chat_history"] = chat_history

            # Execute agent
            result = self.agent_executor.invoke(agent_input)

            # Update memory
            if memory:
                memory.save_context(
                    {"input": query},
                    {"output": result["output"]}
                )

            # Format response
            response = {
                "output": result["output"],
                "intermediate_steps": result.get("intermediate_steps", []),
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "tools_used": []
            }

            # Extract tools used
            for step in result.get("intermediate_steps", []):
                if len(step) >= 2:
                    action, observation = step[0], step[1]
                    if hasattr(action, 'tool'):
                        response["tools_used"].append({
                            "tool": action.tool,
                            "input": action.tool_input,
                            "output": str(observation)[:200] + "..." if len(str(observation)) > 200 else str(observation)
                        })

            return response

        except Exception as e:
            logger.error(f"Error executing agent: {e}")
            return {
                "output": f"Error processing request: {str(e)}",
                "error": True,
                "session_id": session_id
            }

    def call_function_directly(self, function_name: str, **kwargs) -> str:
        """Call function directly without agent (fallback)"""
        if LANGCHAIN_TOOLS_AVAILABLE and self.tools:
            # Find tool by name
            for tool in self.tools:
                if tool.name == function_name:
                    try:
                        return tool.func(**kwargs)
                    except Exception as e:
                        return f"Error calling {function_name}: {e}"
            return f"Function {function_name} not found"

        elif hasattr(self, 'functions') and function_name in self.functions:
            # Use stored functions
            try:
                return self.functions[function_name](**kwargs)
            except Exception as e:
                return f"Error calling {function_name}: {e}"

        return f"Function {function_name} not available"

    def get_available_functions(self) -> List[Dict[str, str]]:
        """Get list of available functions/tools"""
        if LANGCHAIN_TOOLS_AVAILABLE and self.tools:
            return [
                {
                    "name": tool.name,
                    "description": tool.description
                }
                for tool in self.tools
            ]
        elif hasattr(self, 'functions'):
            return [
                {
                    "name": name,
                    "description": f"Function: {name}"
                }
                for name in self.functions.keys()
            ]
        return []

    def clear_session(self, session_id: str) -> bool:
        """Clear session memory"""
        try:
            if session_id in self.session_memories:
                del self.session_memories[session_id]
                return True
            return False
        except Exception as e:
            logger.error(f"Error clearing session {session_id}: {e}")
            return False

    def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        return {
            "active_sessions": len(self.session_memories),
            "available_tools": len(self.tools) if LANGCHAIN_TOOLS_AVAILABLE else len(getattr(self, 'functions', {})),
            "agent_available": self.agent_executor is not None,
            "langchain_available": LANGCHAIN_TOOLS_AVAILABLE
        }


# Global instance
_intelligent_function_agent = None


def get_intelligent_function_agent(vector_store_manager=None, conversation_manager=None) -> IntelligentFunctionAgent:
    """Get or create global intelligent function agent"""
    global _intelligent_function_agent
    if _intelligent_function_agent is None:
        _intelligent_function_agent = IntelligentFunctionAgent(
            vector_store_manager, conversation_manager)
    return _intelligent_function_agent


def intelligent_function_call(query: str, session_id: str = "default") -> str:
    """Intelligent function calling with AI agent"""
    try:
        agent = get_intelligent_function_agent()
        result = agent.execute_with_agent(query, session_id)

        if result.get("error"):
            return result["output"]

        # Format response with tool information
        response = result["output"]
        if result.get("tools_used"):
            response += "\n\n🔧 **Tools Used:**\n"
            for tool_info in result["tools_used"]:
                response += f"- {tool_info['tool']}: {tool_info['output'][:100]}...\n"

        return response

    except Exception as e:
        logger.error(f"Error in intelligent function call: {e}")
        return f"Error processing request: {str(e)}"
