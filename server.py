import http.server
import socketserver
import mimetypes
import os

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Expires', '0')
        self.send_header('Pragma', 'no-cache')
        super().end_headers()

    def do_GET(self):
        # Force correct MIME types
        if self.path.endswith('.css'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/css; charset=utf-8')
            self.end_headers()
            with open(self.path[1:], 'rb') as f:
                self.wfile.write(f.read())
            return
        elif self.path.endswith('.js'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript; charset=utf-8')
            self.end_headers()
            with open(self.path[1:], 'rb') as f:
                self.wfile.write(f.read())
            return
        elif self.path.endswith('.html') or self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            # Handle root path
            fpath = 'index.html' if self.path == '/' else self.path[1:]
            with open(fpath, 'rb') as f:
                self.wfile.write(f.read())
            return
        
        return super().do_GET()

# Ensure MIME types are known (backup)
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

print(f"Serving on http://localhost:{PORT}")
print("Press Ctrl+C to stop.")

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
