# Advanced Conversation Chain Manager
# IT Helpdesk Bot with LangChain RAG Integration

import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

# LangChain imports (will be installed via requirements)
try:
    from langchain.chains import ConversationalRetrievalChain
    from langchain.memory import ConversationSummaryBufferMemory
    from langchain.prompts import PromptTemplate, ChatPromptTemplate
    from langchain.schema import BaseRetriever, Document
    from langchain_openai import AzureChatOpenAI
    from langchain.callbacks.base import BaseCallbackHandler
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    logging.warning(f"LangChain not available: {e}")
    LANGCHAIN_AVAILABLE = False

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeRetriever(BaseRetriever):
    """Custom retriever that combines multiple knowledge sources"""

    def __init__(self, vector_store_manager=None, chromadb_handler=None):
        self.vector_store_manager = vector_store_manager
        self.chromadb_handler = chromadb_handler
        super().__init__()

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """Retrieve relevant documents from both vector stores"""
        documents = []

        # Try vector store first
        if self.vector_store_manager:
            try:
                namespace_results = self.vector_store_manager.search_all_namespaces(
                    query, k=3)
                for namespace, results in namespace_results.items():
                    for result in results:
                        doc = Document(
                            page_content=result['content'],
                            metadata={
                                **result['metadata'],
                                'source': f"vector_store_{namespace}",
                                'relevance_score': result['relevance_score']
                            }
                        )
                        documents.append(doc)
            except Exception as e:
                logger.error(f"Error retrieving from vector store: {e}")

        # Fallback to ChromaDB if vector store fails or has insufficient results
        if len(documents) < 3 and self.chromadb_handler:
            try:
                from .faq_handler import query_it_knowledge
                chromadb_result = query_it_knowledge(query)

                if "No relevant knowledge found" not in chromadb_result:
                    doc = Document(
                        page_content=chromadb_result,
                        metadata={
                            'source': 'chromadb_fallback',
                            'category': 'Mixed',
                            'relevance_score': 0.8
                        }
                    )
                    documents.append(doc)
            except Exception as e:
                logger.error(f"Error retrieving from ChromaDB: {e}")

        return documents


class ConversationCallbackHandler(BaseCallbackHandler):
    """Custom callback handler for conversation tracking"""

    def __init__(self):
        self.conversation_log = []

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs) -> None:
        """Called when chain starts"""
        self.conversation_log.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'chain_start',
            'inputs': inputs
        })

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        """Called when chain ends"""
        self.conversation_log.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'chain_end',
            'outputs': outputs
        })


class ConversationManager:
    """Advanced conversation manager for IT Helpdesk using LangChain"""

    def __init__(self, vector_store_manager=None, chromadb_handler=None):
        """Initialize LangChain components"""
        if not LANGCHAIN_AVAILABLE:
            raise ImportError(
                "LangChain is not available. Please install required dependencies.")

        self.vector_store_manager = vector_store_manager
        self.chromadb_handler = chromadb_handler

        # Initialize Azure OpenAI chat model
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv(
                "AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv(
                "AZURE_OPENAI_API_VERSION", "2024-07-01-preview"),
            temperature=0.3,
            max_tokens=1000
        )

        # Initialize custom retriever
        self.retriever = KnowledgeRetriever(
            vector_store_manager, chromadb_handler)

        # Initialize callback handler
        self.callback_handler = ConversationCallbackHandler()

        # Initialize different chain types
        self.chains = {}
        self._setup_chains()

        # Session memory storage
        self.session_memories = {}

        logger.info("ConversationManager initialized successfully")

    def _setup_chains(self):
        """Setup different types of chains for various scenarios"""

        # 1. RAG Chain for knowledge-based questions
        rag_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert IT Helpdesk assistant. Use the provided context to answer questions accurately and helpfully.

Context from knowledge base:
{context}

Guidelines:
- Provide clear, step-by-step solutions when possible
- Reference specific tools, software versions, and procedures
- If the context doesn't contain the answer, say so and suggest creating a ticket
- Be concise but comprehensive
- Use bullet points and numbered lists for clarity

Chat History:
{chat_history}"""),
            ("human", "{question}")
        ])

        self.chains['rag'] = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=True,
            verbose=True,
            combine_docs_chain_kwargs={"prompt": rag_prompt}
        )

        # 2. Troubleshooting Chain for step-by-step guidance
        troubleshooting_prompt = PromptTemplate(
            input_variables=["problem", "context", "chat_history"],
            template="""You are an IT troubleshooting expert. Guide the user through systematic problem resolution.

Problem: {problem}
Context: {context}
Previous conversation: {chat_history}

Provide:
1. Quick diagnosis of the most likely causes
2. Step-by-step troubleshooting instructions
3. What to expect after each step
4. When to escalate to IT support

