import sys
import os

# Set root path to import app and utils correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app import app

# Vercel serverless WSGI entry point
# 'app' is the Flask WSGI instance
