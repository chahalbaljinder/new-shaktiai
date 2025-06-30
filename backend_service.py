"""
FastAPI Backend Service for SHAKTI-AI
This service acts as a bridge between the Next.js frontend and the existing Python backend.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import sys
import os
import tempfile
from datetime import datetime
import io
import logging
import smtplib
import urllib.parse
import webbrowser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to Python path to import from core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.email_service import email_service
    logger.info("Successfully imported email service")
except ImportError as e:
    logger.error(f"Failed to import email service: {e}")
    email_service = None

try:
    from core.crew import ask_shakti_ai
    logger.info("Successfully imported ask_shakti_ai")
except ImportError as e:
    logger.error(f"Failed to import ask_shakti_ai: {e}")
    ask_shakti_ai = None

try:
    from core.get_voice_input import get_voice_input
    logger.info("Successfully imported voice input functionality")
except ImportError as e:
    logger.error(f"Failed to import voice input: {e}")
    get_voice_input = None

try:
    from database.db_config import WishesDatabase
    logger.info("Successfully imported WishesDatabase")
except ImportError as e:
    logger.error(f"Failed to import WishesDatabase: {e}")
    WishesDatabase = None

try:
    import speech_recognition as sr
    logger.info("Successfully imported speech_recognition")
except ImportError as e:
    logger.error(f"Failed to import speech_recognition: {e}")
    sr = None

app = FastAPI(title="SHAKTI-AI Backend Service", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    agent_type: str

class ChatResponse(BaseModel):
    response: str
    agent_name: str
    citations: Optional[List[Dict[str, Any]]] = None

class WishRequest(BaseModel):
    title: str
    content: str
    category: Optional[str] = "personal"
    priority: Optional[str] = "medium"
    reminder_date: Optional[str] = None

class WishUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    reminder_date: Optional[str] = None

class ShareWishRequest(BaseModel):
    wish_id: int
    method: str  # "email" or "whatsapp"
    recipient: str
    sender_name: Optional[str] = "SHAKTI-AI User"

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "default"

# Initialize database
try:
    wishes_db = WishesDatabase()
    # Initialize the database tables
    wishes_db.init_database()
    logger.info("Wishes database initialized successfully")
except Exception as e:
    logger.warning(f"Could not initialize wishes database: {e}")
    wishes_db = None

@app.get("/")
async def root():
    return {"message": "SHAKTI-AI Backend Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Agent endpoints
@app.get("/api/agents/list")
async def get_agents():
    """Get list of available AI agents."""
    agents = {
        "maternal": {
            "name": "Maaya",
            "role": "Maternal Health Nurse",
            "expertise": "pregnancy, childbirth, and baby care",
            "specialties": ["pregnancy", "prenatal care", "childbirth", "postpartum", "breastfeeding", "infant care"]
        },
        "reproductive": {
            "name": "Gynika",
            "role": "Reproductive Health Advisor",
            "expertise": "menstruation, puberty, and contraception",
            "specialties": ["menstruation", "puberty", "contraception", "fertility", "reproductive health", "sexual health"]
        },
        "mental": {
            "name": "Meher",
            "role": "Mental Health Counselor",
            "expertise": "trauma, anxiety, and abuse recovery",
            "specialties": ["anxiety", "depression", "trauma", "PTSD", "domestic violence", "mental wellness"]
        },
        "legal": {
            "name": "Nyaya",
            "role": "Legal Rights Advisor",
            "expertise": "Indian laws related to women's rights",
            "specialties": ["women's rights", "family law", "workplace harassment", "domestic violence law", "property rights"]
        },
        "feminist": {
            "name": "Vaanya",
            "role": "Feminist Health Educator",
            "expertise": "menopause, hormonal health, and women's empowerment",
            "specialties": ["menopause", "hormonal health", "women's empowerment", "body autonomy", "health advocacy"]
        }
    }
    return {"agents": agents}

@app.post("/api/agents/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Chat with a specific AI agent."""
    try:
        if not ask_shakti_ai:
            raise HTTPException(status_code=503, detail="AI agent system not available")
        
        # Call the existing SHAKTI-AI system with a single agent
        response = ask_shakti_ai(request.message, [request.agent_type])
        
        # Get agent name
        agent_names = {
            "maternal": "Maaya",
            "reproductive": "Gynika",
            "mental": "Meher",
            "legal": "Nyaya",
            "feminist": "Vaanya"
        }
        
        agent_name = agent_names.get(request.agent_type, "SHAKTI-AI")
        
        logger.info(f"Successfully processed chat request for agent: {agent_name}")
        
        return ChatResponse(
            response=response,
            agent_name=agent_name,
            citations=[]  # Citations are embedded in the response text
        )
        
    except Exception as e:
        logger.error(f"Error in chat_with_agent: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process chat: {str(e)}")

