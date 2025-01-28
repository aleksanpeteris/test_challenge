import json
import requests
import typer

from loguru import logger
from pathlib import Path

APP_BASE_URL = "http://localhost:8000"

app = typer.Typer()

@app.command('upload')
def upload_files(input: list[Path]):
    """
    Upload a single file or multiple files provided as space-separated paths.
    """
    initial_files_list = json.loads(requests.get(url=f"{APP_BASE_URL}/documents/").text)
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
        updated_files_list = json.loads(requests.get(url=f"{APP_BASE_URL}/documents/").text)
        assert len(updated_files_list) == len(initial_files_list) + 1, "File wasn't uploaded"

@app.command('clean_all')
def clean_files():
    """
    Clean all uploaded files.
    """
    for file in json.loads(list_files.text):
        d = requests.delete(url=f"{APP_BASE_URL}/documents/{file['id']}")
        d.raise_for_status()

    updated_files_list = json.loads(requests.get(url=f"{APP_BASE_URL}/documents/").text)
    assert len(updated_files_list) == 0 , "Files weren't deleted"

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