# 📚 APEX Knowledge Base Setup Guide

## Overview
This guide walks you through updating the knowledge base from SHAKTI-AI agents to APEX agents for women scientists in government organizations.

## Current Status ✅
- ✅ Directory structure created for APEX agents
- ✅ Knowledge base manager updated to use `athena`, `asha`, `scribe`
- ✅ Retriever updated for new agent names

## Step-by-Step Process

### **Step 1: Understand Agent Specializations**

#### **Athena - Policy & Procedure Guide** ⚖️
**Purpose:** Navigate government policies, legal procedures, and rights
**PDF Types Needed:**
- Government HR circulars and policies
- POSH Act documentation and guidelines
- Maternity Leave and Child Care Leave policies
- Transfer and posting guidelines
- Legal rights documents for women in government
- Department-specific policies (DRDO, ISRO, CSIR)
- Grievance redressal procedures
- Anti-harassment policies and protocols

#### **Asha - Wellness & Support Companion** 🌸
**Purpose:** Emotional wellness, work-life balance, confidential support
**PDF Types Needed:**
- Work-life balance guides for scientists
- Mental health resources and counseling guides
- Stress management techniques for researchers
- Emotional wellness and self-care resources
- Career development guides for women scientists
- Support group resources and networks
- Mindfulness and meditation guides
- Confidence building and leadership resources

#### **Scribe - Documentation & Workflow Expert** 📋
**Purpose:** Document generation, form filling, process automation
**PDF Types Needed:**
- Official form templates and examples
- Leave application formats and procedures
- Transfer request documentation
- Grievance filing procedures and forms
- Administrative process flowcharts
- Document submission checklists
- Workflow automation guides
- Government correspondence templates

### **Step 2: Gather PDF Documents**

#### **Option A: Search and Download PDFs**
1. **Government websites:**
   - Department of Personnel and Training (DoPT)
   - Ministry of Science and Technology
   - DRDO, ISRO, CSIR official websites
   - National Commission for Women (NCW)

2. **Policy documents to find:**
   - POSH Act implementation guidelines
   - Central Government Health Scheme (CGHS) documents
   - Maternity benefit rules
   - Child care leave guidelines
   - Transfer policy documents

#### **Option B: Use Existing Resources**
- Check if your organization has internal policy documents
- Download from official government portals
- Academic papers on women in science policies

### **Step 3: Organize PDFs in Directories**

Place PDFs in the correct directories:
```
knowledge_base/
└── raw_pdfs/
    ├── athena/          # Policy & legal documents
    ├── asha/            # Wellness & support resources
    └── scribe/          # Forms & procedure documents
```

### **Step 4: Process Knowledge Base**

#### **Method 1: Using Python Script**
```python
from knowledge_base.kb_manager import KnowledgeBaseManager

# Initialize manager
kb_manager = KnowledgeBaseManager()

# Check current status
status = kb_manager.get_status()
for agent, info in status.items():
    print(f"{agent}: {info['pdf_count']} PDFs")

# Process all agents
results = kb_manager.process_all_agents(force_rebuild=True)
```

#### **Method 2: Using Setup Script**
```bash
python setup_apex_knowledge_base.py --process
```

#### **Method 3: Individual Agent Processing**
```python
from knowledge_base.kb_manager import KnowledgeBaseManager

kb_manager = KnowledgeBaseManager()

# Process individual agents
kb_manager.process_agent_pdfs('athena', force_rebuild=True)
kb_manager.process_agent_pdfs('asha', force_rebuild=True) 
kb_manager.process_agent_pdfs('scribe', force_rebuild=True)
```

### **Step 5: Verify Knowledge Base**

#### **Check Processing Results:**
```python
from knowledge_base.retriever import KnowledgeRetriever

retriever = KnowledgeRetriever()
print("Available agents:", retriever.get_available_agents())
print("Knowledge stats:", retriever.get_knowledge_stats())
```

#### **Test Retrieval:**
```python
# Test Athena (policy agent)
results = retriever.retrieve_for_agent('athena', 'POSH Act guidelines')
print(f"Athena results: {len(results)} chunks found")

# Test Asha (wellness agent)  
results = retriever.retrieve_for_agent('asha', 'work life balance')
print(f"Asha results: {len(results)} chunks found")

# Test Scribe (documentation agent)
results = retriever.retrieve_for_agent('scribe', 'leave application form')
print(f"Scribe results: {len(results)} chunks found")
```

