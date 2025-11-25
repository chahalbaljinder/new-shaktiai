# Policy Queries System - Complete Guide

## Overview

The Policy Queries system is a comprehensive AI-powered solution that provides DRDO employees with instant access to policy information, document preparation, and intelligent assistance using the APEX RAG (Retrieval-Augmented Generation) system.

## Features

### 1. **Ask Policy Tab**
- **Smart Category Selection**: Choose from 5 policy categories
  - POSH Act
  - Leave Policies
  - Maternity Benefits
  - Transfer Guidelines
  - General Policies

- **AI-Powered Responses**: Get instant, accurate answers powered by APEX agents
  - **Athena**: Legal & Policy Expert
  - **Asha**: Wellness & Support Counselor
  - **Scribe**: Documentation Specialist

- **Source References**: Every response includes source documents and page numbers for transparency

### 2. **Query History Tab**
- View all your past policy questions
- See response times and status
- Quick access to previous answers
- Organized by date and category

### 3. **Applications Tab**
- **AI-Assisted Application Generation**
  - Maternity Leave Applications
  - Child Care Leave (CCL)
  - Transfer Requests
  - Grievance Applications
  - Policy Clarification Requests

- **Features**:
  - Auto-generate properly formatted applications
  - Download as text files
  - Professional government correspondence format
  - Include all necessary details

### 4. **Resources Tab**
- Quick access to policy documents
- Categorized by type (Legal, HR, Benefits, Administrative)
- Direct links to official documents

## Technical Architecture

### Frontend Components

#### PolicyQueries.tsx
```typescript
Location: shakti-ai-nextjs/components/PolicyQueries.tsx
Features:
- 4 interactive tabs
- Real-time API integration
- Beautiful gradient UI
- Responsive design
- Dark mode support
```

#### Key Functionality
- Query submission with category selection
- Application generation with AI
- Query history tracking
- Source citation display

### Backend API Endpoints

#### 1. Policy Queries Endpoint
```python
GET/POST /api/policy-queries
```

**POST Request:**
```json
{
  "query": "What are the maternity leave entitlements?",
  "category": "maternity"
}
```

**Response:**
```json
{
  "message": "Query processed successfully",
  "query": {
    "id": "string",
    "query": "string",
    "category": "string",
    "response": "string",
    "status": "completed",
    "response_time": "2.45s",
    "sources": [
      {
        "document": "string",
        "page": "string",
        "relevance": 0.95
      }
    ]
  }
}
```

**GET Request:**
Returns user's query history (last 50 queries)

#### 2. Application Generation Endpoint
```python
POST /api/generate-application
```

**Request:**
```json
{
  "applicationType": "maternity-leave",
  "details": "Need 6 months maternity leave starting from Jan 2026..."
}
```

**Response:**
```json
{
  "message": "Application generated successfully",
  "application": "Generated application text..."
}
```

### APEX RAG System

#### core/apex_crew.py

**Specialized Agents:**

1. **Athena** (Legal & Policy Expert)
   - Expertise: DRDO policies, POSH Act, legal rights
   - Knowledge Base: Government regulations, policy documents
   - Use Cases: Policy queries, legal rights, compliance

2. **Asha** (Wellness & Support Counselor)
   - Expertise: Mental wellness, work-life balance
   - Use Cases: Stress management, career counseling

3. **Scribe** (Documentation Specialist)
   - Expertise: Application preparation, official correspondence
   - Use Cases: Letter writing, form filling, documentation

**Knowledge Base Integration:**
- Vector store with semantic search
- PDF document processing
- Page-level citation tracking
- Similarity-based retrieval

### Database Schema

#### policy_queries Table
```sql
CREATE TABLE policy_queries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    query TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    response TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    response_time VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_policy_queries_user_id ON policy_queries(user_id);
CREATE INDEX idx_policy_queries_created_at ON policy_queries(created_at DESC);
CREATE INDEX idx_policy_queries_category ON policy_queries(category);
```

## Setup Instructions

