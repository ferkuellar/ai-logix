from pathlib import Path

from app.services.ocr_providers.base import OcrProvider


class MockOcrProvider(OcrProvider):
    def process_image(self, image_path: Path, *, content_type: str) -> dict:
        raw_text = (
            "OXXO Centro\n"
            "Pedido PED-0001\n"
            "Tienda OX-CHIH-001\n"
            "Codigo de barras 7501234567890\n"
            "Producto demo x2\n"
            "Evidencia de entrega completa"
        )

        return {
            "raw_text": raw_text,
            "order_number": "PED-0001",
            "store_code": "OX-CHIH-001",
            "store_name": "OXXO Centro",
            "barcode": "7501234567890",
            "products": [{"name": "Producto demo", "quantity": 2}],
            "status_suggestion": "DELIVERED",
            "observations": f"Mock OCR processed {image_path.name} ({content_type}).",
            "confidence": 0.92,
            "confirmed": False,
        }
