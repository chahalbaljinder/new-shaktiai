# Vaanya - Feminist Health Education Knowledge Base

This directory should contain PDF documents related to feminist health education, including:

- Menopause and perimenopause guides
- Hormonal health information
- Women's empowerment resources
- Body autonomy education
- Health advocacy materials
- Aging and women's health
- Gender-based health disparities
- Feminist health literature

## How to Add PDFs

1. Place your PDF files directly in this directory
2. Run the knowledge base setup script: `python scripts/setup_knowledge_base.py`
3. Choose option 2 to process all agents or option 3 to process only Vaanya

## Supported Formats

- PDF files (.pdf extension)
- Text-based PDFs (not scanned images)
- Documents in English

The system will automatically extract text, chunk it appropriately, and create searchable embeddings for the AI agent to use.
