"""
Document processing module for extracting and chunking text from PDFs.
Enhanced version with better metadata extraction and page tracking.
"""

import os
import re
import json
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import PyPDF2
import pdfplumber
from datetime import datetime

class DocumentProcessor:
    """Enhanced PDF text extraction and chunking with metadata tracking."""
    
    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 100):
        """
        Initialize the document processor.
        
        Args:
            chunk_size: Maximum characters per chunk
            chunk_overlap: Characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.processed_docs = []
        
    def extract_text_with_pages(self, pdf_path: str) -> List[Dict[str, any]]:
        """
        Extract text from PDF with page-by-page metadata.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries with page text and metadata
        """
        pages_data = []
        
        try:
            # Try PyMuPDF first (better metadata support)
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_text = page.get_text()
                
                if page_text.strip():  # Only include pages with content
                    pages_data.append({
                        'page_number': page_num + 1,
                        'text': self.clean_text(page_text),
                        'char_count': len(page_text),
                        'extraction_method': 'PyMuPDF'
                    })
            
            doc.close()
            
        except Exception as e:
            print(f"PyMuPDF failed for {pdf_path}, trying pdfplumber: {e}")
            
            # Fallback to pdfplumber
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        page_text = page.extract_text()
                        if page_text and page_text.strip():
                            pages_data.append({
                                'page_number': page_num + 1,
                                'text': self.clean_text(page_text),
                                'char_count': len(page_text),
                                'extraction_method': 'pdfplumber'
                            })
            except Exception as e2:
                print(f"pdfplumber also failed for {pdf_path}: {e2}")
                
        return pages_data
    
    def extract_document_metadata(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract metadata from PDF document.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with document metadata
        """
        metadata = {
            'filename': Path(pdf_path).name,
            'filepath': pdf_path,
            'title': None,
            'author': None,
            'subject': None,
            'creator': None,
            'creation_date': None,
            'modification_date': None,
            'page_count': 0,
            'file_size': 0
        }
        
        try:
            # Get file stats
            file_stat = Path(pdf_path).stat()
            metadata['file_size'] = file_stat.st_size
            metadata['modification_date'] = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
            
            # Try to extract PDF metadata
            doc = fitz.open(pdf_path)
            pdf_metadata = doc.metadata
            
            metadata.update({
                'title': pdf_metadata.get('title', '').strip() or Path(pdf_path).stem,
                'author': pdf_metadata.get('author', '').strip(),
                'subject': pdf_metadata.get('subject', '').strip(),
                'creator': pdf_metadata.get('creator', '').strip(),
                'creation_date': pdf_metadata.get('creationDate', ''),
                'page_count': len(doc)
            })
            
            doc.close()
            
        except Exception as e:
            print(f"Error extracting metadata from {pdf_path}: {e}")
            # Fallback: at least get basic info
            metadata['title'] = Path(pdf_path).stem
            
        return metadata
        
    def extract_text_from_pdf(self, pdf_path: str, method: str = "pdfplumber") -> str:
        """
        Legacy method for backward compatibility.
        Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            method: Extraction method ("pdfplumber" or "pypdf2")
            
        Returns:
            Extracted text as string
        """
        text = ""
        
        try:
            if method == "pdfplumber":
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            else:  # pypdf2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                        
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            
        return text
        
    def extract_text_from_pdf(self, pdf_path: str, method: str = "pdfplumber") -> str:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            method: Extraction method ("pdfplumber" or "pypdf2")
            
        Returns:
            Extracted text as string
        """
        text = ""
        
        try:
            if method == "pdfplumber":
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            else:  # pypdf2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                        
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            
        return text
    
    def clean_text(self, text: str) -> str:
        """
        Enhanced text cleaning with better preservation of structure.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
            
        # Normalize whitespace but preserve paragraph breaks
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple newlines to double newline
        
        # Remove common PDF artifacts
        text = re.sub(r'(?i)page \d+ of \d+', '', text)
        text = re.sub(r'(?i)©.*?\d{4}[^\n]*', '', text)
        text = re.sub(r'(?i)all rights reserved[^\n]*', '', text)
        
        # Remove URLs but preserve structure
        text = re.sub(r'http[s]?://\S+', '[URL]', text)
        
        # Remove isolated page numbers (digits alone on a line)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        # Clean up excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def create_smart_chunks(self, pages_data: List[Dict], doc_metadata: Dict) -> List[Dict[str, any]]:
        """
        Create intelligent chunks with enhanced metadata tracking.
        
        Args:
            pages_data: List of page data with text and metadata
            doc_metadata: Document-level metadata
            
        Returns:
            List of chunk dictionaries with detailed metadata
        """
        chunks = []
        chunk_id = 0
        
        # Combine all text with page markers
        full_text = ""
        page_boundaries = []
        
        for page_data in pages_data:
            page_start = len(full_text)
            page_text = page_data['text']
            full_text += page_text + "\n\n"
            page_boundaries.append({
                'page_number': page_data['page_number'],
                'start_pos': page_start,
                'end_pos': len(full_text) - 2,  # -2 for the added \n\n
                'char_count': len(page_text)
            })
        
        # Create overlapping chunks
        start = 0
        while start < len(full_text):
            end = min(start + self.chunk_size, len(full_text))
            
            # Try to end at sentence boundary
            if end < len(full_text):
                # Look for sentence endings within reasonable distance
                sentence_end = full_text.rfind('.', start, end + 100)
                if sentence_end > start + self.chunk_size // 2:
                    end = sentence_end + 1
                else:
                    # Look for paragraph breaks
                    para_end = full_text.rfind('\n\n', start, end + 50)
                    if para_end > start + self.chunk_size // 2:
                        end = para_end + 2
            
            chunk_text = full_text[start:end].strip()
            
            if len(chunk_text) < 50:  # Skip very small chunks
                start = end
                continue
            
            # Determine which pages this chunk spans
            chunk_pages = []
            for page_info in page_boundaries:
                # Check if chunk overlaps with this page
                chunk_start_in_doc = start
                chunk_end_in_doc = end
                
                if (chunk_start_in_doc < page_info['end_pos'] and 
                    chunk_end_in_doc > page_info['start_pos']):
                    
                    # Calculate overlap percentage
                    overlap_start = max(chunk_start_in_doc, page_info['start_pos'])
                    overlap_end = min(chunk_end_in_doc, page_info['end_pos'])
                    overlap_length = overlap_end - overlap_start
                    
                    if overlap_length > 0:
                        chunk_pages.append({
                            'page_number': page_info['page_number'],
                            'overlap_chars': overlap_length,
                            'overlap_percentage': (overlap_length / len(chunk_text)) * 100
                        })
            
            # Create chunk with enhanced metadata
            chunk = {
                'id': f"chunk_{chunk_id}",
                'text': chunk_text,
                'doc_title': doc_metadata['title'],
                'doc_filename': doc_metadata['filename'],
                'doc_filepath': doc_metadata['filepath'],
                'pages': chunk_pages,
                'primary_page': chunk_pages[0]['page_number'] if chunk_pages else None,
                'char_count': len(chunk_text),
                'word_count': len(chunk_text.split()),
                'start_pos': start,
                'end_pos': end,
                'chunk_index': chunk_id,
                'total_doc_pages': doc_metadata['page_count'],
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            chunks.append(chunk)
            chunk_id += 1
            
            # Move start position with overlap
            start = max(end - self.chunk_overlap, start + 1)
        
        return chunks
    
    def chunk_text(self, text: str, doc_title: str = "") -> List[Dict[str, any]]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            doc_title: Title of the document
            
        Returns:
            List of chunk dictionaries with metadata
        """
        chunks = []
        sentences = text.split('. ')
        current_chunk = ""
        chunk_id = 0
        
        for sentence in sentences:
            # Check if adding this sentence would exceed chunk size
            if len(current_chunk + sentence + '. ') > self.chunk_size and current_chunk:
                # Save current chunk
                chunks.append({
                    'id': chunk_id,
                    'text': current_chunk.strip(),
                    'doc_title': doc_title,
                    'chunk_size': len(current_chunk),
                    'timestamp': datetime.now().isoformat()
                })
                
                # Start new chunk with overlap
                overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else current_chunk
                current_chunk = overlap_text + sentence + '. '
                chunk_id += 1
            else:
                current_chunk += sentence + '. '
        
        # Add final chunk if it has content
        if current_chunk.strip():
            chunks.append({
                'id': chunk_id,
                'text': current_chunk.strip(),
                'doc_title': doc_title,
                'chunk_size': len(current_chunk),
                'timestamp': datetime.now().isoformat()
            })
            
        return chunks
    
    def process_pdf_enhanced(self, pdf_path: str) -> List[Dict[str, any]]:
        """
        Enhanced PDF processing with detailed metadata and page tracking.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of processed chunks with enhanced metadata
        """
        print(f"📄 Processing: {Path(pdf_path).name}")
        
        # Extract document metadata
        doc_metadata = self.extract_document_metadata(pdf_path)
        
        # Extract text with page information
        pages_data = self.extract_text_with_pages(pdf_path)
        
        if not pages_data:
            print(f"⚠️ Warning: No text extracted from {pdf_path}")
            return []
        
        # Create intelligent chunks
        chunks = self.create_smart_chunks(pages_data, doc_metadata)
        
        print(f"✅ Extracted {len(chunks)} chunks from {doc_metadata['title']} ({len(pages_data)} pages)")
        return chunks
    
    def process_pdf(self, pdf_path: str) -> List[Dict[str, any]]:
        """
        Process a single PDF file using enhanced processing.
        """
        return self.process_pdf_enhanced(pdf_path)
    
    def process_directory(self, directory_path: str) -> List[Dict[str, any]]:
        """
        Process all PDF files in a directory.
        
        Args:
            directory_path: Path to directory containing PDFs
            
        Returns:
            List of all processed chunks from all PDFs
        """
        all_chunks = []
        pdf_files = list(Path(directory_path).glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {directory_path}")
            return []
        
        print(f"Found {len(pdf_files)} PDF files in {directory_path}")
        
        for pdf_file in pdf_files:
            chunks = self.process_pdf(str(pdf_file))
            all_chunks.extend(chunks)
        
        return all_chunks
    
    def save_metadata(self, chunks: List[Dict[str, any]], output_path: str):
        """
        Save chunk metadata to JSON file.
        
        Args:
            chunks: List of chunk dictionaries
            output_path: Path to save metadata JSON
        """
        metadata = {
            'total_chunks': len(chunks),
            'processing_timestamp': datetime.now().isoformat(),
            'chunk_size': self.chunk_size,
            'chunk_overlap': self.chunk_overlap,
            'chunks': chunks
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"Saved metadata for {len(chunks)} chunks to {output_path}")


if __name__ == "__main__":
    # Example usage
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    
    # Test with a single PDF
    # chunks = processor.process_pdf("sample.pdf")
    
    # Test with a directory
    # chunks = processor.process_directory("knowledge_base/raw_pdfs/maaya")
    # processor.save_metadata(chunks, "knowledge_base/metadata/maaya_metadata.json")
    
    print("Document processor ready for use!")
