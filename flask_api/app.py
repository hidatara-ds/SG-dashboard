# flask_api/app.py (Simplified Update)
import sys
import os
import logging
from flask import Flask
from flask_cors import CORS
from config import Config

# Add parent directory to path for webhook imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import existing routes
from routes import bp

# Import webhook functionality  
try:
    from webhook import register_webhook_routes
    _HAS_WEBHOOK = True
except Exception:
    register_webhook_routes = None
    _HAS_WEBHOOK = False

def create_app():
    """Create Flask application with webhook support"""
    app = Flask(__name__)
    CORS(app)
    
    # Simple logging setup
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file_path = os.path.join(logs_dir, 'app.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )
    
    # Register existing API routes
    app.register_blueprint(bp)
    app.logger.info("API routes registered")
    
    # Register webhook routes if available
    if _HAS_WEBHOOK and callable(register_webhook_routes):
        register_webhook_routes(app)
        app.logger.info("Webhook routes registered")
    else:
        app.logger.info("Webhook package not found; skipping webhook routes")
    
    return app

app = create_app()

# Root route for service landing
@app.route('/')
def index():
    return {
        "status": "ok",
        "service": "Smart Greenhouse API",
        "try": ["/api/ping", "/health"]
    }, 200

# Combined health check
@app.route('/health')
def health_check():
    """Simple health check for both API and webhook systems"""
    try:
        from db import get_db_connection, return_db_connection
        
        # Test database connection
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        return_db_connection(conn)
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2025-08-25T10:30:25.000Z"
        }, 200
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2025-08-25T10:30:25.000Z"
        }, 500

if __name__ == "__main__":
    app.logger.info("Starting Smart Greenhouse API with Webhook Support")
    app.run(host="0.0.0.0", port=Config.PORT, debug=(Config.FLASK_ENV == 'development'))