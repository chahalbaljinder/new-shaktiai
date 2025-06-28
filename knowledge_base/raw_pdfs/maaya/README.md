# Maaya - Maternal Health Knowledge Base

This directory should contain PDF documents related to maternal health, including:

- Pregnancy guides and handbooks
- Prenatal care guidelines
- Childbirth information
- Postpartum care documents
- Breastfeeding guides
- Infant care manuals
- Maternal nutrition guidelines
- WHO maternal health recommendations

## How to Add PDFs

1. Place your PDF files directly in this directory
2. Run the knowledge base setup script: `python scripts/setup_knowledge_base.py`
3. Choose option 2 to process all agents or option 3 to process only Maaya

## Supported Formats

- PDF files (.pdf extension)
- Text-based PDFs (not scanned images)
- Documents in English

The system will automatically extract text, chunk it appropriately, and create searchable embeddings for the AI agent to use.
