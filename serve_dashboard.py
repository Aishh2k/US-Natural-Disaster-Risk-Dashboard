import http.server
import socketserver
import os
import webbrowser
import json
import sys

# Add preprocessing directory to path to import chatbot_api
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "preprocessing"))
import chatbot_api

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def load_dotenv(path, override=False):
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key and (override or key not in os.environ):
                os.environ[key] = value


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def is_blocked_path(self):
        requested_path = self.path.split("?", 1)[0]
        parts = [part for part in requested_path.split("/") if part]
        return any(
            part.startswith(".") or part == "__pycache__" or part.endswith(".pyc")
            for part in parts
        )

    def do_GET(self):
        if self.is_blocked_path():
            self.send_error(404, "File not found")
            return
        super().do_GET()

    def do_HEAD(self):
        if self.is_blocked_path():
            self.send_error(404, "File not found")
            return
        super().do_HEAD()

    def do_POST(self):
        if self.path == '/api/chat':
            load_dotenv(os.path.join(DIRECTORY, ".env"), override=True)
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                message = data.get('message')
                context = data.get('context')
                
                response_data = chatbot_api.get_openai_response(message, context)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "File not found")


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main():
    load_dotenv(os.path.join(DIRECTORY, ".env"), override=True)

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("\n" + "="*60)
        print("WARNING: GROQ_API_KEY environment variable not found!")
        print("The chatbot feature will not work without it.")
        print("Add GROQ_API_KEY to .env, then restart this server.")
        print("="*60 + "\n")
    else:
        print("\nSUCCESS: GROQ_API_KEY loaded from environment.\n")

    print(f"Serving dashboard at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")

    webbrowser.open(f"http://localhost:{PORT}")

    with ReusableTCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server.")


if __name__ == "__main__":
    main()
