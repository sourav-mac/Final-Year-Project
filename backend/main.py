from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from pathlib import Path

# Ensure project root is on sys.path so existing project modules can be imported
WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

# Try to import the existing model helpers; if not present, provide stubs
try:
    from kernel_utils import get_model
except Exception:
    def get_model():
        """Stub get_model for development - replace with real loader."""
        return None

try:
    from predict_folder import predict_on_video
except Exception:
    def predict_on_video(video_path, model=None):
        """Stub predictor - replace with real prediction logic."""
        # Return dummy score (0.0 = real, 1.0 = fake)
        return 0.5

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "DFDC Deepfake Detection API"}

@app.post("/predict")
async def predict_video(video: UploadFile = File(...)):
    # Save uploaded file
    tmp_dir = Path("/tmp/dfdc_api_uploads")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_dir / video.filename
    with open(tmp_path, "wb") as f:
        f.write(await video.read())

    model = get_model()
    score = predict_on_video(str(tmp_path), model)

    try:
        tmp_path.unlink()
    except Exception:
        pass

    return {"prediction_score": float(score), "filename": video.filename}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
