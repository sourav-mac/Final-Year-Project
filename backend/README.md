# DFDC Deepfake Detection Backend

Minimal FastAPI backend to expose the existing DFDC deepfake detector as an HTTP API.

Files created:
- `main.py` - FastAPI app with `/predict` endpoint.
- `requirements.txt` - Python dependencies for the backend.

How it works:
- The app attempts to import `get_model` from `kernel_utils.py` and `predict_on_video` from `predict_folder.py` located in the project root.
- If those modules aren't present, stubs are used so the server can start for development.

Run (create a virtualenv first):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Notes:
- For production, fix `allow_origins` in `main.py` and use a persistent model instance.
- Ensure `kernel_utils.py` and `predict_folder.py` are available in the project root.
