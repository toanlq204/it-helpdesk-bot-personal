# Advanced Vector Store Handler
# IT Helpdesk Bot with Pinecone Vector Database Integration

import os
import time
import logging
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import AzureOpenAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Advanced vector store manager for IT Helpdesk knowledge base using Pinecone"""

    def __init__(self):
        """Initialize Pinecone client and embeddings"""
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "it-helpdesk-kb")
        self.dimension = 1536  # Azure OpenAI text-embedding-3-large dimension

        if not self.api_key:
            raise ValueError(
                "PINECONE_API_KEY environment variable is required")

        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.api_key)

        # Initialize Azure OpenAI embeddings
        self.embeddings = AzureOpenAIEmbeddings(
            model=os.getenv("AZOPENAI_EMBEDDING_MODEL",
                            "text-embedding-3-large"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv(
                "AZURE_OPENAI_API_VERSION", "2024-07-01-preview"),
            chunk_size=1000
        )

        # Initialize vector stores for different namespaces
        self.vector_stores = {}
        self._setup_index()

        logger.info("VectorStoreManager initialized successfully")

    def _setup_index(self):
        """Setup Pinecone index if it doesn't exist"""
        try:
            # Check if index exists
            if self.index_name not in [index.name for index in self.pc.list_indexes()]:
                logger.info(f"Creating new Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
                # Wait for index to be ready
                time.sleep(10)

            # Get index reference
            self.index = self.pc.Index(self.index_name)

            # Initialize vector stores for different namespaces
            namespaces = ["faqs", "kb_articles", "policies", "troubleshooting"]
            for namespace in namespaces:
                self.vector_stores[namespace] = PineconeVectorStore(
                    index=self.index,
                    embedding=self.embeddings,
                    namespace=namespace
                )

            logger.info(f"Pinecone index '{self.index_name}' is ready")

        except Exception as e:
            logger.error(f"Error setting up Pinecone index: {e}")
            raise

    def add_documents(self, documents: List[Dict[str, Any]], namespace: str = "faqs") -> bool:
        """Add documents to specified namespace"""
        try:
            if namespace not in self.vector_stores:
                logger.error(f"Unknown namespace: {namespace}")
                return False

            # Convert documents to LangChain Document format
            langchain_docs = []
            for doc in documents:
                # Create comprehensive content for embedding
                content_parts = []

                if doc.get('question'):
                    content_parts.append(f"Question: {doc['question']}")
                if doc.get('answer'):
                    content_parts.append(f"Answer: {doc['answer']}")
                if doc.get('title'):
                    content_parts.append(f"Title: {doc['title']}")
                if doc.get('content'):
                    content_parts.append(f"Content: {doc['content']}")

                page_content = "\n".join(content_parts)

                # Prepare metadata
                metadata = {
                    "id": doc.get('id', f"{namespace}_{len(langchain_docs)}"),
                    "category": doc.get('category', 'General'),
                    "namespace": namespace,
                    "source": f"{namespace}_knowledge_base"
                }

                # Add additional metadata fields
                for key in ['tags', 'related_kb', 'last_updated', 'priority']:
                    if key in doc:
                        metadata[key] = str(doc[key])

                langchain_docs.append(
                    Document(page_content=page_content, metadata=metadata)
                )

            # Add documents to vector store
            vector_store = self.vector_stores[namespace]
            ids = vector_store.add_documents(langchain_docs)

            logger.info(
                f"Added {len(langchain_docs)} documents to namespace '{namespace}'")
            return True

        except Exception as e:
            logger.error(
                f"Error adding documents to namespace '{namespace}': {e}")
            return False

    def search(self, query: str, namespace: str = "faqs", k: int = 5,
               score_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Search for relevant documents in specified namespace"""
        try:
            if namespace not in self.vector_stores:
                logger.error(f"Unknown namespace: {namespace}")
                return []

            vector_store = self.vector_stores[namespace]

            # Perform similarity search with scores
            docs_with_scores = vector_store.similarity_search_with_score(
                query, k=k
            )

            # Filter by score threshold and format results
            results = []
            for doc, score in docs_with_scores:
                # Convert similarity score to relevance score (higher is better)
                relevance_score = 1 - score

                if relevance_score >= score_threshold:
                    result = {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "relevance_score": relevance_score,
                        "namespace": namespace
                    }
                    results.append(result)

            logger.info(
                f"Found {len(results)} relevant documents in namespace '{namespace}'")
            return results

        except Exception as e:
            logger.error(f"Error searching namespace '{namespace}': {e}")
            return []

    def search_all_namespaces(self, query: str, k: int = 3,
                              score_threshold: float = 0.7) -> Dict[str, List[Dict[str, Any]]]:
        """Search across all namespaces and return organized results"""
        all_results = {}

        for namespace in self.vector_stores.keys():
            results = self.search(query, namespace, k, score_threshold)
            if results:
                all_results[namespace] = results

        return all_results

    def get_namespace_stats(self) -> Dict[str, int]:
        """Get document count for each namespace"""
        stats = {}
        try:
            index_stats = self.index.describe_index_stats()
            if 'namespaces' in index_stats:
                for namespace, info in index_stats['namespaces'].items():
                    stats[namespace] = info.get('vector_count', 0)
            else:
                # Fallback for older Pinecone versions
                for namespace in self.vector_stores.keys():
                    stats[namespace] = 0  # Would need to query each namespace
        except Exception as e:
            logger.error(f"Error getting namespace stats: {e}")

        return stats

    def delete_namespace(self, namespace: str) -> bool:
        """Delete all vectors in a namespace"""
        try:
            if namespace not in self.vector_stores:
                logger.error(f"Unknown namespace: {namespace}")
                return False

            # Delete all vectors in the namespace
            self.index.delete(delete_all=True, namespace=namespace)

            logger.info(f"Deleted all vectors in namespace '{namespace}'")
            return True

        except Exception as e:
            logger.error(f"Error deleting namespace '{namespace}': {e}")
            return False

    def migrate_from_chromadb(self, chromadb_handler) -> bool:
        """Migrate data from existing ChromaDB to Pinecone - DEPRECATED"""
        logger.warning(
            "ChromaDB migration is deprecated as ChromaDB has been removed")
        return False


# Global instance
_vector_store_manager = None


def get_vector_store_manager() -> VectorStoreManager:
    """Get or create global vector store manager instance"""
    global _vector_store_manager
    if _vector_store_manager is None:
        _vector_store_manager = VectorStoreManager()
    return _vector_store_manager


def query_vector_knowledge(query: str, namespace: str = None, max_results: int = 5) -> str:
    """Query vector knowledge base and return formatted response"""
    try:
        manager = get_vector_store_manager()

        if namespace:
            # Search specific namespace
            results = manager.search(query, namespace, k=max_results)
            namespace_results = {namespace: results}
        else:
            # Search all namespaces
            namespace_results = manager.search_all_namespaces(
                query, k=max_results)

        if not namespace_results:
            return "No relevant knowledge found in the vector database."

        # Format response
        formatted_response = "🔍 **Knowledge Base Search Results:**\n\n"

        for ns, results in namespace_results.items():
            if results:
                formatted_response += f"**{ns.title()} ({len(results)} results):**\n"

                for i, result in enumerate(results, 1):
                    content = result['content']
                    score = result['relevance_score']
                    category = result['metadata'].get('category', 'General')

                    formatted_response += f"{i}. **{category}** (Relevance: {score:.2f})\n"
                    formatted_response += f"   {content[:300]}{'...' if len(content) > 300 else ''}\n\n"

        return formatted_response.strip()

    except Exception as e:
        logger.error(f"Error querying vector knowledge: {e}")
        return f"Error accessing vector knowledge base: {str(e)}"


# Alias for backward compatibility
def query_pinecone_knowledge(query: str, namespace: str = None, max_results: int = 5) -> str:
    """Alias for query_vector_knowledge for backward compatibility"""
    return query_vector_knowledge(query, namespace, max_results)
