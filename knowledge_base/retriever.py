"""
Retriever module for finding relevant knowledge base content.
"""

import re
from pathlib import Path
from typing import List, Dict, Optional
from knowledge_base.vector_store import VectorStore

class KnowledgeRetriever:
    """Handles retrieval of relevant knowledge from vector stores."""
    
    def __init__(self, kb_base_path: str = "knowledge_base/processed"):
        """
        Initialize the knowledge retriever.
        
        Args:
            kb_base_path: Base path where processed knowledge bases are stored
        """
        self.kb_base_path = Path(kb_base_path)
        self.agent_stores = {}
        self.load_all_stores()
    
    def load_all_stores(self):
        """Load all available vector stores for different agents."""
        agent_names = ['maaya', 'gynika', 'meher', 'nyaya', 'vaanya']
        
        for agent_name in agent_names:
            store_path = self.kb_base_path / f"{agent_name}_vectorstore"
            if store_path.exists():
                try:
                    vector_store = VectorStore()
                    if vector_store.load(str(store_path)):
                        self.agent_stores[agent_name] = vector_store
                        print(f"Loaded knowledge base for {agent_name}")
                    else:
                        print(f"Failed to load knowledge base for {agent_name}")
                except Exception as e:
                    print(f"Error loading {agent_name} knowledge base: {e}")
            else:
                print(f"No knowledge base found for {agent_name} at {store_path}")
    
    def preprocess_query(self, query: str) -> str:
        """
        Preprocess the query for better search results.
        
        Args:
            query: Raw user query
            
        Returns:
            Preprocessed query
        """
        # Convert to lowercase
        query = query.lower()
        
        # Remove extra whitespace
        query = re.sub(r'\s+', ' ', query)
        
        # Remove common stop words that might interfere with search
        stop_words = ['the', 'is', 'at', 'which', 'on', 'and', 'a', 'to', 'are', 'as', 'was', 'will', 'be']
        words = query.split()
        filtered_words = [word for word in words if word not in stop_words]
        
        return ' '.join(filtered_words).strip()
    
    def retrieve_for_agent(self, agent_name: str, query: str, top_k: int = 3, min_similarity: float = 0.3) -> List[Dict]:
        """
        Retrieve relevant knowledge for a specific agent.
        
        Args:
            agent_name: Name of the agent (maaya, gynika, meher, nyaya, vaanya)
            query: Search query
            top_k: Number of top results to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of relevant chunks with metadata
        """
        if agent_name not in self.agent_stores:
            print(f"No knowledge base available for agent: {agent_name}")
            return []
        
        # Preprocess query
        processed_query = self.preprocess_query(query)
        
        # Search in agent's knowledge base
        results = self.agent_stores[agent_name].search(
            processed_query, 
            top_k=top_k, 
            min_similarity=min_similarity
        )
        
        return results
    
    def format_context(self, retrieved_chunks: List[Dict], max_context_length: int = 1500) -> str:
        """
        Format retrieved chunks into a coherent context string.
        
        Args:
            retrieved_chunks: List of retrieved chunk dictionaries
            max_context_length: Maximum length of context to return
            
        Returns:
            Formatted context string
        """
        if not retrieved_chunks:
            return ""
        
        context_parts = []
        current_length = 0
        
        for i, chunk in enumerate(retrieved_chunks):
            chunk_text = chunk['text']
            source_info = f"[Source: {chunk.get('doc_title', 'Unknown')}]"
            
            # Add source information and chunk text
            chunk_with_source = f"{source_info}\n{chunk_text}"
            
            # Check if adding this chunk would exceed max length
            if current_length + len(chunk_with_source) > max_context_length and context_parts:
                break
            
            context_parts.append(chunk_with_source)
            current_length += len(chunk_with_source)
        
        # Join with separators
        context = "\n\n---\n\n".join(context_parts)
        
        return context
    
    def get_enhanced_source_citations(self, retrieved_chunks: List[Dict]) -> List[Dict]:
        """
        Extract enhanced source citations with detailed metadata.
        
        Args:
            retrieved_chunks: List of retrieved chunk dictionaries
            
        Returns:
            List of detailed source citation dictionaries with page info
        """
        sources = []
        
        for i, chunk in enumerate(retrieved_chunks):
            doc_title = chunk.get('doc_title', 'Unknown Document')
            doc_filename = chunk.get('doc_filename', chunk.get('doc_title', 'Unknown'))
            similarity = chunk.get('similarity', 0)
            chunk_id = chunk.get('id', f'chunk_{i}')
            chunk_text = chunk.get('text', '')
            
            # Get page information
            pages = chunk.get('pages', [])
            primary_page = chunk.get('primary_page')
            
            # Create page reference string
            if pages:
                if len(pages) == 1:
                    page_ref = f"Page {primary_page}"
                else:
                    page_nums = [str(p['page_number']) for p in pages]
                    page_ref = f"Pages {'-'.join(page_nums)}"
            else:
                page_ref = "Page unknown"
            
            # Create content preview (first 200 chars)
            preview = chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text
            
            # Create detailed extract (first 500 chars for references)
            extract = chunk_text[:500] + "..." if len(chunk_text) > 500 else chunk_text
            
            citation = {
                'document': doc_title,
                'filename': doc_filename,
                'page_reference': page_ref,
                'pages': pages,
                'primary_page': primary_page,
                'relevance_score': similarity,
                'confidence': 'High' if similarity > 0.8 else 'Medium' if similarity > 0.5 else 'Low',
                'chunk_id': chunk_id,
                'preview': preview,
                'extract': extract,
                'full_text': chunk_text,
                'word_count': len(chunk_text.split()),
                'char_count': len(chunk_text)
            }
            
            sources.append(citation)
        
        return sources
    
    def retrieve_multi_agent(self, query: str, agent_names: List[str], top_k: int = 2) -> Dict[str, List[Dict]]:
        """
        Retrieve knowledge for multiple agents.
        
        Args:
            query: Search query
            agent_names: List of agent names to search
            top_k: Number of results per agent
            
        Returns:
            Dictionary mapping agent names to their retrieved chunks
        """
        results = {}
        
        for agent_name in agent_names:
            if agent_name in self.agent_stores:
                agent_results = self.retrieve_for_agent(agent_name, query, top_k)
                if agent_results:  # Only include if there are results
                    results[agent_name] = agent_results
        
        return results
    
    def get_available_agents(self) -> List[str]:
        """
        Get list of agents with available knowledge bases.
        
        Returns:
            List of agent names with knowledge bases
        """
        return list(self.agent_stores.keys())
    
    def get_knowledge_stats(self) -> Dict[str, Dict]:
        """
        Get statistics for all loaded knowledge bases.
        
        Returns:
            Dictionary with stats for each agent's knowledge base
        """
        stats = {}
        
        for agent_name, vector_store in self.agent_stores.items():
            stats[agent_name] = vector_store.get_stats()
        
        return stats


