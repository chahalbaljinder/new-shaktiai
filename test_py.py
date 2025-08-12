import json
print("Testing Python execution...")
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    print("HTTP server imports successful")
except Exception as e:
    print(f"Error importing HTTP server: {e}")

print("Test complete")
