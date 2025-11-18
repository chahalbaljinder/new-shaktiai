"""
APEX RAG Pipeline Creator
This script processes PDFs for APEX agents and creates the knowledge base.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def process_apex_knowledge_base():
    """Process all APEX agent PDFs and create vector stores."""
    try:
        print("🚀 Starting APEX RAG Pipeline Creation")
        print("=" * 50)
        
        # Import after path setup
        from knowledge_base.kb_manager import KnowledgeBaseManager
        
        # Initialize knowledge base manager
        print("📋 Initializing Knowledge Base Manager...")
        kb_manager = KnowledgeBaseManager()
        
        # Check current status
        print("\n📊 Checking current PDF status:")
        status = kb_manager.get_status()
        
        total_pdfs = 0
        for agent_name in ['athena', 'asha', 'scribe']:
            if agent_name in status:
                pdf_count = status[agent_name]['pdf_count']
                total_pdfs += pdf_count
                print(f"  📁 {agent_name.title()}: {pdf_count} PDFs")
                if pdf_count == 0:
                    print(f"    ⚠️  No PDFs found for {agent_name}")
        
        if total_pdfs == 0:
            print("\n❌ No PDFs found for any agent!")
            print("Please add PDFs to:")
            print("  - knowledge_base/raw_pdfs/athena/")
            print("  - knowledge_base/raw_pdfs/asha/")
            print("  - knowledge_base/raw_pdfs/scribe/")
            return False
        
        print(f"\n📚 Total PDFs to process: {total_pdfs}")
        
        # Process all agents
        print("\n🔄 Processing Knowledge Bases...")
        print("-" * 30)
        
        results = {}
        agents_to_process = ['athena', 'asha', 'scribe']
        
        for agent_name in agents_to_process:
            print(f"\n🤖 Processing {agent_name.title()}...")
            
            try:
                # Check if agent has PDFs
                if agent_name in status and status[agent_name]['pdf_count'] > 0:
                    success = kb_manager.process_agent_pdfs(agent_name, force_rebuild=True)
                    results[agent_name] = success
                    
                    if success:
                        print(f"✅ {agent_name.title()} processing completed successfully!")
                    else:
                        print(f"❌ {agent_name.title()} processing failed!")
                else:
                    print(f"⚠️  Skipping {agent_name.title()} - no PDFs found")
                    results[agent_name] = False
                    
            except Exception as e:
                print(f"❌ Error processing {agent_name}: {str(e)}")
                results[agent_name] = False
        
        # Final results
        print("\n" + "=" * 50)
        print("📊 FINAL RESULTS:")
        
        successful_agents = []
        failed_agents = []
        
        for agent_name, success in results.items():
            if success:
                successful_agents.append(agent_name)
                print(f"✅ {agent_name.title()}: Ready for queries")
            else:
                failed_agents.append(agent_name)
                print(f"❌ {agent_name.title()}: Processing failed")
        
        print(f"\n🎯 Summary: {len(successful_agents)}/3 agents processed successfully")
        
        if successful_agents:
            print(f"\n🚀 Your APEX RAG Pipeline is ready!")
            print("✅ Vector stores created for:", ", ".join([a.title() for a in successful_agents]))
            print("\n🧪 Test your setup:")
            print("python test_apex_rag.py")
        
        if failed_agents:
            print(f"\n⚠️  Failed agents: {', '.join([a.title() for a in failed_agents])}")
            print("Check the error messages above and ensure PDFs are valid")
        
        return len(successful_agents) > 0
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please install required dependencies:")
        print("pip install sentence-transformers faiss-cpu PyPDF2")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'sentence_transformers',
        'faiss',
        'PyPDF2',
        'pathlib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'faiss':
                import faiss
            elif package == 'sentence_transformers':
                import sentence_transformers
            elif package == 'PyPDF2':
                import PyPDF2
            elif package == 'pathlib':
                import pathlib
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\nInstall with:")
        print("pip install sentence-transformers faiss-cpu PyPDF2")
        return False
    
    return True

if __name__ == "__main__":
    print("🔍 Checking dependencies...")
    
    if not check_dependencies():
        exit(1)
    
    print("✅ All dependencies found!")
    
    success = process_apex_knowledge_base()
    
    if success:
        print("\n🎉 APEX RAG Pipeline creation completed!")
    else:
        print("\n💥 APEX RAG Pipeline creation failed!")
        exit(1)