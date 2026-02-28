import pydicom
import numpy as np
from PIL import Image
import io
import base64
import os

# Whitelist of safe tags to keep (De-identification)
SAFE_TAGS = [
    "Modality",
    "BodyPartExamined",
    "StudyDate",
    "SeriesDescription",
    "Manufacturer",
    "RescaleSlope",
    "RescaleIntercept",
    "WindowCenter",
    "WindowWidth",
    "PhotometricInterpretation",
    "Rows",
    "Columns",
    "BitsAllocated",
    "BitsStored",
    "HighBit",
    "PixelRepresentation",
]

def deidentify_metadata(ds):
    """
    Extracts only non-PHI tags from the DICOM dataset.
    """
    metadata = {}
    for tag in SAFE_TAGS:
        if tag in ds:
            value = ds.get(tag)
            # Ensure value is serializable
            metadata[tag] = str(value)
    return metadata

def apply_windowing(pixel_array, window_center, window_width):
    """
    Applies DICOM windowing to the pixel array.
    """
    if window_center is None or window_width is None:
        return pixel_array

    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    windowed = np.clip(pixel_array, img_min, img_max)
    return windowed

def process_dicom(file_path):
    """
    Extracts metadata and converts the DICOM image to Base64 for the LLM.
    Includes PHI stripping and normalization.
    """
    # 1. Size Validation (5MB)
    file_size = os.path.getsize(file_path)
    if file_size > 5 * 1024 * 1024:
        raise ValueError("File size exceeds 5MB limit.")

    try:
        ds = pydicom.dcmread(file_path)
    except Exception as e:
        raise ValueError(f"Invalid or corrupted DICOM file: {str(e)}")

    if "PixelData" not in ds:
        raise ValueError("DICOM file does not contain pixel data.")

    # 2. De-identification
    metadata = deidentify_metadata(ds)

    # 3. Image Processing
    pixel_array = ds.pixel_array

    # 3.0 Handle multi-frame (Take the first frame for analysis)
    if len(pixel_array.shape) == 3:
        pixel_array = pixel_array[0]

    # 3.1 Apply Rescale Slope and Intercept
    rescale_slope = float(ds.get("RescaleSlope", 1.0))
    rescale_intercept = float(ds.get("RescaleIntercept", 0.0))

    pixel_array = pixel_array.astype(np.float32)
    pixel_array = (pixel_array * rescale_slope) + rescale_intercept

    # 3.2 Handle MONOCHROME1 (invert)
    photometric_interpretation = ds.get("PhotometricInterpretation", "MONOCHROME2")
    if photometric_interpretation == "MONOCHROME1":
        pixel_array = np.max(pixel_array) - pixel_array

    # 3.3 Apply Windowing if available
    window_center = ds.get("WindowCenter")
    window_width = ds.get("WindowWidth")

    # Handle potentially multiple values for windowing
    if isinstance(window_center, pydicom.multival.MultiValue):
        window_center = float(window_center[0])
    elif window_center is not None:
        window_center = float(window_center)

    if isinstance(window_width, pydicom.multival.MultiValue):
        window_width = float(window_width[0])
    elif window_width is not None:
        window_width = float(window_width)

    pixel_array = apply_windowing(pixel_array, window_center, window_width)

    # 3.4 Normalize to 8-bit (0-255)
    p_min, p_max = pixel_array.min(), pixel_array.max()
    if p_max > p_min:
        pixel_array = (pixel_array - p_min) / (p_max - p_min) * 255.0
    else:
        pixel_array = pixel_array * 0

    pixel_array = pixel_array.astype(np.uint8)

    # 4. Convert to JPEG Base64
    img = Image.fromarray(pixel_array)
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return metadata, img_str
