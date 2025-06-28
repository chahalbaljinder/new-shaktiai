# SHAKTI-AI: Reproductive & Legal Health AI Agents

SHAKTI-AI is a suite of AI-powered agents designed to support Indian women and families with reproductive health, legal rights, mental wellness, and more. Each agent is tailored for a specific domain, providing empathetic, evidence-based, and culturally relevant guidance with **enhanced PDF reference citations**.

## ✨ New Features
- **🎯 Enhanced PDF References**: Exact page citations with confidence scores
- **📚 Advanced Knowledge Base**: PyMuPDF-powered PDF processing with metadata
- **🔍 Smart Source Citations**: Detailed extracts and content previews
- **📊 Confidence Indicators**: High/Medium/Low reliability scoring
- **📄 Page-Level Tracking**: Precise page number references for all sources

## 🤖 AI Agents
- **Maaya**: Maternal health nurse for pregnancy, childbirth, and baby care
- **Gynika**: Reproductive health advisor for periods, puberty, and contraception
- **Meher**: Emotional support counselor for trauma, anxiety, and abuse
- **Nyaya**: Legal-ethical guide for Indian laws on consent, abortion, and family rights
- **Vaanya**: Feminist educator for menopause and hormonal health

## 📚 Enhanced Knowledge Base System

Each agent utilizes a sophisticated PDF-based knowledge base that provides:

### Advanced Reference Features
- **Exact Page Citations**: "Page 12" or "Pages 15-17" references
- **Document Metadata**: Full titles, authors, and creation dates
- **Confidence Scoring**: 🎯 High (>80%), 📊 Medium (50-80%), 📋 Low (<50%)
- **Content Previews**: 200-character source previews
- **Detailed Extracts**: 500-character key extracts for high-relevance sources
- **Source Verification**: Direct document and filename references

### Knowledge Processing Pipeline
1. **Enhanced PDF Extraction**: PyMuPDF for better text and metadata extraction
2. **Smart Chunking**: Context-preserving text segmentation
3. **Page Tracking**: Maintain page boundaries throughout processing
4. **Vector Embeddings**: Sentence transformer-based similarity matching
5. **Citation Generation**: Structured reference formatting with confidence scores

### Setting Up Knowledge Bases

1. **Add PDF Documents**: Place relevant PDF files in agent directories:
   ```
   knowledge_base/raw_pdfs/maaya/     # Maternal health documents
   knowledge_base/raw_pdfs/gynika/    # Reproductive health documents  
   knowledge_base/raw_pdfs/meher/     # Mental health documents
   knowledge_base/raw_pdfs/nyaya/     # Legal documents
   knowledge_base/raw_pdfs/vaanya/    # Feminist health documents
   ```

2. **Process Documents**: Run the interactive setup script:
   ```bash
   python scripts/setup_knowledge_base.py
   ```

3. **Verify Processing**: Check that vector stores are created in `knowledge_base/processed/`

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root (or copy from `.env.example`) with your Google API key:

```
GOOGLE_API_KEY=your_google_api_key_here
```

You need to obtain a Google API key with access to the Gemini 2.0 Flash model.

### 3. Set Up Knowledge Base (Optional)

If you want to enhance the agents with PDF knowledge bases:

```bash
# Add your PDF documents to the appropriate directories
# Then run the setup script
python scripts/setup_knowledge_base.py
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## Usage

1. Enter your question or concern in the text area
2. Optionally select which expert agents you want to consult
3. Click "Get Guidance" to receive a response
4. If knowledge bases are configured, responses will include relevant citations

## Project Structure

- `app.py`: Streamlit web application
- `llm.py`: LLM implementation using Google's Gemini 2.0 Flash
- `agents.py`: Agent definitions and configurations
- `crew.py`: Agent orchestration with knowledge base integration
- `knowledge_base/`: PDF processing and vector storage system
  - `document_processor.py`: PDF text extraction and chunking
  - `vector_store.py`: FAISS-based vector storage and search
  - `retriever.py`: Knowledge retrieval and context formatting
  - `kb_manager.py`: Knowledge base management and setup
- `scripts/setup_knowledge_base.py`: Interactive setup script
- `.env`: Environment variables and configuration
- `requirements.txt`: Project dependencies

## Knowledge Base Features

- **Multi-format Support**: Handles various PDF types and layouts
- **Intelligent Chunking**: Semantic text splitting with overlap
- **Vector Search**: Fast similarity search using FAISS
- **Source Attribution**: Automatic citation of source documents
- **Easy Management**: Interactive scripts for setup and maintenance
- **Scalable**: Add new documents and rebuild indexes easily

## Disclaimer

SHAKTI-AI provides general information only and is not a substitute for professional medical, legal, or mental health advice. Always consult qualified professionals for specific concerns.
