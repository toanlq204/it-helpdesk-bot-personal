# Advanced Vector Store Handler
# IT Helpdesk Bot with Pinecone Vector Database Integration

import os
import time
import logging
from typing import List, Dict, Any, Optional
try:
    from pinecone import Pinecone, ServerlessSpec
except ImportError:
    # Fallback for older pinecone versions
    import pinecone
    Pinecone = pinecone.Pinecone if hasattr(pinecone, 'Pinecone') else pinecone
    ServerlessSpec = pinecone.ServerlessSpec if hasattr(
        pinecone, 'ServerlessSpec') else None
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

        # Get embedding model from environment
        embedding_model = os.getenv(
            "AZOPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

        # Set dimension based on model
        if "text-embedding-3-large" in embedding_model:
            self.dimension = 3072  # text-embedding-3-large dimension
        elif "text-embedding-3-small" in embedding_model:
            self.dimension = 1536  # text-embedding-3-small dimension
        else:
            self.dimension = 1536  # Default fallback

        if not self.api_key:
            raise ValueError(
                "PINECONE_API_KEY environment variable is required")

        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.api_key)

        # Initialize embeddings - try multiple approaches
        self.embeddings = None
        embedding_error = None

        # Try Azure OpenAI with dedicated embedding key first
        try:
            from langchain_openai import AzureOpenAIEmbeddings

            # Use the dedicated embedding API key
            embedding_key = os.getenv("AZOPENAI_EMBEDDING_API_KEY")
            if not embedding_key:
                embedding_key = os.getenv("AZURE_OPENAI_API_KEY")

            self.embeddings = AzureOpenAIEmbeddings(
                model=os.getenv("AZOPENAI_EMBEDDING_MODEL",
                                "text-embedding-3-small"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=embedding_key,
                api_version=os.getenv(
                    "AZURE_OPENAI_API_VERSION", "2024-07-01-preview"),
                chunk_size=1000
            )
            logger.info("Using Azure OpenAI embeddings with dedicated key")
        except Exception as e:
            embedding_error = str(e)
            logger.warning(f"Azure OpenAI embeddings failed: {e}")

            # Try OpenAI directly as fallback
            try:
                from langchain_openai import OpenAIEmbeddings
                openai_key = os.getenv("OPENAI_API_KEY")
                if openai_key:
                    self.embeddings = OpenAIEmbeddings(
                        model="text-embedding-3-small",
                        openai_api_key=openai_key,
                        chunk_size=1000
                    )
                    logger.info("Using OpenAI embeddings")
                else:
                    raise ValueError("No OpenAI API key available")
            except Exception as e2:
                embedding_error = f"Azure: {e}, OpenAI: {e2}"
                logger.error(
                    f"Both embedding services failed: {embedding_error}")

                # Try using Sentence Transformers embeddings as final fallback
                try:
                    from langchain_community.embeddings import HuggingFaceEmbeddings
                    self.embeddings = HuggingFaceEmbeddings(
                        model_name="sentence-transformers/all-MiniLM-L6-v2"
                    )
                    logger.info(
                        "Using Sentence Transformers embeddings as fallback")
                    self.dimension = 384  # all-MiniLM-L6-v2 dimension
                except Exception as e3:
                    final_error = f"Azure: {e}, OpenAI: {e2}, HuggingFace: {e3}"
                    logger.error(
                        f"All embedding services failed: {final_error}")
                    raise ValueError(
                        f"Could not initialize any embedding service: {final_error}")

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
        """Search for relevant documents in specified namespace using raw Pinecone with improved relevance filtering"""
        try:
            # Use raw Pinecone search for better control
            query_embedding = self.embeddings.embed_query(query)

            # Increase search results to apply better filtering
            search_result = self.index.query(
                vector=query_embedding,
                top_k=min(k * 3, 20),  # Get more results for filtering
                include_metadata=True,
                namespace=namespace
            )

            # Format and filter results with improved relevance scoring
            results = []
            query_keywords = set(query.lower().split())

            for match in search_result.matches:
                # Extract content from metadata
                content = match.metadata.get('text', 'No content available')

                # Enhanced relevance scoring
                base_score = match.score

                # Boost score if query keywords appear in content or metadata
                keyword_boost = 0
                content_lower = content.lower()

                for keyword in query_keywords:
                    if keyword in content_lower:
                        keyword_boost += 0.1
                    if keyword in match.metadata.get('category', '').lower():
                        keyword_boost += 0.15
                    if keyword in match.metadata.get('title', '').lower():
                        keyword_boost += 0.2

                # Apply keyword boost
                enhanced_score = min(base_score + keyword_boost, 1.0)

                # Only include results that meet the threshold
                if enhanced_score >= score_threshold:
                    result = {
                        "content": content,
                        "metadata": match.metadata,
                        "relevance_score": enhanced_score,
                        "namespace": namespace,
                        "id": match.id
                    }
                    results.append(result)

            # Sort by enhanced score and limit to requested number
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            results = results[:k]

            logger.info(
                f"Found {len(results)} relevant documents in namespace '{namespace}'")
            return results

        except Exception as e:
            logger.error(f"Error searching namespace '{namespace}': {e}")
            return []

    def search_all_namespaces(self, query: str, k: int = 3,
                              score_threshold: float = 0.7) -> Dict[str, List[Dict[str, Any]]]:
        """Search across all namespaces and return organized results with improved relevance filtering"""
        all_results = {}

        # Extract keywords for better filtering
        query_keywords = set(query.lower().split())

        for namespace in self.vector_stores.keys():
            results = self.search(query, namespace, k, score_threshold)

            # Additional filtering based on query relevance
            filtered_results = []
            for result in results:
                content = result['content'].lower()
                metadata = result['metadata']

                # Check if result is actually relevant to the query
                relevance_indicators = 0

                # Count keyword matches
                for keyword in query_keywords:
                    if keyword in content:
                        relevance_indicators += 1
                    if keyword in metadata.get('category', '').lower():
                        relevance_indicators += 1
                    if keyword in metadata.get('title', '').lower():
                        relevance_indicators += 2

                # Only include if there's some relevance
                if relevance_indicators > 0 or result['relevance_score'] > 0.85:
                    filtered_results.append(result)

            if filtered_results:
                # Sort by relevance and limit results
                filtered_results.sort(
                    key=lambda x: x['relevance_score'], reverse=True)
                all_results[namespace] = filtered_results[:k]

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


def query_vector_knowledge(query: str, namespace: str = None, max_results: int = 3) -> str:
    """Query vector knowledge base and return formatted response with improved relevance filtering"""
    try:
        manager = get_vector_store_manager()

        if namespace:
            # Search specific namespace
            results = manager.search(
                query, namespace, k=max_results, score_threshold=0.7)
            namespace_results = {namespace: results}
        else:
            # Search all namespaces with higher threshold for better relevance
            namespace_results = manager.search_all_namespaces(
                query, k=max_results, score_threshold=0.7)

        if not namespace_results:
            return "No relevant knowledge found in the vector database."

        # Count total relevant results
        total_results = sum(len(results)
                            for results in namespace_results.values())

        if total_results == 0:
            return "No highly relevant information found for your query. Please try rephrasing your question or be more specific."

        # Format response with better structure
        formatted_response = f"🔍 **Found {total_results} relevant result(s):**\n\n"

        for ns, results in namespace_results.items():
            if results:
                # Sort results by relevance score
                results.sort(key=lambda x: x['relevance_score'], reverse=True)

                formatted_response += f"📁 **{ns.replace('_', ' ').title()}:**\n"

                for i, result in enumerate(results, 1):
                    content = result['content']
                    score = result['relevance_score']
                    category = result['metadata'].get('category', 'General')

                    # Truncate content intelligently at sentence boundaries
                    if len(content) > 250:
                        # Try to cut at sentence boundary
                        truncated = content[:250]
                        last_period = truncated.rfind('.')
                        last_question = truncated.rfind('?')
                        last_exclamation = truncated.rfind('!')

                        cut_point = max(
                            last_period, last_question, last_exclamation)
                        if cut_point > 100:  # Ensure we have reasonable content
                            content = content[:cut_point + 1]
                        else:
                            content = content[:250] + "..."

                    formatted_response += f"   {i}. **{category}** (Relevance: {score:.1f})\n"
                    formatted_response += f"      {content}\n\n"

        # Add helpful footer only if we found good results
        if total_results > 0:
            formatted_response += "💡 *Need more specific information? Feel free to ask follow-up questions.*"

        return formatted_response.strip()

    except Exception as e:
        logger.error(f"Error querying vector knowledge: {e}")
        return f"Error accessing vector knowledge base: {str(e)}"


# Alias for backward compatibility
def query_pinecone_knowledge(query: str, namespace: str = None, max_results: int = 3) -> str:
    """Alias for query_vector_knowledge for backward compatibility"""
    return query_vector_knowledge(query, namespace, max_results)
