import os

UPLOAD_DIR = "uploads"


def create_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)