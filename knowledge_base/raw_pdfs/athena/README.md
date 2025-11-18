# Athena - Policy & Procedure Guide

## Description
Government policies, legal procedures, and rights guidance for women scientists

## Required PDF Documents
Please add relevant PDF documents to this directory for Athena to learn from:

- Government HR circulars and policies
- POSH Act documentation and guidelines
- Maternity Leave and Child Care Leave policies
- Transfer and posting guidelines
- Legal rights documents for women in government
- Department-specific policies (DRDO, ISRO, CSIR)
- Grievance redressal procedures
- Anti-harassment policies and protocols

## Instructions
1. Add PDF files directly to this directory
2. Run the knowledge base processing script to update Athena's knowledge
3. PDFs should be relevant to Government policies, legal procedures, and rights guidance for women scientists

## File Naming Convention
- Use descriptive names for PDFs
- Include version numbers if applicable
- Example: `POSH_Act_Guidelines_2023.pdf`, `Maternity_Leave_Policy_DRDO.pdf`

## Processing
After adding PDFs, run:
```python
from knowledge_base.kb_manager import KnowledgeBaseManager
kb_manager = KnowledgeBaseManager()
kb_manager.process_agent_pdfs('athena', force_rebuild=True)
```

Last updated: Athena knowledge base setup
