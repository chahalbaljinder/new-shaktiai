"""
Simple test to check Python backend functionality
"""
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

class SimpleWishesHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default HTTP logging
        pass
        
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        print(f"GET request: {self.path}")
        
        if self.path == '/api/wishes/list':
            try:
                # Load wishes from file
                wishes_file = 'wishes_data.json'
                if os.path.exists(wishes_file):
                    with open(wishes_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        wishes = data.get('wishes', [])
                else:
                    wishes = []
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {"wishes": wishes, "status": "success"}
                self.wfile.write(json.dumps(response).encode())
                print(f"Returned {len(wishes)} wishes")
                
            except Exception as e:
                print(f"Error: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {"error": str(e), "status": "error"}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        print(f"POST request: {self.path}")
        
        if self.path == '/api/wishes/create':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Create new wish
                wish = {
                    "id": int(datetime.now().timestamp()),
                    "title": data.get('title', ''),
                    "content": data.get('content', ''),
                    "category": data.get('category', 'personal'),
                    "priority": data.get('priority', 'medium'),
                    "reminder_date": data.get('reminder_date', ''),
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
                
                # Load existing wishes
                wishes_file = 'wishes_data.json'
                if os.path.exists(wishes_file):
                    with open(wishes_file, 'r', encoding='utf-8') as f:
                        data_file = json.load(f)
                        wishes = data_file.get('wishes', [])
                else:
                    wishes = []
                
                # Add new wish
                wishes.append(wish)
                
                # Save wishes
                with open(wishes_file, 'w', encoding='utf-8') as f:
                    json.dump({"wishes": wishes}, f, indent=2, ensure_ascii=False)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {"wish": wish, "message": "Wish created successfully", "status": "success"}
                self.wfile.write(json.dumps(response).encode())
                print(f"Created wish: {wish['title']}")
                
            except Exception as e:
                print(f"Error creating wish: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {"error": str(e), "status": "error"}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    print("Starting Simple Wishes Backend...")
    print("Server will run on http://localhost:8000")
    print("Wishes endpoint: /api/wishes/list")
    print("Press Ctrl+C to stop")
    
    try:
        server = HTTPServer(('localhost', 8000), SimpleWishesHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.shutdown()
