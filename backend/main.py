import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .utils.dicom_processor import process_dicom
from .utils.ai_analyzer import analyze_metadata_and_image
from .utils.guardrails import validate_report
import shutil
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze_dicom_file(file: UploadFile = File(...)):
    """
    Endpoint para cargar un archivo DICOM, procesarlo con AI y validarlo.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. Extraer Metadatos y convertir imagen
        metadata, img_base64 = process_dicom(file_path)

        # 2. IA genera el reporte (Groq Llama 3.2 Vision)
        report = analyze_metadata_and_image(metadata, img_base64)

        # 3. Guardrails
        is_valid, message = validate_report(report)
        if not is_valid:
            raise HTTPException(status_code=422, detail=f"Guardrail fallido: {message}")

        return {
            "metadata": metadata,
            "report": report,
            "image": f"data:image/jpeg;base64,{img_base64}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Opcionalmente eliminar archivo local después de procesar
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
