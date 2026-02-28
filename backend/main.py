import os
import uuid
import time
import json
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from .utils.dicom_processor import process_dicom
from .utils.ai_analyzer import analyze_metadata_and_image
from .utils.guardrails import validate_report
from .utils.database import init_db, save_report
import shutil
from dotenv import load_dotenv

load_dotenv()

# Structured Logging Setup
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("radimal-insights")

def log_json(level, data):
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": level,
        **data
    }
    logger.info(json.dumps(log_entry))

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.post("/analyze")
async def analyze_dicom_file(request: Request, file: UploadFile = File(...)):
    """
    Endpoint to upload a DICOM file, process it with AI, and validate it.
    """
    request_id = str(uuid.uuid4())
    start_time = time.time()

    # Enforce 5MB limit
    MAX_FILE_SIZE = 5 * 1024 * 1024 # 5MB

    # Check size if available (some clients might not send it)
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 5MB limit.")

    file_path = os.path.join(UPLOAD_DIR, f"{request_id}_{file.filename}")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1. Extract Metadata and convert image (Run in threadpool to avoid blocking event loop)
        try:
            metadata, img_base64 = await run_in_threadpool(process_dicom, file_path)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # 2. AI generates the report (Groq Llama Vision)
        try:
            report, latency_ms, model_version = await analyze_metadata_and_image(metadata, img_base64)

            # 3. Guardrails
            is_valid, message = validate_report(report)

            if not is_valid:
                # Retry once with reinforced prompt
                log_json("WARNING", {"request_id": request_id, "message": f"Guardrail failed: {message}. Retrying..."})
                retry_prompt = f"Your previous report was rejected because: {message}. Please provide a more accurate and consistent report."
                report, latency_ms, model_version = await analyze_metadata_and_image(metadata, img_base64, retry_prompt=retry_prompt)

                # Check guardrails again
                is_valid, message = validate_report(report)
                if not is_valid:
                    # Mark as needs_human_review
                    await save_report("needs_human_review", metadata, report, latency_ms, model_version)
                    log_json("ERROR", {"request_id": request_id, "message": "Guardrail failed after retry.", "latency_ms": latency_ms})
                    return {
                        "status": "needs_human_review",
                        "metadata": metadata,
                        "report": report,
                        "image": f"data:image/jpeg;base64,{img_base64}",
                        "warning": "Report requires human validation."
                    }

            # 4. Success - Save to DB
            await save_report("completed", metadata, report, latency_ms, model_version)

            total_latency = int((time.time() - start_time) * 1000)
            log_json("INFO", {
                "request_id": request_id,
                "status": "success",
                "ai_latency_ms": latency_ms,
                "total_latency_ms": total_latency,
                "model": model_version
            })

            return {
                "status": "completed",
                "metadata": metadata,
                "report": report,
                "image": f"data:image/jpeg;base64,{img_base64}"
            }

        except Exception as e:
            log_json("ERROR", {"request_id": request_id, "error": str(e)})
            raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