# Convenience function for quick retrieval
def get_relevant_context(query: str, agent_name: str, retriever: Optional[KnowledgeRetriever] = None) -> str:
    """
    Quick function to get relevant context for an agent.
    
    Args:
        query: Search query
        agent_name: Name of the agent
        retriever: Optional existing retriever instance
        
    Returns:
        Formatted context string
    """
    if retriever is None:
        retriever = KnowledgeRetriever()
    
    retrieved_chunks = retriever.retrieve_for_agent(agent_name, query)
    context = retriever.format_context(retrieved_chunks)
    
    return context


if __name__ == "__main__":
    # Example usage
    retriever = KnowledgeRetriever()
    
    print("Available agents:", retriever.get_available_agents())
    print("\nKnowledge base stats:")
    stats = retriever.get_knowledge_stats()
    for agent, stat in stats.items():
        print(f"{agent}: {stat['total_chunks']} chunks")
    
    # Test retrieval
    if retriever.get_available_agents():
        agent = retriever.get_available_agents()[0]
        results = retriever.retrieve_for_agent(agent, "pregnancy nutrition")
        print(f"\nTest search results for {agent}:")
        for result in results[:2]:
            print(f"- {result['text'][:100]}... (similarity: {result['similarity']:.3f})")
    
    print("\nKnowledge retriever ready!")
