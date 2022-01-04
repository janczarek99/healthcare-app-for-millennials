from tempfile import SpooledTemporaryFile
from typing import Optional, Tuple

from azure.storage.blob import BlobServiceClient, BlobClient
from uuid import uuid4, UUID

from src.settings import settings


class AzureBlobStorageClient:
    def __init__(
        self,
        azure_storage_connection_string: str = settings.AZURE_STORAGE_CONNECTION_STRING,
        container_name: str = settings.AZURE_STORAGE_CONTAINER_NAME
    ) -> None:
        self._blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
        self._az_container_name = container_name

    def upload_file(self, user_id: int, entity: str, file: SpooledTemporaryFile) -> str:
        blob_path, blob_client = self._get_blob_client(user_id=user_id, entity=entity)

        file.seek(0)
        # blob_client.upload_blob(file.read())

        return blob_path

    def download_file(self, user_id: int, entity: str, entity_id: UUID) -> SpooledTemporaryFile:
        _, blob_client = self._get_blob_client(user_id=user_id, entity=entity, entity_id=entity_id)

        file = SpooledTemporaryFile(mode="wb")
        file.write(blob_client.download_blob().readall())

        return file

    def _get_blob_client(self, user_id: int, entity: str, entity_id: Optional[UUID] = None) -> Tuple[str, BlobClient]:
        if not entity_id:
            entity_id = uuid4()

        blob_path = settings.AZURE_STORAGE_PATH.format(
            user_id=user_id, entity=entity, entity_id=entity_id
        )

        blob_client = self._blob_service_client.get_blob_client(container=self._az_container_name, blob=blob_path)

        return blob_path, blob_client