### 1. Database Setup
```bash
cd "C:\Users\balli\Desktop\new shaktiai"
.\.venv\Scripts\python.exe database\create_policy_queries_table.py
```

### 2. Start Backend
```bash
.\.venv\Scripts\python.exe apex_backend.py
```

### 3. Start Frontend
```bash
cd shakti-ai-nextjs
npm run dev
```

## Usage Guide

### For Employees

#### Asking a Policy Question
1. Navigate to "Policy Queries" from sidebar
2. Select relevant category (e.g., "Leave Policies")
3. Type your question in the text area
4. Click "Submit Query"
5. Wait for APEX AI to process (usually 2-5 seconds)
6. Review the response with source citations

#### Generating an Application
1. Go to "Applications" tab
2. Select application type from dropdown
3. Provide details in the text area (dates, reasons, etc.)
4. Click "Generate with AI"
5. Review the generated application
6. Click "Download" to save as text file

#### Viewing History
1. Click "Query History" tab
2. Browse past questions and answers
3. Click on any query to see full details

### For Administrators

#### Monitoring Usage
- Track query counts in Dashboard
- View response times
- Monitor popular categories

## Knowledge Base Management

### Adding Policy Documents

1. Place PDF files in appropriate folders:
```
knowledge_base/raw_pdfs/
├── athena/      # Policy and legal documents
├── asha/        # Wellness resources
└── scribe/      # Documentation templates
```

2. Process the knowledge base:
```bash
python create_apex_rag.py
```

3. Test the system:
```bash
python test_apex_rag.py
```

### Supported Document Types
- Government circulars
- Policy manuals
- Act documents
- Guidelines and regulations
- Leave rules
- Transfer policies

## Best Practices

### For Employees
1. **Be Specific**: Ask clear, specific questions
2. **Choose Right Category**: Select the most relevant category
3. **Check Sources**: Review cited documents for official references
4. **Save Applications**: Download generated applications for your records

### For HR/Admin
1. **Keep Documents Updated**: Regularly update policy documents
2. **Monitor Common Queries**: Track frequently asked questions
3. **Improve Knowledge Base**: Add new documents as policies change

## Troubleshooting

### Common Issues

#### "APEX system not available"
- Check if backend is running
- Verify knowledge base is loaded
- Run: `python test_apex_rag.py`

#### Slow Response Times
- Check backend logs
- Verify database connection
- Ensure knowledge base is properly indexed

#### Application Generation Fails
- Provide more details in the input
- Check backend logs for errors
- Verify LLM configuration

## Security & Privacy

- All queries are logged with user_id for accountability
- Responses are stored for audit purposes
- Anonymous queries are not supported (for compliance)
- Source citations ensure transparency

## API Integration

### Example: Submit Query
```typescript
const response = await fetch('http://localhost:8000/api/policy-queries', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    query: 'What is the POSH Act?',
    category: 'posh'
  })
});

const data = await response.json();
console.log(data.query.response);
```

### Example: Generate Application
```typescript
const response = await fetch('http://localhost:8000/api/generate-application', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    applicationType: 'maternity-leave',
    details: 'Expected delivery date: March 2026, Duration: 6 months'
  })
});

const data = await response.json();
console.log(data.application);
```

## Future Enhancements

### Planned Features
1. **Multi-language Support**: Hindi, regional languages
2. **Voice Queries**: Ask questions via voice
3. **Document Upload**: Upload supporting documents
4. **Advanced Search**: Filter by date, category, status
5. **Email Integration**: Send applications directly
6. **Batch Processing**: Generate multiple applications
7. **Template Library**: Pre-built application templates

## Support

For technical support or questions:
- Check backend logs: `apex_backend.py`
- Review frontend console
- Test API endpoints manually
- Contact system administrator

## Changelog

### Version 1.0.0 (November 2025)
- Initial release
- 4 main tabs (Ask, History, Applications, Resources)
- APEX RAG integration
- 3 specialized agents
- Source citation system
- Application generation
- Query history tracking

---

**Note**: This system is designed specifically for DRDO employees and follows government compliance standards for data handling and privacy.
