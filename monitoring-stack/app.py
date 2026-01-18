```python
from flask import Flask, jsonify
import socket
import os
import time
import psutil

app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    
    RPi Cluster Demo
    
        🚀 Raspberry Pi Cluster - Node Info
        Hostname: {socket.gethostname()}
        IP Address: {socket.gethostbyname(socket.gethostname())}
        Container ID: {os.uname().nodename}
        CPU Usage: {psutil.cpu_percent()}%
        Memory Usage: {psutil.virtual_memory().percent}%
        
        Request served at: {time.strftime('%Y-%m-%d %H:%M:%S')}
    
    
    """

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'hostname': socket.gethostname(),
        'timestamp': time.time()
    })

@app.route('/api/info')
def info():
    return jsonify({
        'hostname': socket.gethostname(),
        'container_id': os.uname().nodename,
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
