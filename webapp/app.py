from flask import Flask
import socket
import os

app = Flask(__name__)

@app.route('/')
def home():
    container_id = os.uname().nodename[:12]
    hostname = socket.gethostname()
    
    html = f"""
    <html>
    <head><title>RPi Cluster</title></head>
    <body style="font-family: Arial; padding: 50px; background: #667eea; color: white;">
        <h1>Raspberry Pi Cluster Demo</h1>
        <div style="background: rgba(255,255,255,0.2); padding: 30px; border-radius: 10px;">
            <h2>Container ID: {container_id}</h2>
            <h2>Hostname: {hostname}</h2>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
