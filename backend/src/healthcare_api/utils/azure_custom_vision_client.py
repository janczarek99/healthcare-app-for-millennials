from tempfile import SpooledTemporaryFile

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

from src.exceptions import ValidationErrorException
from src.healthcare_api.utils.enums import CustomVisionModels
from src.settings import settings


class AzureCustomVisionClient:
    def __init__(
        self,
        azure_cv_endpoint: str = settings.AZURE_CV_ENDPOINT,
        azure_cv_sub_key: str = settings.AZURE_CV_KEY,
    ) -> None:
        self._cv_client = CustomVisionPredictionClient(
            endpoint=azure_cv_endpoint,
            credentials=ApiKeyCredentials(in_headers={"Prediction-key": azure_cv_sub_key}),  # noqa
        )

    def classify_image_file(
        self, classification_model: CustomVisionModels, file: SpooledTemporaryFile
    ):
        if classification_model == CustomVisionModels.BRAIN_TUMOUR:
            return self._get_prediction_results(
                classification_model=classification_model, file=file
            )
        elif classification_model == CustomVisionModels.LUNG_CANCER:
            return self._get_prediction_results(
                classification_model=classification_model, file=file
            )
        elif classification_model == CustomVisionModels.PNEUMONIA:
            return self._get_prediction_results(
                classification_model=classification_model, file=file
            )
        else:
            raise ValidationErrorException(f"Model {classification_model} not implemented yet.")

    def _get_prediction_results(
        self, classification_model: CustomVisionModels, file: SpooledTemporaryFile
    ):
        iteration, project_id = classification_model.get_request_parameters
        file.seek(0)
        results = self._cv_client.classify_image(
            project_id=project_id, published_name=iteration, image_data=file.read()
        )
        return {prediction.tag_name: prediction.probability for prediction in results.predictions}
