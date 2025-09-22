# gunicorn_config.py
import os

# Bind to all interfaces and use PORT from environment (Railway/Render set this)
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
