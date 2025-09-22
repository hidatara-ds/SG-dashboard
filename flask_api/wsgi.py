import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import the already-configured Flask app instance that also defines root route
from app import app

if __name__ == "__main__":
    app.run()