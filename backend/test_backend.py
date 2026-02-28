import asyncio
import os
import sys

# Mocking env for test
os.environ["GROQ_API_KEY"] = "test_key"

from utils.dicom_processor import deidentify_metadata
import pydicom

def test_deidentification():
    ds = pydicom.Dataset()
    ds.PatientName = "John Doe"
    ds.PatientID = "12345"
    ds.Modality = "CT"
    ds.BodyPartExamined = "CHEST"

    metadata = deidentify_metadata(ds)
    assert "PatientName" not in metadata
    assert "PatientID" not in metadata
    assert metadata["Modality"] == "CT"
    assert metadata["BodyPartExamined"] == "CHEST"
    print("De-identification test passed!")

if __name__ == "__main__":
    test_deidentification()