# Wishes Vault endpoints
@app.get("/api/wishes/list")
async def get_wishes():
    """Get all wishes from the vault."""
    if not wishes_db:
        raise HTTPException(status_code=503, detail="Wishes database not available")
    
    try:
        # Use a default user_id for now (in production, this would come from authentication)
        user_id = "default_user"
        wishes = wishes_db.get_wishes(user_id, limit=100)
        
        # Transform the wishes to match the expected frontend format
        formatted_wishes = []
        for wish in wishes:
            formatted_wish = {
                "id": wish["id"],
                "title": wish.get("contact_name", "Untitled Wish"),  # Use contact_name as title fallback
                "content": wish["content"],
                "category": "personal",  # Default category since it's not stored
                "priority": "medium",    # Default priority since it's not stored
                "created_at": wish["created_at"].isoformat() if wish["created_at"] else None,
                "updated_at": wish["updated_at"].isoformat() if wish["updated_at"] else None,
                "contact_name": wish.get("contact_name"),
                "contact_email": wish.get("contact_email"),
                "contact_phone": wish.get("contact_phone"),
                "contact_relationship": wish.get("contact_relationship"),
                "sharing_preferences": wish.get("sharing_preferences", {})
            }
            formatted_wishes.append(formatted_wish)
            
        return {"wishes": formatted_wishes}
    except Exception as e:
        logger.error(f"Error in get_wishes: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch wishes: {str(e)}")

@app.post("/api/wishes/create")
async def create_wish(request: WishRequest):
    """Create a new wish in the vault."""
    if not wishes_db:
        raise HTTPException(status_code=503, detail="Wishes database not available")
    
    try:
        # Use a default user_id for now (in production, this would come from authentication)
        user_id = "default_user"
        
        # Save the wish using the actual database interface
        wish_id = wishes_db.save_wish(
            user_id=user_id,
            content=f"Title: {request.title}\n\nContent: {request.content}",
            contact_name=request.title,  # Use title as contact_name for display
            sharing_preferences={
                "category": request.category,
                "priority": request.priority,
                "reminder_date": request.reminder_date
            }
        )
        
        if wish_id:
            return {"success": True, "wish_id": wish_id, "message": "Wish created successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to create wish")
    except Exception as e:
        logger.error(f"Error in create_wish: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create wish: {str(e)}")

@app.put("/api/wishes/{wish_id}")
async def update_wish(wish_id: int, request: WishUpdateRequest):
    """Update an existing wish."""
    if not wishes_db:
        raise HTTPException(status_code=503, detail="Wishes database not available")
    
    try:
        # Use a default user_id for now (in production, this would come from authentication)
        user_id = "default_user"
        
        # Build the content if title or content is provided
        content = None
        if request.title or request.content:
            content = f"Title: {request.title or 'Untitled'}\n\nContent: {request.content or ''}"
        
        # Build sharing preferences
        sharing_preferences = {}
        if request.category:
            sharing_preferences["category"] = request.category
        if request.priority:
            sharing_preferences["priority"] = request.priority
        if request.reminder_date:
            sharing_preferences["reminder_date"] = request.reminder_date
        
        success = wishes_db.update_wish(
            wish_id=wish_id,
            user_id=user_id,
            content=content,
            contact_name=request.title,
            sharing_preferences=sharing_preferences if sharing_preferences else None
        )
        
        if success:
            return {"success": True, "message": "Wish updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Wish not found")
    except Exception as e:
        logger.error(f"Error in update_wish: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update wish: {str(e)}")

