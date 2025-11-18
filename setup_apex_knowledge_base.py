"""
APEX Knowledge Base Setup Script
This script helps you set up the knowledge base for APEX agents (Athena, Asha, Scribe).
"""

import os
import shutil
from pathlib import Path
from knowledge_base.kb_manager import KnowledgeBaseManager

def create_apex_directories():
    """Create directory structure for APEX agents."""
    base_path = Path("knowledge_base")
    
    # APEX agent directories
    apex_agents = ['athena', 'asha', 'scribe']
    
    for agent in apex_agents:
        # Raw PDFs directory
        raw_dir = base_path / "raw_pdfs" / agent
        raw_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {raw_dir}")
        
        # Create README file for each agent
        readme_path = raw_dir / "README.md"
        if not readme_path.exists():
            content = get_agent_readme_content(agent)
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📝 Created README: {readme_path}")

def get_agent_readme_content(agent_name: str) -> str:
    """Get README content for each agent."""
    agent_info = {
        'athena': {
            'name': 'Athena - Policy & Procedure Guide',
            'description': 'Government policies, legal procedures, and rights guidance for women scientists',
            'pdf_types': [
                'Government HR circulars and policies',
                'POSH Act documentation and guidelines',
                'Maternity Leave and Child Care Leave policies', 
                'Transfer and posting guidelines',
                'Legal rights documents for women in government',
                'Department-specific policies (DRDO, ISRO, CSIR)',
                'Grievance redressal procedures',
                'Anti-harassment policies and protocols'
            ]
        },
        'asha': {
            'name': 'Asha - Wellness & Support Companion',
            'description': 'Emotional wellness, work-life balance, and confidential support',
            'pdf_types': [
                'Work-life balance guides for scientists',
                'Mental health resources and counseling guides',
                'Stress management techniques for researchers',
                'Emotional wellness and self-care resources',
                'Career development guides for women scientists',
                'Support group resources and networks',
                'Mindfulness and meditation guides',
                'Confidence building and leadership resources'
            ]
        },
        'scribe': {
            'name': 'Scribe - Documentation & Workflow Expert',
            'description': 'Document generation, form filling, and process automation',
            'pdf_types': [
                'Official form templates and examples',
                'Leave application formats and procedures',
                'Transfer request documentation',
                'Grievance filing procedures and forms',
                'Administrative process flowcharts',
                'Document submission checklists',
                'Workflow automation guides',
                'Government correspondence templates'
            ]
        }
    }
    
    info = agent_info.get(agent_name, {})
    
    return f"""# {info.get('name', agent_name.title())}

## Description
{info.get('description', 'APEX AI agent')}

## Required PDF Documents
Please add relevant PDF documents to this directory for {agent_name.title()} to learn from:

{chr(10).join(f"- {pdf_type}" for pdf_type in info.get('pdf_types', []))}

## Instructions
1. Add PDF files directly to this directory
2. Run the knowledge base processing script to update {agent_name.title()}'s knowledge
3. PDFs should be relevant to {info.get('description', 'the agent\'s domain')}

## File Naming Convention
- Use descriptive names for PDFs
- Include version numbers if applicable
- Example: `POSH_Act_Guidelines_2023.pdf`, `Maternity_Leave_Policy_DRDO.pdf`

## Processing
After adding PDFs, run:
```python
from knowledge_base.kb_manager import KnowledgeBaseManager
kb_manager = KnowledgeBaseManager()
kb_manager.process_agent_pdfs('{agent_name}', force_rebuild=True)
```

Last updated: {agent_name.title()} knowledge base setup
"""

def cleanup_old_agents():
    """Clean up old SHAKTI-AI agent directories (optional)."""
    base_path = Path("knowledge_base")
    old_agents = ['maaya', 'gynika', 'meher', 'nyaya', 'vaanya']
    
    print("\n🧹 Cleaning up old SHAKTI-AI agent data...")
    
    for agent in old_agents:
        # Raw PDFs
        raw_dir = base_path / "raw_pdfs" / agent
        if raw_dir.exists():
            print(f"Found old directory: {raw_dir}")
            response = input(f"Delete {agent} raw PDFs directory? (y/N): ")
            if response.lower() == 'y':
                shutil.rmtree(raw_dir)
                print(f"🗑️ Deleted: {raw_dir}")
        
        # Processed data
        processed_dir = base_path / "processed" / f"{agent}_vectorstore"
        if processed_dir.exists():
            print(f"Found old vectorstore: {processed_dir}")
            shutil.rmtree(processed_dir)
            print(f"🗑️ Deleted: {processed_dir}")
        
        # Metadata
        metadata_file = base_path / "metadata" / f"{agent}_metadata.json"
        if metadata_file.exists():
            metadata_file.unlink()
            print(f"🗑️ Deleted: {metadata_file}")

def setup_apex_knowledge_base():
    """Main setup function for APEX knowledge base."""
    print("🚀 Setting up APEX Knowledge Base")
    print("=" * 50)
    
    # Create APEX directories
    create_apex_directories()
    
    # Ask about cleanup
    print("\n" + "=" * 50)
    cleanup_response = input("Clean up old SHAKTI-AI agent data? (y/N): ")
    if cleanup_response.lower() == 'y':
        cleanup_old_agents()
    
    # Show next steps
    print("\n" + "=" * 50)
    print("🎯 NEXT STEPS:")
    print("1. Add PDF documents to the agent directories:")
    print("   - knowledge_base/raw_pdfs/athena/ (Government policies, POSH Act, legal documents)")
    print("   - knowledge_base/raw_pdfs/asha/ (Wellness guides, mental health resources)")
    print("   - knowledge_base/raw_pdfs/scribe/ (Form templates, procedure documents)")
    print("\n2. Process the knowledge base:")
    print("   python setup_apex_knowledge_base.py --process")
    print("\n3. Or use the Python API:")
    print("   from knowledge_base.kb_manager import KnowledgeBaseManager")
    print("   kb_manager = KnowledgeBaseManager()")
    print("   kb_manager.process_all_agents(force_rebuild=True)")
    
    print("\n✅ APEX Knowledge Base structure is ready!")

def process_apex_knowledge():
    """Process all APEX agent knowledge bases."""
    print("🔄 Processing APEX Knowledge Bases...")
    print("=" * 50)
    
    kb_manager = KnowledgeBaseManager()
    
    # Check what PDFs are available
    print("📋 Checking available PDFs:")
    status = kb_manager.get_status()
    
    for agent_name in ['athena', 'asha', 'scribe']:
        if agent_name in status:
            pdf_count = status[agent_name]['pdf_count']
            print(f"  {agent_name}: {pdf_count} PDFs")
            if pdf_count == 0:
                print(f"    ⚠️ No PDFs found for {agent_name}. Add PDFs to knowledge_base/raw_pdfs/{agent_name}/")
    
    print("\n🚀 Processing knowledge bases...")
    results = kb_manager.process_all_agents(force_rebuild=True)
    
    print("\n" + "=" * 50)
    print("📊 PROCESSING RESULTS:")
    for agent, success in results.items():
        status_emoji = "✅" if success else "❌"
        print(f"  {status_emoji} {agent}")
    
    successful = sum(1 for success in results.values() if success)
    print(f"\n🎯 Complete: {successful}/3 APEX agents ready")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--process':
        process_apex_knowledge()
    else:
        setup_apex_knowledge_base()