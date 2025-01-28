# Usage: python scripts/files_uploader.py upload-files file1.txt file2.txt

import typer
from pathlib import Path
import requests
import threading
import json
from loguru import logger

APP_BASE_URL = "http://localhost:8000"

app = typer.Typer()

def upload_file(file_to_upload):
    global request_status
    try:
        requests.post(url=f"{APP_BASE_URL}/documents/upload/", files=file_to_upload, timeout=10)
        logger.info("Request completed successfully!")
        request_status = "completed"
    except requests.exceptions.Timeout:
        logger.info("Request timed out!")
        request_status = "timed out"
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        request_status = "error"

@app.command('upload')
def upload_files(input: list[Path]):
    """
    Upload a single file or multiple files provided as space-separated paths.
    """

    for file in input:
        if not file.exists():
            logger.error(f"File does not exist - {file}")
            continue
        if not file.is_file():
            logger.error(f"Not a valid file - {file}")
            continue
        logger.info(f"Uploading file: {file.name}")

        with open(file, 'rb') as f:
            file_to_upload = {'file': f}
            response = requests.post(url=f"{APP_BASE_URL}/documents/upload/", files=file_to_upload)
            response.raise_for_status()

@app.command('clean_all')
def clean_files():
    """
    Clean all uploaded files.
    """
    list_files = requests.get(url=f"{APP_BASE_URL}/documents/")
    list_files.raise_for_status()

    for file in json.loads(list_files.text):
        d = requests.delete(url=f"{APP_BASE_URL}/documents/{file['id']}")
        d.raise_for_status()

    list_files = requests.get(url=f"{APP_BASE_URL}/documents/")
    list_files.raise_for_status()
    assert not json.loads(list_files.text), "Error: Files weren't deleted"

@app.command('list_files')
def list_files():
    """
    List all uploaded files.
    """
    list_files = requests.get(url=f"{APP_BASE_URL}/documents/")
    list_files.raise_for_status()
    logger.info(f"List of uploaded files: {list_files.text}")

if __name__ == "__main__":
    app()