@app.delete("/api/wishes/{wish_id}")
async def delete_wish(wish_id: int):
    """Delete a wish from the vault."""
    if not wishes_db:
        raise HTTPException(status_code=503, detail="Wishes database not available")
    
    try:
        # Use a default user_id for now (in production, this would come from authentication)
        user_id = "default_user"
        
        success = wishes_db.delete_wish(wish_id, user_id)
        
        if success:
            return {"success": True, "message": "Wish deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Wish not found")
    except Exception as e:
        logger.error(f"Error in delete_wish: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete wish: {str(e)}")

@app.post("/api/wishes/share")
async def share_wish(request: ShareWishRequest):
    """Share a wish via email or WhatsApp."""
    if not wishes_db:
        raise HTTPException(status_code=503, detail="Wishes database not available")
    
    try:
        # Get the wish to share
        user_id = "default_user"
        wishes = wishes_db.get_wishes(user_id, limit=100)
        
        # Find the specific wish
        wish_to_share = None
        for wish in wishes:
            if wish["id"] == request.wish_id:
                wish_to_share = wish
                break
        
        if not wish_to_share:
            raise HTTPException(status_code=404, detail="Wish not found")
        
        wish_content = wish_to_share["content"]
        wish_title = wish_to_share.get("contact_name", "Untitled Wish")
        full_content = f"Title: {wish_title}\n\n{wish_content}"
        
        success = False
        share_url = None
        
        if request.method == "email":
            # Validate email
            if not validate_email(request.recipient):
                raise HTTPException(status_code=400, detail="Invalid email address")
            
            # Send email
            success = send_email_share(
                wish_content=full_content,
                recipient_email=request.recipient,
                sender_name=request.sender_name,
                wish_title=wish_title
            )
            
        elif request.method == "whatsapp":
            # Generate WhatsApp URL
            share_url = generate_whatsapp_share_url(full_content, request.recipient, request.sender_name)
            success = share_url is not None
            
            if not success:
                raise HTTPException(status_code=400, detail="Invalid phone number for WhatsApp")
        
        else:
            raise HTTPException(status_code=400, detail="Invalid sharing method. Use 'email' or 'whatsapp'")
        
        if success:
            # Log the sharing activity
            wishes_db.log_sharing(
                wish_id=request.wish_id,
                shared_with=request.recipient,
                sharing_method=request.method,
                status='sent',
                notes=f"Shared by {request.sender_name}"
            )
            
            response_data = {
                "success": True, 
                "message": f"Wish shared successfully via {request.method}"
            }
            
            # Include WhatsApp URL if applicable
            if share_url:
                response_data["whatsapp_url"] = share_url
            
            return response_data
        else:
            raise HTTPException(status_code=400, detail="Failed to share wish")
            
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in share_wish: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to share wish: {str(e)}")