### **Step 6: Update Core System Integration**

The following files are already updated to use APEX agents:
- ✅ `core/crew.py` - Uses `ask_apex` with correct agent mapping
- ✅ `backend_service.py` - Endpoints updated for APEX agents
- ✅ `app.py` - UI shows APEX agent selection
- ✅ `knowledge_base/retriever.py` - Agent names updated
- ✅ `knowledge_base/kb_manager.py` - Agent processing updated

### **Step 7: Clean Up Old Data (Optional)**

Remove old SHAKTI-AI agent data:
```python
import shutil
from pathlib import Path

base_path = Path("knowledge_base")
old_agents = ['maaya', 'gynika', 'meher', 'nyaya', 'vaanya']

for agent in old_agents:
    # Remove raw PDFs
    raw_dir = base_path / "raw_pdfs" / agent
    if raw_dir.exists():
        shutil.rmtree(raw_dir)
    
    # Remove processed data  
    processed_dir = base_path / "processed" / f"{agent}_vectorstore"
    if processed_dir.exists():
        shutil.rmtree(processed_dir)
    
    # Remove metadata
    metadata_file = base_path / "metadata" / f"{agent}_metadata.json"
    if metadata_file.exists():
        metadata_file.unlink()
```

## Quick Start Commands

### 1. Check current structure:
```bash
ls knowledge_base/raw_pdfs/
# Should show: athena  asha  scribe
```

### 2. Add PDFs to agent directories:
```bash
# Example: Add POSH Act PDF to Athena
cp "POSH_Act_Guidelines.pdf" knowledge_base/raw_pdfs/athena/
```

### 3. Process knowledge base:
```python
python -c "
from knowledge_base.kb_manager import KnowledgeBaseManager
kb = KnowledgeBaseManager()
results = kb.process_all_agents(force_rebuild=True)
print('Results:', results)
"
```

### 4. Test the system:
```python
python -c "
from core.crew import ask_apex
response = ask_apex('What is the POSH Act?', ['legal-guide'])
print(response[:200] + '...')
"
```

## Troubleshooting

### **Issue: No PDFs found**
- Check that PDFs are in the correct directories
- Ensure PDFs are valid and readable
- Verify file extensions are `.pdf`

### **Issue: Processing fails**
- Check Python dependencies (sentence-transformers, faiss, etc.)
- Ensure sufficient disk space for vector storage
- Check file permissions

### **Issue: No search results**
- Verify knowledge base was processed successfully
- Check that vector stores were created in `knowledge_base/processed/`
- Test with broader search terms

## File Locations

### Raw PDFs:
- `knowledge_base/raw_pdfs/athena/` - Policy documents
- `knowledge_base/raw_pdfs/asha/` - Wellness resources  
- `knowledge_base/raw_pdfs/scribe/` - Forms and procedures

### Processed Data:
- `knowledge_base/processed/athena_vectorstore/` - Athena's vector index
- `knowledge_base/processed/asha_vectorstore/` - Asha's vector index
- `knowledge_base/processed/scribe_vectorstore/` - Scribe's vector index

### Metadata:
- `knowledge_base/metadata/athena_metadata.json` - Athena's processing info
- `knowledge_base/metadata/asha_metadata.json` - Asha's processing info
- `knowledge_base/metadata/scribe_metadata.json` - Scribe's processing info

## Next Steps After Setup

1. **Test the full system:**
   ```bash
   python app.py
   # Try asking questions to different agents
   ```

2. **Add more specialized PDFs as you find them**

3. **Monitor and improve based on user feedback**

4. **Consider adding more specific domain knowledge as needed**

## Success Indicators ✅

- [ ] 3 agent directories created with PDFs
- [ ] Knowledge base processing completes without errors
- [ ] Vector stores created for all 3 agents
- [ ] Search queries return relevant results
- [ ] APEX agents respond with appropriate knowledge
- [ ] Old SHAKTI-AI references cleaned up

---

**🎯 You now have a complete roadmap to update your knowledge base for APEX!**