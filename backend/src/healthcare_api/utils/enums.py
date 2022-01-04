from enum import Enum
from typing import List, Any

from src.settings import settings


class BaseEnum(Enum):
    @classmethod
    def get_names(cls) -> List[str]:
        return [str(e.name) for e in cls]

    @classmethod
    def get_values(cls) -> List[Any]:
        return [e.value for e in cls]


class CustomVisionModels(BaseEnum):
    LUNG_CANCER = settings.LUNG_CANCER_CV_URL
    PNEUMONIA = settings.PNEUMONIA_CV_URL
    BRAIN_TUMOUR = settings.BRAIN_TUMOUR_CV_URL


class AzureStorageEntityTypes(BaseEnum):
    DOCUMENTS = "documents"