# Voice endpoints
@app.post("/api/voice/speech-to-text")
async def speech_to_text(audio: UploadFile = File(...)):
    """Convert speech audio to text using uploaded file."""
    temp_file_path = None
    
    try:
        # Determine file format from content type or filename
        content_type = audio.content_type or ''
        filename = audio.filename or ''
        
        logger.info(f"Processing audio file: {filename}, content-type: {content_type}")
        
        # Save uploaded file temporarily with appropriate extension
        suffix = ".wav"
        if 'webm' in content_type.lower() or filename.lower().endswith('.webm'):
            suffix = ".webm"
        elif 'mp4' in content_type.lower() or filename.lower().endswith('.mp4'):
            suffix = ".mp4"
        elif 'mpeg' in content_type.lower() or filename.lower().endswith('.mp3'):
            suffix = ".mp3"
        elif 'ogg' in content_type.lower() or filename.lower().endswith('.ogg'):
            suffix = ".ogg"
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        logger.info(f"Saved audio to: {temp_file_path}, size: {len(content)} bytes")
        
        # Check if file is empty
        if len(content) == 0:
            return {"text": "", "success": False, "error": "Audio file is empty. Please try recording again."}
        
        # Use the same approach as the original Streamlit app
        recognizer = sr.Recognizer()
        
        # Configure recognizer like in the original app
        recognizer.energy_threshold = 400
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 3
        recognizer.phrase_threshold = 3
        
        text = None
        
        # Try to process with speech recognition
        try:
            with sr.AudioFile(temp_file_path) as source:
                # Adjust for ambient noise like in original app
                recognizer.adjust_for_ambient_noise(source, duration=1.0)
                audio_data = recognizer.record(source)
                
                # Try Google Speech Recognition first (like original)
                text = recognizer.recognize_google(audio_data)
                logger.info(f"Google Speech Recognition successful: {text[:50]}...")
                
        except (sr.UnknownValueError, sr.RequestError) as e:
            logger.warning(f"Google recognition failed: {e}")
            try:
                # Fallback to offline Sphinx like original
                with sr.AudioFile(temp_file_path) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_sphinx(audio_data)
                logger.info(f"Sphinx Recognition successful: {text[:50]}...")
                
            except Exception as sphinx_error:
                logger.error(f"Sphinx recognition also failed: {sphinx_error}")
                return {"text": "", "success": False, "error": "Could not understand the speech. Please speak more clearly and try again."}
        
        except Exception as audio_error:
            logger.error(f"Audio processing failed: {audio_error}")
            return {"text": "", "success": False, "error": f"Audio format not supported: {suffix}. Please try using a different browser or record in WAV format."}
        
        if not text or not text.strip():
            return {"text": "", "success": False, "error": "No speech detected in audio. Please try speaking more clearly."}
        
        # Apply the same medical context enhancements as original app
        enhanced_text = enhance_medical_context(text)
        
        return {"text": enhanced_text.strip(), "success": True}
        
    except Exception as e:
        logger.error(f"Error in speech_to_text: {e}")
        return {"text": "", "success": False, "error": f"Failed to process audio: {str(e)}"}
    
    finally:
        # Clean up temp files
        try:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        except Exception as cleanup_error:
            logger.warning(f"Failed to clean up temp files: {cleanup_error}")

def enhance_medical_context(text):
    """
    Enhance recognized text with medical term corrections and agent name recognition.
    Same function as used in the original Streamlit app.
    """
    if not text:
        return text
    
    import re
    
    text_lower = text.lower()
    enhanced = text
    
    # Fix common agent name misrecognitions
    agent_corrections = {
        "maya": "Maaya",
        "maa": "Maaya", 
        "maia": "Maaya",
        "gyneka": "Gynika",
        "genika": "Gynika",
        "mehir": "Meher",
        "meer": "Meher",
        "nyya": "Nyaya",
        "naya": "Nyaya",
        "vanya": "Vaanya",
        "vania": "Vaanya",
        "shakti ai": "SHAKTI-AI",
        "shakthi": "SHAKTI"
    }
    
    for incorrect, correct in agent_corrections.items():
        pattern = r'\b' + re.escape(incorrect) + r'\b'
        enhanced = re.sub(pattern, correct, enhanced, flags=re.IGNORECASE)
    
    # Fix common medical term misrecognitions
    medical_corrections = {
        "pregency": "pregnancy",
        "pregant": "pregnant",
        "menstration": "menstruation",
        "periode": "periods",
        "contraceptive": "contraception",
        "menapose": "menopause",
        "hormons": "hormones",
        "bledding": "bleeding",
        "nausia": "nausea",
        "dizy": "dizzy",
        "breastfeding": "breastfeeding",
        "ovulaion": "ovulation",
        "fertillity": "fertility",
        "anxiaty": "anxiety",
        "harrasment": "harassment"
    }
    
    for incorrect, correct in medical_corrections.items():
        pattern = r'\b' + re.escape(incorrect) + r'\b'
        enhanced = re.sub(pattern, correct, enhanced, flags=re.IGNORECASE)
    
    return enhanced

