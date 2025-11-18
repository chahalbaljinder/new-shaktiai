# Scribe - Documentation & Workflow Expert

## Description
Document generation, form filling, and process automation

## Required PDF Documents
Please add relevant PDF documents to this directory for Scribe to learn from:

- Official form templates and examples
- Leave application formats and procedures
- Transfer request documentation
- Grievance filing procedures and forms
- Administrative process flowcharts
- Document submission checklists
- Workflow automation guides
- Government correspondence templates

## Instructions
1. Add PDF files directly to this directory
2. Run the knowledge base processing script to update Scribe's knowledge
3. PDFs should be relevant to Document generation, form filling, and process automation

## File Naming Convention
- Use descriptive names for PDFs
- Include version numbers if applicable
- Example: `POSH_Act_Guidelines_2023.pdf`, `Maternity_Leave_Policy_DRDO.pdf`

## Processing
After adding PDFs, run:
```python
from knowledge_base.kb_manager import KnowledgeBaseManager
kb_manager = KnowledgeBaseManager()
kb_manager.process_agent_pdfs('scribe', force_rebuild=True)
```

Last updated: Scribe knowledge base setup
