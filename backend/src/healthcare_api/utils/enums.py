from enum import Enum
from typing import List, Any, Tuple

from src.settings import settings


class CustomVisionModels(Enum):
    LUNG_CANCER = "LUNG_CANCER"
    PNEUMONIA = "PNEUMONIA"
    BRAIN_TUMOUR = "BRAIN_TUMOUR"

    @classmethod
    def get_names(cls) -> List[str]:
        return [str(e.name) for e in cls]

    @classmethod
    def get_values(cls) -> List[Any]:
        return [e.value for e in cls]

    @property
    def url(self):
        return eval(f"settings.{self.name}_CV_URL")


class AzureStorageEntityTypes(Enum):
    DOCUMENTS = "documents"
    PHOTOS = "photos"

