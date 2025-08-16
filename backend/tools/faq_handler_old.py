# ChromaDB Knowledge Base Handler for IT Helpdesk Bot
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ITKnowledgeBase:
    def __init__(self, persist_directory: str = "./chromadb_data"):
        """Initialize ChromaDB client and collections"""
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Configuration for HuggingFace embedding
        self.hf_token = os.getenv("AZOPENAI_EMBEDDING_API_KEY")
        self.embedding_model = os.getenv(
            "AZOPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

        if not self.hf_token:
            logger.warning(
                "AZOPENAI_EMBEDDING_API_KEY not found. Using default embeddings.")

        # Initialize collections with proper embedding function
        self.collections = {}
        self._initialize_collections()

        logger.info("ITKnowledgeBase initialized successfully")

    def _get_embedding_function(self):
        """Get embedding function for ChromaDB"""
        if self.hf_token:
            # Use HuggingFace embedding
            return chromadb.utils.embedding_functions.HuggingFaceEmbeddingFunction(
                api_key=self.hf_token,
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        else:
            # Use default embedding
            return chromadb.utils.embedding_functions.DefaultEmbeddingFunction()

    def _initialize_collections(self):
        """Initialize all required collections"""
        embedding_function = self._get_embedding_function()

        collection_names = ["it_faqs", "software_guides", "it_policies"]

        for name in collection_names:
            try:
                # Try to get existing collection
                collection = self.client.get_collection(
                    name=name,
                    embedding_function=embedding_function
                )
                logger.info(f"Found existing collection: {name}")
            except ValueError:
                # Create new collection if it doesn't exist
                collection = self.client.create_collection(
                    name=name,
                    embedding_function=embedding_function
                )
                logger.info(f"Created new collection: {name}")

            self.collections[name.replace("it_", "")] = collection

    def add_knowledge(self, collection_name: str, documents: List[Dict[str, Any]]):
        """Add documents to a specific collection"""
        # Map collection names
        collection_key = collection_name.replace("it_", "")
        if collection_key not in self.collections:
            logger.error(f"Collection {collection_name} not found")
            return

        collection = self.collections[collection_key]

        # Prepare data for ChromaDB
        ids = []
        texts = []
        metadatas = []

        for i, doc in enumerate(documents):
            doc_id = doc.get('id', f"{collection_name}_{i}")

            # Create comprehensive text for embedding
            title = doc.get('title', '')
            content = doc.get('content', '')
            question = doc.get('question', '')
            answer = doc.get('answer', '')

            text = f"{title} {question} {answer} {content}".strip()

            if not text:
                continue

            metadata = {k: v for k, v in doc.items() if k not in [
                'id', 'content']}
            metadata['source'] = collection_name

            ids.append(doc_id)
            texts.append(text)
            metadatas.append(metadata)

        if texts:
            # Add to collection
            try:
                collection.add(
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(
                    f"Added {len(texts)} documents to {collection_name}")
            except Exception as e:
                logger.error(
                    f"Error adding documents to {collection_name}: {e}")

    def query_knowledge(self, query: str, collection_name: str = None, n_results: int = 3) -> List[Dict[str, Any]]:
        """Query knowledge base for relevant information"""
        results = []

        # Query specific collection or all collections
        collections_to_query = [collection_name] if collection_name else list(
            self.collections.keys())

        for coll_name in collections_to_query:
            try:
                collection = self.collections[coll_name]
                query_results = collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    include=['documents', 'metadatas', 'distances']
                )

                # Format results
                for i in range(len(query_results['documents'][0])):
                    result = {
                        'collection': coll_name,
                        'content': query_results['documents'][0][i],
                        'metadata': query_results['metadatas'][0][i],
                        'distance': query_results['distances'][0][i],
                        # Convert distance to relevance
                        'relevance_score': 1 - query_results['distances'][0][i]
                    }
                    results.append(result)

            except Exception as e:
                logger.error(
                    f"Error querying collection {coll_name}: {str(e)}")

        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:n_results * len(collections_to_query)]

    def get_contextual_knowledge(self, query: str, session_id: str) -> str:
        """Get relevant knowledge formatted for OpenAI context"""
        results = self.query_knowledge(query)

        if not results:
            return "No relevant knowledge found in the database."

        context_parts = []
        context_parts.append("📚 **Relevant IT Knowledge:**\n")

        for i, result in enumerate(results[:5], 1):  # Limit to top 5 results
            collection_emoji = {
                'faqs': '❓',
                'software': '💻',
                'policies': '📋'
            }.get(result['collection'], '📄')

            context_parts.append(
                f"{collection_emoji} **{result['collection'].title()} #{i}** (Relevance: {result['relevance_score']:.2f})")
            context_parts.append(f"{result['content']}\n")

            # Add metadata if available
            if result['metadata']:
                metadata_str = ", ".join(
                    [f"{k}: {v}" for k, v in result['metadata'].items()])
                context_parts.append(f"*{metadata_str}*\n")

        return "\n".join(context_parts)

    def check_collection_status(self) -> Dict[str, int]:
        """Get status of all collections"""
        status = {}
        for name, collection in self.collections.items():
            try:
                count = collection.count()
                status[name] = count
            except Exception as e:
                logger.error(f"Error checking collection {name}: {str(e)}")
                status[name] = 0

        return status


# Global instance
_knowledge_base = None


def get_knowledge_base() -> ITKnowledgeBase:
    """Get or create global knowledge base instance"""
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = ITKnowledgeBase()
    return _knowledge_base


def query_it_knowledge(query: str, collection: str = None) -> str:
    """Function to be called by OpenAI tools"""
    try:
        kb = get_knowledge_base()
        context = kb.get_contextual_knowledge(query, "default")
        return context
    except Exception as e:
        logger.error(f"Error querying IT knowledge: {str(e)}")
        return f"Error accessing knowledge base: {str(e)}"
