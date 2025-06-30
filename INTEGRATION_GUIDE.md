# SHAKTI-AI Integrated Application Setup

This document provides instructions for running the fully integrated SHAKTI-AI application with both frontend and backend services.

## Quick Start

### Prerequisites
1. Node.js (v18 or higher)
2. Python (v3.10 or higher)
3. PostgreSQL (optional - for wishes vault database)

### Installation

1. **Frontend Setup (Next.js)**
   ```bash
   cd shakti-ai-nextjs
   npm install
   ```

2. **Backend Setup (Python)**
   ```bash
   # In the root directory
   pip install -r requirements.txt
   pip install fastapi uvicorn python-multipart
   ```

3. **Environment Configuration**
   - Copy `.env.local.example` to `.env.local` in the `shakti-ai-nextjs` directory
   - Update database credentials if using PostgreSQL

### Running the Application

1. **Start the Python Backend Service**
   ```bash
   # In the root directory
   python -m uvicorn backend_service:app --host 0.0.0.0 --port 8000 --reload
   ```
   This starts the FastAPI service on http://localhost:8000

2. **Start the Next.js Frontend**
   ```bash
   cd shakti-ai-nextjs
   npm run dev
   ```
   This starts the frontend on http://localhost:3001

3. **Access the Application**
   Open your browser and go to: http://localhost:3001

## Features Available

### ✅ Fully Integrated Features

1. **AI Agents & Knowledge Base**
   - Real AI agent conversations using the SHAKTI-AI system
   - Knowledge base retrieval with citations
   - Support for all 5 agents: Maaya, Gynika, Meher, Nyaya, Vaanya

2. **Wishes Vault**
   - Create, edit, and delete wishes
   - Database persistence (PostgreSQL)
   - Share wishes via email or WhatsApp
   - Categories and priority levels
   - Search and filtering

3. **Voice Interface**
   - Real speech-to-text using Web API and backend processing
   - Text-to-speech using Web Speech API
   - Voice control for hands-free interaction

4. **Modern UI/UX**
   - Responsive design that works on all devices
   - Smooth animations and transitions
   - Toast notifications for user feedback
   - Modern gradient backgrounds and styling

### Backend Integration

The application uses a FastAPI backend service (`backend_service.py`) that wraps the existing Python functionality:

- **AI Agents**: Integrates with `core/crew.py` for real AI responses
- **Voice Processing**: Uses `core/get_voice_input.py` for speech recognition
- **Database**: Connects to `database/wishes_vault_db.py` for wishes storage
- **Knowledge Base**: Utilizes the existing RAG system for contextual responses

### API Endpoints

The backend service provides these API endpoints:

- `GET /api/agents/list` - Get available AI agents
- `POST /api/agents/chat` - Chat with a specific agent
- `GET /api/wishes/list` - Get all wishes
- `POST /api/wishes/create` - Create a new wish
- `PUT /api/wishes/{id}` - Update a wish
- `DELETE /api/wishes/{id}` - Delete a wish
- `POST /api/wishes/share` - Share a wish via email/WhatsApp
- `POST /api/voice/speech-to-text` - Convert speech to text
- `POST /api/voice/text-to-speech` - Convert text to speech

### Frontend Architecture

The Next.js frontend uses:

- **React Query** for server state management
- **Zustand** for client state management
- **Framer Motion** for animations
- **Tailwind CSS** for styling
- **TypeScript** for type safety
- **Sonner** for toast notifications

## Troubleshooting

### Common Issues

1. **Backend Service Won't Start**
   - Ensure all Python dependencies are installed
   - Check that ports 8000 is available
   - Verify environment variables are set correctly

2. **Frontend Can't Connect to Backend**
   - Ensure backend service is running on port 8000
   - Check CORS settings in `backend_service.py`
   - Verify `NEXT_PUBLIC_API_URL` in `.env.local`

3. **Voice Features Not Working**
   - Ensure microphone permissions are granted
   - Check browser compatibility (Chrome/Edge recommended)
   - Verify audio device is working

4. **Database Connection Issues**
   - Install and configure PostgreSQL
   - Update database credentials in environment variables
   - Run database setup scripts if needed

### Development Tips

1. **Hot Reload**: Both services support hot reload for development
2. **Debugging**: Check browser console and terminal outputs for errors
3. **API Testing**: Backend API documentation available at http://localhost:8000/docs
4. **Database Management**: Use PostgreSQL admin tools or pgAdmin for database management

## Production Deployment

For production deployment:

1. Build the Next.js application: `npm run build`
2. Use a production WSGI server for the Python backend
3. Configure environment variables for production
4. Set up a reverse proxy (nginx) to serve both services
5. Configure SSL certificates for HTTPS

## Support

If you encounter issues:

1. Check the console logs for both frontend and backend
2. Verify all dependencies are installed correctly
3. Ensure environment variables are configured properly
4. Test individual components separately to isolate issues
