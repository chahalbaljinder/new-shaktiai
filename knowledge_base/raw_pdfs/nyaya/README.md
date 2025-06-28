# Nyaya - Legal Rights Knowledge Base

This directory should contain PDF documents related to women's legal rights in India, including:

- Indian Constitution articles on women's rights
- Family law documents
- Domestic violence protection laws
- Workplace harassment guidelines
- Property rights information
- Divorce and custody laws
- Women's safety legislation
- Legal aid resources

## How to Add PDFs

1. Place your PDF files directly in this directory
2. Run the knowledge base setup script: `python scripts/setup_knowledge_base.py`
3. Choose option 2 to process all agents or option 3 to process only Nyaya

## Supported Formats

- PDF files (.pdf extension)
- Text-based PDFs (not scanned images)
- Documents in English

The system will automatically extract text, chunk it appropriately, and create searchable embeddings for the AI agent to use.
