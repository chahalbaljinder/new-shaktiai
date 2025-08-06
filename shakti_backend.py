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
    AI_AVAILABLE = False

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
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            status = "Real AI Agents" if AI_AVAILABLE else "AI Import Failed"
            response = {
                "message": f"SHAKTI-AI Backend ({status}) is running!", 
                "status": "ok",
                "ai_available": AI_AVAILABLE,
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
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
        else:
            self.send_response(404)
            self.end_headers()

def run_real_ai_backend():
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
    print("📍 Backend running at: http://localhost:8000")
    print("🌐 API endpoint: /api/agents/chat")
    print("🔗 Frontend should connect automatically")
    print("")
    print("Press Ctrl+C to stop the server")
    print("")
    
    try:
        server = HTTPServer(('localhost', 8000), RealAIHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 SHAKTI-AI backend stopped")
        server.shutdown()

if __name__ == "__main__":
    run_real_ai_backend()
