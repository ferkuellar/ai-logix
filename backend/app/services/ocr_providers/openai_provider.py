import base64
import json
from pathlib import Path

from fastapi import HTTPException, status

from app.services.ocr_providers.base import OcrProvider


class OpenAiOcrProvider(OcrProvider):
    def __init__(self, *, api_key: str | None, model: str):
        self.api_key = api_key
        self.model = model

    def process_image(self, image_path: Path, *, content_type: str) -> dict:
        if not self.api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY is required when OCR_PROVIDER=openai.",
            )

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OpenAI SDK is not installed.",
            ) from exc

        image_data = base64.b64encode(image_path.read_bytes()).decode("utf-8")
        image_url = f"data:{content_type};base64,{image_data}"
        client = OpenAI(api_key=self.api_key)

        try:
            response = client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": (
                                    "Extract operational delivery data from this OXXO evidence image. "
                                    "Return only valid JSON with keys: order_number, store_code, store_name, "
                                    "barcode, products, status_suggestion, observations, confidence, raw_text."
                                ),
                            },
                            {
                                "type": "input_image",
                                "image_url": image_url,
                                "detail": "auto",
                            },
                        ],
                    }
                ],
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"OpenAI OCR provider failed: {exc}",
            ) from exc

        output_text = getattr(response, "output_text", "") or ""

        try:
            extracted = json.loads(output_text)
        except json.JSONDecodeError:
            extracted = {
                "raw_text": output_text,
                "order_number": None,
                "store_code": None,
                "store_name": None,
                "barcode": None,
                "products": [],
                "status_suggestion": None,
                "observations": "OpenAI response was not valid JSON.",
                "confidence": 0.0,
            }

        extracted.setdefault("raw_text", output_text)
        extracted.setdefault("confirmed", False)
        return extracted