# Add a new endpoint for direct microphone access (future enhancement)
@app.post("/api/voice/direct-speech")
async def direct_speech_recognition():
    """
    Direct microphone access for speech recognition.
    This would require running on the same machine as the client.
    For now, we'll keep the file upload approach but with better processing.
    """
    return {"message": "Direct microphone access not implemented in web API. Use file upload method."}

@app.post("/api/voice/direct-speech-to-text")
async def direct_speech_to_text():
    """Direct microphone access for speech-to-text (like original Streamlit app)."""
    try:
        # Import the original voice input function
        from core.get_voice_input import get_voice_input
        
        logger.info("Starting direct microphone speech recognition")
        
        # Use the original implementation with medical context enhancement
        text = get_voice_input()
        
        if text and text.strip():
            logger.info(f"Direct speech recognition successful: {text[:50]}...")
            return {"text": text.strip(), "success": True}
        else:
            logger.warning("No speech detected or could not understand audio")
            return {"text": "", "success": False, "error": "No speech detected or could not understand audio. Please speak clearly and try again."}
            
    except ImportError as e:
        logger.error(f"Voice input module not available: {e}")
        return {"text": "", "success": False, "error": "Voice input functionality not available on this system."}
    except Exception as e:
        logger.error(f"Error in direct_speech_to_text: {e}")
        return {"text": "", "success": False, "error": f"Failed to process voice input: {str(e)}"}

@app.post("/api/voice/text-to-speech")
async def text_to_speech(request: TTSRequest):
    """Convert text to speech audio."""
    try:
        # For now, return a simple response indicating TTS is not fully implemented
        # In a full implementation, you would use a TTS library like gTTS, pyttsx3, etc.
        return {"message": "Text-to-speech functionality will be implemented with gTTS or similar", "text": request.text}
        
    except Exception as e:
        logger.error(f"Error in text_to_speech: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate speech: {str(e)}")

# Email configuration endpoints
@app.get("/api/email/test")
async def test_email_configuration():
    """Test SMTP configuration."""
    if not email_service:
        raise HTTPException(status_code=503, detail="Email service not available")
    
    try:
        is_configured = email_service.is_configured()
        connection_test = email_service.test_connection() if is_configured else False
        
        return {
            "configured": is_configured,
            "connection_test": connection_test,
            "message": "SMTP configuration test completed",
            "smtp_host": email_service.smtp_host,
            "smtp_port": email_service.smtp_port,
            "smtp_user": email_service.smtp_user if email_service.smtp_user else "Not configured"
        }
    except Exception as e:
        logger.error(f"Error testing email configuration: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to test email configuration: {str(e)}")

@app.get("/api/email/setup-instructions")
async def get_email_setup_instructions():
    """Get email setup instructions for different providers."""
    if not email_service:
        raise HTTPException(status_code=503, detail="Email service not available")
    
    try:
        instructions = email_service.get_setup_instructions()
        return {
            "instructions": instructions,
            "current_config": {
                "configured": email_service.is_configured(),
                "smtp_host": email_service.smtp_host,
                "smtp_port": email_service.smtp_port,
                "smtp_user": email_service.smtp_user if email_service.smtp_user else "Not configured"
            }
        }
    except Exception as e:
        logger.error(f"Error getting setup instructions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get setup instructions: {str(e)}")

