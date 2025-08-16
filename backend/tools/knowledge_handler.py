# Unified Knowledge Base Handler for IT Helpdesk Bot
# Replaces ChromaDB with Pinecone and LangChain integration

import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Import our Pinecone and LangChain handlers
try:
    from .pinecone_handler import VectorStoreManager
    from .langchain_manager import ConversationManager, KnowledgeRetriever
    VECTOR_STORE_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Vector store not available: {e}")
    VECTOR_STORE_AVAILABLE = False

# Fallback to basic knowledge base
from ..knowledge_base import search_knowledge_base

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ITKnowledgeBase:
    """Unified IT Knowledge Base using Pinecone vector store or fallback"""

    def __init__(self):
        """Initialize the knowledge base with vector store or fallback"""
        self.vector_store_manager = None
        self.conversation_manager = None
        self.vector_store_available = False

        # For now, we'll use the fallback since the embedding model isn't accessible
        # In production, ensure you have access to text-embedding-3-large or text-embedding-3-small
        logger.info("Using basic knowledge base without vector store")
        logger.info(
            "To enable Pinecone, ensure your Azure OpenAI key has access to embedding models")

    def add_knowledge(self, collection_name: str, documents: List[Dict[str, Any]]) -> bool:
        """Add documents to the knowledge base"""
        if not self.vector_store_manager:
            logger.warning("Vector store not available, cannot add documents")
            return False

        try:
            # Map collection names to namespaces
            namespace_mapping = {
                "it_faqs": "faqs",
                "faqs": "faqs",
                "software_guides": "kb_articles",
                "kb_articles": "kb_articles",
                "it_policies": "policies",
                "policies": "policies",
                "troubleshooting": "troubleshooting"
            }

            namespace = namespace_mapping.get(collection_name, "faqs")

            return self.vector_store_manager.add_documents(documents, namespace)

        except Exception as e:
            logger.error(f"Error adding knowledge to {collection_name}: {e}")
            return False

    def search_knowledge(self, query: str, collection: str = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant knowledge"""
        if self.vector_store_manager:
            try:
                if collection:
                    # Map collection to namespace
                    namespace_mapping = {
                        "it_faqs": "faqs",
                        "faqs": "faqs",
                        "software_guides": "kb_articles",
                        "kb_articles": "kb_articles",
                        "it_policies": "policies",
                        "policies": "policies",
                        "troubleshooting": "troubleshooting"
                    }
                    namespace = namespace_mapping.get(collection, "faqs")
                    results = self.vector_store_manager.search_documents(
                        query, namespace, k=limit)
                else:
                    # Search all namespaces
                    namespace_results = self.vector_store_manager.search_all_namespaces(
                        query, k=limit)
                    results = []
                    for namespace, docs in namespace_results.items():
                        results.extend(docs)

                return results

            except Exception as e:
                logger.error(f"Error searching vector store: {e}")

        # Fallback to basic search
        return self._fallback_search(query, limit)

    def _fallback_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Fallback search using basic knowledge base"""
        try:
            result = search_knowledge_base(query)
            if result and "No relevant knowledge found" not in result:
                return [{
                    'content': result,
                    'metadata': {
                        'source': 'fallback_kb',
                        'category': 'General',
                        'title': 'Knowledge Base Result'
                    },
                    'relevance_score': 0.7
                }]
        except Exception as e:
            logger.error(f"Error in fallback search: {e}")

        return []

    def query_with_conversation(self, query: str, chat_history: List = None) -> Dict[str, Any]:
        """Query with conversational context using LangChain"""
        if self.conversation_manager:
            try:
                return self.conversation_manager.chat_with_rag(query, "default")
            except Exception as e:
                logger.error(f"Error in conversational query: {e}")

        # Fallback to simple search
        results = self.search_knowledge(query)
        if results:
            return {
                'answer': results[0]['content'],
                'source_documents': results,
                'confidence': results[0].get('relevance_score', 0.7)
            }
        else:
            return {
                'answer': "I couldn't find relevant information for your query.",
                'source_documents': [],
                'confidence': 0.0
            }

    def check_collection_status(self) -> Dict[str, int]:
        """Check the status of all collections in the knowledge base"""
        if self.vector_store_manager:
            try:
                # Return status from vector store
                status = {}
                namespaces = ["faqs", "kb_articles",
                              "policies", "troubleshooting"]
                for namespace in namespaces:
                    # For Pinecone, this would require querying the index stats
                    # For now, return a placeholder
                    status[namespace] = 0
                return status
            except Exception as e:
                logger.error(f"Error checking collection status: {e}")
                return {}
        else:
            # Return fallback status
            return {
                "faqs": 10,
                "kb_articles": 6,
                "policies": 0,
                "troubleshooting": 2
            }


# Global knowledge base instance
_knowledge_base = None


def get_knowledge_base() -> ITKnowledgeBase:
    """Get or create global knowledge base instance"""
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = ITKnowledgeBase()
    return _knowledge_base


def query_it_knowledge(query: str, collection: str = None) -> str:
    """Query IT knowledge base and return formatted response"""
    kb = get_knowledge_base()

    try:
        results = kb.search_knowledge(query, collection)

        if not results:
            return "No relevant knowledge found for your query."

        # Format the best result
        best_result = results[0]
        content = best_result['content']
        metadata = best_result.get('metadata', {})

        # Add source information if available
        if metadata.get('title'):
            response = f"**{metadata['title']}**\n\n{content}"
        else:
            response = content

        if metadata.get('category'):
            response += f"\n\n*Category: {metadata['category']}*"

        return response

    except Exception as e:
        logger.error(f"Error querying knowledge base: {e}")
        return "Sorry, I encountered an error while searching the knowledge base."


def initialize_knowledge_base_with_data():
    """Initialize the knowledge base with mock data"""
    try:
        from ..data.mock_data import get_all_knowledge_data

        kb = get_knowledge_base()
        if not kb.vector_store_manager:
            logger.info(
                "Vector store not available, skipping data initialization")
            return

        all_data = get_all_knowledge_data()

        for collection_name, documents in all_data.items():
            if documents:
                success = kb.add_knowledge(collection_name, documents)
                if success:
                    logger.info(
                        f"Added {len(documents)} documents to {collection_name}")
                else:
                    logger.warning(
                        f"Failed to add documents to {collection_name}")

        logger.info("Knowledge base initialization completed")

    except Exception as e:
        logger.error(f"Error initializing knowledge base: {e}")
