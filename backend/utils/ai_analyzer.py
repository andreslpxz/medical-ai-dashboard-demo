import os
import json
import asyncio
from groq import AsyncGroq
import httpx
import time

MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

async def analyze_metadata_and_image(metadata, img_base64, retry_prompt=None):
    """
    Uses AsyncGroq to generate a medical report.
    Includes exponential backoff retries and structured delimiters.
    """
    client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))

    system_prompt = "You are an expert radiologist. Analyze the clinical data and image provided to generate a structured report."

    user_content = f"""
<clinical_metadata>
{json.dumps(metadata, indent=2)}
</clinical_metadata>

<analysis_instructions>
Please generate a structured medical report in JSON format with the following fields:
- Findings: (Detailed findings)
- Impression: (Final diagnostic impression)
- Recommendations: (Clinical recommendations)

The report must use precise medical terminology.
</analysis_instructions>
"""
    if retry_prompt:
        user_content += f"\n\n<additional_instruction>\n{retry_prompt}\n</additional_instruction>"

    max_retries = 2
    base_delay = 1 # second
    timeout = 8.0 # seconds

    for attempt in range(max_retries + 1):
        try:
            start_time = time.time()
            response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_content},
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
                response_format={"type": "json_object"},
                timeout=timeout
            )
            latency_ms = int((time.time() - start_time) * 1000)
            content = response.choices[0].message.content
            return json.loads(content), latency_ms, MODEL_NAME

        except (httpx.HTTPStatusError, Exception) as e:
            # Handle 429 and 5xx
            status_code = getattr(e, "status_code", None)
            if attempt < max_retries:
                if status_code == 429 or (status_code and status_code >= 500) or "timeout" in str(e).lower():
                    delay = base_delay * (2 ** attempt)
                    await asyncio.sleep(delay)
                    continue
            raise e
