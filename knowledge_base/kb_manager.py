"""
Knowledge base manager for coordinating document processing and vector store operations.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from knowledge_base.document_processor import DocumentProcessor
from knowledge_base.vector_store import VectorStore
from datetime import datetime

class KnowledgeBaseManager:
    """Manages the entire knowledge base lifecycle."""
    
    def __init__(self, base_path: str = "knowledge_base"):
        """
        Initialize the knowledge base manager.
        
        Args:
            base_path: Base path for knowledge base files
        """
        self.base_path = Path(base_path)
        self.raw_pdfs_path = self.base_path / "raw_pdfs"
        self.processed_path = self.base_path / "processed"
        self.metadata_path = self.base_path / "metadata"
        
        # Ensure directories exist
        for path in [self.raw_pdfs_path, self.processed_path, self.metadata_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        self.processor = DocumentProcessor()
        self.agent_names = ['maaya', 'gynika', 'meher', 'nyaya', 'vaanya']
    
    def process_agent_pdfs(self, agent_name: str, force_rebuild: bool = False) -> bool:
        """
        Process all PDFs for a specific agent.
        
        Args:
            agent_name: Name of the agent
            force_rebuild: Whether to rebuild even if processed data exists
            
        Returns:
            True if successful, False otherwise
        """
        if agent_name not in self.agent_names:
            print(f"Invalid agent name: {agent_name}")
            return False
        
        agent_pdf_path = self.raw_pdfs_path / agent_name
        agent_vector_path = self.processed_path / f"{agent_name}_vectorstore"
        agent_metadata_path = self.metadata_path / f"{agent_name}_metadata.json"
        
        # Check if already processed and not forcing rebuild
        if not force_rebuild and agent_vector_path.exists():
            print(f"Knowledge base for {agent_name} already exists. Use force_rebuild=True to rebuild.")
            return True
        
        # Check if PDF directory exists and has PDFs
        if not agent_pdf_path.exists():
            print(f"PDF directory not found for {agent_name}: {agent_pdf_path}")
            return False
        
        pdf_files = list(agent_pdf_path.glob("*.pdf"))
        if not pdf_files:
            print(f"No PDF files found for {agent_name} in {agent_pdf_path}")
            return False
        
        print(f"Processing {len(pdf_files)} PDFs for {agent_name}...")
        
        try:
            # Process all PDFs in the agent's directory
            all_chunks = self.processor.process_directory(str(agent_pdf_path))
            
            if not all_chunks:
                print(f"No content extracted from PDFs for {agent_name}")
                return False
            
            # Save processed chunks metadata
            self.processor.save_metadata(all_chunks, str(agent_metadata_path))
            
            # Create and build vector store
            vector_store = VectorStore()
            if not vector_store.build_index(all_chunks):
                print(f"Failed to build vector index for {agent_name}")
                return False
            
            # Save vector store
            if not vector_store.save(str(agent_vector_path)):
                print(f"Failed to save vector store for {agent_name}")
                return False
            
            print(f"Successfully processed {len(all_chunks)} chunks for {agent_name}")
            return True
            
        except Exception as e:
            print(f"Error processing PDFs for {agent_name}: {e}")
            return False
    
    def process_all_agents(self, force_rebuild: bool = False) -> Dict[str, bool]:
        """
        Process PDFs for all agents.
        
        Args:
            force_rebuild: Whether to rebuild existing knowledge bases
            
        Returns:
            Dictionary mapping agent names to success status
        """
        results = {}
        
        print("Processing knowledge bases for all agents...")
        print("=" * 50)
        
        for agent_name in self.agent_names:
            print(f"\nProcessing {agent_name.upper()}...")
            results[agent_name] = self.process_agent_pdfs(agent_name, force_rebuild)
            
            if results[agent_name]:
                print(f"✅ {agent_name} knowledge base ready")
            else:
                print(f"❌ {agent_name} knowledge base failed")
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        print(f"\n" + "=" * 50)
        print(f"Knowledge base processing complete: {successful}/{len(self.agent_names)} agents ready")
        
        return results
    
    def get_status(self) -> Dict[str, Dict]:
        """
        Get status of all knowledge bases.
        
        Returns:
            Dictionary with status information for each agent
        """
        status = {}
        
        for agent_name in self.agent_names:
            agent_pdf_path = self.raw_pdfs_path / agent_name
            agent_vector_path = self.processed_path / f"{agent_name}_vectorstore"
            agent_metadata_path = self.metadata_path / f"{agent_name}_metadata.json"
            
            # Count PDF files
            pdf_count = len(list(agent_pdf_path.glob("*.pdf"))) if agent_pdf_path.exists() else 0
            
            # Check if processed
            is_processed = agent_vector_path.exists() and agent_metadata_path.exists()
            
            # Get chunk count if processed
            chunk_count = 0
            if is_processed and agent_metadata_path.exists():
                try:
                    with open(agent_metadata_path, 'r') as f:
                        metadata = json.load(f)
                        chunk_count = metadata.get('total_chunks', 0)
                except:
                    pass
            
            status[agent_name] = {
                'pdf_count': pdf_count,
                'is_processed': is_processed,
                'chunk_count': chunk_count,
                'pdf_path': str(agent_pdf_path),
                'vector_path': str(agent_vector_path)
            }
        
        return status
    
    def add_pdfs_to_agent(self, agent_name: str, pdf_paths: List[str]) -> bool:
        """
        Add new PDFs to an agent's knowledge base.
        
        Args:
            agent_name: Name of the agent
            pdf_paths: List of paths to PDF files to add
            
        Returns:
            True if successful, False otherwise
        """
        if agent_name not in self.agent_names:
            print(f"Invalid agent name: {agent_name}")
            return False
        
        agent_pdf_path = self.raw_pdfs_path / agent_name
        agent_pdf_path.mkdir(exist_ok=True)
        
        # Copy PDFs to agent directory
        copied_files = []
        for pdf_path in pdf_paths:
            src_path = Path(pdf_path)
            if src_path.exists() and src_path.suffix.lower() == '.pdf':
                dst_path = agent_pdf_path / src_path.name
                try:
                    import shutil
                    shutil.copy2(src_path, dst_path)
                    copied_files.append(str(dst_path))
                    print(f"Added {src_path.name} to {agent_name}")
                except Exception as e:
                    print(f"Failed to copy {src_path}: {e}")
            else:
                print(f"Invalid PDF file: {pdf_path}")
        
        if copied_files:
            print(f"Added {len(copied_files)} PDFs to {agent_name}. Run process_agent_pdfs() to update knowledge base.")
            return True
        else:
            print("No PDFs were successfully added.")
            return False
    
    def cleanup_agent(self, agent_name: str) -> bool:
        """
        Clean up processed data for an agent (keeping raw PDFs).
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            True if successful, False otherwise
        """
        if agent_name not in self.agent_names:
            print(f"Invalid agent name: {agent_name}")
            return False
        
        try:
            import shutil
            
            # Remove processed vector store
            agent_vector_path = self.processed_path / f"{agent_name}_vectorstore"
            if agent_vector_path.exists():
                shutil.rmtree(agent_vector_path)
                print(f"Removed vector store for {agent_name}")
            
            # Remove metadata
            agent_metadata_path = self.metadata_path / f"{agent_name}_metadata.json"
            if agent_metadata_path.exists():
                agent_metadata_path.unlink()
                print(f"Removed metadata for {agent_name}")
            
            return True
            
        except Exception as e:
            print(f"Error cleaning up {agent_name}: {e}")
            return False


if __name__ == "__main__":
    # Example usage
    kb_manager = KnowledgeBaseManager()
    
    # Show current status
    print("Current knowledge base status:")
    status = kb_manager.get_status()
    for agent, info in status.items():
        print(f"{agent}: {info['pdf_count']} PDFs, {'✅' if info['is_processed'] else '❌'} processed ({info['chunk_count']} chunks)")
    
    # Uncomment to process all agents
    # kb_manager.process_all_agents()
    
    print("\nKnowledge base manager ready!")
