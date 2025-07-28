"""
Simple Mock Backend for SHAKTI-AI
This provides immediate responses so the chat interface works
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime

class MockBackendHandler(BaseHTTPRequestHandler):
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
            response = {"message": "SHAKTI-AI Mock Backend is running!", "status": "ok"}
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
                
                # Generate mock responses based on agent type
                responses = {
                    'reproductive': f"Hello! I'm Dr. Gynika, your reproductive health specialist. You asked: '{message}'. This is a mock response - I'd be happy to help with questions about reproductive health, pregnancy, contraception, and women's health concerns.",
                    
                    'feminist': f"Greetings! I'm Advocate Vaanya, your feminist rights expert. Regarding your question: '{message}' - This is a mock response. I specialize in women's rights, workplace equality, legal protections, and feminist advocacy.",
                    
                    'legal': f"Hello! I'm Counselor Nyaya, your legal rights advisor. You mentioned: '{message}'. This is a mock response - I can help you understand your legal rights, constitutional protections, and legal procedures.",
                    
                    'maternal': f"Hi there! I'm Maya, your maternal health specialist. About your question: '{message}' - This is a mock response. I focus on pregnancy care, childbirth preparation, postpartum support, and maternal wellness.",
                    
                    'mental': f"Welcome! I'm Life Coach Meher, your mental health and wellness expert. You asked: '{message}'. This is a mock response - I can guide you through stress management, emotional wellness, and mental health support."
                }
                
                # Get appropriate response
                mock_response = responses.get(agent_type, f"Hello! This is a mock response to your message: '{message}'. The real AI agents will provide more detailed and helpful responses once the full backend is running.")
                
                # Send successful response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "response": mock_response,
                    "agent_type": agent_type,
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                    "note": "This is a mock response. Real AI agents will provide more detailed guidance."
                }
                
                self.wfile.write(json.dumps(response).encode())
                print(f"Mock response sent for {agent_type}: {message}")
                
            except Exception as e:
                # Send error response
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {
                    "error": str(e),
                    "status": "error"
                }
                
                self.wfile.write(json.dumps(error_response).encode())
                print(f"Error processing request: {e}")
        else:
            self.send_response(404)
            self.end_headers()

def run_mock_backend():
    print("🚀 Starting SHAKTI-AI Mock Backend...")
    print("📍 Backend will be available at: http://localhost:8000")
    print("💬 This will enable the chat interface to work with mock responses")
    print("🔄 The real AI agents can be connected later")
    print("")
    
    server = HTTPServer(('localhost', 8000), MockBackendHandler)
    print("✅ Mock backend started successfully!")
    print("🌐 Frontend can now connect to: http://localhost:8000/api/agents/chat")
    print("📱 Test your ChatGPT-like interface now!")
    print("")
    print("Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Mock backend stopped")
        server.shutdown()

if __name__ == "__main__":
    run_mock_backend()
