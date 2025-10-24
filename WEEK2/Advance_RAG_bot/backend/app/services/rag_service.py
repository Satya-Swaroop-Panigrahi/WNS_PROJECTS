from typing import List, Dict, Any, Optional
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import json
import logging
import pickle
import asyncio
from config import settings

# Try to import ChromaDB, but make it optional
try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logging.warning("ChromaDB not available - using FAISS only")

logger = logging.getLogger(__name__)

class BaseRAG:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_store_path = settings.VECTOR_STORE_PATH
        self.index = None
        self.documents = []
        self.document_metadata = []
        self.logger = logging.getLogger(__name__)
        
        # Ensure vector store directory exists
        os.makedirs(self.vector_store_path, exist_ok=True)
        
    def load_documents(self, document_names: List[str]):
        """Load selected documents into memory with enhanced processing"""
        self.documents = []
        self.document_metadata = []
        
        # Load from vector store if available
        self._load_vector_store()
        
        logger.info(f"Loading documents: {document_names}")
        logger.info(f"Current document count: {len(self.documents)}")
        
    def _load_vector_store(self):
        """Load existing vector store"""
        try:
            index_path = os.path.join(self.vector_store_path, "faiss_index.bin")
            metadata_path = os.path.join(self.vector_store_path, "metadata.json")
            
            if os.path.exists(index_path) and os.path.exists(metadata_path):
                self.index = faiss.read_index(index_path)
                with open(metadata_path, 'r') as f:
                    self.document_metadata = json.load(f)
                logger.info(f"Loaded vector store with {self.index.ntotal} vectors")
        except Exception as e:
            logger.warning(f"Failed to load vector store: {e}")
            self.index = None
            self.document_metadata = []
    
    def _save_vector_store(self):
        """Save vector store to disk"""
        try:
            if self.index is not None:
                index_path = os.path.join(self.vector_store_path, "faiss_index.bin")
                metadata_path = os.path.join(self.vector_store_path, "metadata.json")
                
                faiss.write_index(self.index, index_path)
                with open(metadata_path, 'w') as f:
                    json.dump(self.document_metadata, f)
                logger.info("Vector store saved successfully")
        except Exception as e:
            logger.error(f"Failed to save vector store: {e}")
        
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Enhanced semantic search with better ranking"""
        if not self.documents or self.index is None:
            logger.warning("No documents or index available for search")
            return []
            
        try:
            # Encode query
            query_embedding = self.encoder.encode([query])
            
            # Search with higher k to get more candidates
            search_k = min(k * 2, self.index.ntotal)
            distances, indices = self.index.search(query_embedding, search_k)
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.document_metadata):
                    metadata = self.document_metadata[idx]
                    score = float(distances[0][i])
                    
                    # Enhanced result with metadata
                    result = {
                        "content": self.documents[idx] if idx < len(self.documents) else "",
                        "score": score,
                        "type": "semantic",
                        "source": "document",
                        "metadata": metadata,
                        "relevance": "high" if score > 0.7 else "medium" if score > 0.5 else "low"
                    }
                    results.append(result)
            
            # Sort by score and return top k
            results.sort(key=lambda x: x["score"], reverse=True)
            return results[:k]
            
        except Exception as e:
            logger.error(f"Semantic search error: {e}")
            return []

class KnowledgeGraphRAG(BaseRAG):
    def __init__(self):
        super().__init__()
        self.knowledge_graph = {}
        self.entity_relationships = {}
        self.logger = logging.getLogger(__name__)
    
    def build_knowledge_graph(self, documents: List[str]):
        """Build knowledge graph from documents with entity extraction"""
        self.logger.info("Building knowledge graph from documents")
        
        # Simple entity extraction (in production, use spaCy or similar)
        entities = set()
        relationships = []
        
        for doc in documents:
            # Extract entities (simplified)
            words = doc.lower().split()
            for word in words:
                if len(word) > 3 and word.isalpha():
                    entities.add(word)
            
            # Extract relationships (simplified)
            if "is a" in doc.lower():
                relationships.append(("entity", "is_a", "concept"))
            if "has" in doc.lower():
                relationships.append(("entity", "has", "property"))
        
        # Build graph structure
        self.knowledge_graph = {
            "entities": list(entities),
            "relationships": relationships
        }
        
        self.logger.info(f"Knowledge graph built with {len(entities)} entities and {len(relationships)} relationships")
    
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Knowledge graph enhanced search with reasoning"""
        self.logger.info("Using knowledge graph enhanced search")
        
        # Get semantic results first
        semantic_results = super().search(query, k)
        
        # Add knowledge graph reasoning
        if self.knowledge_graph:
            # Find relevant entities
            query_entities = [word for word in query.lower().split() if word in self.knowledge_graph["entities"]]
            
            # Enhance results with graph reasoning
            for result in semantic_results:
                result["kg_entities"] = query_entities
                result["reasoning"] = f"Found {len(query_entities)} relevant entities in knowledge graph"
                result["type"] = "knowledge_graph_enhanced"
        
        return semantic_results

class HybridRAG(BaseRAG):
    def __init__(self, search_service):
        super().__init__()
        self.search_service = search_service
        self.logger = logging.getLogger(__name__)
    
    async def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Enhanced hybrid search combining semantic and internet search with intelligent ranking"""
        self.logger.info(f"Performing hybrid search for: {query}")
        
        # Get semantic results from documents
        semantic_results = super().search(query, k)
        
        # Get internet search results
        internet_results = await self.search_service.search(query)
        
        # Enhanced ranking algorithm
        combined_results = []
        
        # Add semantic results with higher weight
        for result in semantic_results:
            result["search_type"] = "semantic"
            result["weight"] = result.get("score", 0) * 1.2  # Boost semantic results
            combined_results.append(result)
        
        # Add internet results with adjusted weight
        for result in internet_results:
            result["search_type"] = "internet"
            result["weight"] = 0.8  # Base weight for internet results
            combined_results.append(result)
        
        # Intelligent ranking based on multiple factors
        def ranking_score(result):
            base_score = result.get("weight", 0)
            
            # Boost for high relevance
            if result.get("relevance") == "high":
                base_score *= 1.3
            elif result.get("relevance") == "medium":
                base_score *= 1.1
            
            # Boost for semantic results (document context)
            if result.get("search_type") == "semantic":
                base_score *= 1.2
            
            # Boost for recent internet results
            if result.get("search_type") == "internet" and "snippet" in result:
                snippet_length = len(result.get("snippet", ""))
                if snippet_length > 100:  # Longer snippets often more informative
                    base_score *= 1.1
            
            return base_score
        
        # Sort by ranking score
        ranked_results = sorted(combined_results, key=ranking_score, reverse=True)
        
        self.logger.info(f"Hybrid search returned {len(ranked_results)} total results "
                        f"({len(semantic_results)} semantic, {len(internet_results)} internet)")
        
        # Return top k results with metadata
        top_results = ranked_results[:k]
        for i, result in enumerate(top_results):
            result["rank"] = i + 1
            result["final_score"] = ranking_score(result)
        
        return top_results

class RAGFactory:
    @staticmethod
    def create_rag(variant: str, search_service=None) -> BaseRAG:
        logger.info(f"Creating RAG variant: {variant}")
        if variant == "knowledge_graph":
            return KnowledgeGraphRAG()
        elif variant == "hybrid":
            if search_service is None:
                logger.warning("No search service provided for hybrid RAG, falling back to basic")
                return BaseRAG()
            return HybridRAG(search_service)
        else:

            return BaseRAG()
