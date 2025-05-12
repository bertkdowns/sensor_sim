import time
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Parameters
MAX_LEVEL = 100  # Maximum hydro level
UPDATE_INTERVAL = 5  # Update interval in seconds

# Global variable to store the current hydro level
current_level = random.uniform(0, MAX_LEVEL)

# Function to simulate random walk
def update_hydro_level():
    global current_level
    step = random.uniform(-5, 5)  # Random step
    current_level = max(0, min(MAX_LEVEL, current_level + step))  # Keep within bounds

# HTTP request handler
class HydroLevelHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"{current_level:.2f}".encode())

# Start the HTTP server
def start_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, HydroLevelHandler)
    print("HTTP server running on port 8080...")
    httpd.serve_forever()

# Main function
if __name__ == "__main__":

    # Start the HTTP server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Update and print hydro level every 5 seconds
    try:
        while True:
            update_hydro_level()
            print(f"Hydro level: {current_level:.2f}")
            time.sleep(UPDATE_INTERVAL)
    except KeyboardInterrupt:
        print("\nSimulation stopped.")