Be methodical, clear, and patient. If one solution doesn't work, suggest the next most likely fix."""
        )

        # 3. Ticket Management Chain for support requests
        ticket_prompt = PromptTemplate(
            input_variables=["request", "context", "chat_history"],
            template="""You are an IT support ticket specialist. Help users create effective support tickets or check existing ones.

Request: {request}
Context: {context}
Previous conversation: {chat_history}

For ticket creation:
- Gather all necessary information
- Suggest appropriate priority levels
- Recommend category and urgency
- Ensure completeness before submission

For ticket inquiries:
- Provide clear status updates
- Explain next steps
- Set realistic expectations"""
        )

    def get_or_create_memory(self, session_id: str) -> ConversationSummaryBufferMemory:
        """Get or create conversation memory for a session"""
        if session_id not in self.session_memories:
            self.session_memories[session_id] = ConversationSummaryBufferMemory(
                llm=self.llm,
                max_token_limit=1000,
                return_messages=True,
                memory_key="chat_history",
                input_key="question"
            )
        return self.session_memories[session_id]

    def chat_with_rag(self, question: str, session_id: str = "default") -> Dict[str, Any]:
        """Enhanced RAG conversation with memory"""
        try:
            memory = self.get_or_create_memory(session_id)

            # Update the chain with current memory
            chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.retriever,
                memory=memory,
                return_source_documents=True,
                verbose=True,
                callbacks=[self.callback_handler]
            )

            # Get response
            result = chain({"question": question})

            # Format response with source information
            response = {
                "answer": result["answer"],
                "sources": [],
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }

            # Add source information
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    source_info = {
                        "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                        "metadata": doc.metadata,
                        "relevance_score": doc.metadata.get("relevance_score", 0.8)
                    }
                    response["sources"].append(source_info)

            return response

        except Exception as e:
            logger.error(f"Error in RAG chat: {e}")
            return {
                "answer": f"I encountered an error while processing your question: {str(e)}",
                "sources": [],
                "session_id": session_id,
                "error": True
            }

    def guided_troubleshooting(self, problem: str, session_id: str = "default") -> Dict[str, Any]:
        """Start guided troubleshooting session"""
        try:
            memory = self.get_or_create_memory(session_id)

            # Get relevant context from retriever
            context_docs = self.retriever.get_relevant_documents(problem)
            context = "\n".join([doc.page_content for doc in context_docs[:3]])

            # Get chat history
            chat_history = memory.chat_memory.messages if memory.chat_memory else []
            history_text = "\n".join(
                [f"{msg.type}: {msg.content}" for msg in chat_history[-4:]])

            # Generate troubleshooting response
            troubleshooting_prompt = PromptTemplate(
                input_variables=["problem", "context", "chat_history"],
                template="""You are an IT troubleshooting expert. Guide the user through systematic problem resolution.

Problem: {problem}
Context: {context}
Previous conversation: {chat_history}

Provide:
1. Quick diagnosis of the most likely causes
2. Step-by-step troubleshooting instructions
3. What to expect after each step
4. When to escalate to IT support

Be methodical, clear, and patient. If one solution doesn't work, suggest the next most likely fix."""
            )

            formatted_prompt = troubleshooting_prompt.format(
                problem=problem,
                context=context,
                chat_history=history_text
            )

            response = self.llm.invoke(formatted_prompt)

            # Update memory
            memory.save_context(
                {"question": f"Troubleshooting: {problem}"},
                {"answer": response.content}
            )

            return {
                "answer": response.content,
                "type": "troubleshooting",
                "problem": problem,
                "session_id": session_id,
                "next_steps": "Follow the steps above, then let me know the results"
            }

        except Exception as e:
            logger.error(f"Error in guided troubleshooting: {e}")
            return {
                "answer": f"Error starting troubleshooting session: {str(e)}",
                "error": True
            }

    def get_conversation_summary(self, session_id: str) -> str:
        """Get conversation summary for a session"""
        try:
            if session_id in self.session_memories:
                memory = self.session_memories[session_id]
                return memory.predict_new_summary(
                    memory.chat_memory.messages,
                    ""
                )
            return "No conversation history found for this session."
        except Exception as e:
            logger.error(f"Error getting conversation summary: {e}")
            return f"Error retrieving conversation summary: {str(e)}"

    def clear_session_memory(self, session_id: str) -> bool:
        """Clear memory for a specific session"""
        try:
            if session_id in self.session_memories:
                del self.session_memories[session_id]
                return True
            return False
        except Exception as e:
            logger.error(f"Error clearing session memory: {e}")
            return False

    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about active sessions"""
        return {
            "active_sessions": len(self.session_memories),
            "total_conversations": len(self.callback_handler.conversation_log),
            "session_ids": list(self.session_memories.keys())
        }


# Global instance
_conversation_manager = None


def get_conversation_manager(vector_store_manager=None, chromadb_handler=None) -> Optional[ConversationManager]:
    """Get or create global conversation manager instance"""
    global _conversation_manager

    if not LANGCHAIN_AVAILABLE:
        logger.warning("LangChain not available, returning None")
        return None

    if _conversation_manager is None:
        try:
            _conversation_manager = ConversationManager(
                vector_store_manager, chromadb_handler)
        except Exception as e:
            logger.error(f"Failed to initialize conversation manager: {e}")
            return None

    return _conversation_manager


def enhanced_chat_query(question: str, session_id: str = "default") -> str:
    """Enhanced conversational query using LangChain with RAG capabilities"""
    try:
        manager = get_conversation_manager()
        if manager:
            result = manager.chat_with_rag(question, session_id)
            return result["answer"]
        else:
            # Fallback to basic functionality
            return "Advanced conversation features not available. Using basic response mode."
    except Exception as e:
        logger.error(f"Error in enhanced chat query: {e}")
        return f"Error processing query: {str(e)}"
