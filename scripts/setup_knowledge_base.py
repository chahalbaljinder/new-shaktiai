#!/usr/bin/env python3
"""
Setup script for SHAKTI-AI knowledge base.
This script helps you set up and manage the PDF knowledge bases for all agents.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from knowledge_base.kb_manager import KnowledgeBaseManager

def main():
    """Main setup function."""
    print("🧬 SHAKTI-AI Knowledge Base Setup")
    print("=" * 40)
    
    # Initialize knowledge base manager
    kb_manager = KnowledgeBaseManager()
    
    while True:
        print("\nOptions:")
        print("1. Show current status")
        print("2. Process all agent knowledge bases")
        print("3. Process specific agent")
        print("4. Add PDFs to agent")
        print("5. Cleanup agent data")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            show_status(kb_manager)
        elif choice == "2":
            process_all_agents(kb_manager)
        elif choice == "3":
            process_specific_agent(kb_manager)
        elif choice == "4":
            add_pdfs_to_agent(kb_manager)
        elif choice == "5":
            cleanup_agent(kb_manager)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def show_status(kb_manager: KnowledgeBaseManager):
    """Show current knowledge base status."""
    print("\n📊 Current Knowledge Base Status:")
    print("-" * 40)
    
    status = kb_manager.get_status()
    
    for agent, info in status.items():
        status_icon = "✅" if info['is_processed'] else "❌"
        print(f"{agent.upper()}: {info['pdf_count']} PDFs | {status_icon} Processed | {info['chunk_count']} chunks")
        print(f"   PDF Path: {info['pdf_path']}")
        if info['is_processed']:
            print(f"   Vector Store: {info['vector_path']}")
        print()

def process_all_agents(kb_manager: KnowledgeBaseManager):
    """Process knowledge bases for all agents."""
    print("\n🔄 Processing all agent knowledge bases...")
    
    force_rebuild = input("Force rebuild existing knowledge bases? (y/N): ").strip().lower() == 'y'
    
    results = kb_manager.process_all_agents(force_rebuild=force_rebuild)
    
    print("\n📋 Results:")
    for agent, success in results.items():
        icon = "✅" if success else "❌"
        print(f"{icon} {agent}")

def process_specific_agent(kb_manager: KnowledgeBaseManager):
    """Process knowledge base for a specific agent."""
    print("\n🎯 Process Specific Agent")
    print("Available agents:", ", ".join(kb_manager.agent_names))
    
    agent_name = input("Enter agent name: ").strip().lower()
    
    if agent_name not in kb_manager.agent_names:
        print(f"Invalid agent name. Must be one of: {', '.join(kb_manager.agent_names)}")
        return
    
    force_rebuild = input("Force rebuild if already exists? (y/N): ").strip().lower() == 'y'
    
    success = kb_manager.process_agent_pdfs(agent_name, force_rebuild=force_rebuild)
    
    if success:
        print(f"✅ Successfully processed knowledge base for {agent_name}")
    else:
        print(f"❌ Failed to process knowledge base for {agent_name}")

def add_pdfs_to_agent(kb_manager: KnowledgeBaseManager):
    """Add PDFs to an agent's knowledge base."""
    print("\n📄 Add PDFs to Agent")
    print("Available agents:", ", ".join(kb_manager.agent_names))
    
    agent_name = input("Enter agent name: ").strip().lower()
    
    if agent_name not in kb_manager.agent_names:
        print(f"Invalid agent name. Must be one of: {', '.join(kb_manager.agent_names)}")
        return
    
    print("\nEnter PDF file paths (one per line, empty line to finish):")
    pdf_paths = []
    while True:
        path = input("PDF path: ").strip()
        if not path:
            break
        pdf_paths.append(path)
    
    if pdf_paths:
        success = kb_manager.add_pdfs_to_agent(agent_name, pdf_paths)
        if success:
            rebuild = input("\nRebuild knowledge base now? (y/N): ").strip().lower() == 'y'
            if rebuild:
                kb_manager.process_agent_pdfs(agent_name, force_rebuild=True)
    else:
        print("No PDF paths provided.")

def cleanup_agent(kb_manager: KnowledgeBaseManager):
    """Clean up an agent's processed data."""
    print("\n🧹 Cleanup Agent Data")
    print("Available agents:", ", ".join(kb_manager.agent_names))
    
    agent_name = input("Enter agent name to cleanup: ").strip().lower()
    
    if agent_name not in kb_manager.agent_names:
        print(f"Invalid agent name. Must be one of: {', '.join(kb_manager.agent_names)}")
        return
    
    confirm = input(f"Are you sure you want to cleanup {agent_name}? This will remove processed data but keep PDFs. (y/N): ").strip().lower()
    
    if confirm == 'y':
        success = kb_manager.cleanup_agent(agent_name)
        if success:
            print(f"✅ Successfully cleaned up {agent_name}")
        else:
            print(f"❌ Failed to cleanup {agent_name}")
    else:
        print("Cleanup cancelled.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please check your setup and try again.")