# Helper functions for sharing wishes
async def send_wish_via_email(recipient: str, wish_id: int, sender_name: str):
    """Send a wish to the recipient via email."""
    try:
        # Fetch the wish details from the database
        wish = wishes_db.get_wish_by_id(wish_id)
        
        if not wish:
            raise HTTPException(status_code=404, detail="Wish not found")
        
        # Prepare the email content
        subject = f"Wish Shared with You - ID: {wish_id}"
        body = f"Hello,\n\nYou have received a new wish from {sender_name}.\n\n"
        body += f"Title: {wish['title']}\n\n"
        body += f"Content: {wish['content']}\n\n"
        body += "Best regards,\nSHAKTI-AI"
        
        # Send the email (using a dummy SMTP server for now)
        smtp_server = "smtp.example.com"
        smtp_port = 587
        smtp_user = "your_email@example.com"
        smtp_password = "your_password"
        
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        logger.info(f"Wish {wish_id} shared via email to {recipient}")
        
    except Exception as e:
        logger.error(f"Error in send_wish_via_email: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send wish via email: {str(e)}")

async def send_wish_via_whatsapp(recipient: str, wish_id: int, sender_name: str):
    """Send a wish to the recipient via WhatsApp."""
    try:
        # Fetch the wish details from the database
        wish = wishes_db.get_wish_by_id(wish_id)
        
        if not wish:
            raise HTTPException(status_code=404, detail="Wish not found")
        
        # Prepare the WhatsApp message
        message = f"Hello, you have received a new wish from {sender_name}.\n\n"
        message += f"*Title:* {wish['title']}\n\n"
        message += f"*Content:* {wish['content']}"
        
        # Encode the message for URL
        encoded_message = urllib.parse.quote(message)
        
        # Create the WhatsApp share link (using the web.whatsapp.com for desktop)
        whatsapp_url = f"https://api.whatsapp.com/send?text={encoded_message}"
        
        # Open the URL in a web browser (this will prompt the user to send the message)
        webbrowser.open(whatsapp_url)
        
        logger.info(f"Wish {wish_id} shared via WhatsApp to {recipient}")
        
    except Exception as e:
        logger.error(f"Error in send_wish_via_whatsapp: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send wish via WhatsApp: {str(e)}")

# Helper functions for sharing
def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_phone_for_whatsapp(phone):
    """Format phone number for WhatsApp."""
    # Remove all non-digit characters
    phone = ''.join(filter(str.isdigit, phone))
    
    # Add India country code if not present and phone has 10 digits
    if len(phone) == 10:
        phone = '91' + phone
    elif len(phone) == 11 and phone.startswith('0'):
        phone = '91' + phone[1:]
    
    return phone if len(phone) >= 10 else None

def send_email_share(wish_content, recipient_email, sender_name="SHAKTI-AI User", wish_title="My Wish"):
    """Send wish via email using the email service."""
    try:
        if email_service:
            return email_service.send_wish_share_email(
                wish_content=wish_content,
                recipient_email=recipient_email,
                sender_name=sender_name,
                wish_title=wish_title
            )
        else:
            logger.error("Email service not available")
            return False
        
    except Exception as e:
        logger.error(f"Email sharing failed: {e}")
        return False

def generate_whatsapp_share_url(wish_content, phone_number, sender_name="SHAKTI-AI User"):
    """Generate WhatsApp sharing URL."""
    try:
        formatted_phone = format_phone_for_whatsapp(phone_number)
        if not formatted_phone:
            return None
        
        message = f"""🌟 Important Message from {sender_name} via SHAKTI-AI

My wishes and thoughts:
{wish_content}

This message was sent securely through SHAKTI-AI, a platform that supports women's health and well-being.

With care ❤️

---
Shared on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
SHAKTI-AI: For every woman, every phase, every fight.
"""
        
        # URL encode the message
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/{formatted_phone}?text={encoded_message}"
        
        return whatsapp_url
        
    except Exception as e:
        logger.error(f"WhatsApp URL generation failed: {e}")
        return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
