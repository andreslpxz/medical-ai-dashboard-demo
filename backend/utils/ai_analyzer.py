import os
from groq import Groq
import json

def analyze_metadata_and_image(metadata, img_base64):
    """
    Uses Groq (Llama Vision) to generate a medical report based on metadata and image.
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
    You are an expert radiologist specialized in HealthTech. Analyze the following information from a DICOM file.

    Metadata:
    {json.dumps(metadata, indent=2)}

    Please generate a structured medical report in JSON format with the following fields:
    - Findings: (Detailed findings)
    - Impression: (Final diagnostic impression)
    - Recommendations: (Clinical recommendations)

    The report must use precise medical/veterinary terminology and avoid hallucinations.
    """

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}"
                        },
                    },
                ],
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
