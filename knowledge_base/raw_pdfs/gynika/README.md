# Gynika - Reproductive Health Knowledge Base

This directory should contain PDF documents related to reproductive health, including:

- Menstrual health guides
- Puberty education materials
- Contraception information
- Fertility awareness documents
- Sexual health resources
- Reproductive anatomy guides
- Gynecological health information
- WHO reproductive health guidelines

## How to Add PDFs

1. Place your PDF files directly in this directory
2. Run the knowledge base setup script: `python scripts/setup_knowledge_base.py`
3. Choose option 2 to process all agents or option 3 to process only Gynika

## Supported Formats

- PDF files (.pdf extension)
- Text-based PDFs (not scanned images)
- Documents in English

The system will automatically extract text, chunk it appropriately, and create searchable embeddings for the AI agent to use.
