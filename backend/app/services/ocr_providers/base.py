from abc import ABC, abstractmethod
from pathlib import Path


class OcrProvider(ABC):
    @abstractmethod
    def process_image(self, image_path: Path, *, content_type: str) -> dict:
        raise NotImplementedError
