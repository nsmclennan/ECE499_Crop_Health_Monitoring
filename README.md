# CropHealth — Flask Photo Analysis App

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
# Open http://localhost:5000
```

## API Keys

Ask for API keys and sent ~/.env
OPENAI_API_KEY = $KEY
OPENAI_VECTOR_STORE_ID = $STORE_ID

Then
```bash
source ~/.env
```

Run the script.

## Git

Add the following to gitignore to not submit test files:

```
uploads/
results/
```