import os
from groq import Groq
import json

def analyze_metadata_and_image(metadata, img_base64):
    """
    Usa Groq (Llama Vision) para generar el reporte médico basado en metadatos e imagen.
    """
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
    Eres un radiólogo experto especializado en HealthTech. Analiza la siguiente información de un archivo DICOM.

    Metadatos:
    {json.dumps(metadata, indent=2)}

    Por favor genera un reporte médico estructurado en formato JSON con los siguientes campos:
    - Findings: (Hallazgos detallados)
    - Impression: (Impresión diagnóstica final)
    - Recommendations: (Recomendaciones clínicas)

    El reporte debe usar terminología médica/veterinaria precisa y evitar alucinaciones.
    """

    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
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
