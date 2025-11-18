# Asha - Wellness & Support Companion

## Description
Emotional wellness, work-life balance, and confidential support

## Required PDF Documents
Please add relevant PDF documents to this directory for Asha to learn from:

- Work-life balance guides for scientists
- Mental health resources and counseling guides
- Stress management techniques for researchers
- Emotional wellness and self-care resources
- Career development guides for women scientists
- Support group resources and networks
- Mindfulness and meditation guides
- Confidence building and leadership resources

## Instructions
1. Add PDF files directly to this directory
2. Run the knowledge base processing script to update Asha's knowledge
3. PDFs should be relevant to Emotional wellness, work-life balance, and confidential support

## File Naming Convention
- Use descriptive names for PDFs
- Include version numbers if applicable
- Example: `POSH_Act_Guidelines_2023.pdf`, `Maternity_Leave_Policy_DRDO.pdf`

## Processing
After adding PDFs, run:
```python
from knowledge_base.kb_manager import KnowledgeBaseManager
kb_manager = KnowledgeBaseManager()
kb_manager.process_agent_pdfs('asha', force_rebuild=True)
```

Last updated: Asha knowledge base setup
