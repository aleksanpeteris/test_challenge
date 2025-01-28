1. python3 -m venv venv
2. source venv/bin/activate
3. pip install scripts/requirements.txt
4. python3 scripts/files_uploader.py challengeOverview.md

# Files Uploader script

## How to run the script

1. Create a virtual environment and install the dependencies
```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install scripts/requirements.txt
```

2. Run the script
To upload a file, run the following command
```bash
    python3 scripts/files_uploader.py upload <file_1> <file_2> ... <file_n>
```

To cleanup the files, run the following command
```bash
    python3 scripts/files_uploader.py clean_all
```

To list uploaded files, run the following command
```bash
    python3 scripts/files_uploader.py list_files
```