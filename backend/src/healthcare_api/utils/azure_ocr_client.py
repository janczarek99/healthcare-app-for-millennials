import time
from tempfile import SpooledTemporaryFile

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

from src.settings import settings


class AzureOCRClient:
    def __init__(
        self, azure_ocr_endpoint: str = settings.AZURE_OCR_ENDPOINT, azure_ocr_sub_key: str = settings.AZURE_OCR_KEY
    ) -> None:
        self._ocr_client = ComputerVisionClient(
            endpoint=azure_ocr_endpoint, credentials=CognitiveServicesCredentials(subscription_key=azure_ocr_sub_key) # noqa
        )

    def get_text_from_image(self, file: SpooledTemporaryFile) -> str:
        operation_id = self._get_operation_id(file)

        result_lines = ""

        while True:
            read_result = self._ocr_client.get_read_result(operation_id)

            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    result_lines += "\n".join(text_result.lines)
                break

            time.sleep(1)

        return result_lines

    def _get_operation_id(self, file: SpooledTemporaryFile) -> str:
        file.seek(0)
        response = self._ocr_client.read_in_stream(file.read(), raw=True)
        operation_id = response.headers["Operation-Location"]
        return operation_id.split("/")[-1]
