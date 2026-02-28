import pydicom
import numpy as np
from PIL import Image
import io
import base64

def process_dicom(file_path):
    """
    Extracts metadata and converts the DICOM image to Base64 for the LLM.
    """
    ds = pydicom.dcmread(file_path)

    metadata = {
        "PatientName": str(ds.get("PatientName", "Unknown")),
        "PatientID": str(ds.get("PatientID", "Unknown")),
        "Modality": str(ds.get("Modality", "Unknown")),
        "BodyPartExamined": str(ds.get("BodyPartExamined", "Unknown")),
        "StudyDate": str(ds.get("StudyDate", "Unknown")),
    }

    # Convert to image (assuming standard grayscale)
    pixel_array = ds.pixel_array

    # Basic normalization
    pixel_array = pixel_array.astype(float)
    rescaled = (np.maximum(pixel_array, 0) / pixel_array.max()) * 255.0
    rescaled = np.uint8(rescaled)

    img = Image.fromarray(rescaled)
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return metadata, img_str
