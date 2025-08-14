"""
Real SHAKTI-AI Backend Service
Connects your ChatGPT interface to actual AI agents with knowledge base
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the real SHAKTI-AI functions
try:
    from core.crew import ask_shakti_ai
    print("✅ Successfully imported SHAKTI-AI crew")
    AI_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importing SHAKTI-AI: {e}")
    print("🔧 Running in fallback mode without AI agents")
    AI_AVAILABLE = False
    
    # Create fallback function
    def ask_shakti_ai(message, agent_type="general"):
        return {
            "response": f"Hello! I'm {agent_type} agent. Due to system configuration, I'm running in limited mode. Your message was: {message}",
            "agent": agent_type,
            "status": "fallback_mode"
        }

class RealAIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default HTTP logging to keep output clean
        pass
        
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            status = "Real AI Agents" if AI_AVAILABLE else "AI Import Failed"
            response = {
                "message": f"SHAKTI-AI Backend ({status}) is running!", 
                "status": "ok",
                "ai_available": AI_AVAILABLE,
                "timestamp": datetime.now().isoformat(),
                "port": os.environ.get('PORT', 8000)
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/api/wishes/list':
            # Handle wishes list request via GET
            self.handle_wishes_list()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/agents/chat':
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                message = data.get('message', '')
                agent_type = data.get('agent_type', 'general')
                
                print(f"🔄 Processing query for {agent_type}: {message}")
                
                if AI_AVAILABLE:
                    # Map frontend agent types to SHAKTI-AI agent types
                    agent_mapping = {
                        'reproductive': ['reproductive'],
                        'feminist': ['feminist'],
                        'legal': ['legal'],
                        'maternal': ['maternal'],
                        'mental': ['mental']
                    }
                    
                    # Get the agent types for SHAKTI-AI
                    shakti_agents = agent_mapping.get(agent_type, ['reproductive'])
                    
                    # Call the real SHAKTI-AI function
                    print(f"🤖 Calling SHAKTI-AI with agents: {shakti_agents}")
                    ai_response = ask_shakti_ai(message, shakti_agents)
                    
                    print(f"✅ Real AI response received ({len(ai_response)} chars)")
                    response_text = ai_response
                    
                else:
                    response_text = f"❌ AI agents are not available. Error during import. Please check the core.crew module."
                
                # Send successful response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "response": response_text,
                    "agent_type": agent_type,
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "ai_mode": "real" if AI_AVAILABLE else "error"
                }
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"❌ Error processing request: {e}")
                # Send error response
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {
                    "error": f"Backend error: {str(e)}",
                    "status": "error",
                    "timestamp": datetime.now().isoformat(),
                    "ai_mode": "error"
                }
                
                self.wfile.write(json.dumps(error_response).encode())
        
        elif self.path == '/api/wishes/list':
            # Handle wishes list request
            self.handle_wishes_list()
        elif self.path == '/api/wishes/create':
            # Handle create wish request
            self.handle_create_wish()
        elif self.path.startswith('/api/wishes/') and self.path.endswith('/delete'):
            # Handle delete wish request
            self.handle_delete_wish()
        elif self.path.startswith('/api/wishes/') and self.path.endswith('/update'):
            # Handle update wish request
            self.handle_update_wish()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_wishes_list(self):
        """Handle getting list of wishes"""
        try:
            wishes = self.load_wishes()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "wishes": wishes,
                "status": "success"
            }
            self.wfile.write(json.dumps(response).encode())
            print(f"✅ Returned {len(wishes)} wishes")
            
        except Exception as e:
            print(f"❌ Error loading wishes: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                "error": f"Failed to load wishes: {str(e)}",
                "status": "error"
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def handle_create_wish(self):
        """Handle creating a new wish"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            wish = {
                "id": len(self.load_wishes()) + 1,
                "title": data.get('title', ''),
                "content": data.get('content', ''),
                "category": data.get('category', 'personal'),
                "priority": data.get('priority', 'medium'),
                "reminder_date": data.get('reminder_date', ''),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            wishes = self.load_wishes()
            wishes.append(wish)
            self.save_wishes(wishes)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "wish": wish,
                "message": "Wish created successfully",
                "status": "success"
            }
            self.wfile.write(json.dumps(response).encode())
            print(f"✅ Created wish: {wish['title']}")
            
        except Exception as e:
            print(f"❌ Error creating wish: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                "error": f"Failed to create wish: {str(e)}",
                "status": "error"
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def handle_delete_wish(self):
        """Handle deleting a wish"""
        try:
            # Extract wish ID from path
            wish_id = int(self.path.split('/')[-2])
            
            wishes = self.load_wishes()
            wishes = [w for w in wishes if w.get('id') != wish_id]
            self.save_wishes(wishes)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "Wish deleted successfully",
                "status": "success"
            }
            self.wfile.write(json.dumps(response).encode())
            print(f"✅ Deleted wish ID: {wish_id}")
            
        except Exception as e:
            print(f"❌ Error deleting wish: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                "error": f"Failed to delete wish: {str(e)}",
                "status": "error"
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def handle_update_wish(self):
        """Handle updating a wish"""
        try:
            # Extract wish ID from path
            wish_id = int(self.path.split('/')[-2])
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            wishes = self.load_wishes()
            for i, wish in enumerate(wishes):
                if wish.get('id') == wish_id:
                    wishes[i].update({
                        "title": data.get('title', wish['title']),
                        "content": data.get('content', wish['content']),
                        "category": data.get('category', wish['category']),
                        "priority": data.get('priority', wish['priority']),
                        "reminder_date": data.get('reminder_date', wish['reminder_date']),
                        "updated_at": datetime.now().isoformat()
                    })
                    break
            
            self.save_wishes(wishes)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "Wish updated successfully",
                "status": "success"
            }
            self.wfile.write(json.dumps(response).encode())
            print(f"✅ Updated wish ID: {wish_id}")
            
        except Exception as e:
            print(f"❌ Error updating wish: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                "error": f"Failed to update wish: {str(e)}",
                "status": "error"
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def load_wishes(self):
        """Load wishes from JSON file"""
        try:
            wishes_file = os.path.join(os.path.dirname(__file__), 'wishes_data.json')
            if os.path.exists(wishes_file):
                with open(wishes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('wishes', [])
            return []
        except Exception:
            return []
    
    def save_wishes(self, wishes):
        """Save wishes to JSON file"""
        try:
            wishes_file = os.path.join(os.path.dirname(__file__), 'wishes_data.json')
            with open(wishes_file, 'w', encoding='utf-8') as f:
                json.dump({"wishes": wishes}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving wishes: {e}")
            raise

def run_real_ai_backend():
    # Get port from environment variable (Railway sets this automatically)
    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0'  # Listen on all interfaces for cloud deployment
    
    print("🚀 Starting SHAKTI-AI Real Backend with Actual Agents")
    print("==================================================")
    
    if AI_AVAILABLE:
        print("✅ Real SHAKTI-AI agents loaded successfully!")
        print("🧠 Your agents have access to knowledge base")
        print("💬 Users will get authentic expert responses")
    else:
        print("❌ Real AI agents failed to load")
        print("🔧 Check if all dependencies are installed")
        print("📚 Ensure knowledge base is properly set up")
    
    print("")
    print(f"📍 Backend running at: http://{host}:{port}")
    print("🌐 API endpoint: /api/agents/chat")
    print("🔗 Frontend should connect automatically")
    print("")
    print("Press Ctrl+C to stop the server")
    print("")
    
    try:
        server = HTTPServer((host, port), RealAIHandler)
        print(f"✅ Server started successfully on {host}:{port}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 SHAKTI-AI backend stopped")
        server.shutdown()
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        raise

if __name__ == "__main__":
    run_real_ai_backend()
