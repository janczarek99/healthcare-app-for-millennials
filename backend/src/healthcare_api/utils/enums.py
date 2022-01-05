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
    def get_request_parameters(self) -> Tuple[str, str]:
        iteration_no = settings.dict().get(f"AZURE_CV_MODEL_{self.name}_ITERATION")
        project_id = settings.dict().get(f"AZURE_CV_MODEL_{self.name}_PROJECT_ID")

        return f"Iteration{iteration_no}", project_id


class AzureStorageEntityTypes(Enum):
    DOCUMENTS = "documents"
    PHOTOS = "photos"
