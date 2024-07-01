import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

DATABASE_FILE = os.path.join(BASE_DIR, 'files.db')

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000
LOCAL = False
