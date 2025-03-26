# GeoFy - Geolocation Tracking Tool

GeoFy is a powerful tool designed to capture the geolocation of users through their IP address and browser-based location services. It utilizes tunneling services like Cloudflare and Serveo to expose the local server to the internet, making it accessible from anywhere.

## Features
- Fetch public IP address and geolocation of users.
- Uses Google Maps to display captured coordinates.
- Supports tunneling via Cloudflare and Serveo.
- Lightweight HTTP server for serving the landing page.
- Automatically installs missing dependencies (Cloudflared, SSH).
- Interactive CLI for easy setup.

## Future Updates
🚀 The following features are planned for future releases:
- **Custom Port Selection**: Allow users to define the port for the local server.
- **URL Shortening**: Provide shortened URLs for better sharing.
- **Ngrok Support**: Add Ngrok as an additional tunneling option.
- **IP-based Location Detection**: Get approximate location when GPS access is denied.
- **Logging to File**: Save captured locations to a file for later review.

## Installation
Clone the repository and run the script:

```sh
 git clone https://github.com/Fusion-boy/GeoFy.git
 cd GeoFy
 python GeoFy.py
```

## Usage
1. Run the script and choose your preferred tunneling service.
2. Share the generated link with your target.
3. Capture the IP address and geolocation when the user visits the link.

## Dependencies
- Python 3.x
- Cloudflared (will be installed automatically if missing)
- OpenSSH (required for Serveo tunneling)

## Disclaimer
This tool is for educational and research purposes only. Misuse of this tool for unauthorized tracking is strictly prohibited.The author holds no responsibility for any misuse of this project.

## Contribution
Feel free to contribute by submitting pull requests and reporting issues.

---

🌍 **Stay tuned for more updates!**

