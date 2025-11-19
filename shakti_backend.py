"""
Real APEX Backend Service
Connects your ChatGPT interface to actual AI agents with knowledge base
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the real APEX functions
try:
    from core.crew import ask_apex
    print("✅ Successfully imported APEX crew")
    AI_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importing APEX: {e}")
    AI_AVAILABLE = False

class RealAIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Custom logging to see requests
        print(f"🌐 {format % args}")
        
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            status = "Real AI Agents" if AI_AVAILABLE else "AI Import Failed"
            response = {
                "message": f"APEX Backend ({status}) is running!", 
                "status": "ok",
                "ai_available": AI_AVAILABLE,
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/api/agents':
            # Handle agent status request
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "agents": [
                    {"id": "athena", "name": "Athena", "type": "policy", "available": AI_AVAILABLE},
                    {"id": "asha", "name": "Asha", "type": "wellness", "available": AI_AVAILABLE},
                    {"id": "scribe", "name": "Scribe", "type": "documentation", "available": AI_AVAILABLE}
                ],
                "status": "online" if AI_AVAILABLE else "offline",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/api/agents/list':
            # Handle agent list request (for frontend compatibility)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "agents": {
                    "legal-guide": {
                        "name": "Athena",
                        "role": "Policy & Research Advisor", 
                        "expertise": "policy guidance, research funding, legal compliance",
                        "specialties": ["DRDO IPR", "women scientist schemes", "research policies", "funding guidelines"]
                    },
                    "wellness": {
                        "name": "Asha",
                        "role": "Wellness & Support Counselor",
                        "expertise": "mental health, work-life balance, stress management", 
                        "specialties": ["stress management", "imposter syndrome", "mental health", "workplace wellness"]
                    },
                    "documentation": {
                        "name": "Scribe",
                        "role": "Documentation & Procedures Expert",
                        "expertise": "office procedures, documentation formats, administrative processes",
                        "specialties": ["office memorandums", "e-office procedures", "transfer applications", "official formats"]
                    }
                }
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
                    # Map frontend agent types to APEX agent types
                    agent_mapping = {
                        'legal-guide': ['legal-guide'],
                        'wellness': ['wellness'],
                        'documentation': ['documentation'],
                        'policy': ['legal-guide'],
                        'support': ['wellness']
                    }
                    
                    # Get the agent types for APEX
                    apex_agents = agent_mapping.get(agent_type, ['legal-guide'])
                    
                    # Call the real APEX function
                    print(f"🤖 Calling APEX with agents: {apex_agents}")
                    try:
                        ai_response = ask_apex(message, apex_agents)
                        print(f"✅ Real AI response received ({len(ai_response)} chars)")
                        response_text = ai_response
                    except Exception as ai_error:
                        print(f"🚨 APEX Error: {ai_error}")
                        print(f"🔍 Error Type: {type(ai_error).__name__}")
                        import traceback
                        print(f"📍 Full Traceback:")
                        traceback.print_exc()
                        response_text = f"⚠️ AI Agent Error: {str(ai_error)}\n\nThe AI agents are having technical difficulties. This may be due to a configuration or dependency issue."
                    
                else:
                    response_text = f"❌ AI agents are not available. Error during import. Please check the core.crew module."
                # Get agent name for response
                agent_names = {
                    'legal-guide': 'Athena',
                    'wellness': 'Asha', 
                    'documentation': 'Scribe',
                    'policy': 'Athena',
                    'support': 'Asha'
                }
                agent_name = agent_names.get(agent_type, 'APEX')
                
                # Send successful response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "response": response_text,
                    "agent_name": agent_name,
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
    print("🚀 Starting APEX Real Backend with Actual Agents")
    print("==============================================")
    
    if AI_AVAILABLE:
        print("✅ Real APEX agents loaded successfully!")
        print("🧠 Your agents have access to knowledge base")
        print("💬 Users will get authentic expert responses")
    else:
        print("❌ Real AI agents failed to load")
        print("🔧 Check if all dependencies are installed")
        print("📚 Ensure knowledge base is properly set up")
    
    print("")
    print("📍 Backend running at: http://localhost:8000")
    print("🌐 API endpoint: /api/agents/chat")
    print("🔗 Frontend should connect automatically")
    print("")
    print("Press Ctrl+C to stop the server")
    print("")
    
    server = None
    try:
        server = HTTPServer(('localhost', 8000), RealAIHandler)
        print("🚀 Server initialized successfully")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 APEX backend stopped by user")
    except Exception as e:
        print(f"\n💥 Server error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if server:
            print("🔧 Shutting down server...")
            server.shutdown()
            server.server_close()

if __name__ == "__main__":
    run_real_ai_backend()