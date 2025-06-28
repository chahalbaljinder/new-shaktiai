"""
Vector store module for managing embeddings and similarity search.
"""

import os
import json
import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from sentence_transformers import SentenceTransformer
import faiss

class VectorStore:
    """Manages document embeddings and similarity search using FAISS."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the vector store.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.chunks = []
        self.metadata = {}
        
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Create embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            Numpy array of embeddings
        """
        print(f"Creating embeddings for {len(texts)} texts...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings.astype('float32')
    
    def build_index(self, chunks: List[Dict[str, any]]) -> bool:
        """
        Build FAISS index from document chunks.
        
        Args:
            chunks: List of chunk dictionaries with 'text' field
            
        Returns:
            True if successful, False otherwise
        """
        if not chunks:
            print("No chunks provided to build index")
            return False
            
        try:
            # Extract texts from chunks
            texts = [chunk['text'] for chunk in chunks]
            
            # Create embeddings
            embeddings = self.create_embeddings(texts)
            
            # Build FAISS index
            self.index = faiss.IndexFlatIP(self.dimension)  # Inner product (cosine similarity)
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Add to index
            self.index.add(embeddings)
            
            # Store chunks and metadata
            self.chunks = chunks
            self.metadata = {
                'total_chunks': len(chunks),
                'model_name': self.model_name,
                'dimension': self.dimension,
                'index_type': 'IndexFlatIP'
            }
            
            print(f"Successfully built index with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"Error building index: {e}")
            return False
    
    def search(self, query: str, top_k: int = 5, min_similarity: float = 0.3) -> List[Dict[str, any]]:
        """
        Search for similar chunks given a query.
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of similar chunks with similarity scores
        """
        if self.index is None:
            print("Index not built. Call build_index() first.")
            return []
        
        try:
            # Create query embedding
            query_embedding = self.model.encode([query]).astype('float32')
            faiss.normalize_L2(query_embedding)
            
            # Search
            similarities, indices = self.index.search(query_embedding, top_k)
            
            # Format results
            results = []
            for i, (similarity, idx) in enumerate(zip(similarities[0], indices[0])):
                if similarity >= min_similarity and idx < len(self.chunks):
                    result = self.chunks[idx].copy()
                    result['similarity'] = float(similarity)
                    result['rank'] = i + 1
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    def save(self, save_path: str) -> bool:
        """
        Save the vector store to disk.
        
        Args:
            save_path: Directory path to save the vector store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            save_path = Path(save_path)
            save_path.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            if self.index is not None:
                faiss.write_index(self.index, str(save_path / "index.faiss"))
            
            # Save chunks and metadata
            with open(save_path / "chunks.pkl", 'wb') as f:
                pickle.dump(self.chunks, f)
            
            with open(save_path / "metadata.json", 'w') as f:
                json.dump(self.metadata, f, indent=2)
            
            print(f"Vector store saved to {save_path}")
            return True
            
        except Exception as e:
            print(f"Error saving vector store: {e}")
            return False
    
    def load(self, load_path: str) -> bool:
        """
        Load the vector store from disk.
        
        Args:
            load_path: Directory path to load the vector store from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            load_path = Path(load_path)
            
            # Check if files exist
            index_file = load_path / "index.faiss"
            chunks_file = load_path / "chunks.pkl"
            metadata_file = load_path / "metadata.json"
            
            if not all(f.exists() for f in [index_file, chunks_file, metadata_file]):
                print(f"Vector store files not found in {load_path}")
                return False
            
            # Load FAISS index
            self.index = faiss.read_index(str(index_file))
            
            # Load chunks
            with open(chunks_file, 'rb') as f:
                self.chunks = pickle.load(f)
            
            # Load metadata
            with open(metadata_file, 'r') as f:
                self.metadata = json.load(f)
            
            print(f"Vector store loaded from {load_path}")
            print(f"Loaded {len(self.chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return False
    
    def get_stats(self) -> Dict[str, any]:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with vector store statistics
        """
        stats = {
            'total_chunks': len(self.chunks),
            'model_name': self.model_name,
            'dimension': self.dimension,
            'index_built': self.index is not None
        }
        
        if self.chunks:
            # Calculate text statistics
            text_lengths = [len(chunk['text']) for chunk in self.chunks]
            stats.update({
                'avg_chunk_length': np.mean(text_lengths),
                'min_chunk_length': np.min(text_lengths),
                'max_chunk_length': np.max(text_lengths)
            })
        
        return stats


if __name__ == "__main__":
    # Example usage
    vector_store = VectorStore()
    
    # Example chunks
    sample_chunks = [
        {'text': 'Pregnancy requires proper nutrition and regular checkups.', 'id': 1},
        {'text': 'Morning sickness is common during first trimester.', 'id': 2},
        {'text': 'Prenatal vitamins are important for fetal development.', 'id': 3}
    ]
    
    # Build index
    if vector_store.build_index(sample_chunks):
        # Test search
        results = vector_store.search("pregnancy nutrition", top_k=2)
        print("Search results:", results)
        
        # Save and load test
        vector_store.save("test_vectorstore")
        
        # Test loading
        new_vs = VectorStore()
        if new_vs.load("test_vectorstore"):
            print("Successfully loaded vector store")
            print("Stats:", new_vs.get_stats())
    
    print("Vector store module ready!")
